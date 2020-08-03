from flask import Flask
from flask import request
import requests
from flask import jsonify

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
#{"email":"test@mail.ru","password":"qwer"}
# output
#{"message":"ok"} - "ok" , "user exist" , error text
@application.route("/registration" , methods=['GET', 'POST'])  
def registration():
    resp = {'message':'ok'}
    status = 200
    try:
        getData = request.get_data()
        json_params = json.loads(getData) 
        print(json_params)

        #регистрация пользователя
        resp = registrationauth.reg_new_user(resp,json_params)

        
    except Exception as e: 
        print(e)
        status = 400
        resp['message'] = e
        
    return jsonify(resp)

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
        
    return jsonify(resp)

        

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    application.run(debug=False, port=port, host='0.0.0.0' , threaded=True)


