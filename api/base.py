import json
import logging

import requests
from requests.adapters import HTTPAdapter
import api

_log = logging.getLogger(__name__)


def build_endpoint(api_command: str):
    """
    собирает итоговую урлу по схеме
    "https://base_url + / + api_command"
    :rtype str
    """
    return '{0}/{1}'.format(api.BASE_URL, api_command)


class Sender(object):

    @staticmethod
    def prepare_sender():
        s = requests.session()
        s.mount(api.BASE_URL, HTTPAdapter(max_retries=0))
        return s

    @staticmethod
    def get(endpoint: str, params: dict=None, answer_log: str='json'):
        """
        :rtype: Response
        """
        s = Sender.prepare_sender()
        if params is not None:
            _log.debug('\n[GET] from {url} with params = {params}'.format(url=endpoint, params=json.dumps(params)))
            result = s.get(endpoint, params=params)
        else:
            _log.debug('\n[GET] from {url}'.format(url=endpoint))
            result = s.get(endpoint)

        return Response(result, answer_log)

    @staticmethod
    def post(endpoint: str, request_body: dict, answer_log: str='json'):
        """
        :rtype: Response
        """
        s = Sender.prepare_sender()
        _log.debug('\n[POST] to {url}\n{j}'.format(url=endpoint, j=json.dumps(request_body, indent=2)))
        result = s.post(endpoint, json=request_body)

        return Response(result, answer_log)


class Response(object):
    """ обертка над стандартным ответом requests.Response с учетом специфики """

    def __init__(self, std_response: requests.Response, answer_log: str='json'):
        self.status_code = std_response.status_code
        self.caller = std_response.request
        self.text = std_response.text
        self.body = None
        self.cookies = std_response.cookies

        assert answer_log in ('json', 'text', 'no'), 'unsupported answer_log mode'

        try:
            self.body = std_response.json()
        except ValueError:
            pass  # suppressed error: "No JSON object could be decoded"

        if answer_log == 'json':
            _log.debug('\n[Response]: {}'.format(json.dumps(self.body, indent=2)))
        if answer_log == 'text':
            _log.debug('\n[Response]: {}'.format(self.text.encode('utf-8')))
