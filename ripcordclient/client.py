# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 OpenStack LLC.
# Copyright (C) 2013 PolyBeacon, Inc.
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from keystoneclient.v2_0 import client as ksclient

from ripcordclient.openstack.common import importutils


def _get_ksclient(**kwargs):
    """Get an endpoint and auth token from Keystone.

    :param kwargs: keyword args containing credentials:
            * username: name of user
            * password: user's password
            * auth_url: endpoint to authenticate against
            * cacert: path of CA TLS certificate
            * insecure: allow insecure SSL (no cert verification)
            * tenant_{name|id}: name or ID of tenant
    """
    return ksclient.Client(username=kwargs.get('username'),
                           password=kwargs.get('password'),
                           tenant_id=kwargs.get('tenant_id'),
                           tenant_name=kwargs.get('tenant_name'),
                           auth_url=kwargs.get('auth_url'),
                           region_name=kwargs.get('region_name'),
                           cacert=kwargs.get('cacert'),
                           insecure=kwargs.get('insecure'))


def _get_endpoint(client, **kwargs):
    """Get an endpoint using the provided keystone client."""
    return client.service_catalog.url_for(
        service_type=kwargs.get('service_type') or 'sip',
        endpoint_type=kwargs.get('endpoint_type') or 'publicURL')


def get_client(api_version, **kwargs):

    if kwargs.get('os_auth_token') and kwargs.get('ripcord_url'):
        token = kwargs.get('os_auth_token')
        endpoint = kwargs.get('ripcord_url')
    elif (kwargs.get('os_username') and
            kwargs.get('os_password') and
            kwargs.get('os_auth_url') and
            (kwargs.get('os_tenant_id') or
                kwargs.get('os_tenant_name'))):

        ks_kwargs = {
            'username': kwargs.get('os_username'),
            'password': kwargs.get('os_password'),
            'tenant_id': kwargs.get('os_tenant_id'),
            'tenant_name': kwargs.get('os_tenant_name'),
            'auth_url': kwargs.get('os_auth_url'),
            'insecure': kwargs.get('insecure'),
        }
        _ksclient = _get_ksclient(**ks_kwargs)
        token = _ksclient.auth_token
        endpoint = kwargs.get('ripcord_url') or \
            _get_endpoint(_ksclient, **ks_kwargs)

    cli_kwargs = {
        'token': token,
        'insecure': kwargs.get('insecure'),
    }

    return Client(api_version, endpoint, **cli_kwargs)


def Client(version, *args, **kwargs):
    module = importutils.import_module('ripcordclient.v1.client')
    client_class = getattr(module, 'Client')
    return client_class(*args, **kwargs)
