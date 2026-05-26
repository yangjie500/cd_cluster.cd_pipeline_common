#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Yang Jie
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
---
module: parse_structured_filename
short_description: Extracts structured key-value pairs from a delimited filename string.
description:
  - Takes a filename, automatically removes any file extensions
    (including multi-part extensions like .tar.gz),
    splits the remaining base name using a user-defined delimiter,
    and maps the pieces into an ordered list of keys.
options:
  filename:
    description: The full filename or string containing the structured data.
    required: true
    type: str
  delimiter:
    description: The character or substring used to separate the fields in the filename.
    required: true
    type: str
  keys:
    description: An ordered list of keys to pair with the extracted text segments.
    required: true
    type: list
    elements: str
author:
  - Yang Jie (@yangjie500)
"""

EXAMPLES = """
- name: Extract metadata from an artifact filename
  parse_structured_filename:
    filename: "hello+--12345+--v1.1.1+---20052026T121212.tar.gz"
    delimiter: "+--"
    keys:
      - name
      - tag
      - version
      - datetime
  register: artifact_metadata
"""

RETURN = """
parsed_data:
  description: A dictionary containing the extracted keys and their corresponding values.
  returned: success
  type: dict
"""

import os

from ansible.module_utils.basic import AnsibleModule


# Set of common archive and file extensions to explicitly strip
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
    # Scripts and Code Sources (including C++, C#, Rust, Python, Go, etc.)
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
    # Compiled Binaries, Objects, and Project Metadata
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
    # Media and Images
    ".png",
    ".jpg",
    ".jpeg",
    ".svg",
    ".gif",
    ".mp4",
    ".mp3",
}


def main():
    module_args = dict(
        filename=dict(type="str", required=True),
        delimiter=dict(type="str", required=True),
        keys=dict(type="list", elements="str", required=True),
    )

    result = dict(
        changed=False,
        filename="",
        cleaned_base_name="",
        delimiter="",
        extracted_fields=[],
        parsed_data={},
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    result["filename"] = module.params["filename"]
    result["delimiter"] = module.params["delimiter"]

    filename = module.params["filename"]
    delimiter = module.params["delimiter"]
    keys = module.params["keys"]

    if not filename.strip():
        module.fail_json(msg="Parameter 'filename' cannot be empty or blank spaces.", **result)

    if not delimiter:
        module.fail_json(msg="Parameter 'delimiter' cannot be empty.", **result)

    # Clean empty strings and whitespace from the user-provided keys
    keys = [k.strip() for k in keys if k.strip()]

    if not keys:
        module.fail_json(
            msg="Parameter 'keys' must contain at least one valid, non-empty key.",
            **result,
        )

    result["parsed_data"] = {k: "" for k in keys}

    # Cleanly remove common file extensions sequentially
    while True:
        root, ext = os.path.splitext(filename)
        if ext.lower() in COMMON_EXTENSIONS:
            filename = root
        else:
            break

    # Extract just the file name if a full directory path was provided
    filename = os.path.basename(filename)

    result["cleaned_base_name"] = filename

    parts = filename.split(delimiter)

    # Filter out empty strings that occur if delimiters are at the very start or end
    parts = [p for p in parts if p != ""]

    result["extracted_fields"] = parts

    # Enforce strict parsing match (if parts count doesn't match keys count, fail)
    if len(parts) != len(keys):
        module.fail_json(
            msg="Parsing mismatch. Expected {} fields based on keys, "
            "but found {} fields using delimiter '{}'.".format(
                len(keys),
                len(parts),
                delimiter,
            ),
            **result,
        )

    result["parsed_data"] = dict(zip(keys, parts))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
