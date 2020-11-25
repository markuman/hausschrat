# Ansible

Ansible can be used as client, for issuing a certificate and also to orchestrate the `revoke_keys` file.


## Orchestrate revoke_file

Can be done with any orchestration tool...  
For example - ansible

```yml
---
- hosts: all
  gather_facts: no

  vars:
    HAUSSCHRAT_URL: http://localhost:8080

  tasks:
    - name: fetch revoke file
      uri:
        url: "{{ HAUSSCHRAT_URL }}/revoke"
        dest: /etc/ssh/revoked_keys
      become: yes
```

`ansible-playbook -i inventories/all_your_hosts.ini revoke_orchestration.yml`