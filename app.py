from flask import Flask
from flask import request
import requests

import os
import json
from ast import literal_eval
import traceback

application = Flask(__name__)

# тестовый вывод
@application.route("/")  
def hello():
    return "Hello World!"

# регистрация пользователя
# проверяем что пользователя нет, далее регистрируем
@application.route("/registration" , methods=['GET', 'POST'])  
def external_receive():
    response = {'message':'ok'}
    status = 200
    try:
        getData = request.get_data()
        json_params = json.loads(getData) 
        
        print(json_params)
    except Exception as e: 
        print(e)
        status = 400
        response['message'] = e
        
    return response , status
        

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    application.run(debug=False, port=port, host='0.0.0.0' , threaded=True)


