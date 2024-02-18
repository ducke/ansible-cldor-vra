#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Cyrill Berg <Cyrill.Berg@bwi.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r'''
---
module: login
author: Cyrill Berg <Cyrill.Berg@bwi.de>
short_description: Login to vRA 8 API.
description: Login to vRA 8 API and returns a token that can be used for future requests.

options:
'''

EXAMPLES = r'''
- name: login
  ansible-cldor-vra.login:
    vra_hostname: my-little-vra.example.com
    api_username: admin
    api_password: secret123

'''

RETURN = r'''
token:
  description: The login token.
  type: str
  returned: always
'''

import traceback, requests

from ansible.module_utils.basic import AnsibleModule, heuristic_log_sanitize, sanitize_keys
#from ansible_collections.ansible-cldor-vra.plugins.module_utils.common import common_module_args

def get_vra_api_token(module, username, password, vra_fqdn):
    try:
        # Authenticate to obtain api token
        url = f"https://{vra_fqdn}/csp/gateway/am/api/login"
        payload = {"username": username, "password": password}
        response = requests.post(url, json=payload, verify=False)
        response.raise_for_status()
        res_json = response.json()
        api_token = res_json.get("cspAuthToken")

        return api_token
    except requests.exceptions.RequestException as e:
        module.fail_json(msg="Authentication failed: {}".format(str(e)))



def main():
    module_args = dict(
        vra_fqdn=dict(type="str"),
        api_timeout=dict(type="float", default=10),
        api_headers=dict(type="dict"),
        api_ssl_verify=dict(type="bool", default=True),
        api_wait_events=dict(type="float", default=0.2),
        api_username=dict(type="str"),
        api_password=dict(type="str", no_log=True),
        api_token=dict(type="str", no_log=True)
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

    username = params["api_username"]
    password = params["api_password"]
    vra_fqdn = params["vra_fqdn"]

    try:
        result["token"] = get_vra_api_token(module, username, password, vra_fqdn)

        if result["token"]:
            module.exit_json(**result)
        else:
            module.fail_json(msg="Failed to obtain API token.")
    except Exception:
        error = traceback.format_exc()
        module.fail_json(msg=error, **result)


if __name__ == '__main__':
    main()
