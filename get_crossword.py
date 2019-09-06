import requests
import json
import datetime
import sys
import re

def save_results(response):
    pattern = r".+scoreList.+?(\[.+?\]).+"
    body = response.text.splitlines()
    for b in body:
        match = re.match(pattern, b)
        if match is not None:
            break
    scores = match.group(1)
    l = json.loads(scores)
    today = datetime.datetime.today()
    date_str = str(today.date())
    d = {date_str: l}
    with open('scores.json', 'w') as fout:
        fout.write(json.dumps(d))
    print('Success')
    
def get_nyt_body(cookie):
    url = "https://www.nytimes.com/puzzles/leaderboards"
    headers = {
    'authority': 'www.nytimes.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'sec-fetch-site': 'none',
    'referer': 'https://www.nytimes.com/crosswords',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': cookie,
    }

    response = requests.get('https://www.nytimes.com/puzzles/leaderboards', headers=headers)
    if response.status_code != 200:
        print("Unable to connect to nyt status_code:%s" % response.status_code)
        return None
    return response

def main(cookie):
    response = get_nyt_body(cookie)
    if response is None:
        sys.exit(1)
        return
    save_results(response)
    

if __name__ == "__main__":
    
    cookie = sys.argv[1]
    main(cookie)