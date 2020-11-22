## usage

For security reason, there is nor admin webinterface nor admin cli.  
To configure and administrate _hausschrat_ all you need is

- a mariadb client
  * mysql or mariadb cli
  * mycli
  * dbeaver
  * ... yes, also properitary clients will work but are not recommended!
- sql skills (_in case that your prefered sql client does not have a gui_)

# Settings

The default values works well for most use cases.

* You may like to change the `authority_name` or the `expire` value.  
* You like to change the `scm_url`.
* You must add/provide
    * `auth_vendor`
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


**`auth_vendor`**  
Default value: `nextcloud`

Defines which vendors `vault` class is used.  
It must be exist in `lib/vendors`.


**`vendor_key_location`**  
Default value: _not set_

The location of the private key for the used vendor.


**`vendor_password_name`**
Default value: _not set_

The location the the password for the private key for the used vendor.

# Revoke

In case you need to revoke a certificate, you must find the related row in `certs` table.  
Once it is found, just set `revoked` to `1`.  
Now you can request `https://{HAUSSCHRAT_URL}/revoke` with your orchestration and announce it to the sshd.