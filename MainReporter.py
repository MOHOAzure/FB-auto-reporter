import requests, inspect

import logging, logging.config
logging.config.fileConfig('conf/logging.conf')
file_logger=logging.getLogger('fileLogger')
console_logger=logging.getLogger()

from conf import secret, config_reporter
from collector import FBNewsCollector, WeatherNewsCollector, PicCollector
# from WeatherNewsCollector import current_weather, forecast_weather
# from FBNewsCollector import get_news
# from PicCollector import get_pic
from MyLogger import file_log_helper

def report_current_weather():
    func_name = inspect.currentframe().f_code.co_name
    console_logger.debug(func_name+": working")
    msg="༺❘༻ Current Weather Report ༺❘༻ \n\n"
    city = config_reporter.city
    for c in city:
        res= WeatherNewsCollector.current_weather(c)
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
         
    file_log_helper(logging.DEBUG, func_name, msg)   
    params = (
        ('message', msg),
        ('access_token', secret.page_token),
    )
    response = requests.post(secret.page_url, params=params)
    
    # log a returned fb post or error message
    if response.status_code==200:
        file_log_helper(logging.INFO, func_name, response)
    else:
        file_log_helper(logging.ERROR, func_name, response)
        
    console_logger.debug(func_name+": finished")
    
def report_forecast_weather():
    func_name = inspect.currentframe().f_code.co_name
    console_logger.debug(func_name+": working")
    msg="༺❘༻ Weather Forecast Report ༺❘༻ \n\n"
    city = config_reporter.city
    for c in city:
        res=WeatherNewsCollector.forecast_weather(c)
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
    file_log_helper(logging.DEBUG, func_name, msg)
    params = (
        ('message', msg),
        ('access_token', secret.page_token),
    )
    response = requests.post(secret.page_url, params=params)
    
    # log a returned fb post or error message
    if response.status_code==200:
        file_log_helper(logging.INFO, func_name, response)
    else:
        file_log_helper(logging.ERROR, func_name, response)
        
    console_logger.debug(func_name+": finished")

def report_fb_page_news():
    func_name = inspect.currentframe().f_code.co_name
    console_logger.debug(func_name+": working")
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
    news = FBNewsCollector.get_news()
    msg ="༺❘༻ FB page news ༺❘༻ \n\n"
    msg += config_reporter.reporter_symbols
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
    file_log_helper(logging.DEBUG, func_name, msg)
    
    params = (
        ('message', msg),
        ('access_token', secret.page_token),
    )
    response = requests.post(secret.page_url, params=params)
    # log a returned fb post or error message
    if response.status_code==200:
        file_log_helper(logging.INFO, func_name, response)
    else:
        file_log_helper(logging.ERROR, func_name, response)
        
    console_logger.debug(func_name+": finished")

def report_pic():
    func_name = inspect.currentframe().f_code.co_name
    console_logger.debug(func_name+": working")
    msg="༺❘༻Pixiv Recommendation ༺❘༻ \n\n"
    pic= PicCollector.get_pic()    
    author=pic["author"]
    url=pic["url"]
    view=pic["total_view"]
    bookmarks=pic["total_bookmarks"]
    date=pic["create_date"]
    tags=pic["tags"]
    msg += (
        "Author: "+author+"\n"+
        "Url: "+url+"\n"+
        "Create_date: "+date+"\n"+
        "Total_view: "+view+"\n"+
        "Total_bookmarks: "+bookmarks+"\n"+
        "Tags: "+tags+"\n"
    )
    file_log_helper(logging.DEBUG, func_name, msg)
    params = (
        ('message', msg),
        ('link', url),
        ('access_token', secret.page_token),
    )
    response = requests.post(secret.page_url, params=params)
    
    # log a returned fb post or error message
    if response.status_code==200:
        file_log_helper(logging.INFO, func_name, response)
    else:
        file_log_helper(logging.ERROR, func_name, response)
        
    console_logger.debug(func_name+": finished")

"""
Quick test
"""
# report_current_weather()
# report_forecast_weather()
# report_fb_page_news()
# report_pic()