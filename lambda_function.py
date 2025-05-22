import json

import requests

def lambda_handler(event, context):
    agent = event['agent']
    actionGroup = event['actionGroup']
    function = event['function']
    parameters = event.get('parameters', [])
    message_version = event['messageVersion']

    print(parameters)

    # Extract latitude and longitude
    lat, lon = None, None
    for param in parameters:
        if param['name'] == 'latitude':
            lat = param['value']
        elif param['name'] == 'longitude':
            lon = param['value']

    if lat is None or lon is None:
        return {
            'statusCode': 400,
            'body': json.dumps('Missing latitude or longitude')
        }

    # Call Open-Meteo API
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m"
    response = requests.get(url)
    print(response)

    if response.status_code != 200:
        return {
            'statusCode': 500,
            'body': json.dumps('Error fetching weather data')
        }

    weather_data = response.json()
    temperature = weather_data.get('current', {}).get('temperature_2m')
    print(temperature)
    if temperature is None:
        return {
            'statusCode': 500,
            'body': json.dumps('Temperature data not found')
        }

    responseBody = {
        "TEXT": {
            "body": f"The current temperature is {temperature}°C."
        }
    }

    action_response = {
        'actionGroup': actionGroup,
        'function': function,
        'functionResponse': {
            'responseBody': responseBody
        }
    }

    result = {'response': action_response, 'messageVersion': message_version}
    print("Response:", result)

    return result
