# Copyright: (c) 2024, Cyrill Berg <Cyrill.Berg@bwi.de>

from __future__ import absolute_import, division, print_function

__metaclass__ = type


def object_changed(superset, subset, ignore=None):
    changed_keys = []
    for key, value in subset.items():
        value2 = superset.get(key)
        if ignore and key in ignore:
            ignore_value = ignore[key]
            if type(ignore_value) == list and value2 in ignore_value:
                continue
            elif value2 == ignore_value:
                continue
            elif ignore_value is None:
                continue
        if type(value) == list:
            for i in range(len(value)):
                if not value2:
                    changed_keys.append((key, superset.get(key), subset[key]))
                elif type(value[i]) == list or type(value[i]) == dict:
                    if i >= len(value2) or object_changed(value2[i], value[i]):
                        changed_keys.append((key, superset.get(key), subset[key]))
                else:
                    if value[i] != value2[i]:
                        changed_keys.append((key, superset.get(key), subset[key]))
        elif type(value) == dict:
            if object_changed(value2, value):
                changed_keys.append((key, superset.get(key), subset[key]))
        else:
            if value != value2:
                changed_keys.append((key, superset.get(key), subset[key]))
    return changed_keys


def clear_params(params: dict):
    ignored_params = [
        "vra_fqdn",
        "api_timeout",
        "api_headers",
        "api_ssl_verify",
        "api_wait_events",
        "api_username",
        "api_password",
        "api_token",
        "state"
    ]
    return {k: v for k, v in params.items() if k not in ignored_params}


def clear_unset_params(params: dict):
    return {k: v for k, v in params.items() if v is not None}


common_module_args = dict(
    vra_fqdn=dict(type="str"),
    api_timeout=dict(type="float", default=10),
    api_headers=dict(type="dict"),
    api_ssl_verify=dict(type="bool", default=True),
    api_wait_events=dict(type="float", default=0.2),
    api_username=dict(type="str"),
    api_password=dict(type="str", no_log=True),
    api_token=dict(type="str", no_log=True)
)
