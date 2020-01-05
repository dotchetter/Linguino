import os
import sys
import json
import ctypes
import tkinter.ttk as ttk
from tkinter import Tk, Button, Text, Label, StringVar, messagebox, OptionMenu, ttk

from post_api_client import POSTApiClient, ApiRateError
from urllib3.exceptions import ConnectionError

class Form:

	BTN_BG = '#16c5b4'
	BTN_FG = '#ffffff'
	FORM_BG = '#eef1f6'
	LABEL_BG = '#eef1f6'
	LABEL_FG = '#000000'
	FORM_GEOMETRY = '580x545+300+100'
	FONT = ('Segoe UI', 11)
	OUTPUT_BOX_FG = '#ffffff'
	ENTRY_BOX_BG = '#f4f4f4'

	def __init__(self, master: Tk, api_client: POSTApiClient):

		self._api_client = api_client
		self._master = master
		self._master.minsize(width = 520, height = 525)
		self._master.geometry(Form.FORM_GEOMETRY)
		self._master.configure(background = Form.FORM_BG)
		self._master.title('Elven tongue translator - Powered by api.funtranslations.com')
		
	def render_ui(self):

		self._instruction_label = Label(master = self._master,
			text = 'Type what you wish to translate, select a language and click the button.\n' \
				   'The app is limited to 5 translations per hour and 60 per day.\n',
			font = Form.FONT,
			background = Form.LABEL_BG,
			foreground = Form.LABEL_FG)

		self._entry_box = Text(master = self._master,
			width = 55, height = 6,
			font = Form.FONT,
			bd = 0)

		self._output_box = Text(master = self._master,
			width = 55, height = 6,
			font = Form.FONT,
			bd = 0)
		
		self._go_button = Button(master = self._master,
			width = 55, height = 1,
			text = 'The button',
			font = Form.FONT,
			background = Form.BTN_BG,
			foreground = Form.BTN_FG,
			highlightthickness = 0,
			command = self._invoke_translation,
			bd = 0)

		self._languages_list = ttk.Combobox(self._master,
			font = Form.FONT,
			width = 53, 
			state = 'readonly')

		# Placement
		self._instruction_label.pack(pady = 20)
		self._entry_box.pack(pady = 5)
		self._output_box.pack(pady = 5)
		self._languages_list.pack(pady = 20)
		self._go_button.pack(pady = 10)
		self._entry_box.insert('end-1c', 'Enter your text here')

		# Configuration
		self._languages_list['values'] = tuple(self._api_client.url_dict.keys())
		self._languages_list.current(0)
		self._entry_box.bind("<Button-1>", lambda x: self._entry_box.delete('1.0', 'end-1c'))

	def _invoke_translation(self):

		if not len(self._entry_box.get('1.0', 'end-1c')):
			return
		try:
			translation = self._api_client.translate(
				pre_translation = self._entry_box.get('1.0', 'end-1c'),
				from_language = self._languages_list.get())
		except ApiRateError as e:
			messagebox.showwarning('Don\'t be hasty, master Meriadoc.', e)
			return
		except Exception as e:
			messagebox.showwarning('An error occured', e)
			return
		
		self._output_box.delete('1.0', 'end-1c')
		self._output_box.insert('end-1c', translation['contents']['translated'])

if __name__ == '__main__':

	master = Tk()
	master.iconbitmap(r'elf.ico')
	
	api_urls = {
		"Quenya": "https://api.funtranslations.com/translate/quenya.json",
		"Valspeak": "https://api.funtranslations.com/translate/valspeak.json",
		"Jive": "https://api.funtranslations.com/translate/jive.json",
		"Cockney": "https://api.funtranslations.com/translate/cockney.json",
		"Brooklyn": "https://api.funtranslations.com/translate/brooklyn.json",
		"Pirate": "https://api.funtranslations.com/translate/pirate.json",
		"Minion": "https://api.funtranslations.com/translate/minion.json",
		"Ferblatin": "https://api.funtranslations.com/translate/ferblatin.json",
		"Dolan": "https://api.funtranslations.com/translate/dolan.json",
		"Fudd": "https://api.funtranslations.com/translate/fudd.json",
		"Valyrian": "https://api.funtranslations.com/translate/valyrian.json",
		"Vulcan": "https://api.funtranslations.com/translate/vulcan.json",
		"Klingon": "https://api.funtranslations.com/translate/klingon.json",
		"Piglatin": "https://api.funtranslations.com/translate/piglatin.json",
		"Yoda": "https://api.funtranslations.com/translate/yoda.json",
		"Sith": "https://api.funtranslations.com/translate/sith.json",
		"Cheunh": "https://api.funtranslations.com/translate/cheunh.json"
	}


	form = Form(master = master, api_client = POSTApiClient(url_dict = api_urls))

	form.render_ui()
	master.mainloop()