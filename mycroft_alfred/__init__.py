import json

import requests
from adapt.intent import IntentBuilder
from mycroft import intent_handler
from mycroft.skills.core import MycroftSkill

__author__ = 'Bart Feenstra'


class AlfredSkill(MycroftSkill):
    def __init__(self, emitter=None):
        MycroftSkill.__init__(self, 'Alfred', emitter)
        self._base_url = 'http://alfred:5000'

    @intent_handler(IntentBuilder('LightsOn'))
    def lights_on(self):
        self._lights_change(True)

    @intent_handler(IntentBuilder('LightsOff'))
    def lights_off(self):
        self._lights_change(False)

    def _lights_change(self, powered):
        body = json.dumps([
            {
                'op': 'replace',
                'path': '/powered',
                'value': powered,
            },
        ])
        return self._request('PATCH', 'devices', body, {
            'Content-Type': 'application/json-patch+json',
        })

    def _request(self, method, path, body=None, headers=None):
        if headers is None:
            headers = {}
        headers['Accept'] = 'application/json'
        url = '%s/%s' % (self._base_url, path.lstrip('/'))
        response = getattr(requests, method.lower())(url, body, headers=headers)
        response.raise_for_status()
        return response
