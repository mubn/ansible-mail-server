# Ansible playbook to setup a mail server

This is an Ansible-Playbook for the great mail server setup described in this tutorial: https://thomas-leister.de/mailserver-debian-stretch/ written by Thomas Leister.

## Requirements

- Ansible >= 2.7
- Debian Stretch server
- SSH key to login to the server
- Public domain resolving to the server

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

## Run

```
ansible-playbook -i ./hosts site.yml --ask-vault-pass
```

## Test

Bats: https://github.com/sstephenson/bats

```
mail_user=USER mail_pass=PASS mail_host=HOST:587 bats smtp.bats
```
