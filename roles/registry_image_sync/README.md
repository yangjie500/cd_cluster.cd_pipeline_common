<!-- DOCSIBLE START -->

# 📃 Role overview

## registry_image_sync



Description: Sync container images and signatures between registries using Skopeo.






<details>
<summary><b>🧩 Argument Specifications in meta/argument_specs</b></summary>

#### Key: main

**Description**: 
- Logs into source and destination registries.
- Generates clean image configurations from components.
- Pushes targeted image blobs along with matching structural .sig signature assets.


**Options**:


  - **registry_image_sync_src_registry_url**
    - **Required**: True
    - **Type**: str
    - **Default**: none
  
    - **Description**: Base hostname URL for the origin remote engine repository registry.
  
  
  

  - **registry_image_sync_src_username**
    - **Required**: True
    - **Type**: str
    - **Default**: none
  
    - **Description**: Username credential targeting read access on the origin registry infrastructure.
  
  
  

  - **registry_image_sync_src_password**
    - **Required**: True
    - **Type**: str
    - **Default**: none
  
    - **Description**: Password secret credential pairing with origin username authentication blocks.
  
  
  

  - **registry_image_sync_src_image_name**
    - **Required**: True
    - **Type**: str
    - **Default**: none
  
    - **Description**: Target source image path scope name cataloged inside origin namespace boundaries.
  
  
  

  - **registry_image_sync_src_image_tag**
    - **Required**: True
    - **Type**: str
    - **Default**: none
  
    - **Description**: Explicit semantic versioning tag pinning down source tracking criteria targets.
  
  
  

  - **registry_image_sync_src_tls_verify**
    - **Required**: false
    - **Type**: bool
    - **Default**: True
  
    - **Description**: Enforces strict TLS security socket certificate validation layer matches on origin queries.
  
  
  

  - **registry_image_sync_dest_registry_url**
    - **Required**: True
    - **Type**: str
    - **Default**: none
  
    - **Description**: Base hostname URL identifying target end destination repository systems.
  
  
  

  - **registry_image_sync_dest_username**
    - **Required**: True
    - **Type**: str
    - **Default**: none
  
    - **Description**: Username operational identity claiming write authorization inside destination space blocks.
  
  
  

  - **registry_image_sync_dest_password**
    - **Required**: True
    - **Type**: str
    - **Default**: none
  
    - **Description**: Secure password or access token string mapped to target target writing identity profiles.
  
  
  

  - **registry_image_sync_dest_image_name**
    - **Required**: True
    - **Type**: str
    - **Default**: none
  
    - **Description**: Target path assignment mapped inside the target target registry systems namespace.
  
  
  

  - **registry_image_sync_dest_image_tag**
    - **Required**: True
    - **Type**: str
    - **Default**: none
  
    - **Description**: Target version tagging naming marker expected on finalized storage structures.
  
  
  

  - **registry_image_sync_dest_tls_verify**
    - **Required**: false
    - **Type**: bool
    - **Default**: True
  
    - **Description**: Enforces TLS verification constraints during outbound storage writes on destination endpoints.
  
  
  



</details>




### Defaults

**These are static variables with lower priority**

#### File: defaults/main.yml

| Var          | Type         | Value       |
|--------------|--------------|-------------|
| [registry_image_sync_src_registry_url](defaults/main.yml#L5)   | str |  |    
| [registry_image_sync_src_username](defaults/main.yml#L6)   | str |  |    
| [registry_image_sync_src_password](defaults/main.yml#L7)   | str |  |    
| [registry_image_sync_src_image_name](defaults/main.yml#L8)   | str |  |    
| [registry_image_sync_src_image_tag](defaults/main.yml#L9)   | str |  |    
| [registry_image_sync_src_tls_verify](defaults/main.yml#L10)   | bool | `True` |    
| [registry_image_sync_dest_registry_url](defaults/main.yml#L13)   | str |  |    
| [registry_image_sync_dest_username](defaults/main.yml#L14)   | str |  |    
| [registry_image_sync_dest_password](defaults/main.yml#L15)   | str |  |    
| [registry_image_sync_dest_image_name](defaults/main.yml#L16)   | str |  |    
| [registry_image_sync_dest_image_tag](defaults/main.yml#L17)   | str |  |    
| [registry_image_sync_dest_tls_verify](defaults/main.yml#L18)   | bool | `True` |    


### Vars

**These are variables with higher priority**
#### File: vars/main.yml

| Var          | Type         | Value       |
|--------------|--------------|-------------|
| [registry_image_sync_src_registry_url](vars/main.yml#L5)   | str |  |    
| [registry_image_sync_src_username](vars/main.yml#L6)   | str |  |    
| [registry_image_sync_src_password](vars/main.yml#L7)   | str |  |    
| [registry_image_sync_src_image_name](vars/main.yml#L8)   | str |  |    
| [registry_image_sync_src_image_tag](vars/main.yml#L9)   | str |  |    
| [registry_image_sync_src_tls_verify](vars/main.yml#L10)   | bool | `True` |    
| [registry_image_sync_dest_registry_url](vars/main.yml#L13)   | str |  |    
| [registry_image_sync_dest_username](vars/main.yml#L14)   | str |  |    
| [registry_image_sync_dest_password](vars/main.yml#L15)   | str |  |    
| [registry_image_sync_dest_image_name](vars/main.yml#L16)   | str |  |    
| [registry_image_sync_dest_image_tag](vars/main.yml#L17)   | str |  |    
| [registry_image_sync_dest_tls_verify](vars/main.yml#L18)   | bool | `True` |    


### Tasks


#### File: tasks/main.yml

| Name | Module | Has Conditions |
| ---- | ------ | -------------- |
| [INFO] Role Configuration: registry_image_sync | ansible.builtin.debug | False |
| [INFO] Sanitize input variables (set defaults) | ansible.builtin.set_fact | False |
| [INFO] Initialize role tracking variables | ansible.builtin.set_fact | False |
| Manage Skopeo Container Image Transfer | block | False |
| Construct complete image URLs | ansible.builtin.set_fact | False |
| Log into source registry via Skopeo | ansible.builtin.command | True |
| Log into destination registry via Skopeo | ansible.builtin.command | True |
| Execute Skopeo core image sync copy | ansible.builtin.command | False |
| Inspect source image to pull its structural Digest hash | ansible.builtin.command | False |
| Parse image digest fact and format as cosign signature tag | ansible.builtin.set_fact | False |
| Create the signature tag | ansible.builtin.set_fact | False |
| [INFO] Showing signature tag | ansible.builtin.debug | False |
| Check source registry for the explicit existence of a signature tag | ansible.builtin.command | False |
| Mark signature presence flag state | ansible.builtin.set_fact | False |
| Copy signature tag over to target destination registry if found | ansible.builtin.command | True |
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
