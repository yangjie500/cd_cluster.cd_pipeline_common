<!-- DOCSIBLE START -->

# 📃 Role overview

## gitlab_push_repository



Description: Wrapper for git push










### Defaults

**These are static variables with lower priority**

#### File: defaults/main.yml

| Var          | Type         | Value       |
|--------------|--------------|-------------|
| [gitlab_push_repository_src_path](defaults/main.yml#L5)   | str | `/tmp/my-repo` |    
| [gitlab_push_repository_branch](defaults/main.yml#L8)   | str | `main` |    
| [gitlab_push_repository_tag](defaults/main.yml#L11)   | str |  |    
| [gitlab_push_repository_message](defaults/main.yml#L14)   | str | `Ansible automated update` |    
| [gitlab_push_repository_url](defaults/main.yml#L17)   | str |  |    
| [gitlab_push_repository_token_user](defaults/main.yml#L20)   | str | `oauth2` |    
| [gitlab_push_repository_verify_remote_server](defaults/main.yml#L23)   | bool | `False` |    
| [gitlab_push_repository_token](defaults/main.yml#L26)   | str |  |    


### Vars

**These are variables with higher priority**
#### File: vars/main.yml

| Var          | Type         | Value       |
|--------------|--------------|-------------|
| [gitlab_push_repository_src_path](vars/main.yml#L5)   | str | `/tmp/my-repo` |    
| [gitlab_push_repository_branch](vars/main.yml#L8)   | str | `main` |    
| [gitlab_push_repository_tag](vars/main.yml#L11)   | str |  |    
| [gitlab_push_repository_message](vars/main.yml#L14)   | str | `Ansible automated update` |    
| [gitlab_push_repository_url](vars/main.yml#L17)   | str |  |    
| [gitlab_push_repository_token_user](vars/main.yml#L20)   | str | `oauth2` |    
| [gitlab_push_repository_verify_remote_server](vars/main.yml#L23)   | bool | `False` |    
| [gitlab_push_repository_token](vars/main.yml#L26)   | str |  |    


### Tasks


#### File: tasks/main.yml

| Name | Module | Has Conditions |
| ---- | ------ | -------------- |
| Role Configuration: {{ role_name }} | ansible.builtin.debug | False |
| Initialize role tracking variables | ansible.builtin.set_fact | False |
| Manage GitLab Push via git_acp | block | False |
| Configure Git to automatically setup remote tracking on push | ansible.builtin.command | False |
| Create and switch to the target branch locally | ansible.builtin.command | True |
| Execute Git Add-Commit-Push | lvrfrc87.git_acp.git_acp | False |
| Push with Tag | block | True |
| Create local tag | ansible.builtin.command | False |
| Push tag to remote | ansible.builtin.command | False |







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
