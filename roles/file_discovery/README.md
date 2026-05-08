<!-- DOCSIBLE START -->

# 📃 Role overview

## file_discovery



Description: Find all files in a folder










### Defaults

**These are static variables with lower priority**

#### File: defaults/main.yml

| Var          | Type         | Value       |
|--------------|--------------|-------------|
| [file_discovery_path](defaults/main.yml#L5)   | str | `/tmp` |    
| [file_discovery_recursive](defaults/main.yml#L8)   | bool | `True` |    
| [file_discovery_patterns](defaults/main.yml#L11)   | str | `*` |    


### Vars

**These are variables with higher priority**
#### File: vars/main.yml

| Var          | Type         | Value       |
|--------------|--------------|-------------|
| [file_discovery_path](vars/main.yml#L5)   | str | `/tmp` |    
| [file_discovery_recursive](vars/main.yml#L8)   | bool | `True` |    
| [file_discovery_patterns](vars/main.yml#L11)   | str | `*` |    


### Tasks


#### File: tasks/main.yml

| Name | Module | Has Conditions |
| ---- | ------ | -------------- |
| [INFO] Role Configuration: file_discovery | ansible.builtin.debug | False |
| [INFO] Initialize role tracking variables | ansible.builtin.set_fact | False |
| Manage File Discovery | block | False |
| Find files in {{ file_discovery_path }} | ansible.builtin.find | False |
| Store discovered paths in custom facts dictionary | ansible.builtin.set_fact | False |







## Author Information
Yang Jie

#### License

MIT

#### Minimum Ansible Version

2.20

#### Platforms

No platforms specified.

#### Dependencies

No dependencies specified.
<!-- DOCSIBLE END -->
