import requests
from json import loads

class ApiRateError(Exception):

	def __init__(self, message = None):
		if not message:
			self.message = 'Api did not respond.'
		else:
			self.message = message


class POSTApiClient:
	
	def __init__(self, url_dict: dict) :
		self._url_dict = url_dict

	def translate(self, pre_translation: str, from_language: str) -> dict:
		
		data = {'text': pre_translation}
		
		try:
			_url = self._url_dict[from_language]
		except KeyError as e:
			raise e

		r = requests.post(url = _url, data = data)
		if r.status_code == 429:
			raise ApiRateError(f'{loads(r.text)["error"]["message"]}')
		return loads(r.text)

	@property
	def url_dict(self) -> dict:
		return self._url_dict
	
	@url_dict.setter
	def url_dict(self, url_dict: dict):
		self._url_dict = url_dict	