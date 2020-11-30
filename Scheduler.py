import schedule, time

import logging, logging.config
logging.config.fileConfig('logging.conf')
console_logger=logging.getLogger()

from MainReporter import report_current_weather, report_forecast_weather, report_fb_page_news, report_pic
import config

def run():
    # set up time to report weather
    schedule.every().day.at( config.report_forecast_weather_time ).do( report_forecast_weather )
    for eachtime in config.report_current_weather_time:
        schedule.every().day.at(eachtime).do( report_current_weather )

    # set up time to report news
    for eachtime in config.report_fb_page_news_time:
        schedule.every().day.at(eachtime).do( report_fb_page_news )

    # set up time to report pictures
    schedule.every().minute.do( report_pic )

    # run scheduler
    console_logger.info("Tasks are scheduled")
    while True:
        schedule.run_pending()
        time.sleep(1)