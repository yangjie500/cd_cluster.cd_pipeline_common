<!-- DOCSIBLE START -->

# 📃 Role overview

## push_image_to_registry_generic



Description: Push container image using skopeo binary (Image MUST be OCI format)






<details>
<summary><b>🧩 Argument Specifications in meta/argument_specs</b></summary>

#### Key: main

**Description**: 
- This role handles registry authentication via Skopeo login and performs a 'skopeo copy' from a local OCI directory to a remote registry.
- It follows a standardized output pattern, returning a structured result object.


**Options**:


  - **push_image_to_registry_generic_src**
    - **Required**: True
    - **Type**: str
    - **Default**: none
  
    - **Description**: Path to the local directory containing the OCI image.
  
  
  

  - **push_image_to_registry_generic_image_name**
    - **Required**: True
    - **Type**: str
    - **Default**: none
  
    - **Description**: The name of the image in the target registry.
  
  
  

  - **push_image_to_registry_generic_image_tag**
    - **Required**: false
    - **Type**: str
    - **Default**: latest
  
    - **Description**: The tag to assign to the pushed image.
  
  
  

  - **push_image_to_registry_generic_registry_url**
    - **Required**: True
    - **Type**: str
    - **Default**: none
  
    - **Description**: The registry URL (e.g., 'ghcr.io' or 'my-registry.com').
  
  
  

  - **push_image_to_registry_generic_registry_username**
    - **Required**: True
    - **Type**: str
    - **Default**: none
  
    - **Description**: Username for registry authentication.
  
  
  

  - **push_image_to_registry_generic_registry_password**
    - **Required**: True
    - **Type**: str
    - **Default**: none
  
    - **Description**: Password or Token for registry authentication.
  
  
  

  - **push_image_to_registry_generic_ssl_verify**
    - **Required**: false
    - **Type**: bool
    - **Default**: True
  
    - **Description**: Whether to enable SSL/TLS certificate verification during login and copy.
  
  
  



</details>




### Defaults

**These are static variables with lower priority**

#### File: defaults/main.yml

| Var          | Type         | Value       |
|--------------|--------------|-------------|
| [push_image_to_registry_generic_src](defaults/main.yml#L5)   | str |  |    
| [push_image_to_registry_generic_image_name](defaults/main.yml#L8)   | str |  |    
| [push_image_to_registry_generic_image_tag](defaults/main.yml#L11)   | str | `latest` |    
| [push_image_to_registry_generic_registry_url](defaults/main.yml#L14)   | str |  |    
| [push_image_to_registry_generic_registry_username](defaults/main.yml#L17)   | str |  |    
| [push_image_to_registry_generic_registry_password](defaults/main.yml#L18)   | str |  |    
| [push_image_to_registry_generic_ssl_verify](defaults/main.yml#L21)   | bool | `True` |    


### Vars

**These are variables with higher priority**
#### File: vars/main.yml

| Var          | Type         | Value       |
|--------------|--------------|-------------|
| [push_image_to_registry_generic_src](vars/main.yml#L5)   | str |  |    
| [push_image_to_registry_generic_image_name](vars/main.yml#L8)   | str |  |    
| [push_image_to_registry_generic_image_tag](vars/main.yml#L11)   | str | `latest` |    
| [push_image_to_registry_generic_registry_url](vars/main.yml#L14)   | str |  |    
| [push_image_to_registry_generic_registry_username](vars/main.yml#L17)   | str |  |    
| [push_image_to_registry_generic_registry_password](vars/main.yml#L18)   | str |  |    
| [push_image_to_registry_generic_ssl_verify](vars/main.yml#L21)   | bool | `True` |    


### Tasks


#### File: tasks/main.yml

| Name | Module | Has Conditions |
| ---- | ------ | -------------- |
| [INFO] Role Configuration: push_image_to_registry_generic | ansible.builtin.debug | False |
| [INFO] Sanitize input variables | ansible.builtin.set_fact | False |
| [INFO] Initialize role tracking variables | ansible.builtin.set_fact | False |
| Manage Skopeo Push | block | False |
| Login to Registry with Skopeo | ansible.builtin.command | False |
| Push image using Skopeo | ansible.builtin.command | False |
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
