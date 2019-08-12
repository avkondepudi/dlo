from __future__ import print_function
import re, json

from .utils import GET

class Data(object):
	
	def __init__(self, **kwargs):

		self._pandas = True
		try: import pandas as pd
		except ImportError: self._pandas = False
		
		for key, value in kwargs.items():
			setattr(self, key, value)
	
	@property
	def _local(self):
		
		_local = {}
		for key, value in self.__dict__.items():
			if key[0]!='_': _local[key] = value
		return _local
	
	@property
	def local(self):
		
		return self._local
	
	@local.setter
	def local(self, local):
		
		for key in self.local.keys():
			delattr(self, key)
		
		for key, value in local.items():
			setattr(self, key, value)
	
	@property
	def endpoint(self):
		return self._endpoint

	@endpoint.setter
	def endpoint(self, endpoint):

		self._endpoint = endpoint
		self._info = self.getInfo()
	
	def setParam(self, param, param_val): 
		
		setattr(self, param, param_val)
	
	def removeParam(self, param):
		
		delattr(self, param)

	def getEndpointResponse(self):

		url = "http://stats.nba.com/stats/%s/?" % (self._endpoint)
		return GET(url)
	
	def getEndpointParams(self):
	
		response = self.getEndpointResponse()
		if self.getEndpointResponse().status_code!=400: raise ValueError("Endpoint %s not valid, possibly deprecated" % (self._endpoint))
			
		msg = response.text
		msg.split(';')
		
		params = []
		for p in msg.split(';'):
			if p[-1]=='.': params.append(p.split()[1])
			else: params.append(p.split()[0])

		return params

	def getInfo(self):

		url = "http://stats.nba.com/stats/%s/?" % (self._endpoint)

		params = self.getEndpointParams()
		params_info = {}
		params_info['params'] = params

		temp_dict = {}
		for param in params:
			temp_dict[param] = "a"

		response = GET(url, params=temp_dict)
		if response.status_code != 400: raise ValueError("Endpoint %s not valid" % (self._endpoint))
		
		msg = response.text.split(';')
		for line in msg:
			if len(line.split())<=2: 
				continue
			if line.split()[2] in params:
				info = {'regex': '', 'values': [], 'required': True}
				if '^' and '$' not in line:
					edge_indices = [i for i, c in enumerate(line) if c=='\'']
					info['regex'] = '^'+line[(edge_indices[0]+1):edge_indices[1]]+'$'
				else: 
					info['regex'] = line[line.find('^'):(line.find('$')+1)]

				if '?' in info['regex']: 
					info['required'] = False
					if '|' in info['regex']:
						info['values'] = ['']+[v[1:-1] for v in info['regex'][2:-3].split('|')]

				if '|' in info['regex']: 
					info['values'] = [v[1:-1] for v in info['regex'][1:-1].split('|')]

				params_info[line.split()[2]] = info

		return params_info

	def getParamInfo(self, param):

		if param in self._info.keys(): return self._info[param]
		else: return {}

	def isParamValueValid(self, param, param_val):
	
		if param not in self._info.keys() and param in self._info['params']: return -1

		regex = self._info[param]['regex']
		x = re.findall(regex, param_val)
		
		if len(x)==1: return 0
		else: return 1

	def getParamValueForUrl(self, param):

		if param in self.__dict__.keys(): 
			val = self.__dict__[param]
			if self.isParamValueValid(param, val)!=1: return val
			else: raise ValueError("%s for param %s not valid" % (val, param))
		else:
			if self.isParamValueValid(param, "")==-1: 
				if "Date" in param: return ""
				else: return "0"
			if self._info[param]['required']:
				vals = self._info[param]['values']
				if vals!=[]: return vals[0]
				else: return "00"
			else: return ""

	def getData(self, print_url=False, pandify=False):

		url = "http://stats.nba.com/stats/%s" % (self._endpoint)

		url_to_print = url + "/?"
		params_dict = {}
		for p in self._info['params']:
			params_dict[p] = self.getParamValueForUrl(p)
			url_to_print += str(p).replace(" ", "%20") + "=" + str(self.getParamValueForUrl(p)).replace(" ", "%20") + "&"

		if print_url: print(url_to_print[:-1])
		response = GET(url, params=params_dict)
		if response.status_code != 200:
			if response.status_code == 500: raise ValueError("Server error, response status code %d" % (response.status_code))
			else: raise ValueError("Incorrect param values passed, response status code %d" % (response.status_code))

		if pandify and self._pandas:

			_data = response.json()

			for i, result in enumerate(_data['resultSets']):

				if result['rowSet']==[]:
					_result = {}
					_result['name'] = result['name']
					_result['data'] = pd.DataFrame()
				else:
					_result = {}
					_result['name'] = result['name']
					_result['data'] = pd.DataFrame.from_dict(result['rowSet'])
					_result['data'].columns = result['headers']

				_data['resultSets'][i] = _result

			return _data

		if pandify: print('Pandas library not found')

		return response.json()

