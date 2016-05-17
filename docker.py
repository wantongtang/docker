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
    payload='{"AttachStdin": false, "AttachStdout":true,"AttachStderr":true,"Tty":false,"Cmd":[%s]}'%cargs
    resp=requests.post('http://%s:2375/containers/%s/exec'%(ip,ids), data=payload,headers=headers)
    #resp=requests.post('http://%s:2375/containers/%s/exec'%(ip,ids), data=payload,headers=headers,proxies=proxies)
    return json.loads(resp.text)['Id']


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
    if(len(sys.argv)<3):
        print "ip [options[list|exec]] args"
        exit()

    ip=sys.argv[1]
    opt=sys.argv[2]
    if opt=='list':
        listDockerId(ip)
    if opt=='exec':
        if(len(sys.argv)<4):
            print "ERROR"
            exit()
        docid=sys.argv[3]
        cmd=sys.argv[4]
        cid=requestCid(ip,docid,cmd)
        print CommandExec(ip,cid),
