#!/usr/bin/python

import requests
import os
import urllib.parse
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from tqdm import tqdm
from colors import *
from time import sleep


__version__ = 1.0
__author__ = 'Humza Malik'

# Globals
er_pg_parse = red('[PageParssingError]')
aborted = red('[DownloadAborted]')
invalid = blue('[Invalid Selection]')
processing = blue('[Processing]')


class DownloadProgressBar(tqdm):
	def update_to(self, b=1, bsize=1, tsize=None):
		if tsize is not None:
			self.total = tsize
		self.update(b * bsize - self.n)


def main():
	base_url = 'http://ftp.alphamediazone.com'
	cat_page(base_url)


def banner(version, author):
	print(cyan("	   _____       _          "))
	print(cyan("	  / ____|     | |         "))
	print(cyan("	 | |  __  ___ | | ___   _ "))
	print(cyan("	 | | |_ |/ _ \| |/ / | | |"))
	print(cyan("	 | |__| | (_) |   <| |_| |"))
	print(cyan("	  \_____|\___/|_|\_\\\__,_|"))
	print(yellow(f'\t Version: {version}\n\t By: {author}'))


def cat_page(base_url, cat_url= ''):
	if os.name == 'nt':
		os.system('cls')
	else:
		os.system('clear')
	banner(__version__, __author__)
	url = f'{base_url}{cat_url}'
	if cat_url.strip() not in ['', '/']:
		line()
		des_path(cat_url)
	line()
	print(processing, end='\r')
	headers = {
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	try:
		resp = requests.get(url, headers=headers).text
	except ConnectionError:
		print(blue('[ConnectionError] Please check your connection or try again later'))
		exit_msg()
	except Exception as e:
		print(f'{red("[Error]")}\n{e}')
		exit_msg()
	soup = BeautifulSoup(resp, 'html.parser')
	try:
		tabletag = soup.find('table')
		table_info = print_table(tabletag)
	except:
		print(er_pg_parse)
		exit_msg()
	table_info = fix_parent_fix(cat_url, table_info)
	while True:
		ask_cat = input(green('Enter Sr. ? '))
		if ask_cat.lower().strip() in ['e', 'exit']:
			exit_msg()
		if ask_cat.lower().strip() in ['h', 'help']:
			help_msg()
			continue
		if ask_cat.isdigit():
			for row in table_info:
				if int(ask_cat) == row[0]:
					if row[1].lower().strip() != 'file':
						cat_page(base_url, row[-1])
					else:
						downit(base_url, row[-1], row[2])
						break
			else:
				print(invalid)

		else:
			print(invalid)


def spr():
	if os.name == 'nt':
		return '\\'
	return '/'


def line():
	print(red('-' * 54))


def exit_msg():
	print(red('[ Exiting... ]'))
	sleep(1)
	exit()


def help_msg():
	print(red('[No HELP AVAILABLE]'))
	input()


def downit(base_url, cat_url, filename):
	line()
	file_name = filename
	link = base_url + cat_url
	print(f'{cyan("[File] ")}{blue(file_name)}')
	sep = spr()
	if not os.path.exists(f'Downloads'):
		os.mkdir('Downloads')
	file_name = f'Downloads{sep}{file_name}'
	try:
		with DownloadProgressBar(unit='B', unit_scale=True,
								 miniters=1, desc=blue('[ Downloading ]')) as t:
			urllib.request.urlretrieve(link, filename=file_name, reporthook=t.update_to)
	except KeyboardInterrupt:
		print(aborted)
		return
	print(cyan('[DownloadComplete]'))
	line()


def print_table(tabletag):
	table_info = []
	tr_tags = tabletag.find_all('tr')
	th_tags = tr_tags[0]
	tr_tags.remove(th_tags)
	table_headers = []
	table_headers.append(red('Sr.'))
	for th in th_tags:
		if th.span is None:
			table_headers.append('')
		else:
			table_headers.append(red(th.span.text.title()))
	table = PrettyTable(table_headers)
	sr_no = 1
	for tr in tr_tags:
		row = []
		row.append(sr_no)
		if tr.find('td', class_='fb-s').text == '':
			row.append('Folder')
		else:
			row.append('File')
		if tr.find('td', class_='fb-n').a is not None:
			name = tr.find('td', class_='fb-n').a.text
			link = tr.find('td', class_='fb-n').a['href']
		row.append(name.title())
		row.append(tr.find('td', class_='fb-d').text)
		row.append(tr.find('td', class_='fb-s').text)
		table.add_row(row)
		row.append(link)
		table_info.append(row)
		sr_no += 1
	print(table)
	return table_info


def fix_parent_fix(cat_url, table_info):
	for row in table_info:
		if row[-1] == '..':
			row[-1] = last_url(cat_url)
	return table_info


def last_url(url):
	toreturn = ''
	temp_list = url.split('/')
	while '' in temp_list : temp_list.remove('')
	del temp_list[-1]
	for a in temp_list:
		toreturn += f'/{a}'
	toreturn += '/'
	return toreturn


def des_path(url):
	url = urllib.parse.unquote(url)
	temp_list = url.split('/')
	while '' in temp_list : temp_list.remove('')
	print(*temp_list, sep=green(' -> '))


if __name__ == '__main__':
	main()
