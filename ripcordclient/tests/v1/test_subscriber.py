# -*- coding: utf-8 -*-
# Copyright (c) 2013 PolyBeacon, Inc.

# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import testtools

from ripcordclient.tests import utils
from ripcordclient.v1 import subscriber

SUBSCRIBER = {
    'username': 'alice',
    'uuid': 'b5142338-d88a-403e-bb14-e1fba0a318d2',
}

CREATE_SUBSCRIBER = {
    'username': 'alice',
}

FIXTURES = {
    '/v1/subscribers': {
        'GET': (
            {},
            [SUBSCRIBER],
        ),
        'POST': (
            {},
            SUBSCRIBER,
        ),
    },
    '/v1/subscribers/%s' % SUBSCRIBER['uuid']: {
        'GET': (
            {},
            SUBSCRIBER,
        ),
        'DELETE': (
            {},
            None,
        ),
    },
}


class SubscriberManagerTest(testtools.TestCase):

    def setUp(self):
        super(SubscriberManagerTest, self).setUp()
        self.api = utils.FakeAPI(FIXTURES)
        self.manager = subscriber.SubscriberManager(self.api)

    def test_create(self):
        res = self.manager.create(**CREATE_SUBSCRIBER)
        expect = [
            ('POST', '/v1/subscribers', {}, CREATE_SUBSCRIBER),
        ]
        self.assertEqual(self.api.calls, expect)
        self.assertTrue(res)

    def test_delete(self):
        res = self.manager.delete(uuid=SUBSCRIBER['uuid'])
        expect = [
            ('DELETE', '/v1/subscribers/%s' % SUBSCRIBER['uuid'], {}, None),
        ]
        self.assertEqual(self.api.calls, expect)
        self.assertEqual(res, None)

    def test_list(self):
        res = self.manager.list()
        expect = [
            ('GET', '/v1/subscribers', {}, None),
        ]
        self.assertEqual(self.api.calls, expect)
        self.assertEqual(len(res), 1)

    def test_show(self):
        res = self.manager.get(uuid=SUBSCRIBER['uuid'])
        expect = [
            ('GET', '/v1/subscribers/%s' % SUBSCRIBER['uuid'], {}, None),
        ]
        self.assertEqual(self.api.calls, expect)
        self.assertEqual(res.uuid, SUBSCRIBER['uuid'])
