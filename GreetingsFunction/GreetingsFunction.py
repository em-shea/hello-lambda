import datetime
import json
import boto3
import os
from random import randint
from botocore.vendored import requests

lambda_client = boto3.client('lambda')

def get_weather(location):
    """Calls Open Weather Map API for weather conditions"""
    response = requests.get('https://api.openweathermap.org/data/2.5/weather?q=' + location + '&appid=' + os.environ['WEATHER_API_KEY'] + '&units=imperial')
    weather_data = response.json()
    current_weather = weather_data["weather"][0]["main"]
    current_weather_icon = weather_data["weather"][0]["icon"]
    current_temp = weather_data["main"]["temp"]
    current_location = weather_data["name"]

    condensed_weather_list = {
        'weather': current_weather,
        'temp': current_temp,
        'image': "https://openweathermap.org/img/w/" + current_weather_icon+ ".png",
        'location_name': current_location,
    }
    return condensed_weather_list

def lambda_handler(event, context):
    invoke_response = lambda_client.invoke(
        FunctionName="RandomEntrySelector",
        InvocationType='RequestResponse',
        Payload=json.dumps({"file":
            os.environ['greetings-list']
        })
    )
    response_json = invoke_response['Payload'].read()
    response_python = json.loads(response_json)
    word = response_python["body"]

    invoke_response_color = lambda_client.invoke(
        FunctionName="RandomEntrySelector",
        InvocationType='RequestResponse',
        Payload=json.dumps({"file":
            os.environ['colors-list']
        })
    )
    response_json_color = invoke_response_color['Payload'].read()
    response_python_color = json.loads(response_json_color)
    word_color = response_python_color["body"]

    if event["queryStringParameters"] != None and "l" in event["queryStringParameters"]:
        location = event["queryStringParameters"]["l"]
    else:
        location = "Seattle"
    weather_data = get_weather(location)

    return {
        'statusCode': 200,
        'headers': {
            'content-type': 'text/html; charset=utf-8'
        },
       'body': f"""
<html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{
                font-family: 'Verdana', sans-serif;
            }}
            h1 {{
                color: {word_color};
            }}
            p {{
                color: #C0C0C0;
                font-style: italic;
            }}
        </style>
    </head>
    <body>
        <h1>{word}</h1>
        <p>Generated at: {(datetime.datetime.now()-datetime.timedelta(hours=7)).replace(microsecond=0).isoformat(' ')} PST</p>
        <p>Weather today: {weather_data["weather"]}, {weather_data["temp"]}°F in {weather_data["location_name"]}</p>
        <img src="{weather_data["image"]}">
    </body>
</html>
"""
    }
