import requests, random, csv, sys

repos = {}
base_url = 'https://api.github.com/repositories?since='
auth_key = ''

def dump_csv():
	with open('repo_info.csv', 'w') as f:
		csvwriter = csv.writer(f)
		for k, v in repos.items():
			csvwriter.writerow(k, v)

def request_loop():
	counter = 0
	while counter <= 100000:
		
		rand_id = random.randrange(1, 82605000)
		resp = requests.get(base_url + str(rand_id))

		if resp.status_code != 403:
			j_resp = resp.json()
		else:
			rate_resp = requests.get('https://api.github.com/rate_limit').json()
			print(rate_resp)
			dump_csv()
			print("\nExiting due to rate limit.\nCounter: " + str(counter))
			sys.exit()

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