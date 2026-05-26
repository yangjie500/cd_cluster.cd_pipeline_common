# Cd_cluster Pipeline_common Collection

This repository contains the `cd_cluster.pipeline_common` Ansible Collection.

<!--start requires_ansible-->
## Ansible version compatibility

This collection has been tested against following Ansible versions: **>=2.15.0**.

For collections that support Ansible 2.9, please ensure you update your `network_os` to use the
fully qualified collection name (for example, `cisco.ios.ios`).
Plugins and modules within a collection may be tested with only specific Ansible versions.
A collection may contain metadata that identifies these versions.
PEP440 is the schema used to describe the versions of Ansible.
<!--end requires_ansible-->

## External requirements

Some modules and plugins require external libraries. Please check the
requirements for each plugin or module you use in the documentation to find out
which requirements are needed.

## Python Dependencies

This collection requires the following Python libraries:

- requests
- tenacity

Dependencies must exist on the machine where the module executes.

### Controller-side execution (recommended)

Recommended usage:

```yaml
- name: Emit signal
  cd_cluster.pipeline_common.signal_emit:
    ...
  delegate_to: localhost
```

## Included content

<!--start collection content-->
### Modules
Name | Description
--- | ---
[cd_cluster.pipeline_common.oauth_token](http://example.com/repository/blob/main/docs/cd_cluster.pipeline_common.oauth_token_module.rst)|Get OAuth/JWT access token using server-side flows
[cd_cluster.pipeline_common.parse_structured_filename](http://example.com/repository/blob/main/docs/cd_cluster.pipeline_common.parse_structured_filename_module.rst)|Extracts structured key-value pairs from a delimited filename string.
[cd_cluster.pipeline_common.register_emitter](http://example.com/repository/blob/main/docs/cd_cluster.pipeline_common.register_emitter_module.rst)|Register signal emitter configuration
[cd_cluster.pipeline_common.replace_placeholders](http://example.com/repository/blob/main/docs/cd_cluster.pipeline_common.replace_placeholders_module.rst)|Replace custom tokens or text placeholders inside a file
[cd_cluster.pipeline_common.signal_emit](http://example.com/repository/blob/main/docs/cd_cluster.pipeline_common.signal_emit_module.rst)|Emit a signal using a registered emitter

<!--end collection content-->

## Using this collection

```bash
    ansible-galaxy collection install cd_cluster.pipeline_common
```

You can also include it in a `requirements.yml` file and install it via
`ansible-galaxy collection install -r requirements.yml` using the format:

```yaml
collections:
  - name: cd_cluster.pipeline_common
```

To upgrade the collection to the latest available version, run the following
command:

```bash
ansible-galaxy collection install cd_cluster.pipeline_common --upgrade
```

You can also install a specific version of the collection, for example, if you
need to downgrade when something is broken in the latest version (please report
an issue in this repository). Use the following syntax where `X.Y.Z` can be any
[available version](https://galaxy.ansible.com/cd_cluster/pipeline_common):

```bash
ansible-galaxy collection install cd_cluster.pipeline_common:==X.Y.Z
```

See
[Ansible Using Collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html)
for more details.

## Release notes

See the
[changelog](https://github.com/ansible-collections/cd_cluster.pipeline_common/tree/main/CHANGELOG.rst).

## Roadmap

<!-- Optional. Include the roadmap for this collection, and the proposed release/versioning strategy so users can anticipate the upgrade/update cycle. -->

## More information

<!-- List out where the user can find additional information, such as working group meeting times, slack/matrix channels, or documentation for the product this collection automates. At a minimum, link to: -->

- [Ansible collection development forum](https://forum.ansible.com/c/project/collection-development/27)
- [Ansible User guide](https://docs.ansible.com/ansible/devel/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/devel/dev_guide/index.html)
- [Ansible Collections Checklist](https://docs.ansible.com/ansible/devel/community/collection_contributors/collection_requirements.html)
- [Ansible Community code of conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html)
- [The Bullhorn (the Ansible Contributor newsletter)](https://docs.ansible.com/ansible/devel/community/communication.html#the-bullhorn)
- [News for Maintainers](https://forum.ansible.com/tag/news-for-maintainers)

## Licensing

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
