import requests, json, sys, datetime, time
from secrets import gh_auth_token

MIN_COMMITS = 30
MAX_COMMITS = 10000
DATE = datetime.datetime.strptime('2016-03-01', '%Y-%m-%d').date()
MIN_AGE = 365 # Measured in days
REPO_COUNT = 0

REPOS = []
REPO_LIST = []
TOKEN_STR = 'token ' + gh_auth_token
HEADERS = {'user-agent': 'prog-lang', 'Authorization': TOKEN_STR}

COUNTER = 0

if len(sys.argv) == 3: # <repo_info_recover.json> <COUNTER>
	print("Recovering from " + sys.argv[1])
	COUNTER = int(sys.argv[2]) + 1
	with open(sys.argv[1], 'r') as infile:
		REPOS = json.load(infile)

def load_csv():
	with open('repo_info.csv', 'r') as infile:
		for line in infile:
			split_lines = line.strip('\n').split(',')
			REPO_LIST.append(split_lines[1])

def dump_json():
	print("Counter: " + str(COUNTER))
	print("Number of entries in repo_info.json: " + str(len(REPOS)))
	with open('repo_info.json', 'w') as outfile:
		json.dump(REPOS, outfile, indent='\t')

def is_past_min_age(c_date):
	c_date = c_date.split('T')[0]
	c_date = datetime.datetime.strptime(c_date, '%Y-%m-%d').date()
	diff = c_date - DATE
	if diff.days >= MIN_AGE:
		return True
	else:
		return False

def handle_rate_limit():
	rate_resp = requests.get('https://api.github.com/rate_limit',
		headers=HEADERS).json()
	reset_time = int(rate_resp['rate']['reset'])
	wait_dur = reset_time - int(time.time()) 
	print("Sleeping for " + str(wait_dur) + " sec. due to rate limit.")
	print("\tCounter: " + str(COUNTER))
	time.sleep(wait_dur)

def request_json(url):
	resp = requests.get(url, headers=HEADERS)
	if resp.status_code != 403:
		return resp.json()
	else:
		handle_rate_limit()
		request_json(url)

def request_loop():
	global COUNTER
	base_url = 'https://api.github.com/repos/'

	while COUNTER < len(REPO_LIST):
		repo = REPO_LIST[COUNTER]
		if COUNTER % 100 == 0:
			print("Counter: " + str(COUNTER))

		repo_info = request_json(base_url + repo)

		if is_past_min_age(repo_info['created_at']):

			page = 1
			commits = []
			done = False
			while len(commits) < MAX_COMMITS and not done:
				commit_pg = request_json(base_url + repo + '/commits?page='
					+ str(page) + '&per_page=100')
				if len(commit_pg) > 0:
					for commit in commit_pg:
						commits.append(commit['commit'])
				else:
					done = True
			
			if len(commits) >= MIN_COMMITS and len(commits) <= MAX_COMMITS:
				repo_info['commits'] = commits
				repo_info.pop('owner')
				REPOS.append(repo_info)

				languages = request_json(base_url + repo + '/languages')
				repo_info['languages'] = languages

		COUNTER += 1

load_csv()
try:
	request_loop()
except Exception as e:
	print(e)
finally:
	dump_json()
