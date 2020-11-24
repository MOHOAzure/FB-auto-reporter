import requests

import config
from WeatherNewsCollector import current_weather, forecast_weather

def report_current_weather():
    msg="❘༻ Current Weather Report ༺❘\n\n"
    city = ['Taipei', 'Tainan']
    for c in city:
        res=current_weather(c)
        if res['code'] == 200:
            msg += (
                    "✦ "+c+" ✦\n"+
                    "Weather condition: "+ res['weather_description'] +"\n"+
                    "Temperature: " + res['temperature'] +"\n"+ 
                    "Feels like: " + res['feel_like_temperature'] +"\n"+ 
                    "Wind: "+ res['wind'] +"\n"+
                    "Humidity: " + res['humidiy'] +"\n\n\n"
                )
        else:
            msg += c+" Not Found \n\n\n"
    print( msg)
    params = (
        ('message', msg),
        ('access_token', config.page_token),
    )
    response = requests.post(config.page_url, params=params)
    print(response)
    
def report_forecast_weather():
    msg="❘༻ Weather Forecast Report ༺❘\n\n"
    city = ['Taipei', 'Tainan']
    for c in city:
        res=forecast_weather(c)
        if res['code'] == '200':
            msg += (
                    "✦ "+c+" ✦\n"+
                    "Forecast Time: "+ res['forecast_time'] +"\n"+
                    "Weather condition: "+ res['weather_description'] +"\n"+
                    "Temperature: " + res['temperature'] +"\n"+ 
                    "Feels like: " + res['feel_like_temperature'] +"\n"+ 
                    "Wind: "+ res['wind'] +"\n"+
                    "Humidity: " + res['humidiy'] +"\n\n\n"
                )
        else:
            msg += c+" Not Found \n\n\n"
    #print( msg)
    params = (
        ('message', msg),
        ('access_token', config.page_token),
    )
    response = requests.post(config.page_url, params=params)
    print(response)
    
# Driver
report_current_weather()