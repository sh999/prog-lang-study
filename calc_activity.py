import json, datetime

languages = ["JavaScript","Java","Python","Ruby","PHP","C++","C","CSS","HTML","C#","Shell","Objective-C","Perl","Go","VimL"]
rows = []
date = datetime.datetime.strptime('2017-03-16', '%Y-%m-%d').date()

with open('repo_info_minimal.json', 'r') as infile:
	repos = json.load(infile)

for repo in repos:
	row = []
	if repo["language"] in languages:
		row.append(repo["full_name"])
		row.append(str(repo["commits_count"]))
		commits = repo["commits"]
		c_date = commits[len(commits)-1].split('T')[0]
		c_date = datetime.datetime.strptime(c_date, '%Y-%m-%d').date()
		diff = date - c_date
		row.append(str(diff.days))
		row.append(str(repo["commits_count"] / diff.days))
		row.append(repo["language"])
		rows.append(tuple(row))

with open('activity_levels.csv', 'w') as outfile:
	outfile.write("repo,num_commits,age_days,commits_per_day,language\n")
	for row in rows:
		outfile.write(','.join(row) + '\n')