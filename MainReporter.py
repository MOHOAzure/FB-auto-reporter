import requests

import config
from WeatherNewsCollector import current_weather, forecast_weather
from FBNewsCollector import get_news

def report_current_weather():
    msg="❘༻ Current Weather Report ༺❘\n\n"
    city = config.city
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
    # print(msg)
    params = (
        ('message', msg),
        ('access_token', config.page_token),
    )
    response = requests.post(config.page_url, params=params)
    print(response)
    
def report_forecast_weather():
    msg="❘༻ Weather Forecast Report ༺❘\n\n"
    city = config.city
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
    # print(msg)
    params = (
        ('message', msg),
        ('access_token', config.page_token),
    )
    response = requests.post(config.page_url, params=params)
    print(response)

def report_fb_page_news():
    """ report format
        ❘༻ FB page news ༺❘
        ✦ type 1 ✦
        type #count
        time
        text
        url
        
        type #count
        time
        text
        url
        
        ✦ type 2 ✦
        ...
    """
    # get news and then make a report
    news = get_news()
    msg ="༺❘༻ FB page news ༺❘༻ \n\n"
    msg += config.reporter_symbols
    for type in news:
        count=1 # count of news in a type
        msg += "§  "+type+" §\n"
        for post in news[type]:
            msg += (
                    "✦ "+type+" #"+str(count)+"\n"+
                    post['time']+"\n"+
                    post['text']+"\n"+
                    post['url']+"\n\n"
            )
            count+=1
        msg += "\n\n"
    # print(msg)
    
    params = (
        ('message', msg),
        ('access_token', config.page_token),
    )
    response = requests.post(config.page_url, params=params)
    print(response)
    