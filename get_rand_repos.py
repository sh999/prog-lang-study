import requests, random, csv, sys, time
from secrets import gh_auth_token

repos = {}
base_url = 'https://api.github.com/repositories?since='
token_str = "token " + gh_auth_token
headers = {'user-agent': 'prog-lang', 'Authorization': token_str}

def dump_csv():
	with open('repo_info.csv', 'w') as f:
		csvwriter = csv.writer(f)
		for k, v in repos.items():
			csvwriter.writerow((k, v))

def request_loop():
	counter = 0
	while counter <= 100000:
		
		rand_id = random.randrange(1, 82605000)
		url = base_url + str(rand_id)
		resp = requests.get(url, headers=headers)

		if resp.status_code != 403:
			j_resp = resp.json()
		else:
			rate_resp = requests.get('https://api.github.com/rate_limit',
				headers=headers).json()
			print(rate_resp)
			print("Sleeping due to rate limit.\n\tCounter: " + str(counter))
			time.sleep(3660)
			

		for entry in j_resp:
			if entry['private'] == False and entry['fork'] == False:
				try:
					atmpt = repos[str(entry['id'])]
				except KeyError:
					repos[str(entry['id'])] = entry['full_name']
					counter += 1
					break

request_loop()
dump_csv()