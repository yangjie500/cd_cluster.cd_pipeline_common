#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Yang Jie
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

import io
import os
import re

from ansible.module_utils.basic import AnsibleModule


__metaclass__ = type

DOCUMENTATION = r"""
---
module: replace_placeholders
short_description: Replace custom tokens or text placeholders inside a
  file
description:
  - Searches for specified text placeholders or variables in a target
    file and replaces them with defined values.
  - Supports default angle-bracket tokens (<key>), Jinja2-style
    placeholders ({{ key }}), and custom word boundaries.
  - Safely handles local backups and respects Ansible check-mode dry
    runs.
options:
  path:
    description: Path to the target text file to modify.
    required: true
    type: path
  placeholders:
    description: Dictionary of placeholder keys and their matching
      replacement values.
    required: true
    type: dict
  whole_word:
    description: Perform exact whole-word matching using regular
      expression boundaries.
    type: bool
    default: false
  jinja_tokens:
    description: Match Jinja-style syntax placeholders like {{ key }}
      instead of the default <key> pattern.
    type: bool
    default: false
  case_sensitive:
    description: Perform exact case-sensitive matching.
    type: bool
    default: true
  backup:
    description: Create a backup file in the same directory before
      performing any modifications.
    type: bool
    default: true
author:
  - Yang Jie (@yangjie500)
"""

EXAMPLES = r"""
- name: Replace standard <key> placeholders with target values
  replace_placeholders:
    path: helm-charts/vault.values.yaml
    placeholders:
      container_registry_url: "xxx/mario/backend_preprod"
      repository_url: "xxx/mario/backend_preprod"

- name: Replace Jinja-style placeholders dynamically
  replace_placeholders:
    path: /etc/app/config.conf
    jinja_tokens: true
    case_sensitive: false
    placeholders:
      db_host: "10.0.0.5"
"""

RETURN = r"""
changed:
  description: Whether the target file was updated.
  type: bool
  returned: always
replaced_total:
  description: Total number of instances successfully replaced across all
    keys.
  type: int
  returned: always
replaced_per_key:
  description: Dictionary showing the explicit count of substitutions
    made per individual key.
  type: dict
  returned: always
backup_file:
  description: Absolute path to the newly generated backup file.
  type: str
  returned: when backup=true and changes were made
"""


def build_pattern(key: str, whole_word: bool, jinja_tokens: bool, flags: int) -> re.Pattern:
    """Constructs the regular expression pattern based on configured options."""
    if jinja_tokens:
        # Matches {{key}}, {{ key }}, and {{   key   }}
        pattern = r"\{\{\s*" + re.escape(key) + r"\s*\}\}"
    elif whole_word:
        # Exact match inside word boundaries
        pattern = r"\b" + re.escape(key) + r"\b"
    else:
        # Default fallback to target pattern <key>
        pattern = r"<" + re.escape(key) + r">"

    return re.compile(pattern, flags)


def run_module():
    module_args = dict(
        path=dict(type="path", required=True),
        placeholders=dict(type="dict", required=True),
        whole_word=dict(type="bool", default=False),
        jinja_tokens=dict(type="bool", default=False),
        case_sensitive=dict(type="bool", default=True),
        backup=dict(type="bool", default=True),
    )

    result = {
        "changed": False,
        "replaced_total": 0,
        "replaced_per_key": {},
        "backup_file": None,
    }

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    path = module.params["path"]
    placeholders = module.params["placeholders"] or {}
    whole_word = module.params["whole_word"]
    jinja_tokens = module.params["jinja_tokens"]
    case_sensitive = module.params["case_sensitive"]
    backup = module.params["backup"]

    if not os.path.exists(path):
        module.fail_json(msg=f"File not found: {path}", **result)

    try:
        with io.open(path, "r", encoding="utf-8") as f:
            original = f.read()
    except Exception as e:
        module.fail_json(msg=f"Failed to read file: {str(e)}", **result)

    content = original
    flags = 0 if case_sensitive else re.IGNORECASE

    total_replacements = 0
    per_key = {}

    # Iterate through target keys to process substitutions
    for key, value in sorted(placeholders.items()):
        pattern = build_pattern(key, whole_word, jinja_tokens, flags)
        content, count = pattern.subn(str(value), content)
        per_key[key] = count
        total_replacements += count

    result["replaced_total"] = total_replacements
    result["replaced_per_key"] = per_key

    # Check if modifications were actually executed
    if total_replacements > 0 and content != original:
        result["changed"] = True

        if not module.check_mode:
            # Create a localized backup file safely via Ansible core API
            if backup:
                result["backup_file"] = module.backup_local(path)

            # Write out content atomically to avoid file corruption spikes
            try:
                tmp_file_ctx = module.tmpdir or os.path.dirname(path)
                tmp_dest = os.path.join(tmp_file_ctx, f".ansible_tmp_{os.path.basename(path)}")
                with io.open(tmp_dest, "w", encoding="utf-8", newline="") as f:
                    f.write(content)
                module.atomic_move(tmp_dest, path)
            except Exception as e:
                module.fail_json(
                    msg=f"Failed to write modifications safely to file: {str(e)}",
                    **result,
                )

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
