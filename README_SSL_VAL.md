# SSL Validation Automation for WebSphere

This repository provides an Ansible-2.9–compatible solution to:

1. **Discover** all Application Servers and the Deployment Manager in a WebSphere cell, retrieving their `WC_defaulthost_secure` host/port.
2. **Validate** each server’s SSL certificate against a pre-set expected serial (dynamic Ansible fact).
3. **Aggregate** results into “OK” and “Error/Down” lists.
4. **Render** an Outlook-friendly HTML report, injected with your `limit` and `cellname` context.
5. **Email** the report inline—no temporary files needed—via a sub-task in an Ansible role.

## Prerequisites

- **Ansible 2.9** installed on the control node.
- Python (with Jinja2) on the controller.
- Access to target WebSphere nodes configured under the `websphere_servers` group.
- OpenSSL on each target for `openssl s_client`.
- An SMTP relay reachable from the control node.
- Jython runtime available to WebSphere’s `wsadmin.sh`.

## File Structure

```
.
├── validate_ssl_certificates.yml    # Main playbook
├── wsadmin_jython_script.py         # Jython script to list secure ports
└── roles/
    └── ssl_validation/
        ├── tasks/
        │   ├── ssl_checks.yml       # Per-server SSL check logic
        │   └── mail_report.yml      # Email-report sub-task
        └── templates/
            └── ssl_report.html.j2   # HTML report template
```

## Installation

1. Clone this repository onto your control node:
   ```bash
   git clone https://your.repo/url.git
   cd your-repo
   ```
2. Install any required Ansible collections:
   ```bash
   ansible-galaxy collection install community.general
   ```

## Configuration

1. Define your WebSphere hosts under `[websphere_servers]` in your inventory.
2. Set the following variables in `group_vars/websphere_servers.yml` or inventory:
   - `cellname`: Your WebSphere cell name.
   - `limit`: A context string to use in the report subject.
   - Dynamic facts named `<short_hostname>_cert_serial` for each host.
3. Update SMTP settings in `roles/ssl_validation/tasks/mail_report.yml`.

## Usage

Run the playbook:
```bash
ansible-playbook -i inventory validate_ssl_certificates.yml
```
- The play will gather secure-port data, validate SSL certificates, and send an HTML report email.

## Customization

- **Styling**: Edit `templates/ssl_report.html.j2` for branding or layout tweaks.
- **Checks**: Extend `ssl_checks.yml` for OCSP or fingerprint validation.
- **Notifications**: Swap the mail task for Slack, PagerDuty, or other notifiers.

## How It Works

1. **Port Discovery**: Runs `wsadmin_jython_script.py` to list `WC_defaulthost_secure` endpoints.
2. **Parsing & Filtering**: Cleans and splits CSV output into structured data.
3. **SSL Validation**: Uses `openssl s_client` to fetch serials; handles down servers and mismatches.
4. **Report Generation**: Aggregates results into `ok_list` and `down_list`, and renders an HTML template.
5. **Email**: Sends the rendered HTML inline via Ansible’s `mail` module.

## License & Support

Licensed under MIT. For issues or contributions, please use the project’s issue tracker.
