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

import logging

from ripcordclient.shell.v1 import base


class CreateSubscriber(base.CreateCommand):
    """Create a subscriber."""

    log = logging.getLogger(__name__ + '.CreateSubscriber')
    resource = 'subscribers'

    def add_known_arguments(self, parser):
        parser.add_argument(
            'username', help='The username of the subscriber.')
        parser.add_argument(
            'domain_id', help='The domain id of the subscriber.')
        parser.add_argument(
            'password', help='The password of the subscriber.')
        parser.add_argument(
            '--email', help='The email address of the subscriber.')
        parser.add_argument(
            '--disabled', type=bool, default=False, help='(Default: False)')

    def args2body(self, parsed_args):
        body = {
            'disabled': parsed_args.disabled,
            'domain_id': parsed_args.domain_id,
            'password': parsed_args.password,
            'username': parsed_args.username,
        }
        if parsed_args.email:
            body['email_address'] = parsed_args.email
        return body


class DeleteSubscriber(base.DeleteCommand):
    """Delete a given subscriber."""

    log = logging.getLogger(__name__ + '.DeleteSubscriber')
    resource = 'subscribers'


class ListSubscriber(base.ListCommand):
    """List subscribers."""

    list_columns = [
        'uuid',
        'username',
        'domain_id',
        'email_address',
        'rpid',
        'disabled',
        'user_id',
        'project_id',
        'created_at',
        'updated_at',
    ]
    log = logging.getLogger(__name__ + '.ListSubscriber')
    resource = 'subscribers'


class ShowSubscriber(base.ShowCommand):
    """Show information of a given subscriber."""

    log = logging.getLogger(__name__ + '.ShowSubscriber')
    resource = 'subscribers'


class UpdateSubscriber(base.UpdateCommand):
    """Update a subscriber."""

    log = logging.getLogger(__name__ + '.UpdateSubscriber')
    resource = 'subscribers'

    def add_known_arguments(self, parser):
        parser.add_argument(
            '--disabled', type=bool, default=False, help='(Default: False)')
        parser.add_argument(
            '--domain_id', help='The domain id of the subscriber.')
        parser.add_argument(
            '--password', help='The password of the subscriber.')
        parser.add_argument(
            '--username', help='The name of the subscriber.')

    def args2body(self, parsed_args):
        body = {
            'disabled': parsed_args.disabled,
        }
        if parsed_args.domain_id:
            body['domain_id'] = parsed_args.domain_id
        if parsed_args.username:
            body['password'] = parsed_args.password
        if parsed_args.username:
            body['username'] = parsed_args.username

        return body
