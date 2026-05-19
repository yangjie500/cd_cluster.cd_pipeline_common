<!-- DOCSIBLE START -->

# 📃 Role overview

## validate_environment_inputs



Description: Validation role that ensures mandatory environment variables and secrets are loaded, non-empty, and tracked safely before pipeline execution.






<details>
<summary><b>🧩 Argument Specifications in meta/argument_specs</b></summary>

#### Key: main

**Description**: 
- An enterprise-grade validation role that ensures mandatory environment variables and secrets are loaded and non-empty.
- It aggregates all validation failures and tracks the extracted values cleanly for downstream consumption.


**Options**:


  - **validate_environment_lists_check_variables**
    - **Required**: False
    - **Type**: list
    - **Default**: []
  
    - **Description**: The list of standard environment variable names to validate and expose in cleartext log outputs.
  
  
  

  - **validate_environment_lists_check_secrets**
    - **Required**: False
    - **Type**: list
    - **Default**: []
  
    - **Description**: The list of secret environment variable names to validate and capture in cleartext, but mask from logging streams.
  
  
  



</details>




### Defaults

**These are static variables with lower priority**

#### File: defaults/main.yml

| Var          | Type         | Value       |
|--------------|--------------|-------------|
| [validate_environment_inputs_check_variables](defaults/main.yml#L5)   | list | `[]` |    
| [validate_environment_inputs_check_secrets](defaults/main.yml#L8)   | list | `[]` |    


### Vars

**These are variables with higher priority**
#### File: vars/main.yml

| Var          | Type         | Value       |
|--------------|--------------|-------------|
| [validate_environment_inputs_check_variables](vars/main.yml#L5)   | list | `[]` |    
| [validate_environment_inputs_check_secrets](vars/main.yml#L8)   | list | `[]` |    


### Tasks


#### File: tasks/main.yml

| Name | Module | Has Conditions |
| ---- | ------ | -------------- |
| [INFO] Role Configuration: validate_environment_inputs | ansible.builtin.debug | False |
| [INFO] Sanitize input variables (set defaults for UNDEFINED lists) | ansible.builtin.set_fact | False |
| [INFO] Initialize role tracking variables | ansible.builtin.set_fact | False |
| Manage Environment List Validation | block | False |
| Fail if input parameters are not valid lists | ansible.builtin.fail | True |
| Verify environment variables exist and are not empty | ansible.builtin.fail | True |
| Verify environment secrets exist and are not empty | ansible.builtin.fail | True |
| Parse and aggregate missing variables and secrets | ansible.builtin.set_fact | False |
| Trigger role failure block if any items failed validation | ansible.builtin.fail | True |
| Print the validated environment variables | ansible.builtin.debug | False |
| [INFO] Construct tracked metadata map for variables | ansible.builtin.set_fact | False |
| [INFO] Extract cleartext secrets into tracking payload | ansible.builtin.set_fact | False |
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
