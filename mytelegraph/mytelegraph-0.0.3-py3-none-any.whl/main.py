#! /usr/bin/env python3

import os
import sys
import json
import argparse
import requests 
from telegraph.api import Telegraph
from telegraph.conf import token
from telegraph.utils import html_to_nodes

__author__="Muhammad Al Fajri"
__email__="fajrim228@gmail.com"
__telegram__="https://t.me/ini_peninggi_badan"

def create_page(path, values: dict = None):
	"""
	Simple!
	"""
	try:
		r = requests.post(f'https://api.telegra.ph/{path}', params=values)
		return r.json()
	except Exception as e:
		raise e
	
def get_all_page():
	'''
	Place a description
	'''
	T = Telegraph(access_token = token)
	response = T.get_page_list()
	return response

def create_token(author: str, short_name: str):
	'''
	Place a description
	'''
	data = {
		'short_name':short_name,
		'author_name':author
	}
	r = requests.post('https://api.telegra.ph/createAccount', params=data)
	return r.text
	
def main(
		string_input: str = None,
		args_filename: str = None,
		args_title: str = None,
		args_author: str = None,
		args_author_url: str = None,
		args_page: str = None
	):
	global __author__
	author_name = __author__
	author_url = "https://t.me/" + __telegram__
	'''
	* this is the main script, you only need to call this one.
	* take an argument (text/html) for now, default to None

	'''
	if args_page:
		print(get_all_page())
		sys.exit(0)
	if args_filename:
		html_file = args_filename
	elif not args_filename:
		html_file = os.getenv('HTML_FILE')
	else:
		return None
	if args_title:
		title = args_title
	else:
		title = html_file.replace('-', ' ')
	if args_author:
		author_name = args_author
	else:
		author_name = author_name
	if args_author_url:
		author_url = args_author_url
	else:
		author_url = author_url
	a = open(html_file).read()
	if string_input:
		content = html_to_nodes(string_input)
	else:
		content = html_to_nodes(a)
	content_json = json.dumps(content, ensure_ascii=False)
	data = {
		'access_token':token,
		'title': title,
		'author_name': author_name,
		'author_url': author_url,
		'content': content_json,
		'return_content': True
	}
	try:
		return (
			create_page('createPage', data)['result']
		)
	except Exception as e:
		return None
