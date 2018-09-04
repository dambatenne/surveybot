#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Пример работы с json-rpc. ПОказывает описание опросов, а также заполняет один ответ (простой текст) и приктерпляет один файл.
#


import urllib2
import json
import sys
import base64
import os

# Параметры подлючения к серверу
APIURL = "http://psi.rc.center/psi/index.php?r=admin/remotecontrol"
user = 'admin'
password = 'password'

# Параметры прохождения опроса. Данный пример отвечает на один вопрос и прикрепляет файл (смотрите ограничение по типу и размеру в настройках)
surveyId = '798664' # Данный ID получен на шаге "Получить сисок вопросов"
groupId = '2' # Данный ID получен на шаге "Получить сисок вопросов"
questionId = '6' # Данный ID получен на шаге "Получить сисок вопросов"
attachFile = '/Firefox_wallpaper.png'
attachQuestionId = '7' # Данный ID получен на шаге "Получить сисок вопросов"
participant_email = 'efrik_001@mail.ru' # Почта для получения токена участника опроса (участнк должен быть добавлен в опрос)

def get_session_key():
    u"""Получить ключь для сессис"""
    req = urllib2.Request(url=APIURL ,\
                          data='{\"method\":\"get_session_key\",\"params\":[\"' + user + '\",\"' + password + '\"],\"id\":1}')
    req.add_header('content-type', 'application/json')
    req.add_header('connection', 'Keep-Alive')
    try:
        f = urllib2.urlopen(req)
        myretun = f.read()
        j=json.loads(myretun)
        return j['result']
    except :
        e = sys.exc_info()[0]
        print ( "<p>Error: %s</p>" % e )

def get_question_properties(skey, QuestionID):
    req = urllib2.Request(url=APIURL,\
                          data='{\"method\":\"get_question_properties\",\"params\":[\"'+skey+'\",'+QuestionID
                                    +',[\"gid\",\"type\",\"help\",\"language\",\"sid\",\"question_order\",\"question\",\"subquestions\"]],\"id\": 1}')

    req.add_header('content-type', 'application/json')
    req.add_header('connection', 'Keep-Alive')
    try:
        f = urllib2.urlopen(req)
        myretun = f.read()
        j=json.loads(myretun)
        return j['result']
    except :
        e = sys.exc_info()[0]
        print ( "<p>Error: %s</p>" % e )


def release_session_key(relkey):
    u"""Закрыть сессию"""

    req = urllib2.Request(url=APIURL,\
                          data='{\"method\":\"release_session_key\",\"params\":[\"'+relkey+'\"],\"id\":1}')
    req.add_header('content-type', 'application/json')
    req.add_header('connection', 'Keep-Alive')
    try:
        f = urllib2.urlopen(req)
        myretun = f.read()
        #print myretun
        j=json.loads(myretun)
        return j['result']
    except :
        e = sys.exc_info()[0]
        print ( "<p>Error: %s</p>" % e )


def export_responses2(skey,sid):
    req = urllib2.Request(url=APIURL, data='{\"method\":\"export_responses\",\"params\":[\"'+skey+'\",\"'+sid+'\",\"csv\",\"ru\",\"full\"], "id\": 1}')
    req.add_header('content-type', 'application/json')
    req.add_header('connection', 'Keep-Alive')
    try:
        f = urllib2.urlopen(req)
        myretun = f.read()
        #print myretun
        j=json.loads(myretun)
        return j['result']
    except :
        e = sys.exc_info()[0]
        print ( "<p>Error: %s</p>" % e )


def list_surveys(skey):
    u"""Получить сисок голосований"""

    req = urllib2.Request(url=APIURL, data='{\"method\":\"list_surveys\",\"params\":[\"'+skey+'\",\"'+user+'\"], "id\": 1}')
    req.add_header('content-type', 'application/json')
    req.add_header('connection', 'Keep-Alive')
    try:
        f = urllib2.urlopen(req)
        myretun = f.read()
        j=json.loads(myretun)
        return j['result']
    except :
        e = sys.exc_info()[0]
        print ( "<p>Error: %s</p>" % e )

def list_groups(skey, sid):
    u"""Получить сисок групп ответов"""

    req = urllib2.Request(url=APIURL, data='{\"method\":\"list_groups\",\"params\":[\"'+skey+'\",\"'+sid+'\"], "id\": 1}')
    req.add_header('content-type', 'application/json')
    req.add_header('connection', 'Keep-Alive')
    try:
        f = urllib2.urlopen(req)
        myretun = f.read()
        j=json.loads(myretun)
        return j['result']
    except :
        e = sys.exc_info()[0]
        print ( "<p>Error: %s</p>" % e )


def list_questions(skey, sid, gid):
    u"""Получить сисок групп ответов"""

    req = urllib2.Request(url=APIURL, data='{\"method\":\"list_questions\",\"params\":[\"'+skey+'\",\"'+sid+'\",\"'+gid+'\"], "id\": 1}')
    req.add_header('content-type', 'application/json')
    req.add_header('connection', 'Keep-Alive')
    try:
        f = urllib2.urlopen(req)
        myretun = f.read()
        j=json.loads(myretun)
        return j['result']
    except :
        e = sys.exc_info()[0]
        print ( "<p>Error: %s</p>" % e )


def add_response(skey, sid, gid, qid, val, token, attachQid=None, attachDescription=None, fileName=None):
    u"""добавить ответ"""
    fieldname = '{0}X{1}X{2}'.format(sid, gid, qid) # Вычисляем имя поля в таблице
    attach_fieldname = '{0}X{1}X{2}'.format(sid, gid, attachQid) # Вычисляем имя поля в таблице
    if attachQid and attachDescription:
        attachDescription_str =  '[{\\"title\\": \\"\\", \\"comment\\": \\"\\", \\"name\\": \\"'+fileName+'\\", \\"filename\\": \\"'+str(attachDescription["filename"])+'\\", \\"size\\": '+str(attachDescription["size"])+', \\"ext\\": \\"' + str(attachDescription["ext"]) + '\\"}]'
        adata = '{\"method\":\"add_response\",\"params\":[\"' + skey + '\",\"' + sid + '\", {\"' + fieldname + '\":\"' + val + '\", \"token\": \"' + token + '\", \"lastpage\":\"1\", \"' + attach_fieldname + '\":\"' + attachDescription_str + '\", \"' + attach_fieldname + '_filecount' + '\":\"1\"}], "id\": 1}'
    else:
        adata = '{\"method\":\"add_response\",\"params\":[\"'+skey+'\",\"'+sid+'\", {\"'+fieldname+'\":\"'+ val +'\", \"token\": \"' + token + '\", \"lastpage\":\"1\"}], "id\": 1}'


    req = urllib2.Request(url=APIURL, data=adata)
    req.add_header('content-type', 'application/json')
    req.add_header('connection', 'Keep-Alive')
    try:
        f = urllib2.urlopen(req)
        myretun = f.read()
        j=json.loads(myretun)
        return j['result']
    except :
        e = sys.exc_info()[0]
        print ( "<p>Error: %s</p>" % e )


def upload_file(skey, sid, gid, qid, fileName, path):
    u"""Загрузить файл"""
    fieldname = '{0}X{1}X{2}'.format(sid, gid, qid) # Вычисляем имя поля в таблице

    with open(path, "rb") as binary_file:
        content = base64.b64encode(binary_file.read())

    req = urllib2.Request(url=APIURL, data='{\"method\":\"upload_file\",\"params\":[\"'+skey+'\",\"'+sid+'\",\"' + fieldname +'\", \"' + fileName +'\", \"' + content + '\"], "id\": 1}')
    req.add_header('content-type', 'application/json')
    req.add_header('connection', 'Keep-Alive')
    try:
        f = urllib2.urlopen(req)
        myretun = f.read()
        j=json.loads(myretun)
        return j['result']
    except :
        e = sys.exc_info()[0]
        print ( "<p>Error: %s</p>" % e )

def list_participants(skey, sid, email=None):
    u"""Получить список участников"""
    if email:
        data = '{\"method\":\"list_participants\",\"params\":[\"' + skey + '\",\"' + sid + '\", 0, 10, false, false, { "email":"' + email + '" }], "id\": 1}'
    else:
        data = '{\"method\":\"list_participants\",\"params\":[\"' + skey + '\",\"' + sid + '\", 0, 10, false, false], "id\": 1}'

    req = urllib2.Request(url=APIURL, data=data)
    req.add_header('content-type', 'application/json')
    req.add_header('connection', 'Keep-Alive')
    try:
        f = urllib2.urlopen(req)
        myretun = f.read()
        j=json.loads(myretun)
        return j['result']
    except :
        e = sys.exc_info()[0]
        print ( "<p>Error: %s</p>" % e )

print u"### Получить сессионный ключь для пользователя имеющего права на API #############################################"
mykey=get_session_key()

print u"### Получить сисок голосований #############################################"
surveys = list_surveys(mykey)
print u"### Получить сисок вопросов ##########################################################################################"
for survey_item in surveys:
    print u"survey id: {0} active: {1} title: {2} ########################################################".format(survey_item['sid'], survey_item['active'], unicode(survey_item['surveyls_title']))
    groups = list_groups(mykey, str(survey_item['sid']))
    if type(groups) is dict:
        print groups['status']
        continue
    for group_item in groups:
        print u"group id: '{0}' group name: '{1}' ##########################################".format(group_item['gid'], unicode(group_item['group_name']))
        questions = list_questions(mykey, str(survey_item['sid']), str(group_item['gid']))
        if type(questions) is dict:
            print questions['status']
            continue
        for question_item in questions:
            if question_item == u'status':
                break;
            print u"quest id: '{0}' title: {1} Вопрос: '{2}' ".format(question_item['qid'], question_item['title'], unicode(question_item['question']))
            print u"Cвойства вопроса:"
            print get_question_properties(mykey, str(question_item['qid']))


print u"### Список участников для голосования {0} #############################################".format(surveyId)
for participant in list_participants(mykey, surveyId):
    participant_info = participant['participant_info']
    print u'token: {0} firstname: {1} lastname: {3} email: {3}'.format(participant['token'], participant_info['firstname'], participant_info['lastname'], participant_info['email'])


print u"### Загрузить файл а затем ответить на вопрос и прекрипить загруженный файл #############################################"
participant_token = list_participants(mykey, surveyId, participant_email)[0]["token"]
attachDescription = upload_file(mykey, surveyId, groupId, attachQuestionId, os.path.basename(attachFile), attachFile)
print add_response(mykey, surveyId, groupId, questionId, 'Test upload', participant_token, attachQuestionId, attachDescription, os.path.basename(attachFile))


print u"### Получить результаты активных голосований в csv #############################################"
for item in surveys:
    if item['active'] == 'N':
        continue

    print "id: {0} active: {1}".format(item['sid'], item['active'])
    print export_responses2(mykey, str(item['sid'])).decode('base64')


release_session_key(mykey)
