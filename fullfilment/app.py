from flask import Flask, Response, request,session
from datetime import date
import json
import os
import requests
# from data_util import Hawker
from googlesearch import search
from util import *

app = Flask(__name__)
app.secret_key = os.urandom(12)
app.config['SESSION_TYPE'] = 'filesystem'
session={'hawkercentre':'','places':[]}

def getWeatherIntentHandler(cityName,when):
    r=requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={cityName}&APPID=817a02b6bfa5ff220f322512de9e995e").text
    resp=json.loads(r)
    return f"The weather in {cityName} {when} is {resp['weather'][0]['description']}"

@app.after_request
def after(response):
    # todo with response
    print(response.status)
    print(response.headers)
    print(response.get_data())
    # print(session['city'])
    return response

@app.route("/", methods = ["POST"])
def main():
    searchurl = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
    detailsapi='https://maps.googleapis.com/maps/api/place/details/json?placeid='
    api_key="AIzaSyAdgXfoqQEivZTjt4lWw3BIebCHxStm2Fk"

    req = request.get_json(silent=True, force=True)
    intent_name = req["queryResult"]["intent"]["displayName"]
    print(req)
    if intent_name == "getWeather":
        cityName = req["queryResult"]["parameters"]["City"]
        when=req["queryResult"]["parameters"]["date"] or date.today()
        # session['city']=cityName
        # session['when']=when  
        resp_text = getWeatherIntentHandler(cityName,when)
    elif intent_name == "get_near":
        resp={"fulfillmentText":"Please tell us your current location"}
    elif intent_name == "get_near - fallback":
        location=req["queryResult"]['queryText']
        r = requests.get(searchurl + 'query=' + location + ' hawker centres'
                        '&key=' + api_key) 
        HCs=r.json()['results'][:5]
        for hc in HCs:
            session['places'].append({'placeid':hc['place_id'],'name':hc['name']})       
        resp={"fulfillmentText":'**'.join([hc['name'] for hc in HCs])}   
        # resp = {        
        #     "fulfillmentText":{
        #         "speech":"test",
        #         "messages":[{"type":"suggestion_chips","platform":"google","suggestions":[{"title":"yes"},{"title":"no"}]}]
        #     }
        # }
    elif intent_name == "request_permission":
        resp = {        
        "payload":{"google":{"expectUserResponse":True,"systemIntent":""}}
        }
        resp["payload"]["google"]["systemIntent"] = {
                "intent": "actions.intent.PERMISSION",
                "data": {
                    "@type": "type.googleapis.com/google.actions.v2.PermissionValueSpec",
                    "optContext": 'test',
                    "permissions": ['DEVICE_PRECISE_LOCATION']
                }
        }
    elif intent_name == "action_intent_PERMISSION":  
        print(req) 
    elif intent_name == "get_near - fallback - fallback":
        session['hawkercentre']=req["queryResult"]['queryText']        
        resp={"fulfillmentText":'would you like to order?'}  
    elif intent_name == "get_near - fallback - fallback - yes":
        # r = requests.get(detailsapi + 
        #     [place['placeid'] for place in session['places'] if place['name']==session['hawkercentre']][0] 
        #     +'&key=' + api_key) 
        for r in search('foodpanda '+ session['hawkercentre'], num=1, stop=1, pause=2):                
            deliveryurl=r   
        # print(r.json())                           
        resp={"fulfillmentText":deliveryurl} 
    elif intent_name == "get_hawker_details":
        # hawker_name=""
        # parameter_key=[]  
        # hawker_name= req["queryResult"]["parameters"]["hawkerName"]
        # parameter= req["queryResult"]["parameters"]
        # for para in parameter:
        #     if parameter[para]:
        #         i=0
        #         parameter_key.insert(i,para)
        #         i+=1
        # resp_text = getHawkerIntentHandler(hawker_name,parameter_key)        
        resp={"fulfillmentText":'test'}  
    elif intent_name == "get_near - fallback - custom":
        resp={"fulfillmentText":'hawker details selected'} 
    return Response(json.dumps(resp), status=200, content_type="application/json")

# def getHawkerIntentHandler(hawker_name, key):
#     intent=""
#     haw = Hawker()
#     for keys in key:
#         if keys=='address':
#             intent ="ADDRESS_MYENV"
#             hawker_details=haw.read_hawker_info(hawker_name,intent)
#             print (hawker_details)
#             return f"address of {hawker_name} is {hawker_details}"
#         if keys=='stalls':
#             intent='NO_OF_FOOD_STALLS'
#             hawker_details=haw.read_hawker_info(hawker_name,intent)
#             return f"there are {hawker_details} food stalls in {hawker_name}"
#         if keys=='ratings':
#             intent='ratings'
#             hawker_details=haw.read_hawker_info(hawker_name,intent)
#             return f"{hawker_name} have {hawker_details} ratings out of 5"
#         if keys=='description' or key=='info' or key=='information':
#             intent='DESCRIPTION_MYENV'
#             hawker_details=haw.read_hawker_info(hawker_name,intent)
#             return f"{hawker_details}"

app.run(host='0.0.0.0', port=8000, debug=True)