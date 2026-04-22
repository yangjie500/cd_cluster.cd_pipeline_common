<!-- DOCSIBLE START -->

# 📃 Role overview

## fetch_files_sftp



Description: Use SFTP protocol to fetch file from remote server.










### Defaults

**These are static variables with lower priority**

#### File: defaults/main.yml

| Var          | Type         | Value       |
|--------------|--------------|-------------|
| [fetch_files_sftp_username](defaults/main.yml#L2)   | str |  |    
| [fetch_files_sftp_sftp_password](defaults/main.yml#L3)   | str |  |    
| [fetch_files_sftp_sftp_ip](defaults/main.yml#L4)   | str |  |    
| [fetch_files_sftp_file_path](defaults/main.yml#L5)   | str |  |    


### Vars

**These are variables with higher priority**
#### File: vars/main.yml

| Var          | Type         | Value       |
|--------------|--------------|-------------|
| [fetch_files_sftp_username](vars/main.yml#L2)   | str |  |    
| [fetch_files_sftp_sftp_password](vars/main.yml#L3)   | str |  |    
| [fetch_files_sftp_sftp_ip](vars/main.yml#L4)   | str |  |    
| [fetch_files_sftp_file_path](vars/main.yml#L5)   | str |  |    
| [fetch_files_sftp_file_path_dest](vars/main.yml#L6)   | str |  |    


### Tasks


#### File: tasks/main.yml

| Name | Module | Has Conditions |
| ---- | ------ | -------------- |
| Role Configuration: fetch_files_sftp | ansible.builtin.debug | False |
| Manage SFTP File Transfer | block | False |
| Pull file from SFTP server | ansible.builtin.shell | False |







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
