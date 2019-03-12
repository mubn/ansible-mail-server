# Ansible playbook to setup a mail server

This is an Ansible-Playbook for the great mail server setup tutorial https://thomas-leister.de/mailserver-debian-stretch/

## Configuration

All variables are stored in `group_vars/all/vars.yml`. Credentiald are stored in `group_vars/all/vault.yml` (Password: "vault").

- Database user: "vmail", pass: "vmail" (Please change it)
- Mail user: "mail", pass: "mail" (Please change it)
- Rspam admin password: "rspamadmpw"

## Run

```
ansible-playbook -i ./hosts site.yml --ask-vault-pass
```
