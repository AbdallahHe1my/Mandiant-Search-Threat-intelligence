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
headers = CaseInsensitiveDict()
headers["accept"] = "application/json"
headers["Authorization"] = "Bearer %s" %auth_token
headers["Content-Type"] = "application/json"
columns = ["IP"] #The first column in your CSV folder as mentioned "" IP ""
df = pd.read_csv("Your CSV Folder.csv", usecols=columns) #Add the CSV folder that you got here that contains the DATA you want to search for
def parseIndicators(indicatorArray):
    for indicator in indicatorArray:
        with open(fname, "a", encoding="utf-8") as f:
            f.write(f"{indicator['value']},{indicator['mscore']},{indicator['type']},{indicator['last_seen']}" + '\nr')
for xi in range(1,df[df.columns[0]].count()):
    ip = str(str(df.values[xi]))
    val = ip.split("['", 1)[1].split("']")[0]
    x =  '''
    {
    "limit": 10,
    "offset": 0,
    "requests": [
        {
        "values": [
        "'''
    y = """"
        ]
        }
    ]
    }
    """
    print (val)
    data = (x + val + y)
    resp = requests.post(url, headers=headers, data=data)
    parseIndicators(resp.json()['indicators'])
print("Done !, Thanks for using the script :) by Abdallah ")