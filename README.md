# Ansible playbook to setup a mail server

Ansible playbook for the mail server described in [Thomas Leister's tutorial](https://thomas-leister.de/mailserver-debian-stretch/).

## Requirements

- Ansible >= 2.14
- Collections from `requirements.yml` (`ansible-galaxy collection install -r requirements.yml`)
- Debian 11 (Bullseye) or 12 (Bookworm)
- SSH access to the server
- A public domain with DNS records pointing at the server

## Layout

```
ansible.cfg
inventory/hosts.yml          # inventory
group_vars/mail/             # host-group variables and vault
roles/                       # common, certbot, mariadb, dovecot, rspamd, postfix
site.yml                     # site playbook
```

## Configuration

### Inventory

Set the mail server hostname in [inventory/hosts.yml](inventory/hosts.yml).

### Variables

Public settings live in [group_vars/mail/vars.yml](group_vars/mail/vars.yml).

| Variable | Purpose |
| --- | --- |
| `mail_hostname` | Short hostname |
| `mail_domain` | Mail domain |
| `mail_user` | Primary mailbox local part |
| `mail_letsencrypt_enabled` | `true` for Let's Encrypt, `false` for a self-signed cert (tests) |
| `mail_apt_upgrade` | Set `true` to run `apt upgrade` (off by default) |

TLS certificate paths are derived in the certbot role from `mail_letsencrypt_enabled`. Override `mail_tls_cert_path` and `mail_tls_key_path` only when you bring your own files.

Secrets are read from the vault and mapped in `vars.yml`:

- `vmail_pass` → `mail_db_password`
- `mail_user_pass_hash` → `mail_user_password_hash`
- `rspamadm_pass` → `rspamd_controller_password`

### Credentials

Copy [group_vars/mail/vault.yml.example](group_vars/mail/vault.yml.example) to `group_vars/mail/vault.yml`, fill in the secrets, and encrypt it:

```
ansible-vault encrypt group_vars/mail/vault.yml
```

Create a mailbox password hash with `doveadm pw -s SHA512-CRYPT`.

Let's Encrypt issuance uses standalone HTTP-01 and needs port 80 free on first run.

## Run the playbook

```
ansible-galaxy collection install -r requirements.yml
ansible-playbook site.yml --ask-vault-pass
```

Limit a single role with tags, for example `--tags postfix`.

## Test

### Molecule

```
ANSIBLE_VAULT_PASSWORD_FILE=<YOUR_VAULT_PASS_FILE_PATH> molecule converge
ANSIBLE_VAULT_PASSWORD_FILE=<YOUR_VAULT_PASS_FILE_PATH> molecule verify
ANSIBLE_VAULT_PASSWORD_FILE=<YOUR_VAULT_PASS_FILE_PATH> molecule test
```

Molecule disables Let's Encrypt and uses a self-signed certificate.

### Bats

```
mail_user=USER mail_pass=PASS mail_host=HOST:587 bats test/smtp.bats
```
