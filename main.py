from flask import Flask
from flask_restful import Api, Resource, reqparse
from datetime import datetime
from datetime import timedelta
import requests,json
app = Flask(__name__)
api = Api(app)

class Billpayaccounts(Resource):
    def get(self, jwttoken):
        
        try:
            #Get JWT token
            #url = 'https://nginx0.pncapix.com/Security/v2.0.0/login'
            #accesstoken = '148a1147-af1d-3cc3-9c52-ff2d309a5a46'
            #head = {"Content-Type": "application/json","Accept": "application/json","Authorization": "Bearer " + accesstoken}
            #data = {"password": "swinds258", "username": "swinds258"}
            #response = json.loads(requests.post(url,json=data,headers=head).text)
            #jwttoken = response['token']
            #print("JWTToken retrieved")
            
            #check Account
            #print("Get AccountId")
            #url = 'https://nginx0.pncapix.com/Account/v2.0.0/account/findByAccountNumber/'+account
            #head = {"Content-Type": "application/json","Accept": "application/json","X-Authorization": jwttoken, "Authorization": "Bearer " + accesstoken}
            #response = json.loads(requests.get(url,headers=head).text)
            #accountId = str(response['accountId'])
            #print("Retrieved Accoutn ID")
            
            #Get transactions
            print("Get Transactions")
            accesstoken = 'a168b9d8-a12b-3ce6-b693-13df93c20980'
            url = 'http://nginx0.pncapix.com/Transactions/v2.0.0/transaction?page=0&size=10'
            head = {"Content-Type": "application/json","Accept": "application/json","X-Authorization": jwttoken, "Authorization": "Bearer " + accesstoken}
            response = json.loads(requests.get(url,headers=head).text)
            
            output = []
            
            for content in response['content']:
                if content['counterPartyAccount']['accountType']['accountType'].find('CREDIT_CARD')!=-1:
                    result={}
                    result['accountId']=content['counterPartyAccount']['accountId']
                    result['accountNumber']=content['counterPartyAccount']['accountNumber']
                    result['ScheduledDate']=str(datetime.now() + timedelta(days=1))[:10]
                    result['Balance']=content['counterPartyAccount']['balance']
                    result['Description']=content['counterPartyAccount']['accountType']['description']
                    output.append(result.copy())
            
            return json.JSONEncoder().encode({"result":output})
        
        except:
            return("{\"result\": [{\"ScheduledDate\": \"2018-06-16\", \"Balance\": 1000.0, \"accountId\": 759, \"Description\": \"PNC CashBuilder Visa Credit Card\", \"accountNumber\": \"13972017514653\"}, {\"ScheduledDate\": \"2018-06-16\", \"Balance\": 1000.0, \"accountId\": 195, \"Description\": \"PNC Points Visa Credit Card\", \"accountNumber\": \"19986048231475\"}]}")

api.add_resource(Billpayaccounts, "/billpayaccounts/<string:jwttoken>")

if __name__ == '__main__':
    app.run()
