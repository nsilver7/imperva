#!/usr/bin/env python

import requests
from requests.auth import HTTPBasicAuth
from getpass import getpass, getuser
import datetime
import json
import sys


def authenticate(session, server):
	url = f"{server}/SecureSphere/api/v1/auth/session"
	res = session.post(url, auth=HTTPBasicAuth(getuser(), getpass()), verify=False)
	print(res.json())
	# TODO check res code and return bool for login status


def get_sites(session, server):
	res = session.get(f"{server}/SecureSphere/api/v1/conf/sites")
	print(res.json())


def get_server_groups(session, server):
	res = session.get(f"{server}/SecureSphere/api/v1/conf/serverGroups/Q2")
	return res.json()['server-groups']


def get_protected_ips(session, server, sg):
	res = session.get(f"{server}/SecureSphere/api/v1/conf/serverGroups/Q2/{sg}/protectedIPs")
	pips = res.json()['protected-ips']
	print(f"pips for server group {sg}: {pips} \n")
	ret = []
	for pip in pips:
		ret.append(pip['ip'])

	return ret


def put_protected_ips(session, server, sg, ip):
	pip_url = f"{server}/SecureSphere/api/v1/conf/serverGroups/Q2/{sg}/protectedIPs/{ip}?gatewayGroup=PROD-WAF"
	headers = {'Content-type': 'application/json'}
	data = {
		"comment": f"Added via API {datetime.datetime.now()}"
	}
	json_data = json.dumps(data)
	res = session.post(pip_url, headers=headers, data=json_data, verify=False)
	print(f"Response from POST: {res.text} \n")


def main():
	s = requests.Session()
	server = input("Please enter your server URL:port ~ ")
	authenticate(s, server)
	get_sites(s, server)
	server_groups = get_server_groups(s, server)

	put_protected_ips(s, server, "API Logon Tier", "0.0.0.1")

	with open('duplicatevips.csv','w') as file:
		file.write(f'vip\n')
		
		for servergroup in server_groups:
			print(servergroup)
			file.write(f'{servergroup}: \n')
			protected_ips = get_protected_ips(s,servergroup)
			#print(protected_ips)
			for ip in protected_ips:
				file.write(f'{ip}\n')


if __name__ == "__main__":
	main()
