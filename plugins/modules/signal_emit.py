#!/usr/bin/python

from __future__ import absolute_import, annotations, division, print_function


__metaclass__ = type


DOCUMENTATION = r"""
---
module: signal_emit

short_description: Emit a signal using a registered emitter

description:
  - Emits a signal using emitter configuration previously created by C(register_emitter).
  - The module accepts a C(registration_id), resolves the internal state file,
    loads the emitter configuration, and emits the signal.
  - Intended to run on the Ansible controller with C(delegate_to) set to C(localhost).

options:
  registration_id:
    description:
      - Opaque registration ID returned by C(register_emitter).
    type: str
    required: true

  event_type:
    description:
      - Logical event type to emit.
    type: str
    required: true

  message:
    description:
      - Human-readable signal message.
    type: str
    required: true

  payload:
    description:
      - Additional structured metadata to send with the signal.
    type: dict
    required: false
    default: {}

author:
  - Yang Jie
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
    event_type: job_started
    message: "Job started"
    payload:
      job_id: "{{ tower_job_id }}"
      stage: precheck
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

from pathlib import Path

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.cd_cluster.pipeline_common.plugins.module_utils.emitter.emitter import (
    Signal,
)
from ansible_collections.cd_cluster.pipeline_common.plugins.module_utils.emitter.factory import (
    create_chain_emitter,
)
from ansible_collections.cd_cluster.pipeline_common.plugins.modules.register_emitter import (
    get_state_file,
)


def load_state_file(path: Path) -> dict:
    with path.open("r") as f:
        return json.load(f)


def main() -> None:
    module = AnsibleModule(
        argument_spec={
            "registration_id": {
                "type": "str",
                "required": True,
                "no_log": True,
            },
            "event_type": {
                "type": "str",
                "required": True,
            },
            "message": {
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
        event_type=module.params["event_type"],
        message=module.params["message"],
        payload=module.params["payload"],
    )

    response = emitter.emit(signal)

    if not response.ok:
        module.fail_json(
            msg="Failed to emit signal",
            registration_id=registration_id,
            status_code=response.status_code,
            body=response.body,
            error=response.error,
        )

    module.exit_json(
        changed=False,
        msg="Signal emitted",
        registration_id=registration_id,
        status_code=response.status_code,
        body=response.body,
    )


if __name__ == "__main__":
    main()
