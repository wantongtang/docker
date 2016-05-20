#!/usr/bin/env python
# coding:utf-8
import json
import requests
import sys
mycmd = 'ifconfig' # 批量执行的命令

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
    resp=requests.post('http://%s:2375/containers/%s/exec'%(ip,ids), data=payload,headers=headers,timeout=2)
    #resp=requests.post('http://%s:2375/containers/%s/exec'%(ip,ids), data=payload,headers=headers,proxies=proxies)
    
    return json.loads(resp.text)['Id']


def CommandExec(ip,cid):
    headers = {'content-type': 'application/json'}
    payload='{"Detach": false,"Tty": false}'
    resp=requests.post('http://%s:2375/exec/%s/start'%(ip,cid), data=payload,headers=headers)
    return resp.text

def listDockerId(ip):
#    print "IP:%s"%ip
    data=resp=requests.get('http://%s:2375/containers/json'%ip,timeout=2)
    jsond=json.loads(data.text)
    for i in xrange(1,len(jsond)):
#        print jsond[i-1]['Id']
	output=open('result1.txt','a')
	output.write("\n %s    %s"%(line.replace('\n',''),jsond[i-1]['Id']))
	output.close()
	result = CommandExec(ip,requestCid(ip,jsond[i-1]['Id'],mycmd))
	if not( '172' in result.split('.')[0]  or '192' in result.split('.')[0] or '10' in result.split('.')[0]):
		print ("ip:%s  OS: %s"%(ip,result))		
    	output=open('result_cmd1.txt','a')
        output.write("\n %s   %s"%(ip,result))
        output.close()
	
if __name__== '__main__':
	if len(sys.argv)==2:
		try :
			file_obj=open(sys.argv[1])
		except:
			print 'file %s do not exist'%(sys.argv)
		if file_obj:
			for line in file_obj:
				try:
					ip = line.replace('\n','')
				        listDockerId(ip)
				except:
					print 'timeout'
		file_obj.close()



