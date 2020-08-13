

from flask import Flask
from flask import request
import requests
from flask import jsonify

from flask_cors import CORS, cross_origin

import os
import json
from ast import literal_eval
import traceback

from user_auth import registrationauth

application = Flask(__name__)
cors = CORS(application, resources = {
                            r"/*":{
                                "origins" : "*"
                                }
                            }
           )


# тестовый вывод
@application.route("/")  
def hello():
    resp = {'message':"Hello World!"}
    
    response = jsonify(resp)
    response.headers.add('Access-Control-Allow-Origin', '*')
    
    return response

# регистрация пользователя
# проверяем что пользователя нет, далее регистрируем
# input
#{"email":"test@mail.ru","expiresIn":"3600","idToken":"abc","kind":"aabbcc","localId":"qwe","refreshToken":"qazwsx"}
#{"email":"test@mail.ru","password":"qwer"}
# output
#{"message":"ok"} - "ok" , "user exist" , error text
@application.route("/registration" , methods=['GET', 'POST'])  
def registration():
    resp = {'message':'ok'}
    status = 200
    try:
        getData = request.get_data()
        print(getData)
        json_params = json.loads(getData) 
        print(json_params)

        #регистрация пользователя
        resp = registrationauth.reg_new_user(resp,json_params)


        
    except Exception as e: 
        print(e)
        status = 400
        resp['message'] = e
      
    response = jsonify(resp)
    response.headers.add('Access-Control-Allow-Origin', '*')
    
    return response

# авторизация пользователя
# проверяем что пользователя нет, далее регистрируем
# input
#{"displayName" :"",  "email":"test@mail.ru","expiresIn":"3600","idToken":"abc","kind":"aabbcc","localId":"qwe","refreshToken":"qazwsx", "registered":True}
#{"email":"test@mail.ru","password":"qwer"}
# output
#{"message":"ok"} - "ok" , "incorrect {}" 
@application.route("/authorization" , methods=['GET', 'POST'])  
def authorization():
    resp = {'message':'ok'}
    status = 200
    try:
        getData = request.get_data()
        json_params = json.loads(getData) 
        print(json_params)

        #авторизация пользователя
        resp = registrationauth.auth_user(resp,json_params)

    except Exception as e: 
        print(e)
        status = 400
        resp['message'] = e
        
    response = jsonify(resp)
    response.headers.add('Access-Control-Allow-Origin', '*')
        
    return response

        

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    application.run(debug=False, port=port, host='0.0.0.0' , threaded=True)


