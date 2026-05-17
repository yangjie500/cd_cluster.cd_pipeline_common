<!-- DOCSIBLE START -->

# 📃 Role overview

## push_image_to_registry



Description: Orchestrates OCI image pushing by routing to Cosign or Skopeo sub-roles.






<details>
<summary><b>🧩 Argument Specifications in meta/argument_specs</b></summary>

#### Key: main

**Description**: 
- Inspects the 'index.json' file of a local OCI image layout.
- Routes to 'push_image_to_registry_cosign' if Cosign annotations are present.
- Routes to 'push_image_to_registry_generic' (Skopeo) if no special annotations are found.
- Aggregates files modified/deleted/created and execution outputs into a structured result.


**Options**:


  - **push_image_to_registry_src**
    - **Required**: True
    - **Type**: str
    - **Default**: none
  
    - **Description**: Path to the local directory containing the OCI image layout and index.json.
  
  
  

  - **push_image_to_registry_image_name**
    - **Required**: True
    - **Type**: str
    - **Default**: none
  
    - **Description**: The name of the image as it should be published in the target registry.
  
  
  

  - **push_image_to_registry_image_tag**
    - **Required**: false
    - **Type**: str
    - **Default**: latest
  
    - **Description**: The tag to apply to the pushed image.
  
  
  

  - **push_image_to_registry_registry_url**
    - **Required**: True
    - **Type**: str
    - **Default**: none
  
    - **Description**: The main registry target URL or repository path (e.g., 'ghcr.io/my-org').
  
  
  

  - **push_image_to_registry_registry_login_url**
    - **Required**: False
    - **Type**: str
    - **Default**: none
  
    - **Description**: The authentication endpoint URL (e.g., 'ghcr.io'). Defaults to registry_url if unconfigured.
  
  
  

  - **push_image_to_registry_registry_username**
    - **Required**: True
    - **Type**: str
    - **Default**: none
  
    - **Description**: Username required to authenticate against the registry endpoints.
  
  
  

  - **push_image_to_registry_registry_password**
    - **Required**: True
    - **Type**: str
    - **Default**: none
  
    - **Description**: Password or Access Token used to authenticate against the registry endpoints.
  
  
  

  - **push_image_to_registry_ssl_verify**
    - **Required**: false
    - **Type**: bool
    - **Default**: True
  
    - **Description**: Enforces or disables SSL/TLS validation checks for registry interactions.
  
  
  



</details>




### Defaults

**These are static variables with lower priority**

#### File: defaults/main.yml

| Var          | Type         | Value       |
|--------------|--------------|-------------|
| [push_image_to_registry_src](defaults/main.yml#L5)   | str |  |    
| [push_image_to_registry_image_name](defaults/main.yml#L8)   | str |  |    
| [push_image_to_registry_image_tag](defaults/main.yml#L11)   | str | `latest` |    
| [push_image_to_registry_registry_url](defaults/main.yml#L14)   | str |  |    
| [push_image_to_registry_registry_login_url](defaults/main.yml#L18)   | str |  |    
| [push_image_to_registry_registry_username](defaults/main.yml#L21)   | str |  |    
| [push_image_to_registry_registry_password](defaults/main.yml#L22)   | str |  |    
| [push_image_to_registry_ssl_verify](defaults/main.yml#L25)   | bool | `True` |    


### Vars

**These are variables with higher priority**
#### File: vars/main.yml

| Var          | Type         | Value       |
|--------------|--------------|-------------|
| [push_image_to_registry_src](vars/main.yml#L5)   | str |  |    
| [push_image_to_registry_image_name](vars/main.yml#L8)   | str |  |    
| [push_image_to_registry_image_tag](vars/main.yml#L11)   | str | `latest` |    
| [push_image_to_registry_registry_url](vars/main.yml#L14)   | str |  |    
| [push_image_to_registry_registry_login_url](vars/main.yml#L18)   | str |  |    
| [push_image_to_registry_registry_username](vars/main.yml#L21)   | str |  |    
| [push_image_to_registry_registry_password](vars/main.yml#L22)   | str |  |    
| [push_image_to_registry_ssl_verify](vars/main.yml#L25)   | bool | `True` |    


### Tasks


#### File: tasks/main.yml

| Name | Module | Has Conditions |
| ---- | ------ | -------------- |
| [INFO] Role Configuration: push_image_to_registry | ansible.builtin.debug | False |
| [INFO] Sanitize input variables | ansible.builtin.set_fact | False |
| [INFO] Initialize role tracking variables | ansible.builtin.set_fact | False |
| Push OCI-Compliant Image to Registry | block | False |
| Load index.json from source | ansible.builtin.slurp | False |
| Parse index.json facts | ansible.builtin.set_fact | False |
| Strategy: Evaluate which binary to push images to registry | ansible.builtin.set_fact | False |
| Push OCI-Compliant Image to Registry (Cosign) | ansible.builtin.include_role | True |
| Push OCI-Compliant Image to Registry (Skopeo) | ansible.builtin.include_role | True |







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
