from pixivpy3 import *

import config

def get_pic():
    """
    type: None
    rtype pic(dict)
    {
        "author":str,
        "url":str,
        "total_view":str,
        "total_bookmarks": str,
        "create_date":str,
        "tags": str
    }
    """
    # report recommended pic
    api = AppPixivAPI()
    api.login(config.pixiv_account, config.pixiv_pw)
    json_result = api.illust_recommended()
    # the first recommended one
    illust = json_result.illusts[0]
    pic={
        "author":str(illust.user.name),
        "url":config.pixiv_base_url+str(illust.id),
        "total_view":str(illust.total_view),
        "total_bookmarks": str(illust.total_bookmarks),
        "create_date":str(illust.create_date),
        "tags": (', '.join( ['#'+t.name for t in illust.tags] )),
    }
    return pic

