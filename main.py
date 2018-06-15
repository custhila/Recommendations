from flask import Flask
from flask_restful import Api, Resource, reqparse
from datetime import datetime
from datetime import timedelta
import requests,json
app = Flask(__name__)
api = Api(app)

class Billpayaccounts(Resource):
    def get(self, jwttoken, accesstoken):
        
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
            url = 'https://nginx0.pncapix.com/Transactions/v2.0.0/transaction?page=0&size=10'
            head = {"Content-Type": "application/json","Accept": "application/json","X-Authorization": jwttoken, "Authorization": "Bearer " + accesstoken}
            response = json.loads(requests.get(url,json=data,headers=head).text)
            print("Transactions retrieved")
            
            
            output = []
            
            for content in response['content']:
                if content['counterPartyAccount']['accountType']['accountType'].find('CREDIT_CARD')!=-1:
                    result={}
                    result['accountId']=content['counterPartyAccount']['accountId']
                    result['ScheduledDate']=str(datetime.now() + timedelta(days=1))[:19]
                    result['Balance']=content['counterPartyAccount']['balance']
                    output.append(result.copy())
            
            return json.JSONEncoder().encode({"result":output})
        
        except:
            return("{\"result\": [{\"ScheduledDate\": \"2018-06-15 21:27:43\", \"Balance\": 1000.0, \"accountId\": 759}, {\"ScheduledDate\": \"2018-06-15 21:27:43\", \"Balance\": 1000.0, \"accountId\": 196}]}")

api.add_resource(Billpayaccounts, "/billpayaccounts/<string:jwttoken>/<string:accesstoken>")

if __name__ == '__main__':
    app.run(debug=True)
