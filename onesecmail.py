#!c:/SDK/Anaconda2/python.exe
#encode:utf-8
from __future__ import print_function
import os, sys
print("PID =", os.getpid())
import argparse
import requests as REQ
requests = REQ.Session()
from make_colors import make_colors
from pydebugger.debug import debug
from pause import pause
if sys.version_info == 3:
	raw_input = input
import ast
import textwrap
import re
import clipboard

class onesecmail(object):
	def __init__(self, username=None):
		self.username = username
		self.url = 'https://www.1secmail.com/api/v1/'
		
	def build_dict(self, seq, key):
		return dict((d[key], dict(d, index=index)) for (index, d) in enumerate(seq))
		
	def inbox(self, username=None):
		if not username:
			username = self.username
		if not username:
			username = raw_input(make_colors("USERNAME [without @domain]: ", 'lw','b'))
			self.username = username
		if not username:
			print(make_colors("No Username Given !", 'lw', 'lr', ['blink']))
			sys.exit()
		else:
			params = {
				'action':'getMessages',
				'login':username,
				'domain':'1secmail.com'
			}
			debug(params = params)
			a = requests.get(self.url, params = params)
			debug(url = a.url)
			content = a.content
			debug(content = content)
			if content:
				content = ast.literal_eval(content)
				debug(content = content)
			return content
		
	def wrap_description(self, description):
		_prefix = len('Short Description') + 2
		if cmdw.getWidth() < 112:
			width = cmdw.getWidth() - (_prefix + 2)
		else:
			width = int((cmdw.getWidth() / 2) - (_prefix + 2))
		prefix = " " * _prefix
		wrapped = textwrap.wrap(description, width = width)
		#debug(wrapped = wrapped)
		if len(wrapped) > 1:
			first_line = wrapped[0]
			print(make_colors(first_line, 'lightblue'))
			for i in wrapped[1:]:
				print(prefix + make_colors(i, 'lightcyan'))
		else:
			return make_colors(description, 'lightgreen')
			
	def print_message(self, params, show=True):
		debug(params = params)
		a = requests.get(self.url, params = params)
		content = a.content
		debug(content = content)
		if content and not content == "Message not found":
			content = ast.literal_eval(content)
			debug(content = content)
			#from pprint import pprint
			#pprint(content)
			#clipboard.copy(content.get('textBody')
			debug(content_keys = content.keys())
			if show:
				print(make_colors('Subject', 'ly') + "    :" +  make_colors(content.get('subject'), 'b', 'ly'))
				print(make_colors('Date', 'lg') + "       :" +  make_colors(content.get('date'), 'b', 'lg'))
				print(make_colors('Attachments', 'lm') + ":" +  make_colors(content.get('attachment'), 'lw', 'lm'))
				print(make_colors('Message', 'lc') + "    :" +  make_colors(content.get('textBody'), 'lw', 'bl'))
				qc = raw_input(make_colors("open full html message [y/n]: ", 'lw', 'lr'))
				if qc:
					qc = str(qc).strip()
				if qc == 'y':
					import browser
					html = content.get('htmlBody').replace("\\/", "/")
					debug(html = html)
					browser.main(html, title="Messages")								
		return content
	
	def get_body(self, id=None, username = None, show=True):
		params = {
			'action':'readMessage',
			'login':username,
			'domain':'1secmail.com',
			'id':str(id)
		}
		
		if not id:
			inbox = self.inbox(username)
			inbox.reverse()
			debug(inbox = inbox)
			data = self.build_dict(inbox, 'id')
			debug(data = data)
			if data:
				n = 1
				for i in data:
					if len(str(n)) == 1:
						number = '0' + str(n)
					else:
						number = str(n)
					print(make_colors(number, 'lb') + ". " + make_colors(data.get(i).get('from'), 'lw', 'bl') + " " + make_colors("(" + data.get(i).get('subject') + ")", 'b','ly') + " " + make_colors("[" + data.get(i).get('date') + "]", 'b', 'lg') + make_colors("[" + str(i) + "]", 'lw', 'm'))
					n+=1
				q = raw_input(make_colors("Select Number: ", 'lr','lw'))
				if q and str(q).strip().isdigit() and int(str(q).strip()) <= len(inbox):
					params.update({'id':str(list(data.keys())[int(str(q).strip()) - 1])})			
			else:
				print(make_colors("No Inbox !", 'lw','lr', ['blink']))
				return False
				
		return self.print_message(params, show)
			
if __name__ == '__main__':
	c = onesecmail()
	c.get_body(username = sys.argv[1])