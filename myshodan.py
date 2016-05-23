import shodan
mykey = '5ISgqbZ9usGsN9MP1yv5LiYTzrj4H'
api=shodan.Shodan(mykey)
results=api.search('port:2375 X-Content-Type-Options: nosniff')

output=open('shodan.txt','a')
for result in results['matches']:
	print 'IP:%s'%result['ip_str']
        output.write("\n%s"%(result['ip_str']))
output.close()
