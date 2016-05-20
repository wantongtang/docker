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

def listDockerId(ip):
    print "IP:%s"%ip
    data=resp=requests.get('http://%s:2375/containers/json'%ip)
    jsond=json.loads(data.text)
    for i in xrange(1,len(jsond)):
        print jsond[i-1]['Id']

if __name__ == "__main__":
    if not (len(sys.argv)==3):
        print "usage: python shell.py ip cid"
	print "example:"
	print "python shell.py  115.159.45.79 105db2dd6cb68d6feb37038e5eabe52ae32b94e5873613741a36eb5998433509"
        exit()

    ip=sys.argv[1]
    docid=sys.argv[2]

    while True:
	textline=raw_input('>>')
	if textline:
		command = textline.replace("^H","^?")
        	cid=requestCid(ip,docid,command)
		if not cid:
			print 'exec cmd fail'
		else:
			print CommandExec(ip,cid)
	else:
		continue
