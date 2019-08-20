import requests

HEADERS = {'user-agent': 'Safari/537.36'}

def GET(url, logger, params=None, HEADERS=HEADERS, retries=5):

	response = None
	while retries:
		try: 
			response = requests.get(url, params=params, headers=HEADERS, timeout=10)
		except requests.exceptions.ReadTimeout: 
			pass

		if response!=None: return response

		retries -= 1
		logger.info("Retries left: %d", retries)
	
	raise requests.exceptions.ReadTimeout

def EXCEPTION(msg, logger):
	try:
		raise ValueError()
	except ValueError as e:
		logger.exception(msg, exc_info=True)