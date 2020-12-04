import requests, inspect

import logging, logging.config
logging.config.fileConfig('conf/logging.conf')
file_logger=logging.getLogger('fileLogger')
console_logger=logging.getLogger()
from MyLogger import file_log_helper

from conf import secret, config_reporter
from collector import FBNewsCollector, WeatherNewsCollector, PicCollector
from Messenger import send_admin_report

def report_current_weather():
    func_name = inspect.currentframe().f_code.co_name
    console_logger.debug(func_name+": working")
    msg=""
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

    msg_copy = msg # for admin
    msg = config_reporter.decorators["weather"]["current"]["report"]+"\n\n"+msg
    file_log_helper(logging.DEBUG, func_name, msg)   
    params = (
        ('message', msg),
        ('access_token', secret.page_token),
    )
    response = requests.post(secret.page_url, params=params)
    
    # log the link to the report or an error message
    # send a copy of report to page admin if everything is OK
    if response.status_code==200:
        file_log_helper(logging.INFO, func_name, response)
        msg_copy = config_reporter.decorators["weather"]["current"]["msg"]+"\n\n"+msg_copy
        send_admin_report(msg_copy)
    else:
        file_log_helper(logging.ERROR, func_name, response)
        
    console_logger.debug(func_name+": finished")
    
def report_forecast_weather():
    func_name = inspect.currentframe().f_code.co_name
    console_logger.debug(func_name+": working")
    msg=""
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
    
    msg_copy = msg # for admin
    msg = config_reporter.decorators["weather"]["forecast"]["report"]+"\n\n"+msg
    file_log_helper(logging.DEBUG, func_name, msg)
    params = (
        ('message', msg),
        ('access_token', secret.page_token),
    )
    response = requests.post(secret.page_url, params=params)
    
    # log the link to the report or an error message
    # send a copy of report to page admin if everything is OK
    if response.status_code==200:
        file_log_helper(logging.INFO, func_name, response)
        msg_copy = config_reporter.decorators["weather"]["forecast"]["msg"]+"\n\n"+msg_copy
        send_admin_report(msg_copy)
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
    msg ="\n\n"
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

    msg = config_reporter.decorators["news"]["report"]+"\n\n"+msg
    file_log_helper(logging.DEBUG, func_name, msg)
    
    params = (
        ('message', msg),
        ('access_token', secret.page_token),
    )
    response = requests.post(secret.page_url, params=params)
    
    # log a returned fb post or an error message
    # send a report containg the post url to page admin if everything is OK
    if response.status_code==200:
        file_log_helper(logging.INFO, func_name, response)
        
        # if fb api returns id, it means there is a post and it is formatted as "pageid_postid"
        composite_id=response.json()["id"]
        pid = composite_id.split('_')
        page_id = pid[0]
        post_id = pid[1]
        url = "www.facebook.com/"+page_id+"/posts/"+post_id
        msg = config_reporter.decorators["news"]["msg"]+"\n\n"+url
        send_admin_report(msg)
    else:
        file_log_helper(logging.ERROR, func_name, response)
        
    console_logger.debug(func_name+": finished")

def report_pic():
    func_name = inspect.currentframe().f_code.co_name
    console_logger.debug(func_name+": working")
    msg=""
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
    msg_copy = msg # for admin
    msg = config_reporter.decorators["pic"]["report"]+"\n\n"+msg
    file_log_helper(logging.DEBUG, func_name, msg)
    params = (
        ('message', msg),
        ('link', url),
        ('access_token', secret.page_token),
    )
    response = requests.post(secret.page_url, params=params)
    
    # log a returned fb post or an error message
    # send a copy of report to page admin if everything is OK
    if response.status_code==200:
        file_log_helper(logging.INFO, func_name, response)
        msg_copy = config_reporter.decorators["pic"]["msg"]+"\n\n"+msg_copy
        send_admin_report(msg_copy)
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