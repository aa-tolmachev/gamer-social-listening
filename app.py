from flask import Flask
from flask import request
import requests

import os
import json
from ast import literal_eval
import traceback

from user_auth import registrationauth

application = Flask(__name__)

# тестовый вывод
@application.route("/")  
def hello():
    return "Hello World!"

# регистрация пользователя
# проверяем что пользователя нет, далее регистрируем
# input
#{"email":"test@mail.ru","expiresIn":"3600","idToken":"abc","kind":"aabbcc","localId":"qwe","refreshToken":"qazwsx"}
# output
#{"message":"ok"} - "ok" , "user exist" , error text
@application.route("/registration" , methods=['GET', 'POST'])  
def registration():
    response = {'message':'ok'}
    status = 200
    try:
        getData = request.get_data()
        json_params = json.loads(getData) 
        print(json_params)

        #регистрация пользователя
        response = registrationauth.reg_new_user(response,json_params)

        
    except Exception as e: 
        print(e)
        status = 400
        response['message'] = e
        
    return response , status

# авторизация пользователя
# проверяем что пользователя нет, далее регистрируем
# input
#{"displayName" :"",  "email":"test@mail.ru","expiresIn":"3600","idToken":"abc","kind":"aabbcc","localId":"qwe","refreshToken":"qazwsx", "registered":True}
# output
#{"message":"ok"} - "ok" , "incorrect {}" 
@application.route("/authorization" , methods=['GET', 'POST'])  
def authorization():
    response = {'message':'ok'}
    status = 200
    try:
        getData = request.get_data()
        json_params = json.loads(getData) 
        print(json_params)

        #авторизация пользователя
        response = registrationauth.auth_user(response,json_params)
        
    except Exception as e: 
        print(e)
        status = 400
        response['message'] = e
        
    return response , status

        

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    application.run(debug=False, port=port, host='0.0.0.0' , threaded=True)

