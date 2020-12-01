"""
A script to collect news of fb fan pages and group pages
"""
import time, datetime

from facebook_scraper import get_posts
from conf import secret, config_reporter, config_schedule

def merge_dict(d1, d2):
    """
    if a key of two dict is the same, then extend the list of that key.
    """
    for k in d1.keys():
        if k in d2:
            d1[k].extend(d2[k])
    return d1

def get_today_of_tz():
    """
    rtype:(datetime object)
        the date converted to the specified time zone where users resident
    """
    today = datetime.datetime.today() # today of machine
    tz = config_schedule.tz # the specified time zone
    machine_tz_sec= (time.localtime().tm_gmtoff) # the time zone of machine, tm_gmtoff returns east of UTC in seconds
    delta_zone = tz[0]
    delta_hour = int(tz[1:3])
    delta_minute = int(tz[3:])
    delta_sec = (delta_hour*3600)+(delta_minute*60)
    delta = datetime.timedelta(seconds= delta_sec-machine_tz_sec)
    
    # today of the specified time zone
    if delta_zone == "+":
        today -= delta
    elif delta_zone == "-":
        today += delta
        
    return today
    
def get_news():
    # collect group pages news, and classify news in types
    group_news = get_group_news()
    # collect fan pages news, and classify news in types
    fan_news = get_fan_news()
    # merge group and fan pages news
    news = merge_dict(group_news, fan_news)
    return news
    
def get_group_news():
    """
    type: None
    rtype: group_news(dict)
    {
        "type":[
            {
                "time":str,
                "text":str,
                "url":str,
            },
        ],
    }
    """
    group_news={}
    
    for type in config_reporter.group_page_urls.keys():
        if type not in group_news:
            group_news[type]=[]
        for pid in config_reporter.group_page_urls[type]:
            for post in get_posts(group=pid, pages=1):
                if get_today_of_tz().date() == post['time'].date():
                    a_post = {}
                    a_post['time']=str(post['time'])
                    a_post['text']=post['text'][:50]
                    a_post['url']=""
                    if post['post_id']:
                        a_post['url']= "www.facebook.com/groups/"+pid+"/permalink/"+str(post['post_id'])
                    else:
                        a_post['url']= post['post_url']
                    # ignore the news has no link to any fb pages or shared content
                    if a_post['url']:
                        group_news[type].append(a_post)
    return group_news

def get_fan_news():
    """
    type: None
    rtype: fan_news(dict)
    {
        "type":[
            {
                "time":str,
                "text":str,
                "url":str,
            },
        ],
    }
    """    
    fan_news={}    
    for type in config_reporter.fan_page_urls.keys():
        if type not in fan_news:
            fan_news[type]=[]
        for pid in config_reporter.fan_page_urls[type]:
            for post in get_posts(group=pid, pages=1):
                if get_today_of_tz().date() == post['time'].date():
                    a_post = {}
                    a_post['time']=str(post['time'])
                    a_post['text']=post['text'][:50]
                    a_post['url']=""
                    if post['post_id']:
                        a_post['url']= "www.facebook.com/"+pid+"/posts/"+str(post['post_id'])
                    else:
                        a_post['url']= post['post_url']
                    # ignore the news has no link
                    if a_post['url']:
                        fan_news[type].append(a_post)
    return fan_news