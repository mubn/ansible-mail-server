# Ansible playbook to setup a mail server

This is an Ansible-Playbook for the great mail server setup described in this tutorial: https://thomas-leister.de/mailserver-debian-stretch/ written by Thomas Leister.

## Requirements

- Ansible >= 2.7
- Server with Debian Bullseye operating system
- SSH key to login to the server
- Public domain resolving to the server

## Configuration

### Inventory

Set the hostname in the inventory file [hosts](hosts)

### Variables

All variables are stored in the [vars](group_vars/all/vars.yml) file. Set the values according to your server.

### Credentials

Credentials are stored in the [vault.yml](group_vars/all/vault.yml). The Password is "vault".
Please change the password with `ansible-vault rekey group_vars/all/vault.yml`.

- Database user: "vmail", pass: "vmail" (Please change it)
- Mail user: "mail", pass: "mail" (Please change it)
- Rspam admin password: "rspamadmpw"

## Run the playbook

```
ansible-playbook -i ./hosts site.yml --ask-vault-pass
```

## Test

### Molecule

The results of the ansible playbook can be tested with [Molecule](https://molecule.readthedocs.io/en/latest/)

#### Test with molecule

Build the mail server

```
ANSIBLE_VAULT_PASSWORD_FILE=<YOUR_VAULT_PASS_FILE_PATH> molecule converge
```

Verify the installation

```
ANSIBLE_VAULT_PASSWORD_FILE=<YOUR_VAULT_PASS_FILE_PATH> molecule verify
```

Build, test and destroy in one command

```
ANSIBLE_VAULT_PASSWORD_FILE=<YOUR_VAULT_PASS_FILE_PATH> molecule test
```

### Bats

Send a email on the ready system with [bats](https://github.com/sstephenson/bats)

```
mail_user=USER mail_pass=PASS mail_host=HOST:587 bats smtp.bats
```
