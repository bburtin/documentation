#!/usr/bin/env python3

import sys
import requests
import json
from os import getenv

def pull_rbac():
  api_endpoint = 'https://app.datadoghq.com/api/v2/permissions'
  headers = {'DD-API-KEY': sys.argv[1], 'DD-APPLICATION-KEY': sys.argv[2]}
  formatted_permissions_dict = {}
  permission = []

  r = requests.get(api_endpoint, headers=headers)

  if r.status_code == requests.codes.ok:
    json_result = r.json()
    data = json_result['data']

    for permission in data:
      group_name = permission['attributes']['group_name']
      permission_name = permission['attributes']['name']

      # Remove legacy logs permissions from dictionary before converting to JSON.  These legacy permissions are hard-coded in rbac-permissions-table partial until they can be deprecated.
      if permission_name == 'logs_live_tail' or permission_name == 'logs_read_index_data':
        del permission

      if group_name not in formatted_permissions_dict.keys():
        formatted_permissions_dict[group_name] = [permission]
      else:
        formatted_permissions_dict[group_name].append(permission)

    formatted_permissions_json = json.dumps(formatted_permissions_dict)

    with open('data/permissions.json', 'w') as outfile:
      outfile.write(formatted_permissions_json)
  else:
    print('RBAC api request failed.')
    
    if getenv("LOCAL") != 'True':
      sys.exit(1)

pull_rbac()

