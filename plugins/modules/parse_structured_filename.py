#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Yang Jie
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
---
module: parse_structured_filename

short_description: Extract structured key-value metadata from a delimited filename.

description:
  - Takes a filename or path, removes common file extensions
    (including multi-part extensions such as C(.tar.gz)),
    splits the remaining base filename using a user-defined delimiter,
    and maps the extracted fields into user-defined field names.

options:
  filename:
    description:
      - Full filename or path containing structured metadata.
    required: true
    type: str

  delimiter:
    description:
      - Delimiter used to separate metadata fields.
    required: true
    type: str

  field_names:
    description:
      - Ordered list of field names used to map extracted values.
    required: true
    type: list
    elements: str

author:
  - Yang Jie (@yangjie500)
"""

EXAMPLES = """
- name: Extract metadata from structured filename
  cd_cluster.pipeline_common.parse_structured_filename:
    filename: "hello+--12345+--v1.1.1+--20052026T121212.tar.gz"
    delimiter: "+--"
    field_names:
      - name
      - tag
      - version
      - datetime
  register: artifact_metadata

- name: Extract metadata from absolute path
  cd_cluster.pipeline_common.parse_structured_filename:
    filename: "/var/tmp/builds/hello+--12345+--v1.1.1+--20052026T121212.tar.gz"
    delimiter: "+--"
    field_names:
      - name
      - tag
      - version
      - datetime
"""

RETURN = """
parsed_data:
  description:
    - Dictionary containing parsed structured metadata.
  returned: success
  type: dict
  sample:
    name: hello
    tag: "12345"
    version: v1.1.1
    datetime: 20052026T121212

cleaned_base_name:
  description:
    - Filename after extension stripping.
  returned: success
  type: str

extracted_fields:
  description:
    - Ordered list of extracted values.
  returned: success
  type: list
  elements: str
"""

import os

from ansible.module_utils.basic import AnsibleModule


COMMON_EXTENSIONS = {
    # Archive and Compression
    ".tar",
    ".gz",
    ".gzip",
    ".tgz",
    ".zip",
    ".zipx",
    ".bz2",
    ".tbz2",
    ".xz",
    ".txz",
    ".7z",
    ".rar",
    ".zst",
    ".tzst",
    # Application Packages and Build Artifacts
    ".jar",
    ".war",
    ".ear",
    ".whl",
    ".rpm",
    ".deb",
    ".apk",
    ".msi",
    ".exe",
    ".dmg",
    ".iso",
    # Configuration and Structured Data
    ".yaml",
    ".yml",
    ".json",
    ".xml",
    ".ini",
    ".cfg",
    ".conf",
    ".toml",
    ".csv",
    ".tsv",
    # Scripts and Code Sources
    ".sh",
    ".bash",
    ".py",
    ".pl",
    ".rb",
    ".js",
    ".ts",
    ".go",
    ".cpp",
    ".cc",
    ".cxx",
    ".h",
    ".hpp",
    ".cs",
    ".rs",
    # Compiled Artifacts
    ".o",
    ".obj",
    ".dll",
    ".pdb",
    ".csproj",
    ".sln",
    ".rlib",
    ".d",
    # Documentation and Text
    ".txt",
    ".log",
    ".md",
    ".pdf",
    ".doc",
    ".docx",
    # Media
    ".png",
    ".jpg",
    ".jpeg",
    ".svg",
    ".gif",
    ".mp4",
    ".mp3",
}


def strip_common_extensions(filename: str) -> str:
    """
    Remove common single-part and multi-part file extensions.
    """

    while True:
        root, ext = os.path.splitext(filename)

        if ext.lower() in COMMON_EXTENSIONS:
            filename = root
        else:
            break

    return filename


def main() -> None:
    module_args = dict(
        filename=dict(type="str", required=True),
        delimiter=dict(type="str", required=True),
        field_names=dict(
            type="list",
            elements="str",
            required=True,
        ),
    )

    result = dict(
        changed=False,
        filename="",
        cleaned_base_name="",
        delimiter="",
        extracted_fields=[],
        parsed_data={},
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    result["filename"] = module.params["filename"]
    result["delimiter"] = module.params["delimiter"]

    filename = module.params["filename"]
    delimiter = module.params["delimiter"]
    field_names = module.params["field_names"]

    if not filename.strip():
        module.fail_json(
            msg="Parameter 'filename' cannot be empty or blank spaces.",
            **result,
        )

    if not delimiter:
        module.fail_json(
            msg="Parameter 'delimiter' cannot be empty.",
            **result,
        )

    field_names = [field_name.strip() for field_name in field_names if field_name.strip()]

    if not field_names:
        module.fail_json(
            msg=(
                "Parameter 'field_names' must contain at least one " "valid, non-empty field name."
            ),
            **result,
        )

    result["parsed_data"] = {field_name: "" for field_name in field_names}

    filename = strip_common_extensions(filename)

    filename = os.path.basename(filename)

    result["cleaned_base_name"] = filename

    extracted_fields = filename.split(delimiter)

    extracted_fields = [field for field in extracted_fields if field != ""]

    result["extracted_fields"] = extracted_fields

    if len(extracted_fields) != len(field_names):
        module.fail_json(
            msg=(
                "Parsing mismatch. Expected {} fields based on "
                "field_names, but found {} fields using delimiter '{}'."
            ).format(
                len(field_names),
                len(extracted_fields),
                delimiter,
            ),
            **result,
        )

    result["parsed_data"] = dict(
        zip(
            field_names,
            extracted_fields,
        ),
    )

    module.exit_json(**result)


if __name__ == "__main__":
    main()
