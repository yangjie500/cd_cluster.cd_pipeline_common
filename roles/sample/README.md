<!-- DOCSIBLE START -->

# 📃 Role overview

## sample



Description: Sample role to test molecule is working










### Defaults

**These are static variables with lower priority**

#### File: defaults/main.yml

| Var          | Type         | Value       |
|--------------|--------------|-------------|
| [sample_hello_file_path](defaults/main.yml#L2)   | str | `/tmp/hello.txt` |    
| [sample_hello_file_content](defaults/main.yml#L3)   | str | `Hello from Molecule test` |    





### Tasks


#### File: tasks/main.yml

| Name | Module | Has Conditions |
| ---- | ------ | -------------- |
| Create hello file | ansible.builtin.copy | False |







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
