import requests

HEADERS = {'user-agent': 'Safari/537.36'}

def GET(url, params=None, HEADERS=HEADERS, retries=5):

	response = None
	while retries:
		try: response = requests.get(url, params=params, headers=HEADERS, timeout=10)
		except requests.exceptions.ReadTimeout: 
			pass
		if response!=None:
			return response

		retries -= 1
		print('Retries left: %d' % (retries))
	
	raise requests.exceptions.ReadTimeout
