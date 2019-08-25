from flask import Flask, Response, request,session
from datetime import date
import json
import os
import requests
from data_util import Hawker
from googlesearch import search

app = Flask(__name__)
app.secret_key = os.urandom(12)
app.config['SESSION_TYPE'] = 'filesystem'
session={'hawkercentre':'','places':[],'parameter':''}

# @app.after_request
# def after(response):
#     # todo with response
#     print(response.status)
#     print(response.headers)
#     print(response.get_data())
#     # print(session['city'])
#     return response

@app.route("/", methods = ["POST"])
def main():
    searchurl = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
    detailsapi='https://maps.googleapis.com/maps/api/place/details/json?placeid='
    api_key="AIzaSyAdgXfoqQEivZTjt4lWw3BIebCHxStm2Fk"

    req = request.get_json(silent=True, force=True)
    intent_name = req["queryResult"]["intent"]["displayName"]
    haw=Hawker()
    if intent_name == "get_near":
        resp={"fulfillmentText":"Please tell us your current location"}
    elif intent_name == "get_near - fallback":
        location=req["queryResult"]['queryText']
        # r = requests.get(searchurl + 'query=' + location + ' hawker centres'
        #                 '&key=' + api_key) 
        # HCs=r.json()['results'][:5]
        # HCs=[hc['name'] for hc in HCs]
        # /for hc in HCs:
            # session['places'].append({'placeid':hc['place_id'],'name':hc['name']}) 
        hawker_centres=haw.getHawkersbyLocation(location)  
        # print(hawker_centre_actuals) 
        if(len(hawker_centres)>0):
            resp_text='**'+'**'.join([hc for hc in hawker_centres])
        else:
            resp_text='No hawker centre found nearby'    
        resp={"fulfillmentText":resp_text}      
    elif intent_name == "get_near - fallback - custom-2":
        session['hawkercentre']=req["queryResult"]['queryText']        
        resp={"fulfillmentText":'would you like to order?'}  
    elif intent_name == "get_near - fallback - custom-2 - yes":
        for r in search('foodpanda '+ session['hawkercentre'], num=1, stop=1, pause=0):                
            deliveryurl=r                             
        resp={"fulfillmentText":deliveryurl} 
    elif intent_name == "get_hawker_details":
        hawker_name= req["queryResult"]["parameters"]["hawkerName"]        
        session['parameter']= req["queryResult"]["parameters"] 
        if(hawker_name==''):
            print(session['hawkercentre']) 
            resp_text = getHawkerIntentHandler(haw,session['hawkercentre'],session['parameter'])
        else:    
            actual_name=haw.getHawkersbyLocation(hawker_name)
            if(len(actual_name)!=0):
                actual_name=actual_name[0]
                session['hawkercentre']=actual_name
                resp_text=f"did you mean {actual_name} ?" 
            else:
                resp_text='Hawker centre not found'  
                  
        resp={"fulfillmentText":resp_text}  
    elif intent_name=="get_hawker_details - yes":
        resp_text = getHawkerIntentHandler(haw,session['hawkercentre'],session['parameter'])
        resp={"fulfillmentText":resp_text} 
    elif intent_name == "get_near - fallback - custom":
        resp={"fulfillmentText":'hawker details selected'} 
    elif intent_name == "find_hawker_centres":
        resp_text="you could try "+ haw.searchHawker(req["queryResult"]['queryText'])['name']  
        resp={"fulfillmentText":resp_text}  
    return Response(json.dumps(resp), status=200, content_type="application/json")

def getHawkerIntentHandler(haw,hawker_name, parameters):
    print(parameters)
    desc= parameters["description"]
    not_found='Could not find what you are looking for'
    if(desc):
        resp_text= haw.getHawkerDetailsFromDescription(hawker_name,desc)
        if(resp_text!=-1):
            return resp_text
        else:
            return not_found
    else:
        for key,value in parameters.items():
            if(value):
                if key=='address':
                    intent ="ADDRESS_MYENV"
                    hawker_details=haw.getHawkerDetails(hawker_name ,intent)
                    if(hawker_details!=-1):
                        return f"address of {hawker_name} is {hawker_details}."
                    else:
                        return not_found
                elif key=='stalls':
                    intent='NO_OF_FOOD_STALLS'
                    hawker_details=haw.getHawkerDetails(hawker_name,intent)
                    if(hawker_details!=-1):
                        return f"there are {hawker_details} food stalls in {hawker_name}."
                    else:
                        return not_found
                elif key=='ratings':
                    intent='ratings'
                    hawker_details=haw.getHawkerDetails(hawker_name,intent)
                    if(hawker_details!=-1):
                        return f"{hawker_name} have {hawker_details} ratings out of 5."
                    else:
                        return not_found

app.run(host='0.0.0.0', port=8000, debug=True)