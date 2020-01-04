import os
import sys
import json
import ctypes
from ui import Form
from tkinter import Tk
from post_api_client import POSTApiClient

def load_api_urls(path: str, filename: str) -> dict:
	try:
		with open(filename, 'r', encoding = 'utf-8') as file:
			api_url_dict = json.load(file)
	except exception as e:
		raise e
	return api_url_dict

if __name__ == '__main__':

	master = Tk()
	if 'win' in sys.platform:
		ctypes.windll.shcore.SetProcessDpiAwareness(1)

	try: 
		api_url_from_json = load_api_urls(path = os.getcwd(), filename = 'api_url.json')
	except Exception as e:
		messagebox.showerror('An error occured and the app cannot open.', e)
		sys.exit()

	form = Form(master = master, api_client = POSTApiClient(url_dict = api_url_from_json))

	form.render_ui()
	master.mainloop()