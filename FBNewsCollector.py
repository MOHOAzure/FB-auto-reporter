from facebook_scraper import get_posts

import config

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
    
    for type in config.group_page_urls.keys():
        if type not in group_news:
            group_news[type]=[]
        for pid in config.group_page_urls[type]:
            for post in get_posts(group=pid, pages=1):
                a_post = {}
                a_post['time']=str(post['time'])
                a_post['text']=post['text'][:50]
                a_post['url']=""
                if post['post_id']:
                    a_post['url']= "www.facebook.com/groups/"+pid+"/permalink/"+str(post['post_id'])
                else:
                    a_post['url']= post['post_url']
                # ignore the news has no link
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
    for type in config.fan_page_urls.keys():
        if type not in fan_news:
            fan_news[type]=[]
        for pid in config.fan_page_urls[type]:
            for post in get_posts(group=pid, pages=1):
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
