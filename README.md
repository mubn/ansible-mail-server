# Ansible playbook to setup a mail server

This is an Ansible-Playbook for the great mail server setup described in this tutorial: https://thomas-leister.de/mailserver-debian-stretch/ written by Thomas Leister.

## Requirements

- Ansible >= 2.7
- Debian Stretch server with ssh key login

## Configuration

### Variables

All variables are stored in `group_vars/all/vars.yml`. Set the values according to your server.

### Credentials

Credentials are stored in [group_vars/all/vault.yml](group_vars/all/vault.yml). The Password is "vault".
Please change the password with `ansible-vault rekey group_vars/all/vault.yml`.

- Database user: "vmail", pass: "vmail" (Please change it)
- Mail user: "mail", pass: "mail" (Please change it)
- Rspam admin password: "rspamadmpw"

### Keys

- The DKIM-Key ist stored as vault file [roles/rspamd/files/2019.key](roles/rspamd/files/2019.key). The Password is "vault". Please generate your own Key on the Server with:

```
rspamadm dkim_keygen -b 2048 -s 2019 -k 2019.key > 2019.txt
```

and save it in this playbook.

## Run

```
ansible-playbook -i ./hosts site.yml --ask-vault-pass
```

## Todo's

Write tests
