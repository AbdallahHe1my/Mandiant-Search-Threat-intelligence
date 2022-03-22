import time
import requests
import pandas as pd
from requests.structures import CaseInsensitiveDict
from requests.auth import HTTPBasicAuth

APIv3_key='Your API Key' #Add your API key here
APIv3_secret='You Secert API Key' #Add your second API here
API_URL = 'https://api.intelligence.fireeye.com/token'
headers = {
    'grant_type': 'client_credentials'
    }
r = requests.post(API_URL, auth=HTTPBasicAuth(APIv3_key, APIv3_secret), data=headers)
data = r.json()
auth_token = data.get('access_token')
print('Token request API response: %s' % r.status_code)
print('Authorization Token: %s' % auth_token)

url = "https://api.intelligence.fireeye.com/v4/indicator"
fname = "ICO's"+ str(time.time())+".csv"
with open(fname, "a", encoding="utf-8") as f:
    f.write(f"IP,Mscore,type,Last Seen" + '\n')
headers = CaseInsensitiveDict()
headers["accept"] = "application/json"
headers["Authorization"] = "Bearer %s" %auth_token
headers["Content-Type"] = "application/json"
columns = ["IP"] #The first column in your CSV folder as mentioned "" IP ""
ips=""
df = pd.read_csv("Your CSV Folder.csv", usecols=columns) #Add the CSV folder that you got here that contains the DATA you want to search for
i=0
pcount=0
def parseIndicators(indicatorArray):
    for indicator in indicatorArray:
        with open(fname, "a", encoding="utf-8") as f:
            f.write(f"{indicator['value']},{indicator['mscore']},{indicator['type']},{indicator['last_seen']}" + '\n')
for i in range (0,df[df.columns[0]].count()):
    ip = str(str(df.values[i]))
    val = ip.split("['", 1)[1].split("']")[0]
    ips += '''    "'''+val+'''",'''+"\n         "
    numlastip= df[df.columns[0]].count()-1
    lastshit = str(str(df.values[numlastip]))
    lastshitip = lastshit.split("['", 1)[1].split("']")[0]
    lastip =  '''    "'''+lastshitip+'''"'''+"\n"
    x =  '''
    {
    "limit": 15,
    "offset": 0,
    "requests": [
        {
        "values": [
        '''
    y = """
        ]
        }
    ]
    }
    """
    data = (x +ips+lastip + y)
    if (pcount == 15):
        resp = requests.post(url, headers=headers, data=data)
        pcount=0
        ips=""
        print(data)
        if resp.status_code != 204:
            print(resp.json())
            parseIndicators(resp.json()['indicators'])
        elif resp.status_code == 204:
            with open(fname, "a", encoding="utf-8") as f:
                f.write(f""+val+", No Data found Check other resources" + '\n')
    pcount += 1
print("Done !, Thanks for using the script :) by Abdallah ")