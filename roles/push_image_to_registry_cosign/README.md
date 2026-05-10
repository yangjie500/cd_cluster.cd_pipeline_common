<!-- DOCSIBLE START -->

# 📃 Role overview

## push_image_to_registry_cosign



Description: Push container image using cosign binary (Image MUST be OCI format)






<details>
<summary><b>🧩 Argument Specifications in meta/argument_specs</b></summary>

#### Key: main

**Description**: 


**Options**:


  - **push_image_to_registry_cosign_src**
    - **Required**: True
    - **Type**: str
    - **Default**: none
  
    - **Description**: Source directory containing the container files
  
  
  

  - **push_image_to_registry_cosign_image_name**
    - **Required**: false
    - **Type**: str
    - **Default**: 
  
    - **Description**: Name of the container image
  
  
  

  - **push_image_to_registry_cosign_image_tag**
    - **Required**: false
    - **Type**: str
    - **Default**: latest
  
    - **Description**: Tag for the container image
  
  
  

  - **push_image_to_registry_cosign_registry_url**
    - **Required**: True
    - **Type**: str
    - **Default**: none
  
    - **Description**: The registry URL for pushing the image
  
  
  

  - **push_image_to_registry_cosign_registry_login_url**
    - **Required**: True
    - **Type**: str
    - **Default**: none
  
    - **Description**: The URL used for cosign authentication
  
  
  

  - **push_image_to_registry_cosign_registry_username**
    - **Required**: True
    - **Type**: str
    - **Default**: none
  
    - **Description**: Username for registry authentication
  
  
  

  - **push_image_to_registry_cosign_registry_password**
    - **Required**: True
    - **Type**: str
    - **Default**: none
  
    - **Description**: Password/Token for registry authentication
  
  
  

  - **push_image_to_registry_cosign_ssl_verify**
    - **Required**: false
    - **Type**: bool
    - **Default**: False
  
    - **Description**: Verify remote server TLS certificates
  
  
  



</details>




### Defaults

**These are static variables with lower priority**

#### File: defaults/main.yml

| Var          | Type         | Value       |
|--------------|--------------|-------------|
| [push_image_to_registry_cosign_src](defaults/main.yml#L5)   | str |  |    
| [push_image_to_registry_cosign_image_name](defaults/main.yml#L8)   | str |  |    
| [push_image_to_registry_cosign_image_tag](defaults/main.yml#L11)   | str | `latest` |    
| [push_image_to_registry_cosign_registry_url](defaults/main.yml#L14)   | str |  |    
| [push_image_to_registry_cosign_registry_login_url](defaults/main.yml#L17)   | str |  |    
| [push_image_to_registry_cosign_registry_username](defaults/main.yml#L20)   | str |  |    
| [push_image_to_registry_cosign_registry_password](defaults/main.yml#L21)   | str |  |    
| [push_image_to_registry_cosign_ssl_verify](defaults/main.yml#L24)   | bool | `False` |    


### Vars

**These are variables with higher priority**
#### File: vars/main.yml

| Var          | Type         | Value       |
|--------------|--------------|-------------|
| [push_image_to_registry_cosign_src](vars/main.yml#L5)   | str |  |    
| [push_image_to_registry_cosign_image_name](vars/main.yml#L8)   | str |  |    
| [push_image_to_registry_cosign_image_tag](vars/main.yml#L11)   | str | `latest` |    
| [push_image_to_registry_cosign_registry_url](vars/main.yml#L14)   | str |  |    
| [push_image_to_registry_cosign_registry_login_url](vars/main.yml#L17)   | str |  |    
| [push_image_to_registry_cosign_registry_username](vars/main.yml#L20)   | str |  |    
| [push_image_to_registry_cosign_registry_password](vars/main.yml#L21)   | str |  |    
| [push_image_to_registry_cosign_ssl_verify](vars/main.yml#L24)   | bool | `False` |    


### Tasks


#### File: tasks/main.yml

| Name | Module | Has Conditions |
| ---- | ------ | -------------- |
| [INFO] Role Configuration: push_image_to_registry_cosign | ansible.builtin.debug | False |
| [INFO] Sanitize input variables (set defaults for UNDEFINED strings) | ansible.builtin.set_fact | False |
| [INFO] Initialize role tracking variables | ansible.builtin.set_fact | False |
| Manage Cosign Push | block | False |
| Login to Cosign Registry | ansible.builtin.command | False |
| Push (Load) image to registry | ansible.builtin.command | False |
| [INFO] Update custom facts with operation output | ansible.builtin.set_fact | False |







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
