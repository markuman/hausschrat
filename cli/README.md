# hausschrat cli

## setup

Use pip to install.  
`pip3 install hausschrat --user`  

No magic here. That's all.

## usage

The configuration file of _hausschrat_ cli is located in `~/.config/hausschrat.yml`.  
At least a profile named `default` must be configured.

```yml
default:
  server: http://localhost:8080
  scm_url: https://git.osuv.de
  api_token: 123abc
  user: ma
  key: markus@dell
  expire: +5h
  cert_file: ~/.ssh/test-cert.pub

gitlab:
  scm_url: https://gitlab.com
  api_token: ...
  user: ec2-user
  key: rsa@aws
  expire: +1h

my_company:
  server: https://hausschrat.mycompany.tld
  scm_url: https://gitlab.mycompany.tld
  api_token: ...
  user: some_user
```

All parameters which are not set in addition profiles will be taken from the `default` profile.  
In the upper `my_company` profile example, the values of `expire` and `cert_file` are taken from the `default` profile.