from secrets import gh_auth_token
import requests
import pprint
import csv
import json
import re
def get_repo_data(repo_name,outfile):
	'''
		Called by loop_repos
		Request repo data given the repo name
		Write to outfile
	'''
	url = 'https://api.github.com/repos/'+repo_name
	token_str = 'token ' + gh_auth_token
	headers = {'user-agent': 'prog-lang', 'Authorization': token_str}
	resp = requests.get(url, headers=headers)
	j_resp = resp.json()
	pprint.pprint(resp.json())
	with open(outfile, 'a') as f:
		json.dump(j_resp,f)
		f.write("\n")

def loop_repos():
	'''
		Loop through input csv of repo list
		For each repo url, call get_repo_data
	'''
	infile = "repo_info.csv"
	# Each json line is indiv. repo data
	outfile = "repo_data.json"
	open(outfile, 'w').close()
	with open(infile) as f:
		for line in f:
			# regex to get repo url
			regex = r",(\S*)\n"
			match = re.search(regex, line)
			if match != None:
				repo_name = match.group(1)
				print(repo_name)
				# GET request, write data to outfile
				get_repo_data(repo_name,outfile)

loop_repos()