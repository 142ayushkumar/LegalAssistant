import requests
import json

api_key = '770bdff2a1fd42078b79ee0381542aa6'

def corrected_text(example_text = 'hy buddi, i am doin am zing. hw ar you?'):
    '''
        Pass this function a string and it will give the spell correct output
        string as its output using bing spell check api.
    '''
    # Calling the bing spell check api
    endpoint = 'https://api.cognitive.microsoft.com/bing/v7.0/spellcheck'

    data = {'text': example_text}
    params = {
        'mkt':'en-us',
        'mode':'proof'
        }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Ocp-Apim-Subscription-Key': api_key,
        }

    response = requests.post(endpoint, headers=headers, params=params, data=data)
    json_response = json.dumps(response.json(), indent=2)
    # Bing spell check api ends here, we get json response of the flagged tokens

    dict_response = json.loads(json_response)
    flagged_tokens = dict_response['flaggedTokens']
    corrected = ''
    i = 0
    # move through all the flaggedTokens and make the correct string
    for flagged in flagged_tokens:
        offset = flagged['offset']
        token = flagged['token']
        suggestion = flagged['suggestions'][0]['suggestion']
        corrected = corrected + example_text[i:offset] + suggestion
        i = offset + len(token)
    corrected = corrected + example_text[i:len(example_text)]

    return corrected
