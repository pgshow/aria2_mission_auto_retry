import json
import time
import os
from urllib.request import urlopen


# request action
def req(method, params):
    jsonreq = json.dumps({'jsonrpc': '2.0', 'id': 'qwer',
                          'method': method,
                          'params': params,
                        }).encode()
    try:
        c = urlopen('http://localhost:6800/jsonrpc', jsonreq)
        result = json.loads(c.read())['result']
        if result:
            return result
    except Exception as e:
        print(e)


while 1:
    time.sleep(120)
    
    # check the stopped tasks, num 10 means only check top 10 missions
    stopped = req('aria2.tellStopped', [0, 10])
    
    if not stopped:
        continue
        
    for mission in stopped:
        time.sleep(1)
        
        try:
        
            # Only resume the one which stopped with errors, then add a new and remove the old one
            if mission['errorCode'] == '0':
                continue
            
            gid = mission['gid']
            folder = mission['dir']
            path = mission['files'][0]['path']
            url = mission['files'][0]['uris'][0]['uri']
            
            add_result = req('aria2.addUri', [[url],{'refer': url,'dir':folder}])
            
            if add_result:
                
                print("Download: " + url + ", Path: " + path + " add Success")
                time.sleep(1)
                
                if req('aria2.removeDownloadResult', [gid]):
                    print("Download: " + url + ", Path: " + path + " remove Success")
                else:
                    print("Download: " + url + ", Path: " + path + " remove Failed")
                    
            else:
            
                print("Download: " + url + ", Path " + path + " add Failed")

        except Exception as e:
            print(e)
    
