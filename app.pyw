import requests
from json import loads
from tkinter import Tk, Button, Text, Label, StringVar, messagebox
from urllib3.exceptions import ConnectionError

class POSTApiClient:
	
	def __init__(self, url: str):
		self._url = url

	def translate(self, pre_translation: str) -> dict:
		data = {
			'text': pre_translation
		}

		r = requests.post(url = self._url, data = data)
		if r.status_code != 200:
			if r.status_code == 401:
				raise ConnectionError('You have exceeded the api limit of 6 per hour and 60 per day.')
			else:
				raise ConnectionError('An error occured and the request could not be completed.')
		return loads(r.text)

	@property
	def url(self):
		return self._url
	
	@url.setter
	def url(self, url: str):
		self._url = url	


class Form:

	BTN_BG = '#151515'
	BTN_FG = '#f0f0f0'
	FORM_BG = '#252525'
	FORM_GEOMETRY = '600x380+0+0'
	FONT = 'Calibri, 11'

	def __init__(self, master: Tk, api_client: POSTApiClient):

		self._api_client = api_client
		self._master = master
		self._master.minsize(width = 500, height = 380)
		self._master.maxsize(width = 500, height = 380)
		self._master.geometry(Form.FORM_GEOMETRY)
		self._master.configure(background = Form.FORM_BG)
		self._master.title('Sindarin Translator')
		
	def render_ui(self):

		self._instruction_label = Label(master = self._master,
										text = 'You are limited to 6 translations per hour. Max 60 per day.',
										font = Form.FONT,
										background = Form.FORM_BG,
										foreground = Form.BTN_FG)

		self._entry_box = Text(master = self._master,
							   width = 58, height = 6,
							   font = Form.FONT,
							   background = '#f4f4f4')

		self._output_box = Text(master = self._master,
							   width = 58, height = 6,
							   font = Form.FONT,
							   background = '#f4f4f4')
		
		self._go_button = Button(master = self._master,
								width = 52, height = 2,
								text = 'Translate',
								font = Form.FONT,
								background = Form.BTN_BG,
								foreground = Form.BTN_FG,
								highlightthickness = 0,
								command = self._invoke_translation,
								bd = 0)

		self._instruction_label.place(x = 68, y = 30)
		self._entry_box.place(x = 15, y = 70)
		self._output_box.place(x = 15, y = 200)
		self._go_button.place(x = 15, y = 320)

	def _invoke_translation(self):
		try:
			translation = self._api_client.translate(
				pre_translation = self._entry_box.get('1.0', 'end-1c'))
		except Exception as e:
			messagebox.showwarning('An error occured', e)
			return
			
		self._output_box.delete('1.0', 'end-1c')
		self._output_box.insert('end-1c', translation['contents']['translated'])
		

if __name__ == '__main__':
	master = Tk()
	form = Form(master = master, api_client = POSTApiClient(
		url = 'https://api.funtranslations.com/translate/sindarin.json'))

	form.render_ui()
	master.mainloop()