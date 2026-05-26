#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Yang Jie
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, annotations, division, print_function


__metaclass__ = type


DOCUMENTATION = r"""
module: signal_emit

short_description: Emit a signal using a registered emitter

description:
  - This module requires the Python libraries C(requests) and C(tenacity).
  - When executing on managed nodes, the dependencies must be installed on those managed nodes.
  - Emits a signal using emitter configuration previously created by
    C(register_emitter).
  - The module accepts a C(registration_id), resolves the internal state file,
    loads the emitter configuration, and emits the signal.
  - Intended to run on the Ansible controller with C(delegate_to)
    set to C(localhost).

options:
  registration_id:
    description:
      - Opaque registration ID returned by C(register_emitter).
    type: str
    required: true

  signal_id:
    description:
      - Unique identifier for this emitted signal/event.
      - Useful for deduplication, retries, auditing, and tracing.
      - Automatically generated when omitted.
    type: str
    required: false

  correlation_id:
    description:
      - Correlation identifier used to group related signals/events together.
      - Typically shared across all signals emitted by the same workflow,
        pipeline execution, or job.
    type: str
    required: false

  event_type:
    description:
      - Logical event type to emit.
    type: str
    required: true

  signal_message:
    description:
      - Human-readable signal message.
    type: str
    required: true

  payload:
    description:
      - Additional structured metadata to send with the signal.
      - Business-specific identifiers such as C(job_id) are typically stored here.
    type: dict
    required: false
    default: {}

author:
  - Yang Jie (@yangjie500)
"""

EXAMPLES = r"""
- name: Register emitters
  register_emitter:
    emitters:
      - service: loki
        transport: requests
        endpoint: "https://gateway.example.com/api/logs/v1/{tenant}/loki/api/v1/push"
        options:
          tenant_id: application
          tenant_mode: path
  register: emitter_registration
  delegate_to: localhost
  run_once: true

- name: Emit signal
  signal_emit:
    registration_id: "{{ emitter_registration.registration_id }}"
    signal_id: "sig-001"
    correlation_id: "{{ tower_workflow_job_id }}"
    event_type: job_started
    message: "Job started"
    payload:
      job_id: "{{ tower_job_id }}"
      stage: precheck
  delegate_to: localhost

- name: Emit pipeline completion signal
  signal_emit:
    registration_id: "{{ emitter_registration.registration_id }}"
    correlation_id: "{{ pipeline_id }}"
    event_type: pipeline_finished
    message: "Pipeline completed successfully"
    payload:
      job_id: "{{ tower_job_id }}"
      status: success
  delegate_to: localhost
"""

RETURN = r"""
msg:
  description:
    - Result message.
  type: str
  returned: always
  sample: Signal emitted

registration_id:
  description:
    - Opaque emitter registration ID used.
  type: str
  returned: always
  sample: 5e2d8f5b1de848ea7d45bcb4af0fb922

signal_id:
  description:
    - Unique identifier for the emitted signal.
  type: str
  returned: success
  sample: sig-001

correlation_id:
  description:
    - Correlation identifier associated with the emitted signal.
  type: str
  returned: success
  sample: workflow-abc123

status_code:
  description:
    - Status code returned by the underlying transport, when available.
  type: int
  returned: success
  sample: 204

body:
  description:
    - Response body returned by the underlying transport.
  type: str
  returned: success
  sample: ""

error:
  description:
    - Error returned by the underlying emitter or transport.
  type: str
  returned: failure
  sample: "Server error: 503"
"""

import json
import os
import uuid

from pathlib import Path

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.cd_cluster.pipeline_common.plugins.module_utils.emitter.emitter import (
    Signal,
)
from ansible_collections.cd_cluster.pipeline_common.plugins.module_utils.emitter.factory import (
    create_chain_emitter,
)


STATE_DIR = Path(
    os.environ.get(
        "SIGNAL_EMITTER_STATE_DIR",
        "/tmp/ansible-signal",
    ),
)


def get_state_file(
    registration_id: str,
) -> Path:
    """
    Resolve internal state file path.
    """

    return STATE_DIR / f"{registration_id}.json"


def load_state_file(path: Path) -> dict:
    with path.open("r") as f:
        return json.load(f)


def generate_signal_id() -> str:
    """Generate unique signal identifier."""

    return str(uuid.uuid4())


def main() -> None:
    module = AnsibleModule(
        argument_spec={
            "registration_id": {
                "type": "str",
                "required": True,
            },
            "signal_id": {
                "type": "str",
                "required": False,
            },
            "correlation_id": {
                "type": "str",
                "required": False,
            },
            "event_type": {
                "type": "str",
                "required": True,
            },
            "signal_message": {
                "type": "str",
                "required": True,
            },
            "payload": {
                "type": "dict",
                "required": False,
                "default": {},
            },
        },
        supports_check_mode=True,
    )

    registration_id = module.params["registration_id"]
    state_file = get_state_file(registration_id)

    if module.check_mode:
        module.exit_json(
            changed=False,
            msg="Signal would be emitted",
            registration_id=registration_id,
        )

    if not state_file.exists():
        module.fail_json(
            msg="Emitter registration does not exist. Run register_emitter first.",
            registration_id=registration_id,
        )

    state = load_state_file(state_file)

    emitters_config = state.get("emitters")
    if not emitters_config:
        module.fail_json(
            msg="Emitter registration does not contain any emitters",
            registration_id=registration_id,
        )

    emitter = create_chain_emitter(
        configs=emitters_config,
    )

    signal = Signal(
        signal_id=module.params["signal_id"] or generate_signal_id(),
        correlation_id=module.params["correlation_id"],
        event_type=module.params["event_type"],
        message=module.params["signal_message"],
        payload=module.params["payload"],
    )

    response = emitter.emit(signal)

    if not response.ok:
        module.fail_json(
            msg="Failed to emit signal",
            signal_id=signal.signal_id,
            correlation_id=signal.correlation_id,
            registration_id=registration_id,
            status_code=response.status_code,
            body=response.body,
            error=response.error,
        )

    module.exit_json(
        changed=False,
        signal_id=signal.signal_id,
        correlation_id=signal.correlation_id,
        msg="Signal emitted",
        registration_id=registration_id,
        status_code=response.status_code,
        body=response.body,
    )


if __name__ == "__main__":
    main()
