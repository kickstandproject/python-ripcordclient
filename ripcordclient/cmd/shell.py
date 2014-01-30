# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright (C) 2013 PolyBeacon, Inc.
#
# Author: Paul Belanger <paul.belanger@polybeacon.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Command-line interface for the Ripcord APIs.
"""

import sys

from cliff import app
from cliff import commandmanager
from oslo.config import cfg

from ripcordclient import client
from ripcordclient.common import exception
from ripcordclient.common import utils
from ripcordclient.openstack.common import log as logging
from ripcordclient.shell.v1 import subscriber
from ripcordclient import version


CONF = cfg.CONF

COMMAND = {
    'subscriber-create': subscriber.CreateSubscriber,
    'subscriber-delete': subscriber.DeleteSubscriber,
    'subscriber-list': subscriber.ListSubscriber,
    'subscriber-update': subscriber.UpdateSubscriber,
    'subscriber-show': subscriber.ShowSubscriber,
}

COMMANDS = {
    '1': COMMAND,
}

LOG = logging.getLogger(__name__)


class Shell(app.App):

    def __init__(self, apiversion='1'):
        super(Shell, self).__init__(
            description=__doc__.strip(), version=version.VERSION_INFO,
            command_manager=commandmanager.CommandManager('ripcord.shell'))
        self.commands = COMMANDS
        for key, val in self.commands[apiversion].items():
            self.command_manager.add_command(key, val)

        self.api_version = apiversion

    def authenticate_user(self):
        if not (self.options.os_auth_token and self.options.ripcord_url):
            if not self.options.os_username:
                raise exception.CommandError(
                    'You must provide a username via either --os-username or '
                    'env[OS_USERNAME]')
            if not self.options.os_password:
                raise exception.CommandError(
                    'You must provide a password via either --os-password or '
                    'env[OS_PASSWORD]')
            if not (self.options.os_tenant_id or self.options.os_tenant_name):
                raise exception.CommandError(
                    'You must provide a tenant_id via either --os-tenant-id '
                    'or env[OS_TENANT_ID]')
            if not self.options.os_auth_url:
                raise exception.CommandError(
                    'You must provide an auth url via either --os-auth-url or '
                    'env[OS_AUTH_URL]')

        self.client_manager = client.get_client(
            self.api_version, **(self.options.__dict__))

        return

    def build_option_parser(self, description, version, argparse_kwargs=None):
        parser = super(Shell, self).build_option_parser(
            description, version, argparse_kwargs)

        parser.add_argument(
            '--os-auth-token', default=utils.env('OS_AUTH_TOKEN'),
            help='Defaults to env[OS_AUTH_TOKEN]')
        parser.add_argument(
            '--os-auth-url', default=utils.env('OS_AUTH_URL'),
            help='Defaults to env[OS_AUTH_URL]')
        parser.add_argument(
            '--os-password', default=utils.env('OS_PASSWORD'),
            help='Defaults to env[OS_PASSWORD]')
        parser.add_argument(
            '--os-tenant-id', default=utils.env('OS_TENANT_ID'),
            help='Defaults to env[OS_TENANT_ID]')
        parser.add_argument(
            '--os-tenant-name', default=utils.env('OS_TENANT_NAME'),
            help='Defaults to env[OS_TENANT_NAME]')
        parser.add_argument(
            '--os-username', default=utils.env('OS_USERNAME'),
            help='Defaults to env[OS_USERNAME]')
        parser.add_argument(
            '--ripcord-url', default=utils.env('ripcord_URL'),
            help='Defaults to env[RIPCORD_URL]')

        return parser

    def configure_logging(self):
        if self.options.debug:
            CONF.debug = True
        elif self.options.verbose_level:
            CONF.verbose = True

        return

    def initialize_app(self, argv):
        super(Shell, self).initialize_app(argv)

        logging.setup('ripcordclient')
        cmd_name = None

        if argv:
            cmd_info = self.command_manager.find_command(argv)
            cmd_factory, cmd_name, sub_argv = cmd_info

        if self.interactive_mode or cmd_name != 'help':
            self.authenticate_user()


def main(argv=sys.argv[1:]):
    return Shell().run(argv)
