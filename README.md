# Ansible Server Configuration

Project 03 in Ismet Xani's DevOps portfolio. A small Ansible playbook installs
Nginx on a Debian-family Linux host, starts and enables the service, and checks
that its local HTTP endpoint returns 200.

## Configuration

- Local-only inventory with the standard /usr/bin/python3 interpreter.
- Explicit ansible.builtin modules and Debian-family prerequisite check.
- Package cache refreshed only when older than one hour.
- Installed Nginx kept at the repository-provided version, without forcing upgrades.
- Existing web content and site configuration are not overwritten.
- HTTP verification is skipped in check mode because check mode does not start Nginx.

This is a local configuration demonstration. It does not configure TLS, a
firewall, authentication, a hardened public site, or a remote production fleet.
The default Nginx package may listen on all interfaces; use an isolated lab and
review exposure before running it elsewhere.

## PowerShell and Ubuntu WSL

Ansible runs inside Linux. The local inventory targets the Linux environment
where Ansible is invoked, not Windows or AWS. Ubuntu needs Python, Ansible,
working package repositories, and a functioning service manager.

```powershell
wsl -d Ubuntu
```

Then, in Ubuntu:

```bash
cd /mnt/c/Users/ismet/Documents/DevOps-Portfolio/03-ansible-server-configuration
ansible-playbook -i inventory.ini nginx.yml --syntax-check
ansible-playbook -i inventory.ini nginx.yml --check --ask-become-pass
ansible-playbook -i inventory.ini nginx.yml --ask-become-pass
curl -I http://127.0.0.1/
```

Check mode predicts changes; it does not prove installation or HTTP reachability.
Enter your own sudo password at the prompt. No password belongs in Git or the
inventory. Running the real playbook installs software and enables a local service.

## Automated verification

The Validate Ansible workflow installs ansible-core 2.20.1 with Python 3.12 on a
disposable Ubuntu 24.04 GitHub runner, checks syntax, and executes the playbook
twice. The script fails if either run fails, HTTP verification fails, or the
second run reports any changed task. Package-cache expiration can legitimately
cause later runs to refresh the cache; the test checks two immediate runs.

```bash
python3 scripts/verify.py
```

The script makes real local changes and requires an isolated Linux test host
with passwordless sudo. It is intended for the disposable CI runner. A CI pass
proves behavior on that runner, not production deployment or TLS security.

## Verification status

On October 19, 2026, local Ubuntu WSL syntax validation passed and the existing
Nginx endpoint returned HTTP 200. Running the revised configuration with elevated
local privileges was blocked by automatic approval review; local installation
and idempotency were therefore not claimed. The workflow performs those checks
on a disposable runner instead; consult its result for the current commit.

[GitHub Actions](https://github.com/ismet1292-wq/03-ansible-server-configuration/actions)

Python compatibility reference:
[Ansible support matrix](https://docs.ansible.com/projects/ansible/latest/reference_appendices/release_and_maintenance.html).
