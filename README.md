# hausschrat
_the long awaited ssh ca_

- based on source-code hosting services
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


# server

## setup

The setup is easy, because all what _hausschrat_ needs is a valid mariadb database connection  
with a database (_utf8mb4_) names `hausschrat`.  
Once it's started, it creates two tables.

1. `hausschrat`
2. `certs`

The `hausschrat table is where the configuration lives.  
The `certs` table is where all cert public keys will be stored.

## usage

For security reason, there is nor admin webinterface nor admin cli.  
To configure and administrate _hausschrat_ all you need is

- a mariadb client
  * mysql or mariadb cli
  * mycli
  * dbeaver
  * ... yes, also properitary clients will work
- sql skills (_in case that your prefered sql client does not have a gui_)

# cli

## setup

## usage

# Ansible

## setup

## usage

## revoke orchestration

