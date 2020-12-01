"""
A script to collect pixiv pictures
"""
from pixivpy3 import *

from conf import secret, config_reporter

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
    api.login(secret.pixiv_account, secret.pixiv_pw)
    json_result = api.illust_recommended()
    # the first recommended one
    illust = json_result.illusts[0]
    pic={
        "author":str(illust.user.name),
        "url":config_reporter.base_url_pixiv+str(illust.id),
        "total_view":str(illust.total_view),
        "total_bookmarks": str(illust.total_bookmarks),
        "create_date":str(illust.create_date),
        "tags": (', '.join( ['#'+(t.name) for t in illust.tags] )),
    }
    return pic
