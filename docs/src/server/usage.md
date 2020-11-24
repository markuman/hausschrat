## usage

For security reason, there is nor admin webinterface nor admin cli.  
To configure and administrate _hausschrat_ all you need is

- a sql client
  * dbeaver
  * etc pp
- sql skills (_in case that your prefered sql client does not have a gui_)

# Settings

The default values works well for most use cases.

* You may like to change the `authority_name` or the `expire` value.  
* You like to change the `scm_url`.
* You must add/provide
    * `vendor`
    * `vendor_key_location`
    * `vendor_password_name`

That's all.

## Parameter Options

**`expire`**  
Default value: `+1w` (_1 week_).

Max time until a issued certificate expired.  
The user cannot request longer durations.
Supported units are: `{"m":"minutes", "h":"hours", "d":"days", "w":"weeks"}`


**`mode`**  
Default value: `user`  

Supported modes:

* `user`: Certificates are only issued with their `api_token` belonging user.
* `host`: Certificates are only issued to a single host. The usename doesn't matter.
* `open`: Everthing what is requested will be issues.


**`authority_name`**  
Default value: `hausschrat`

The identifier of the certificate authority.


**`scm_url`**  
Default value: `https://gitlab.com`  

When `scm_url` is not set, _hausschrat_ will request every source control managment tool which is requested. This is not a recommended mode and might be only useful for personal needs.    
When `scm_url` is set (_e.g. to `https://gitlab.com`), _hausschrat_ will only request it. All other requested 
source conrole managment tools are forbidden (_return status code 403_).


**`vendor`**  
Default value: `mixed`

Defines which vendors `vault` class is used.  
It must be exist in `lib/vendors`.


**`vendor_key_location`**  
Default value: _not set_

The location of the private key for the used vendor.


**`vendor_password_name`**
Default value: _not set_

The location the the password for the private key for the used vendor.


**`public_key`**  
Default value: _not set_

This is the placeholder to the CA public key. You don't nedd and should not care about it.  
Once it is requested, _hausschrat_ will fetch the private key again, re-generate the public key and
save it there for performance reasons.

# Revoke

In case you need to revoke a certificate, you must find the related row in `certs` table.  
Once it is found, just set `revoked` to `1`.  
Now you can request `https://{HAUSSCHRAT_URL}/revoke` with your orchestration and announce it to the sshd.

# Servers Public Key

You can also use the API endpoint `/public_key` in your orchestration to fetch the CA public key and announce it to the sshd.  
Once it is fetched and regenerated, it will be stored in the `hausschrat` table - for performance issue.

# Orchestrate revoke_file

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