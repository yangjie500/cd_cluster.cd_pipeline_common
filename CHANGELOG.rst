=====================================================
Cd\_cluster Pipeline\_common Collection Release Notes
=====================================================

.. contents:: Topics

v1.1.0
======

Minor Changes
-------------

- Added baseline development tooling and validation support, including unit test scaffolding, pre-commit configuration, and VS Code workspace settings.
- Added the `check_archive_contents` module to validate required files within `.tar`, `.tar.gz`, and `.tar.bz2` archives, including support for nested path basename matching and structured validation results.
- Added the `fetch_files_sftp` role to retrieve files from remote SFTP servers
- Added the `gitlab_clone_repository` role to clone repositories from both public and private GitLab instances.
- Added the `gitlab_push_repository` role to push local repository changes and tags to remote GitLab repositories, including support for pushing to alternate branches.
- Added the `oauth_token` module to retrieve access tokens using OAuth server-side authentication flows.
- Added the `parse_structured_filename` module to extract structured key-value metadata from delimited filenames, including support for stripping common file extensions and validating extracted fields against expected key mappings.
- Added the `push_image_to_registry_cosign` role to push OCI-compliant container images and signature artifacts to remote registries using Sigstore Cosign.
- Added the `push_image_to_registry_generic` role to push OCI-compliant container images to remote registries using Skopeo.
- Added the `push_image_to_registry` role to provide a unified interface for pushing OCI-compliant container images using either Skopeo or Sigstore Cosign.
- Added the `register_emitter` and `signal_emit` modules to support reusable emitter registration and structured signal emission workflows.
- Added the `registry_image_sync` role to support registry-to-registry OCI image synchronization, including registry authentication, configurable TLS verification, unsigned image handling.
- Added the `replace_placeholders` module to replace placeholder values in files using `<VAR>` and `{{ VAR }}` token formats.
- Added the `validate_environment_inputs` role to validate required environment variables and secrets before pipeline execution.
- Added the `verify_signature_cosign` module to verify container image and artifact signatures using Sigstore Cosign.
- Added the initial collection project structure, including automated documentation generation, Molecule scenario setup, and CI/CD configuration targeting Ansible 2.20 and Python 3.12.

Bugfixes
--------

- Added retry handling for registry image push operations using Skopeo and Sigstore Cosign.
- Fixed TLS and SSL verification boolean handling across GitLab and registry image roles.
- Updated the execution environment build configuration to include required registry, Git, SSH, and Cosign tooling.

Documentation Changes
---------------------

- Documented runtime dependency requirements for the `requests` and `tenacity` Python libraries.
