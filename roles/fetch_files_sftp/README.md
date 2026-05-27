<!-- DOCSIBLE START -->

# 📃 Role overview

## fetch_files_sftp



Description: Use SFTP protocol to fetch file from remote server.






<details>
<summary><b>🧩 Argument Specifications in meta/argument_specs</b></summary>

#### Key: main

**Description**: 
- Connects to a remote SFTP server using username/password authentication.
- Transfers a remote file from the source path to a local destination path.
- Provides structured role output including failure categorization and transfer metadata.


**Options**:


  - **fetch_files_sftp_username**
    - **Required**: True
    - **Type**: str
    - **Default**: none
    - **Description**: 
   - Username used to authenticate against the remote SFTP server.
  
  
  
  

  - **fetch_files_sftp_sftp_ip**
    - **Required**: True
    - **Type**: str
    - **Default**: none
    - **Description**: 
   - Hostname or IP address of the remote SFTP server.
  
  
  
  

  - **fetch_files_sftp_sftp_password**
    - **Required**: True
    - **Type**: str
    - **Default**: none
    - **Description**: 
   - Password used to authenticate against the remote SFTP server.
  
  
  
  

  - **fetch_files_sftp_file_path_src**
    - **Required**: True
    - **Type**: str
    - **Default**: none
    - **Description**: 
   - Remote source file path on the SFTP server.
  
  
  
  

  - **fetch_files_sftp_file_path_dest**
    - **Required**: True
    - **Type**: str
    - **Default**: none
    - **Description**: 
   - Local destination path where the downloaded file will be stored.
  
  
  
  

  - **fetch_files_sftp_strict_host_key_checking**
    - **Required**: False
    - **Type**: bool
    - **Default**: False
    - **Description**: 
   - Controls whether SSH strict host key checking is enforced during the SFTP transfer.
  
  
  
  



</details>




### Defaults

**These are static variables with lower priority**

#### File: defaults/main.yml

| Var          | Type         | Value       |
|--------------|--------------|-------------|
| [fetch_files_sftp_username](defaults/main.yml#L3)   | str |  |    
| [fetch_files_sftp_sftp_ip](defaults/main.yml#L4)   | str |  |    
| [fetch_files_sftp_sftp_password](defaults/main.yml#L5)   | str |  |    
| [fetch_files_sftp_file_path_src](defaults/main.yml#L7)   | str |  |    
| [fetch_files_sftp_file_path_dest](defaults/main.yml#L8)   | str |  |    
| [fetch_files_sftp_strict_host_key_checking](defaults/main.yml#L9)   | bool | `False` |    
| [fetch_files_sftp_connect_timeout](defaults/main.yml#L11)   | int | `5` |    
| [fetch_files_sftp_connection_attempts](defaults/main.yml#L12)   | int | `1` |    


### Vars

**These are variables with higher priority**
#### File: vars/main.yml

| Var          | Type         | Value       |
|--------------|--------------|-------------|
| [fetch_files_sftp_username](vars/main.yml#L3)   | str |  |    
| [fetch_files_sftp_sftp_ip](vars/main.yml#L4)   | str |  |    
| [fetch_files_sftp_sftp_password](vars/main.yml#L5)   | str |  |    
| [fetch_files_sftp_file_path_src](vars/main.yml#L7)   | str |  |    
| [fetch_files_sftp_file_path_dest](vars/main.yml#L8)   | str |  |    
| [fetch_files_sftp_strict_host_key_checking](vars/main.yml#L9)   | bool | `False` |    
| [fetch_files_sftp_connect_timeout](vars/main.yml#L11)   | int | `5` |    
| [fetch_files_sftp_connection_attempts](vars/main.yml#L12)   | int | `1` |    


### Tasks


#### File: tasks/main.yml

| Name | Module | Has Conditions |
| ---- | ------ | -------------- |
| [INFO] Role Configuration: fetch_files_sftp | ansible.builtin.debug | False |
| [INFO] Sanitize input variables | ansible.builtin.set_fact | False |
| [INFO] Initialize role tracking variables | ansible.builtin.set_fact | False |
| Manage SFTP File Transfer | block | False |
| Validate required SFTP inputs | ansible.builtin.assert | False |
| [INFO] Pull file from SFTP server | ansible.builtin.command | False |
| [INFO] Update tracked files after successful transfer | ansible.builtin.set_fact | False |
| [INFO] Update custom facts with transfer output | ansible.builtin.set_fact | False |







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
