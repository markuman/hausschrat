# DRAFT

# hausschrat

The most easiest SSH CA I can think of.


# design

Nowadays it's wide spread to save your public ssh keys in SCM Tools like GitLab, Gitea, Github etc.  
So why not use this source for your SSH CA?  
Most companies self-hosted a SCM Tool already and possible also bind it to a directory. When the linux server are also bind to the same directory - awesome. That are perfect conditions, because you even don't need to orchestrate the users to all your servers.    
You only need to glue things together. Here comes _hausschrat_ to play.

A user needs to create an access token in their SCM Tool with `read_user` permissions only. With this access token, _hausschrat_ can verify the user, fetch the users belonging public key, sign them and response with the certificate.

## private key handling

_hausschrat_ nor generate a private key nor does it save the private key permanentely.  
For every certificate issue it will fetch the private key and delete is afterwards.  
Furthermore it will work only for private keys which are secured by a password.  

Therefore _hausschrat_ needs two things.  

1. The private key
2. The password for it

Both is fetched via vendors `vault` class.  
Built-in (for demonstration) it supports  
* Nextcloud (file and passwords)
* AWS (S3 and SSM)
* mixed (Private Key from S3, Password from Nextcloud)

For security reason, you should use a mixed `vault`. That garanties that the
private key and its belonging password are stored at different locations.
Seriously, storing them at the same vendor is a threat.

For example. Don't save the private key and its belonging password both at 1password.  
It's recommended to save one part always at a place which is fully under your conrol (_means, no SaaS_).


# SCM

| **host** | **category** |
| --- | --- |
| https://git.osuv.de/m/hausschrat | origin |
| https://gitlab.com/markuman/hausschrat | pull mirror |
| https://github.com/markuman/hausschrat | push mirror |