import schedule, time

from MainReporter import report_current_weather, report_forecast_weather, report_fb_page_news
import config

# set up time to report weather
schedule.every().day.at( config.report_forecast_weather_time ).do( report_forecast_weather )
for eachtime in config.report_current_weather_time:
    schedule.every().day.at(eachtime).do( report_current_weather )

# set up time to report news
for eachtime in config.report_current_weather_time:
    schedule.every().day.at(eachtime).do( report_fb_page_news )

# run scheduler
while True:
    schedule.run_pending()
    time.sleep(1)