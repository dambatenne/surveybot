import requests as req
from collections import OrderedDict
import json

"""
Класс инкапсулирующий методы работы с системой провдения опросов RC PSI (Lime Surveys.py) http://psi.rc.center/psi/
"""


class Survey:

    def __init__(self, api_url, login, password):
        self.headers = {"content-type": "application/json"}
        self.api_url = api_url
        self.login = login
        self.password = password
        self.sess_key = None

    """
    Метод возвращающий ключ сессии для текущего пользователя.
    Ключ используется для всех дальнейших запросов к API
    """
    def get_session_key(self):

        method = "get_session_key"

        params = OrderedDict([
            ("username", self.login),
            ("password", self.password)
        ])

        self.sess_key = self.query(method, params)["result"]

    """
        Метод возвращающий список всех опросов, доступных пользователю
    """
    def list_surveys(self):

        method = "list_surveys"

        params = OrderedDict([
            ("sSessionKey", self.sess_key),
            ("sUsername", self.login)
        ])

        return self.query(method, params)["result"]

    """
    Метод выводит список групп вопросов для конкретного опроса
    """
    def list_groups(self, sid):

        method = "list_groups"

        params = OrderedDict([
            ("sSessionKey", self.sess_key),
            ("iSurveyID", sid)
        ])

        return self.query(method, params)["result"]

    """
    Метод возвращает список вопросов для конкретной группы вопросов
    """
    def list_questions(self, sid, gid):

        method = "list_questions"

        params = OrderedDict([
            ("sSessionKey", self.sess_key),
            ("iSurveyID", sid),
            ("iGroupID", gid)
        ])

        return self.query(method, params)["result"]

    """
    Общий метод для запросов к API
    """
    def query(self, method, params):

        data = OrderedDict([
            ("method", method),
            ("params", params),
            ("id", 1)
        ])

        data = json.dumps(data)

        try:
            r = req.post(self.api_url, headers=self.headers, data=data)
            return r.json()
        except Exception as e:
            print(e)


APIURL = "http://psi.rc.center/psi/index.php?r=admin/remotecontrol"
user = 'admin'
password = 'password'
s = Survey(APIURL, user, password)

s.get_session_key()
sid = s.list_surveys()[0]["sid"]
gid = s.list_groups(sid)[0]["gid"]

for q in s.list_questions(sid, gid):
    print(q)
