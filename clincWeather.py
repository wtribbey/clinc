import requests
import json

def get_api_request(req_data):
    api_key = 'e09ff1dbd4498040f51b500aed04e699'

    if 'lat' in req_data and 'lon' in req_data:
        lat = req_data['lat']
        lon = req_data['lon']

    location = None
    slots    = None
    vals     = None
    place    = None
    if 'slots' in req_data:
        slots = req_data['slots']
        if '_LOCATION_' in slots:
            location = slots['_LOCATION_']
            if 'values' in location:
                vals = location['values']
                if len(vals) >0:
                    place = vals[0]['tokens']

    api_url = "https://api.openweathermap.org/data/2.5/weather?q=ann arbor&appid=e09ff1dbd4498040f51b500aed04e699"

    if float(lat) != 0 and float(lon) != 0:
        api_url = 'https://api.openweathermap.org/data/2.5/weather?q=lat='+str(lat)+'&lon='+str(lon)+'&appid=e09ff1dbd4498040f51b500aed04e699'
    elif None != location:
        print(location)
        api_url = 'https://api.openweathermap.org/data/2.5/weather?q=atlanta'+'&appid=e09ff1dbd4498040f51b500aed04e699'
    else:
        pass

    return api_url


def process(req):
    req_data = json.loads(req)
    state = req_data['state']
    api_resp = None
    if(state == 'weather_forecast'):
        api_req = get_api_request(req_data)
        if None != api_req:
            api_resp = requests.get(api_req)
            api_resp_str = api_resp.json()

    resp = {'request':req,'weather':api_resp_str}
    resp_str = json.dumps(resp)
    return resp_str


def test_weather():
    print('loading request with coordinates of louisville ....')
    with open('testreq-latlon.json') as f:
        req_dict = json.load(f)

    req_data = json.dumps(req_dict)
    resp = process(req_data)
    print(json.dumps(json.loads(resp),indent=2))
    print('\n\n')

    print('loading request with no location data (ann arbor)  ....')
    with open('testreq-none.json') as f:
        req_dict = json.load(f)

    req_data = json.dumps(req_dict)
    resp = process(req_data)
    print(json.dumps(json.loads(resp),indent=2))
    print('\n\n')

    print('loading request with location=detroit ....')
    with open('testreq-nolatlon.json') as f:
        req_dict = json.load(f)

    req_data = json.dumps(req_dict)
    resp = process(req_data)
    print(json.dumps(json.loads(resp),indent=2))

    print('\n\ndone.')

test_weather()