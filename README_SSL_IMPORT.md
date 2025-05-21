# Venafi Self-Signed Certificate Automation for IBM WebSphere

This project automates the full lifecycle of importing self-signed PFX certificates into WebSphere profiles (Deployment Manager, Node Agents, Web Servers), updating SSL configurations, synchronizing nodes, copying trust stores, and generating an Outlook-friendly report emailed to administrators.

---
## Repository Contents

- **`scripts/listProfiles.py`**  
  Jython `wsadmin` script to discover all WebSphere profiles with their hostnames and cell names.

- **`scripts/importCert.py`**  
  Jython `wsadmin` script to import a `.pfx` certificate into a specific WebSphere profile’s keystore, clear or set SSL aliases, handle the default alias cleanup, update plugin properties for web servers, and regenerate & propagate plug-in configuration via the `PluginCfgGenerator` MBean.

- **`playbooks/ssl_import_report.yml`**  
  Ansible 2.9 playbook that:
  1. Discovers all profiles via `listProfiles.py`.
  2. Conditionally copies `trust.p12` from the profile’s `config/<cell>` directory to `properties/` on the matching host.
  3. Invokes `importCert.py` for each profile-host-cell tuple.
  4. Collects and parses only the `Imported cert ...` output lines into structured facts.
  5. Builds an email subject `Venafi Self Signed - <cellName>` safely using Jinja templating.
  6. Renders an Outlook-optimized HTML report (`templates/ssl_report.html.j2`).
  7. Emails the report via the Ansible `mail` module.

- **`playbooks/templates/ssl_report.html.j2`**  
  Outlook-friendly HTML template that presents a centered table of **Profile**, **Keystore**, and **Alias**, with a header showing the cell environment and timestamp.

---
## Prerequisites

- **WebSphere**: Admin access and `wsadmin.sh` on each target node.
- **Jython**: Available to `wsadmin` for running the Python scripts.
- **Ansible 2.9**: Installed on the control machine.
- **SMTP Server**: Accessible for the Ansible `mail` module to send HTML emails.

---
## Directory Layout

```
project-root/
├── scripts/
│   ├── listProfiles.py
│   └── importCert.py
├── playbooks/
│   ├── ssl_import_report.yml
│   └── templates/
│       └── ssl_report.html.j2
└── README.md
```

---
## Usage

1. **Push scripts** to each WebSphere node under `/opt/scripts/` (or amend paths in the playbook).
2. **Adjust variables** in `ssl_import_report.yml` or pass via `--extra-vars`:
   - `PROFILE_NAME`, `HOST_NAME`, `WAS_USER`, `SSL_PASS`, and optionally `WEBSHERE_INSTALL_ROOT`, `SMTP_HOST`, `REPORT_RECIPIENTS`.
3. **Run playbook** against the `websphere_nodes` inventory group:

   ```bash
   ansible-playbook -i inventory playbooks/ssl_import_report.yml \
     --extra-vars "PROFILE_NAME=Dmgr01 HOST_NAME=dmgr01.example.com WAS_USER=wasusr SSL_PASS=secret"
   ```

4. **Review report** at `/tmp/ssl_report_<inventory_hostname>.html` and check your email inbox.

---
## Workflow Details

- **Discovery**: `listProfiles.py` prints lines like `dmgr01: dmgr01.example.com: testcell`.
- **Trust Store Copy**: For each profile mapping where `inventory_hostname == host`, the playbook copies `config/<cell>/trust.p12` to `properties/trust.p12`.
- **Certificate Import**: `importCert.py`:
  - Checks and imports PFX if alias is absent, else exits.
  - Updates SSL config (`modifySSLConfig`), clears default alias, and syncs nodes.
  - For web servers: updates `PluginProperties/CERTLABEL`, then regenerates & propagates plugin XML.
- **Reporting**:
  - Playbook collects only the `Imported cert ...` lines, parses them into a list of dicts using `set_fact` loops.
  - Builds a `mail_subject` via a literal block scalar to avoid YAML quoting issues.
  - Renders the Jinja2 template into HTML and emails it.

---
## Troubleshooting

- **YAML parse errors** around `{{ … }}`: ensure Jinja expressions are not nested inside conflicting quote types.
- **`ERROR` in import output**: playbook’s `failed_when` halts on any line containing `ERROR` from `importCert.py`.
- **Email not sent**: verify SMTP host, port, and credentials; check control node network.

---
## Extending & Customization

- **Additional checks**: Add tasks to verify keystore entries or plugin XML contents.
- **Alternative notifications**: Replace the `mail` task with Slack, PagerDuty, or other modules.
- **Multi-cell support**: Parameterize and loop over multiple cells by extending `profile_data` discovery.

---
*This README covers the entire automated flow: discovery, trust copy, import, config, reporting, and notification.*