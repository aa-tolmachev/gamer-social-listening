import access

import requests

from datetime import datetime
from datetime import timedelta

import psycopg2
import pandas as pd
import numpy as np


PSQL_heroku_keys = access.PSQL_heroku_keys()


#текущая метка времени с минутой часами
def now_str():
    now = datetime.now()
    now_str = str(now.year)+str(now.month if now.month >= 10 else  '0'+str(now.month))+str(now.day if now.day >= 10 else  '0'+str(now.day)) +' '+str(now.hour if now.hour >= 10 else  '0'+str(now.hour)) + str(now.minute if now.minute >= 10 else  '0'+str(now.minute)) + str(now.second if now.second >= 10 else  '0'+str(now.second))
    return now_str


#проверяем есть ли такой пользователь
def is_exist(reg_params):

    response = {'user_exist' : 0}

    #создаем подключение к PSQL
    conn = psycopg2.connect("dbname='%(dbname)s' port='%(port)s' user='%(user)s' host='%(host)s' password='%(password)s'" % PSQL_heroku_keys)
    # создаем запрос
    cur = conn.cursor()

    #получаем дату в строке
    current_str = now_str()

    #смотрим есть ли подобный пользователь
    cur.execute("SELECT * from public.user where email = '%(user_email)s'" % {'user_email' : reg_params['email']} )
    #получаем данные
    df_current_users = pd.DataFrame(cur.fetchall(), columns=[desc[0] for desc in cur.description])

    if df_current_users.shape[0] != 0:
        response['user_exist'] = 1

    cur.close()
    conn.close()

    return response
 

#регистрируем нового пользователя
#{"email":"test@mail.ru","expiresIn":"3600","idToken":"abc","kind":"aabbcc","localId":"qwe","refreshToken":"qazwsx"}
def reg_new_user(response,reg_params):

    email = reg_params['email']
    expiresIn = int(reg_params['expiresIn'])
    idToken = reg_params['idToken']
    kind = reg_params['kind']
    localId = reg_params['localId']
    refreshToken = reg_params['refreshToken']

    #получаем дату в строке
    current_str = now_str()

    check_user_exist = is_exist(reg_params)

    if check_user_exist['user_exist'] == 0:

        #создаем подключение к PSQL
        conn = psycopg2.connect("dbname='%(dbname)s' port='%(port)s' user='%(user)s' host='%(host)s' password='%(password)s'" % PSQL_heroku_keys)
        # создаем запрос
        cur = conn.cursor()

        #создаем запись в строчке последнего шага
        cur.execute(f"INSERT INTO public.user (email , expiresIn, idToken, kind, localId, refreshToken)  VALUES ('{email}', {expiresIn} , '{idToken}' , '{kind}' , '{localId}' , '{refreshToken}')"  )
        conn.commit()

        cur.close()
        conn.close()
    else:
        response['message'] = 'user exist'

    return response
 

#авторизуем пользователя если совпадают параметры
# если не совпадает email , idToken , kind , localId то отказ
#{"displayName" :"",  "email":"test@mail.ru","expiresIn":"3600","idToken":"abc","kind":"aabbcc","localId":"qwe","refreshToken":"qazwsx", "registered":True}
def auth_user(response,reg_params):

    email = reg_params['email']
    expiresIn = int(reg_params['expiresIn'])
    idToken = reg_params['idToken']
    kind = reg_params['kind']
    localId = reg_params['localId']
    refreshToken = reg_params['refreshToken']
    registered = reg_params['registered']

    #получаем дату в строке
    current_str = now_str()

    check_user_exist = is_exist(reg_params)

    if check_user_exist['user_exist'] == 0:
        response['message'] = 'user not exist'
    else:
       #создаем подключение к PSQL
        conn = psycopg2.connect("dbname='%(dbname)s' port='%(port)s' user='%(user)s' host='%(host)s' password='%(password)s'" % PSQL_heroku_keys)
        # создаем запрос
        cur = conn.cursor()

        #смотрим есть ли подобный пользователь
        cur.execute("SELECT * from public.user where email = '%(user_email)s' and idToken = '%(idToken)s' and localId = '%(localId)s'" % {'user_email' : reg_params['email'],'idToken': idToken,'localId':localId} )
        #получаем данные
        df_current_users = pd.DataFrame(cur.fetchall(), columns=[desc[0] for desc in cur.description])

        if df_current_users.shape[0] == 0:
            response['message'] = 'email or idToken or localId not correct'

        cur.close()
        conn.close()

        

    return response
 