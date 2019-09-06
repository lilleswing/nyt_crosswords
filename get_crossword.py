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
    'nyt-a=iO-KNrTLeKmrjNco0vzP52; vistory=a00; vi_www_hp=b20; optimizelyEndUserId=oeu1546533760629r0.2615924416086872; edu_cig_opt=%7B%22isEduUser%22%3Afalse%7D; b2b_cig_opt=%7B%22isCorpUser%22%3Afalse%7D; nyt-gdpr=0; nyt-purr=cfh; NYT-T=ok; nyt-geo=US; NYT-MPS=fd6f3900b6584cdd06a68c46a19e8b6e828a49d3d49e2447b90c24f1ddce2e70377c1766f88cfc63f11ea3592913e508; nyt-d=101.000000000NAI00000s9Iny1%2F6ouh0pA2e%2F1w9pKn0t8dnq1Z0XO70I5Xjy05A34e0zUWSA0U50eC1vA3Ch0rBdyR0J6nyJ07PGT%2F0R4niB0K1WS800PNDo1fUNPW1mVMD1%40a948c6db%2Fbf37799d; NYT-S=1ETWFtaOz.A/a1PmDaDQ3oAmgWLxQuZyROCbboExJAXx.fW.Z.J3Nzm6wl1qsSIblfalTpzrtSHSFRbebnCk3bSqcf/s/hPYX4XBXqwlZsucOa0qNORN2C/oCUXGnqS1ypLzVvSpZreYg0; nyt-auth-method=sso'
    cookie = sys.argv[1]
    main(cookie)