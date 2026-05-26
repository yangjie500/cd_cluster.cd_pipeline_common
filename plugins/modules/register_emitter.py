#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Yang Jie
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, annotations, division, print_function


__metaclass__ = type


DOCUMENTATION = r"""
---
module: register_emitter

short_description: Register signal emitter configuration

description:
  - Registers one or more signal emitters for downstream event delivery.
  - Persists emitter configuration as internal state files.
  - Uses atomic file replacement to prevent partial writes and corruption.
  - Generates an opaque registration identifier for later lookup.

options:
  emitters:
    description:
      - List of emitters to register.
    required: true
    type: list
    elements: dict
    suboptions:
      service:
        description:
          - Emitter backend service.
        required: true
        type: str
        choices:
          - loki
          - cloudportal

      transport:
        description:
          - Transport implementation used by the emitter.
        required: false
        type: str
        default: requests
        choices:
          - requests

      endpoint:
        description:
          - Target endpoint URL for the emitter service.
        required: true
        type: str

      options:
        description:
          - Service-specific emitter configuration.
          - May contain authentication credentials or tokens.
        required: false
        default: {}
        type: dict

notes:
  - State files are written beneath the SIGNAL_EMITTER_STATE_DIR directory.
  - If SIGNAL_EMITTER_STATE_DIR is unset, /tmp/ansible-signal is used.
  - Stored files are created with restrictive permissions.

author:
  - Yang Jie (@yangjie500)
"""

EXAMPLES = r"""
- name: Register Loki emitter
  register_emitter:
    emitters:
      - service: loki
        endpoint: https://loki.example.com/loki/api/v1/push
        options:
          tenant_id: production
          tenant_mode: path
          bearer_token: "asdasdasd"
          verify_ssl: false

- name: Register CloudPortal emitter
  register_emitter:
    emitters:
      - service: loki
        endpoint: https://custom.portal/callback
        options:
            bearer_token: "asdasdasd
            verify_ssl: false


- name: Register multiple emitters
  register_emitter:
    emitters:
      - service: loki
        endpoint: https://loki.example.com/loki/api/v1/push
        options:
          tenant_id: production
          tenant_mode: path
          bearer_token: "asdasdasd"
          verify_ssl: false

      - service: splunk
        endpoint: https://splunk.example.com:8088/services/collector
        options:
          token: secret-token

- name: Preview registration
  register_emitter:
    emitters:
      - service: loki
        endpoint: https://loki.example.com/loki/api/v1/push
  check_mode: true
"""

RETURN = r"""
changed:
  description:
    - Whether the emitter configuration was registered.
  returned: always
  type: bool
  sample: true

msg:
  description:
    - Human-readable status message.
  returned: always
  type: str
  sample: Emitter configuration registered

registration_id:
  description:
    - Opaque registration identifier associated with the stored configuration.
  returned: success
  type: str
  sample: 3c7b8d51a9d34e6a8a7c2f0d9b13ef44
"""

import json
import os
import secrets
import tempfile

from pathlib import Path
from typing import Any

from ansible.module_utils.basic import AnsibleModule


STATE_DIR = Path(
    os.environ.get(
        "SIGNAL_EMITTER_STATE_DIR",
        "/tmp/ansible-signal",
    ),
)


def generate_registration_id() -> str:
    """
    Generate opaque random registration ID.
    """

    return secrets.token_hex(16)


def get_state_file(
    registration_id: str,
) -> Path:
    """
    Resolve internal state file path.
    """

    return STATE_DIR / f"{registration_id}.json"


def atomic_write_json(
    path: Path,
    data: dict[str, Any],
) -> None:
    """
    Atomically write JSON file.

    Prevents:
    - partial writes
    - concurrent corruption
    """

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fd, tmp_name = tempfile.mkstemp(
        dir=str(path.parent),
        prefix=f".{path.name}.",
        suffix=".tmp",
        text=True,
    )

    try:
        with os.fdopen(fd, "w") as tmp:
            json.dump(
                data,
                tmp,
                indent=2,
            )

            tmp.flush()

            os.fsync(
                tmp.fileno(),
            )

        # Restrict permissions because there will be secret
        os.chmod(
            tmp_name,
            0o600,
        )

        # Atomic replace.
        os.replace(
            tmp_name,
            path,
        )

    except Exception:
        try:
            os.unlink(tmp_name)
        except FileNotFoundError:
            pass

        raise


def main() -> None:
    module = AnsibleModule(
        argument_spec={
            "emitters": {
                "type": "list",
                "required": True,
                "elements": "dict",
                "options": {
                    "service": {
                        "type": "str",
                        "required": True,
                        "choices": ["loki", "cloudportal"],
                    },
                    "transport": {
                        "type": "str",
                        "required": False,
                        "default": "requests",
                        "choices": [
                            "requests",
                        ],
                    },
                    "endpoint": {
                        "type": "str",
                        "required": True,
                    },
                    "options": {
                        "type": "dict",
                        "required": False,
                        "default": {},
                        "no_log": True,
                    },
                },
            },
        },
        supports_check_mode=True,
    )

    registration_id = generate_registration_id()

    state_file = get_state_file(
        registration_id,
    )

    state = {
        "version": 1,
        "emitters": module.params["emitters"],
    }

    if module.check_mode:
        module.exit_json(
            changed=True,
            msg="Emitter configuration would be registered",
            registration_id=registration_id,
        )

    try:
        atomic_write_json(
            state_file,
            state,
        )

    except Exception as exc:
        module.fail_json(
            msg=("Failed to register " f"emitter configuration: {exc}"),
        )

    module.exit_json(
        changed=True,
        msg="Emitter configuration registered",
        registration_id=registration_id,
    )


if __name__ == "__main__":
    main()
