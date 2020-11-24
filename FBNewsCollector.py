from facebook_scraper import get_posts

import config

def get_group_news(pid):
    """
    type: pid(str): group page id
    rtype: msg(str)
    """
    msg=""
    count=1
    for post in get_posts(group=pid, pages=1):
        # print(count)
        # print(post['text'][:50])
        # print(post['time'])
        # if post['post_id']:
            # print("www.facebook.com/groups/"+pid+"/permalink/"+str(post['post_id']))
        # else:
            # print(post['post_url'])
        # print("---------------\n")
        # count +=1
        msg += (
            post['text'][:50] + "\n"+
            str(post['time']) + "\n"
        )
        if post['post_id']:
            msg += ("www.facebook.com/groups/"+pid+"/permalink/"+str(post['post_id']) + "\n")
        else:
            msg += str(post['post_id']) + "\n"
        msg += "---------------\n"            
        count +=1
    return msg

def get_fan_news(pid):
    """
    type: pid(str): fan page id
    rtype: msg(str)
    """
    msg=""
    count=1
    for post in get_posts(pid, pages=1):
        # print(count)
        # print(pid)
        # print(post['text'][:50])
        # print(post['time'])
        # if post['post_id']:
            # print("www.facebook.com/groups/"+pid+"/posts/"+str(post['post_id']))
        # else:
            # print(post['post_url'])
        # print("---------------\n")
        
        msg += (
            post['text'][:50] + "\n"+
            str(post['time']) + "\n"
        )
        if post['post_id']:
            msg += ("www.facebook.com/groups/"+pid+"/posts/"+str(post['post_id']) + "\n")
        else:
            msg += str(post['post_id']) + "\n"
        msg += "---------------\n"            
        count +=1
    return msg
