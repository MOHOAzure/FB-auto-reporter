"""
A script to collect weather of a specified city using openweathermap api 
"""
import requests, json 
from datetime import datetime
  
from conf import secret, config_reporter

def forecast_weather(city_name):
    """
    Report tomorrow's 0700 weather
    This function should be called at 2200
    
    type: city_name: str
    rtype: weather: dict
        {
            code: (openweathermap response code),
            forecast_time: local date time
            weather_description: str,
            temperature: str,
            feel_like_temperature: str,
            wind: str,
            humidiy: str
        }
    
    check response format: https://openweathermap.org/forecast5#JSON    
    """
    # API url
    base_url = config_reporter.base_url_openweathermap
    complete_url = base_url + "appid=" + secret.api_key + "&q=" + city_name 
      
    # get method of requests module 
    # return response object 
    response = requests.get(complete_url) 
      
    # json method of response object  
    # convert json format data into 
    # python format data 
    res = response.json() 

    # Now res contains list of nested dictionaries 
    # Check the value of "cod" key is equal to 
    # "200", means city is found
    if res["cod"] == "200":     
        # extract 'tomorrow' weather
        # since api returns 3-hour forecast data within 5 days
        # offset=0: 3 hours later
        # offset=2: 9 hours later
        offset=2
        weather_description = res["list"][offset]["weather"][0]["description"]
        
        timestamp = res["list"][offset]["dt"]
        forecast_time = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S") # to local time
        
        temperature = res["list"][offset]["main"]["temp"] - 273.15 
        feel_like_temperature = res["list"][offset]["main"]["feels_like"] - 273.15   
        # round to 2 decimals
        temperature = round(temperature, 2)
        feel_like_temperature = round(feel_like_temperature, 2)
        
        wind = res["list"][offset]["wind"]['speed']
        # round to 2 decimals
        wind = round(wind, 2)
        
        humidiy = res["list"][offset]["main"]["humidity"] 
        
        # response dict
        res_dic = {
            "code": res["cod"],
            "forecast_time": str(forecast_time),
            "weather_description": str(weather_description),
            "temperature": str(temperature) +"°C",
            "feel_like_temperature": str(feel_like_temperature) +"°C",
            "wind": str(wind) +" m/s",
            "humidiy": str(humidiy) +"%"
        }
        return res_dic
    else:
        res_dic = {"code": res["cod"],}
        return res_dic
        

def current_weather(city_name):
    """
    Report current weather
    This function should be called at 0700, 1200, 1800
    
    type: city_name: str
    rtype: weather: dict
        {
            code: (openweathermap response code),
            weather_description: str,
            temperature: str,
            feel_like_temperature: str,
            wind: str,
            humidiy: str
        }
    
    check response format: https://openweathermap.org/current  
    """
    # API url
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + secret.api_key + "&q=" + city_name 
      
    # get method of requests module 
    # return response object 
    response = requests.get(complete_url) 
      
    # json method of response object  
    # convert json format data into 
    # python format data 
    res = response.json()
      
    # Now res contains list of nested dictionaries 
    # Check the value of "cod" key is equal to 
    # int 200, means city is found
    if res["cod"] == 200: 
        weather_description = res["weather"][0]["description"] 
        
        temperature = res["main"]["temp"] - 273.15 
        feel_like_temperature = res["main"]["feels_like"] - 273.15     
        # round to 2 decimals
        temperature = round(temperature, 2)
        feel_like_temperature = round(feel_like_temperature, 2)
        
        wind = res["wind"]['speed']
        # round to 2 decimals
        wind = round(wind, 2)
        
        humidiy = res["main"]["humidity"] 
                
        # response dict
        res_dic = {
            "code": res["cod"],
            "weather_description": str(weather_description),
            "temperature": str(temperature) +"°C",
            "feel_like_temperature": str(feel_like_temperature) +"°C",
            "wind": str(wind) +" m/s",
            "humidiy": str(humidiy) +"%"
        }
        return res_dic
    else: 
        res_dic = {"code": res["cod"],}
        return res_dic
        