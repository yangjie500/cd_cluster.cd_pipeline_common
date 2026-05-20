<!-- DOCSIBLE START -->

# 📃 Role overview

## verify_signature_cosign



Description: A role that uses Cosign to verify the integrity and provenance of local artifact blobs against a cryptographic signature and public key file.






<details>
<summary><b>🧩 Argument Specifications in meta/argument_specs</b></summary>

#### Key: main

**Description**: 
- A verification role that performs signature attestation on binary blobs.
- It utilizes the 'cosign verify-blob' utility with a local public key file


**Options**:


  - **verify_signature_cosign_blob_file_path**
    - **Required**: True
    - **Type**: str
    - **Default**: none
  
    - **Description**: The absolute or relative local filesystem path to the target artifact blob being verified.
  
  
  

  - **verify_signature_cosign_sig_file_path**
    - **Required**: True
    - **Type**: str
    - **Default**: none
  
    - **Description**: The absolute or relative local filesystem path to the signature file generated for the corresponding blob.
  
  
  

  - **verify_signature_cosign_pub_key_file_path**
    - **Required**: True
    - **Type**: str
    - **Default**: none
  
    - **Description**: The absolute or relative local filesystem path to the public key file (e.g., cosign.pub) used for signature matching.
  
  
  



</details>




### Defaults

**These are static variables with lower priority**

#### File: defaults/main.yml

| Var          | Type         | Value       |
|--------------|--------------|-------------|
| [verify_signature_cosign_blob_file_path](defaults/main.yml#L5)   | str |  |    
| [verify_signature_cosign_sig_file_path](defaults/main.yml#L8)   | str |  |    
| [verify_signature_cosign_pub_key_file_path](defaults/main.yml#L11)   | str |  |    


### Vars

**These are variables with higher priority**
#### File: vars/main.yml

| Var          | Type         | Value       |
|--------------|--------------|-------------|
| [verify_signature_cosign_blob_file_path](vars/main.yml#L5)   | str |  |    
| [verify_signature_cosign_sig_file_path](vars/main.yml#L8)   | str |  |    
| [verify_signature_cosign_pub_key_file_path](vars/main.yml#L11)   | str |  |    


### Tasks


#### File: tasks/main.yml

| Name | Module | Has Conditions |
| ---- | ------ | -------------- |
| [INFO] Role Configuration: verify_signature_cosign | ansible.builtin.debug | False |
| [INFO] Sanitize input variables (set defaults for UNDEFINED strings) | ansible.builtin.set_fact | False |
| [INFO] Initialize role tracking variables | ansible.builtin.set_fact | False |
| Manage Cosign Signature Verification | block | False |
| Execute Cosign Blob Verification Command | ansible.builtin.command | False |
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
