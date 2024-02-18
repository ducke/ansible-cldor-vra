#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Cyrill Berg <Cyrill.Berg@bwi.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: integration
author: foo bar
short_description: Add and update vra integrations / plugins
description: Add and update vra integrations / plugins

options:
'''
EXAMPLES = r'''
- name: Update Integrations
  ansible-cldor-vra.integration:
    vra_hostname: my-little-vra.example.com
    api_token: 13244354656
    name:
    description:
    integrationType:
    providerPackage:

'''
RETURN = r'''
integrationProperties:
  description: The Integration Object
  type: obj
  returned: always
'''
import traceback, requests

from ansible.module_utils.basic import AnsibleModule, heuristic_log_sanitize, sanitize_keys
#from plugins.modules.login import get_vra_api_token

def post_vra_integration(module, vra_fqdn, api_token, providerPackage):
    try:
        url = f"https://{vra_fqdn}/provisioning/ipam/api/providers/packages/import"
        auth_token_string = "Bearer "+api_token
        api_headers = {"Authorization": auth_token_string}
        package_file = open(providerPackage, "rb")

        response = requests.post(url, files = {"form_field_name": package_file}, headers=api_headers, verify=False)
        response.raise_for_status()
        res_json = response.json()
        if response.ok:
            print("Upload completed successfully!")
            print(response.text)
        else:
            print("Something went wrong!")
        return res_json
    except requests.exceptions.RequestException as e:
        module.fail_json(msg="Package Upload failed: {}".format(str(e)))

def main():
    module_args = dict(
        vra_fqdn=dict(type="str"),
        api_timeout=dict(type="float", default=10),
        api_headers=dict(type="dict"),
        api_ssl_verify=dict(type="bool", default=True),
        api_wait_events=dict(type="float", default=0.2),
        api_username=dict(type="str"),
        api_password=dict(type="str", no_log=True),
        api_token=dict(type="str", no_log=True),
        name=dict(type="str"),
        description=dict(type="str"),
        providerPackage=dict(type="str")
    )
    #module_args.update(common_module_args)
    #module_args.pop("api_token")

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )
    params = module.params

    result = {
        "changed": False,
        "token": ""
    }

    vra_fqdn = params["vra_fqdn"]
    api_token = params["api_token"]
    providerPackage = params["providerPackage"]
    

    try:
        if params["api_username"]:
            get_result = get_vra_api_token(module, username, password, vra_fqdn)
            if get_result["token"]:
                result = post_vra_integration(module, vra_fqdn, api_token, providerPackage)
            else:
                module.fail_json(msg="Failed to obtain API token.")
            if result:
                module.exit_json(**result)
            else:
                module.fail_json(msg="Failed to upload file.")
        else:
            result = post_vra_integration(module, vra_fqdn, api_token, providerPackage)
            if result:
                module.exit_json(**result)
            else:
                module.fail_json(msg="Failed to upload file.")
    except Exception:
        error = traceback.format_exc()
        module.fail_json(msg=error, **result)


if __name__ == '__main__':
    main()


