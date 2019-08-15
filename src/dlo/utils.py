import logging

import requests

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

HEADERS = {'user-agent': 'Safari/537.36'}

def GET(url, params=None, HEADERS=HEADERS, retries=5):

	response = None
	while retries:
		try: 
			response = requests.get(url, params=params, headers=HEADERS, timeout=10)
		except requests.exceptions.ReadTimeout: 
			pass
		if response!=None:
			return response

		retries -= 1
		LOGGER.info("Retries left: %d", retries)
	
	raise requests.exceptions.ReadTimeout

def EXCEPTION(logger, msg):
	try:
		raise ValueError()
	except ValueError as e:
		logger.exception(msg, exc_info=True)