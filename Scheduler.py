import schedule, time, datetime

import logging, logging.config
logging.config.fileConfig('logging.conf')
console_logger=logging.getLogger()

from MainReporter import report_current_weather, report_forecast_weather, report_fb_page_news, report_pic
import config, config_schedule

def convert_time(tz, the_time):
    """
    type:
        tz: the specified time zone of schedule
        the_time: the scheduled time (HH:MM)
    
    rtype:
        the_time: the scheduled time (HH:MM) based on the specified tz regardless of server's time zone
    """
    machine_tz_sec= (time.localtime().tm_gmtoff) # get the time zone of machine, tm_gmtoff returns east of UTC in seconds
    delta_zone = tz[0]
    delta_hour = int(tz[1:3])
    delta_minute = int(tz[3:])
    delta_sec = (delta_hour*3600)+(delta_minute*60)
    the_time = datetime.datetime.strptime(the_time, "%H:%M")
    delta = datetime.timedelta(seconds= delta_sec-machine_tz_sec)

    if delta_zone == "+":
        the_time -= delta
    elif delta_zone == "-":
        the_time += delta
        
    return the_time.strftime("%H:%M")
    
def run():
    # set up time to report weather
    report_forecast_weather_time = convert_time(config_schedule.tz, config_schedule.report_forecast_weather_time)
    schedule.every().day.at( report_forecast_weather_time ).do( report_forecast_weather )
    for eachtime in config_schedule.report_current_weather_time:
        eachtime=convert_time(config_schedule.tz, eachtime)
        schedule.every().day.at(eachtime).do( report_current_weather )

    # set up time to report news
    for eachtime in config_schedule.report_fb_page_news_time:
        eachtime=convert_time(config_schedule.tz, eachtime)
        schedule.every().day.at(eachtime).do( report_fb_page_news )

    # set up time to report pictures
    schedule.every().hour.do( report_pic )

    # run scheduler
    console_logger.info("Tasks are scheduled")
    while True:
        schedule.run_pending()
        time.sleep(1)
        