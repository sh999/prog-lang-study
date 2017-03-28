'''
get_stats.py
Input: JSON file containing github repo information
Goal: Extract repo stats 
'''
import json
import pickle
import re
import operator
import sys
from pprint import pprint

def make_pickle(file_string):
	# file_string = "repo_info_default.json"
	# file_string = "test.json"		
	# file_string = "repo_info_minimal.json"
	with open(file_string, 'r',encoding="utf8") as jf:
	    data = json.load(jf)
	outfile = open(file_string+".pickle", "wb")
	pickle.dump(data, outfile)

def get_stats(pickle_filename):
	# data = open("repo_out.pickle","rb")
	print("Loading pickle")
	data = open(pickle_filename,"rb")
	data = pickle.load(data)
	lang_count = {}
	lang_count_lowcommits = {}
	commits_out = open(pickle_filename+"commits_out.csv","w")
	commits_out.write("full_name,language,commits_count\n")
	langs_out = open(pickle_filename+"langs_out.csv","w")
	for repo in data:
		if repo["language"] not in lang_count:
			lang_count[repo["language"]]=0
		else:
			lang_count[repo["language"]] += 1
		# if repo["language"] not in lang_count_lowcommits:
		# 	lang_count_lowcommits[repo["language"]]=0
		# else:
		# 	lang_count_lowcommits[repo["language"]] += 1
		pprint(repo["full_name"]+","+str(repo["commits_count"])+"\n")
		commits_out.write(repo["full_name"]+","+repo["language"]+","+str(repo["commits_count"])+"\n")
	for i in lang_count:
		langs_out.write(i+","+str(lang_count[i])+"\n")
	sorted_lang = sorted(lang_count.items(), key=operator.itemgetter(1))
	pprint(sorted_lang)
	# sorted_lang_lowcommits = sorted(lang_count_lowcommits.items(), key=operator.itemgetter(1))
	# pprint(sorted_lang_lowcommits)

json_file = sys.argv[2]
print(sys.argv)
if sys.argv[1] == "pickle":
	make_pickle(json_file)
elif sys.argv[1] == "stats":
	get_stats(json_file)
