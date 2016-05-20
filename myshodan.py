import shodan
mykey = '5ISgqbZ9usGsN9MP1yv5LiYTzrj4HhKm'
api=shodan.Shodan(mykey)
results=api.search('apache')
for result in results['matches']:
	print 'IP:%s'%result['ip_str']
