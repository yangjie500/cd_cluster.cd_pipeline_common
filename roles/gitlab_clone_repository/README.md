<!-- DOCSIBLE START -->

# 📃 Role overview

## gitlab_clone_repository



Description: Wrapper for git clone










### Defaults

**These are static variables with lower priority**

#### File: defaults/main.yml

| Var          | Type         | Value       |
|--------------|--------------|-------------|
| [gitlab_clone_repository_repo_url](defaults/main.yml#L5)   | str |  |    
| [gitlab_clone_repository_dest_path](defaults/main.yml#L8)   | str | `/var/www/application` |    
| [gitlab_clone_repository_version](defaults/main.yml#L11)   | str | `main` |    
| [gitlab_clone_repository_token_user](defaults/main.yml#L14)   | str | `oauth2` |    
| [gitlab_clone_repository_verify_remote_server](defaults/main.yml#L17)   | bool | `False` |    
| [gitlab_clone_repository_token](defaults/main.yml#L20)   | str |  |    


### Vars

**These are variables with higher priority**
#### File: vars/main.yml

| Var          | Type         | Value       |
|--------------|--------------|-------------|
| [gitlab_clone_repository_repo_url](vars/main.yml#L5)   | str |  |    
| [gitlab_clone_repository_dest_path](vars/main.yml#L8)   | str | `/var/www/application` |    
| [gitlab_clone_repository_version](vars/main.yml#L11)   | str | `main` |    
| [gitlab_clone_repository_token_user](vars/main.yml#L14)   | str | `oauth2` |    
| [gitlab_clone_repository_verify_remote_server](vars/main.yml#L17)   | bool | `False` |    
| [gitlab_clone_repository_token](vars/main.yml#L20)   | str |  |    


### Tasks


#### File: tasks/main.yml

| Name | Module | Has Conditions |
| ---- | ------ | -------------- |
| [INFO] Role Configuration: gitlab_clone_repository | ansible.builtin.debug | False |
| [INFO] Initialize role tracking variables | ansible.builtin.set_fact | False |
| Manage GitLab Clone | block | False |
| Clone the repository from GitLab | ansible.builtin.git | False |
| [INFO] Trigger file discovery to find file created | ansible.builtin.include_role | False |
| [INFO] Add discovered files to parent tracking list | ansible.builtin.set_fact | False |







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
