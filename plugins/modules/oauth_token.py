#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Yang Jie
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, annotations, division, print_function


__metaclass__ = type

DOCUMENTATION = r"""
---
module: oauth_token

short_description: Get OAuth/JWT access token using server-side flows

description:
  - This module requires the Python libraries C(requests) and C(tenacity).
  - When executing on managed nodes, the dependencies must be installed on those managed nodes.
  - Exchanges credentials or assertions for an access token.
  - Supports client credentials, direct access grant/password grant, JWT bearer grant,
    token exchange, and refresh token flow.

options:
  token_url:
    description:
      - OAuth token endpoint.
    type: str
    required: true

  flow:
    description:
      - OAuth flow to use.
    type: str
    required: true
    choices:
      - client_credentials
      - password
      - jwt_bearer
      - token_exchange
      - refresh_token

  client_id:
    description:
      - OAuth client ID.
    type: str
    required: false

  client_secret:
    description:
      - OAuth client secret.
    type: str
    required: false

  username:
    description:
      - Username for password/direct access grant.
    type: str
    required: false

  password:
    description:
      - Password for password/direct access grant.
    type: str
    required: false

  scope:
    description:
      - Optional OAuth scope.
    type: str
    required: false

  audience:
    description:
      - Optional target audience.
    type: str
    required: false

  assertion:
    description:
      - JWT assertion for JWT bearer grant.
    type: str
    required: false

  subject_token:
    description:
      - Subject token for token exchange flow.
    type: str
    required: false

  subject_token_type:
    description:
      - Subject token type for token exchange.
    type: str
    required: false
    default: urn:ietf:params:oauth:token-type:access_token

  requested_token_type:
    description:
      - Requested token type for token exchange.
    type: str
    required: false
    default: urn:ietf:params:oauth:token-type:access_token

  refresh_token:
    description:
      - Refresh token for refresh_token flow.
    type: str
    required: false

  ssl_verify:
    description:
      - To verify SSL Certificate on remote server.
    type: bool
    required: false
    default: true

author:
  - Yang Jie (@yangjie500)
"""

EXAMPLES = r"""
- name: Get token using client credentials
  oauth_token:
    token_url: "https://keycloak.example.com/realms/demo/protocol/openid-connect/token"
    flow: client_credentials
    client_id: loki-client
    client_secret: "{{ client_secret }}"
    scope: "openid"
  register: oauth_result
  no_log: true

- name: Register Loki emitter with bearer token
  register_emitter:
    emitters:
      - service: loki
        transport: requests
        endpoint: "https://gateway.example.com/api/logs/v1/{tenant}/loki/api/v1/push"
        options:
          tenant_id: application
          tenant_mode: path
          bearer_token: "{{ oauth_result.access_token }}"
  register: emitter_registration
  delegate_to: localhost
  no_log: true

- name: Get token using direct access grant
  oauth_token:
    token_url: "https://keycloak.example.com/realms/demo/protocol/openid-connect/token"
    flow: password
    client_id: cli-client
    client_secret: "{{ client_secret }}"
    username: "{{ username }}"
    password: "{{ password }}"
  register: oauth_result
  no_log: true
"""

RETURN = r"""
access_token:
  description:
    - Access token returned by the token endpoint.
  type: str
  returned: success

token_type:
  description:
    - Token type.
  type: str
  returned: success
  sample: Bearer

expires_in:
  description:
    - Token lifetime in seconds.
  type: int
  returned: success
  sample: 300

refresh_token:
  description:
    - Refresh token, if returned by the token endpoint.
  type: str
  returned: success

raw:
  description:
    - Raw parsed token response.
  type: dict
  returned: success
"""

import json

from urllib.parse import urlencode

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.cd_cluster.pipeline_common.plugins.module_utils.transport.models import (
    TransportRequest,
)
from ansible_collections.cd_cluster.pipeline_common.plugins.module_utils.transport.transport import (  # noqa: E501
    RequestsHttpTransport,
)


def build_form_data(params: dict[str, str | None]) -> str:
    """Build x-www-form-urlencoded payload."""
    clean = {key: value for key, value in params.items() if value is not None}
    return urlencode(clean)


def build_token_request(module: AnsibleModule) -> TransportRequest:
    """Build OAuth token request."""
    flow = module.params["flow"]

    grant_type_by_flow = {
        "client_credentials": "client_credentials",
        "password": "password",
        "jwt_bearer": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "token_exchange": "urn:ietf:params:oauth:grant-type:token-exchange",
        "refresh_token": "refresh_token",
    }

    form: dict[str, str | None] = {
        "grant_type": grant_type_by_flow[flow],
        "client_id": module.params.get("client_id"),
        "client_secret": module.params.get("client_secret"),
        "scope": module.params.get("scope"),
        "audience": module.params.get("audience"),
    }

    if flow == "password":
        form["username"] = module.params.get("username")
        form["password"] = module.params.get("password")

    elif flow == "jwt_bearer":
        form["assertion"] = module.params.get("assertion")

    elif flow == "token_exchange":
        form["subject_token"] = module.params.get("subject_token")
        form["subject_token_type"] = module.params.get("subject_token_type")
        form["requested_token_type"] = module.params.get("requested_token_type")

    elif flow == "refresh_token":
        form["refresh_token"] = module.params.get("refresh_token")

    return TransportRequest(
        method="POST",
        target=module.params["token_url"],
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        },
        data=build_form_data(form),
        ssl_verify=module.params.get("ssl_verify"),
    )


def validate_required(module: AnsibleModule) -> None:
    """Validate required parameters for selected OAuth flow."""
    flow = module.params["flow"]

    required_by_flow = {
        "client_credentials": ["client_id", "client_secret"],
        "password": ["client_id", "username", "password"],
        "jwt_bearer": ["client_id", "assertion"],
        "token_exchange": ["client_id", "subject_token"],
        "refresh_token": ["client_id", "refresh_token"],
    }

    missing = [name for name in required_by_flow[flow] if not module.params.get(name)]

    if missing:
        module.fail_json(msg=f"Missing required parameters for {flow}: {', '.join(missing)}")


def main() -> None:
    module = AnsibleModule(
        argument_spec={
            "token_url": {"type": "str", "required": True},
            "flow": {
                "type": "str",
                "required": True,
                "choices": [
                    "client_credentials",
                    "password",
                    "jwt_bearer",
                    "token_exchange",
                    "refresh_token",
                ],
            },
            "client_id": {"type": "str", "required": False},
            "client_secret": {
                "type": "str",
                "required": False,
                "no_log": True,
            },
            "username": {"type": "str", "required": False},
            "password": {
                "type": "str",
                "required": False,
                "no_log": True,
            },
            "scope": {"type": "str", "required": False},
            "audience": {"type": "str", "required": False},
            "assertion": {
                "type": "str",
                "required": False,
                "no_log": True,
            },
            "subject_token": {
                "type": "str",
                "required": False,
                "no_log": True,
            },
            "subject_token_type": {
                "type": "str",
                "required": False,
                "default": "urn:ietf:params:oauth:token-type:access_token",
            },
            "requested_token_type": {
                "type": "str",
                "required": False,
                "default": "urn:ietf:params:oauth:token-type:access_token",
            },
            "refresh_token": {
                "type": "str",
                "required": False,
                "no_log": True,
            },
            "ssl_verify": {"type": "bool", "required": False, "default": True},
        },
        supports_check_mode=False,
    )

    validate_required(module)

    transport = RequestsHttpTransport()
    request = build_token_request(module)
    response = transport.send(request)

    if not response.ok:
        module.fail_json(
            msg="Failed to obtain OAuth token",
            status_code=response.status_code,
            body=response.body,
            error=response.error,
        )

    try:
        token_response = json.loads(response.body)
    except json.JSONDecodeError as exc:
        module.fail_json(
            msg=f"Token endpoint did not return valid JSON: {exc}",
            body=response.body,
        )

    access_token = token_response.get("access_token")
    if not access_token:
        module.fail_json(
            msg="Token endpoint response does not contain access_token",
            body=response.body,
        )

    module.exit_json(
        changed=False,
        access_token=access_token,
        token_type=token_response.get("token_type"),
        expires_in=token_response.get("expires_in"),
        refresh_token=token_response.get("refresh_token"),
        raw=token_response,
    )


if __name__ == "__main__":
    main()
