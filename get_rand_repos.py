import requests, random, csv, sys, time
from secrets import gh_auth_token

counter = 0
repos = {}
base_url = 'https://api.github.com/repositories?since='
token_str = 'token ' + gh_auth_token
headers = {'user-agent': 'prog-lang', 'Authorization': token_str}

if len(sys.argv) == 3: # <repo_info_recover.csv> <counter>
	print("Recovering from " + sys.argv[1])
	counter = int(sys.argv[2])
	with open(argv[1], 'r') as infile:
		for line in infile:
			split_line = line.strip('\n').split(',')
			repos[split_line[0]] = split_line[1] 

def dump_csv():
	with open('repo_info.csv', 'w') as f:
		csvwriter = csv.writer(f)
		for k, v in repos.items():
			csvwriter.writerow((k, v))

def request_loop():
	global counter
	while counter <= 100000:
		
		rand_id = random.randrange(1, 82605000)
		url = base_url + str(rand_id)
		resp = requests.get(url, headers=headers)

		if resp.status_code != 403:
			j_resp = resp.json()
		else:
			rate_resp = requests.get('https://api.github.com/rate_limit',
				headers=headers).json()
			reset_time = int(rate_resp['rate']['reset'])
			wait_dur = reset_time - int(time.time()) 
			print("Sleeping for " + str(wait_dur) + " sec. due to rate limit.")
			print("\tCounter: " + str(counter))
			time.sleep(wait_dur)

		for entry in j_resp:
			if entry['private'] == False and entry['fork'] == False:
				try:
					atmpt = repos[str(entry['id'])]
				except KeyError:
					repos[str(entry['id'])] = entry['full_name']
					counter += 1
					break

		if counter % 100 == 0:
			print("Counter: " + str(counter))

try:
	request_loop()
except Exception as e:
	print(e)
finally:
	dump_csv()
	print("Counter: " + str(counter))
