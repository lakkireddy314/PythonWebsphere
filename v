---
- name: Download Certificate from Venafi using API Key
  hosts: localhost
  gather_facts: no
  vars:
    venafi_url: "https://venafi.example.com"
    venafi_api_key: "your-venafi-api-key"
    venafi_cert_name: "your-certificate-name"
    venafi_zone: "your-policy-zone"
    venafi_output_pfx: "/tmp/certificate.pfx"

  tasks:
    - name: Download certificate from Venafi
      venafi.platform.venafi_request_certificate:
        token: "{{ venafi_api_key }}"
        url: "{{ venafi_url }}"
        cert_name: "{{ venafi_cert_name }}"
        zone: "{{ venafi_zone }}"
        format: "PKCS12"
      register: venafi_cert

    - name: Save certificate to PFX file
      ansible.builtin.copy:
        content: "{{ venafi_cert.certificate_data }}"
        dest: "{{ venafi_output_pfx }}"
        mode: '0600'

    - name: Verify Certificate File
      ansible.builtin.stat:
        path: "{{ venafi_output_pfx }}"
      register: cert_file

    - name: Display Certificate Download Status
      ansible.builtin.debug:
        msg: "Certificate successfully downloaded to {{ venafi_output_pfx }}"
      when: cert_file.stat.exists





- name: Retrieve Certificate from Venafi
  hosts: localhost
  gather_facts: no
  tasks:
    - name: Retrieve certificate from Venafi
      venafi.ansible_collection.venafi_certificate_retrieve:
        venafi_api_url: "https://your-venafi-instance.com"
        username: "your-username"
        password: "your-password"
        certificate_name: "your-certificate-name"
        folder: "/your-folder-path"
        certificates:
          - "certificate"
          - "certificate_chain"
        validate_certs: false  # Whether to validate SSL certificates
