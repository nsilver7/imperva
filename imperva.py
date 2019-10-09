#!/usr/bin/env python

import requests
from requests.auth import HTTPBasicAuth
from getpass import getpass
import json
import sys


def authenticate(session, server):
	url = f"{server}/SecureSphere/api/v1/auth/session"
	res = session.post(url, auth=HTTPBasicAuth('q2security_api', getpass()), verify=False)
	print(res.json())
	# TODO check res code and return bool for login status


def delete_session(session_token, server):
	url = f"{server}/SecureSphere/api/v1/auth/session"
	res = requests.delete(url, headers=session_token, verify=False)


def get_lookup_data_set(session, server):
	res = session.get(f"{server}/SecureSphere/api/v1/conf/dataSets/ElevatedLoginURLs/data")
	print(res.json())


def update_lookup_data_set(action, url, session, server):
	"""
		This function updates the lookup data set 'ElevatedLoginURLs' with the specified
		action/URL.

		Parameters
		==========
		action: str
			This is either "add" or "delete".
		url: str
			The URL that is to be added or deleted.
		session: requests.Session()
			Authenticated session context.
	"""
	lookup_url = f"{server}/SecureSphere/api/v1/conf/dataSets/ElevatedLoginURLs/data"
	proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
	headers = {'Content-type': 'application/json'}
	data = {
		"action": action,
		"records": [{"URL": url}]
	}
	json_data = json.dumps(data)
	res = session.put(lookup_url, headers=headers, data=json_data, verify=False, proxies=proxies)
	j = res.text
	print(f"update API req responded with: {res.status_code}")
	# TODO check res code and return bool for update status
	# return res.json()


def main():
	server = input("Please enter your server URL:port ~ ")
	s = requests.Session()
	authenticate(s, server)
	# get_lookup_data_set(s, server)
	update_lookup_data_set("add", sys.argv[1], s, server)
	# to delete call update_lookup_data_set("delete", sys.argv[1], s)


if __name__ == "__main__":
	main()
