from unittest import TestCase

import requests_mock

from mycroft_alfred import AlfredSkill


class SkillTest(TestCase):
    def setUp(self):
        self._sut = AlfredSkill()

    @requests_mock.mock()
    def test_lights_on(self, m):
        m.patch('http://alfred:5000/devices', request_headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json-patch+json',
        })
        self._sut.lights_on()
        self.assertEquals(len(m.request_history), 1)
        expected_body = [
            {
                'op': 'replace',
                'path': '/powered',
                'value': True,
            },
        ]
        self.assertEquals(m.request_history[0].json(), expected_body)

    @requests_mock.mock()
    def test_lights_off(self, m):
        m.patch('http://alfred:5000/devices', request_headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json-patch+json',
        })
        self._sut.lights_off()
        self.assertEquals(len(m.request_history), 1)
        expected_body = [
            {
                'op': 'replace',
                'path': '/powered',
                'value': False,
            },
        ]
        self.assertEquals(m.request_history[0].json(), expected_body)
