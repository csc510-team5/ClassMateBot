import requests


API_KEY = 'AIzaSyDOqfDutkI2E-rU87Z8rZziXpaqCDOml0M'
SEARCH_ENGINE_ID = '57d91425da7804a1c'

def build_payload(query, start=1, num=10, date_restrict='m1', **params):
    payload = {
        'key': API_KEY,
        'q': query,
        'cx': SEARCH_ENGINE_ID,
        'start': start,
        'num': num,
        'dateRestrict': date_restrict
    }
    
    payload.update(params)
    return payload

def make_request(payload):
    res = requests.get('https://www.googleapis.com/customsearch/v1', params=payload)
    return res.json()

print(make_request(build_payload('monkey')))