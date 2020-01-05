import tkinter.ttk as ttk
from tkinter import Tk, Button, Text, Label, StringVar, messagebox, OptionMenu, ttk
from post_api_client import POSTApiClient
from urllib3.exceptions import ConnectionError

class Form:

	BTN_BG = '#151515'
	BTN_FG = '#f0f0f0'
	FORM_BG = '#252525'
	FONT = ('segoe ui', 14)
	OUTPUT_BOX_FG = '#ffffff'
	ENTRY_BOX_BG = '#f4f4f4'

	def __init__(self, master: Tk, api_client: POSTApiClient):

		self._api_client = api_client
		self._master = master
		self._master.minsize(width = 750, height = 660)
		self._master.configure(background = Form.FORM_BG)
		self._master.title('Linguino by Simon Olofsson')
		
	def render_ui(self):

		self._instruction_label = Label(master = self._master,
			text = 'The app is limited to 6 translations per hour and 60 per day.\n' \
				   'Type something, select a language and click the button.',
			font = Form.FONT,
			background = Form.FORM_BG,
			foreground = Form.BTN_FG)

		self._entry_box = Text(master = self._master,
			width = 52, height = 6,
			font = Form.FONT,
			background = Form.ENTRY_BOX_BG)

		self._output_box = Text(master = self._master,
			width = 52, height = 6,
			font = Form.FONT,
			#background = Form.FORM_BG,
			#foreground = Form.OUTPUT_BOX_FG,
			bd = 0)
		
		self._go_button = Button(master = self._master,
			width = 25, height = 1,
			text = 'The button',
			font = Form.FONT,
			background = Form.BTN_BG,
			foreground = Form.BTN_FG,
			highlightthickness = 0,
			command = self._invoke_translation,
			bd = 0)

		self._languages_list = ttk.Combobox(self._master,
			values = list(self._api_client.url_dict.keys()),
			width = 20,
			state = 'readonly',
			font = Form.FONT)
		self._languages_list.current(0)

		self._instruction_label.place(x = 65, y = 20)
		self._entry_box.place(x = 40, y = 80)
		self._output_box.place(x = 40, y = 220)
		self._languages_list.place(x = 40, y = 405)
		self._go_button.place(x = 251, y = 400)
		self._entry_box.insert('end-1c', 'Enter your text here')

	def _invoke_translation(self):

		if not len(self._entry_box.get('1.0', 'end-1c')):
			return
		try:
			translation = self._api_client.translate(
				pre_translation = self._entry_box.get('1.0', 'end-1c'),
				from_language = self._languages_list.get())
		except Exception as e:
			messagebox.showwarning('An error occured', e)
			return
			
		self._output_box.delete('1.0', 'end-1c')
		self._output_box.insert('end-1c', translation['contents']['translated'])