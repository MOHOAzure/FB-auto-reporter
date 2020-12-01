import logging, logging.config
logging.config.fileConfig('conf/logging.conf')
file_logger=logging.getLogger('fileLogger')

def file_log_helper(level, func_name, response):
    if level == logging.INFO:
        # fb returns "pageid_postid"
        composite_id=response.json()["id"]
        pid = composite_id.split('_')
        page_id = pid[0]
        post_id = pid[1]
        url = "www.facebook.com/"+page_id+"/posts/"+post_id        
        file_logger.info(func_name +"\nUrl: "+url)
    elif level == logging.ERROR:
        file_logger.error(func_name +"\nHTTP Code: "+str(response.status_code)+"\n"+response.text)
    elif level == logging.DEBUG:
        file_logger.debug(func_name +"\nContent: "+response)