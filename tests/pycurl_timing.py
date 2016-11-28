import pycurl
import sys 
import json
import pprint

def curl_stat(WEB_SITES):
    c = pycurl.Curl()
    c.setopt(pycurl.URL, WEB_SITES)              #set url
    c.setopt(pycurl.FOLLOWLOCATION, 1)  
    content = c.perform()                        #execute 
    dns_time = c.getinfo(pycurl.NAMELOOKUP_TIME) #DNS time
    conn_time = c.getinfo(pycurl.CONNECT_TIME)   #TCP/IP 3-way handshaking time
    starttransfer_time = c.getinfo(pycurl.STARTTRANSFER_TIME)  #time-to-first-byte time
    total_time = c.getinfo(pycurl.TOTAL_TIME)  #last requst time
    c.close()

    data = json.dumps({'dns_time':dns_time,         
                   'conn_time':conn_time,        
                   'starttransfer_time':starttransfer_time,    
                   'total_time':total_time})
    return data

if __name__=="__main__":
    data = curl_stat(sys.argv[1])
    pprint.pprint(data)
