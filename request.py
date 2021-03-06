'''
Replace the Prism Element IP address (ip) and cluster login credentials (auth) in the function below. 

This is an example:

def request_details():
  ip = '1.2.3.4'
  auth = HTTPBasicAuth('admin', 'Nutanix/1234')
  return ip,auth

'''

from requests.auth import HTTPBasicAuth

def request_details():
  ip = 'X.X.X.X'
  auth = HTTPBasicAuth('username', 'password')
  return ip,auth
