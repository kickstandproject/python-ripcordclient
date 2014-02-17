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


class CreateDomain(base.CreateCommand):
    """Create a domain."""

    log = logging.getLogger(__name__ + '.CreateDomain')
    resource = 'domains'

    def add_known_arguments(self, parser):
        parser.add_argument(
            'name', help='The name of the domain.')

    def args2body(self, parsed_args):
        body = {
            'name': parsed_args.name,
        }

        return body


class DeleteDomain(base.DeleteCommand):
    """Delete a given domain."""

    log = logging.getLogger(__name__ + '.DeleteDomain')
    resource = 'domains'


class ListDomain(base.ListCommand):
    """List domain."""

    list_columns = [
        'uuid',
        'name',
        'user_id',
        'project_id',
        'created_at',
        'updated_at',
    ]
    log = logging.getLogger(__name__ + '.ListDomain')
    resource = 'domains'


class ShowDomain(base.ShowCommand):
    """Show information of a given domain."""

    log = logging.getLogger(__name__ + '.ShowDomain')
    resource = 'domains'


class UpdateDomain(base.UpdateCommand):
    """Update a domain."""

    log = logging.getLogger(__name__ + '.UpdateDomain')
    resource = 'domains'

    def add_known_arguments(self, parser):
        parser.add_argument(
            '--name', help='The name of the domain.')

    def args2body(self, parsed_args):
        body = {}
        if parsed_args.name:
            body['name'] = parsed_args.name

        return body
