import requests

import config
from WeatherNewsCollector import current_weather, forecast_weather
from FBNewsCollector import get_group_news, get_fan_news

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
    print( msg)
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
    #print( msg)
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
    # collect group pages news, and classify news in types
    group_news = get_group_news()
    # collect fan pages news, and classify news in types
    fan_news = get_fan_news()
    # merge group and fan pages news
    news = merge_dict(group_news, fan_news)
    # make report
    msg ="༺❘༻ FB page news ༺❘༻ \n\n"
    msg += config.reporter_symbols
    for type in news:
        count=1 # count of posts in a type
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
    print( msg)
    
    params = (
        ('message', msg),
        ('access_token', config.page_token),
    )
    response = requests.post(config.page_url, params=params)
    print(response)
    
def merge_dict(d1, d2):
    """
    if a key of two dict is the same, then extend the list of that key.
    """
    for k in d1.keys():
        if k in d2:
            d1[k].extend(d2[k])
    return d1
    
# Driver
report_fb_page_news()
