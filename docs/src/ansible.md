# Ansible

Ansible can be used as client, for issuing a certificate and also to orchestrate the `revoke_keys` file or the CAs public key.

## Orchestrate CAs public key


```yml
---
- hosts: all
  gather_facts: no

  vars:
    HAUSSCHRAT_URL: http://localhost:8080

  tasks:
    - name: fetch CA public key
      uri:
        url: "{{ HAUSSCHRAT_URL }}/public_key"
        dest: /etc/ssh/CAKey
      become: yes
```

## Orchestrate revoke_file

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