# hausschrat

- based on source-code hosting platforms
  - GitLab
  - Gitea
- CLI
- Ansible-Integration
  - Templates for revoke cert orchestration
- Runs everywhere
  - Cloud
  - on-premise
- Included vault providers (_easy to expand (bring your own vault_)
  - Nextcloud
  - AWS

# design

## private key handling

_hausschrat_ nor generate a private key nor does it save the private key permanentely.  
For every certificate issue it will fetch the private key and delete is afterwards.  
Furthermore it will works only for private keys which are secured by a password.  

Therefore _hausschrat_ needs two things.  

1. The private key
2. The password for it

Both is fetched via vendors `vault` class.  
Built-in (for demonstration) it supports  
* Nextcloud (file and passwords)
* AWS (S3 and SSM)
* mixed (Private Key from S3, Password from Nextcloud)

For security reason, you should use a mixed `vault`. That garanties that the
private key is not saved at the same place/vendor with its belonging password.