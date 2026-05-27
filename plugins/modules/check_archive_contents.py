#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Yang Jie
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = r"""
---
module: check_archive_contents
short_description: Verify if a tar archive contains a specific list of required files
description:
  - Inspects a .tar, .tar.gz, or .tar.bz2 archive to confirm
    whether a list of required files exists inside it.
  - Supports both exact relative paths and matches based on the file's base name.
options:
  archive_path:
    description: Path to the tar archive on the target system.
    required: true
    type: path
  required_files:
    description: List of filenames or relative paths that must be present in the archive.
    required: true
    type: list
    elements: str
author:
  - Yang Jie (@yangjie500)
"""

EXAMPLES = r"""
- name: Verify a release bundle contains necessary app configurations
  verify_archive_contents:
    archive_path: /tmp/release-v1.tar.gz
    required_files:
      - settings.conf
      - db/schema.sql
  register: archive_check

- name: Fail execution if files are missing
  ansible.builtin.fail:
    msg: "Critical deployment files are missing from the archive!"
  when: not archive_check.matched
"""

RETURN = r"""
changed:
  description: State showing if the system was modified. Always false for validation modules.
  type: bool
  returned: always
matched:
  description: True if all specified required_files were discovered inside the target archive.
  type: bool
  returned: always
archive_path:
  description: The target path to the analyzed archive file.
  type: str
  returned: always
required_files:
  description: The original list of files provided to the module for validation tracking.
  type: list
  elements: str
  returned: always
found_files:
  description: A sorted list of the subset of required files that were successfully located.
  type: list
  elements: str
  returned: always
"""

import os
import tarfile

from ansible.module_utils.basic import AnsibleModule


def archive_contains_required_files(
    archive_path: str,
    required_files: list[str],
) -> tuple[bool, list[str]]:
    """Efficiently determines if target files exist inside a compressed archive."""
    found = set()
    required_set = set(required_files)

    try:
        with tarfile.open(archive_path, mode="r:*") as tar:
            for name in tar.getnames():
                # Check for an exact relative path match
                if name in required_set:
                    found.add(name)

                # Check for a base filename match
                base_name = os.path.basename(name)
                if base_name in required_set:
                    found.add(base_name)

                # Early exit if we have found every requested file
                if len(found) == len(required_set):
                    break

    except tarfile.TarError:
        # Gracefully hand back empty sets to let the parent handle the error string
        return False, []

    return required_set.issubset(found), sorted(list(found))


def main():
    module = AnsibleModule(
        argument_spec={
            "archive_path": {
                "type": "path",
                "required": True,
            },
            "required_files": {
                "type": "list",
                "elements": "str",
                "required": True,
            },
        },
        supports_check_mode=True,
    )

    archive_path = module.params["archive_path"]
    required_files = module.params["required_files"]

    if not os.path.exists(archive_path):
        module.fail_json(msg=f"archive_path does not exist or cannot be accessed: {archive_path}")

    try:
        matched, found_files = archive_contains_required_files(
            archive_path,
            required_files,
        )
    except Exception as e:
        module.fail_json(msg=f"Unexpected error inspecting archive contents: {str(e)}")

    module.exit_json(
        changed=False,
        matched=matched,
        archive_path=archive_path,
        required_files=required_files,
        found_files=found_files,
    )


if __name__ == "__main__":
    main()
