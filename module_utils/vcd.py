# Copyright © 2018 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause

import os
from pyvcloud.vcd.client import Client
from ansible.module_utils.basic import AnsibleModule
from pyvcloud.vcd.client import BasicLoginCredentials
from ansible.module_utils.vcd_errors import VCDLoginError

DEFAULT_VERSION = '30.0'


def vcd_argument_spec():
    return dict(
        user=dict(type='str', required=False, default=None),
        password=dict(type='str', required=False, no_log=True, default=None),
        org=dict(type='str', required=False, default=None),
        host=dict(type='str', required=False, default=None),
        api_version=dict(type='str', default=DEFAULT_VERSION),
        verify_ssl_certs=dict(type='bool', default=False)
    )


class VcdAnsibleModule(AnsibleModule):
    def __init__(self, *args, **kwargs):
        argument_spec = vcd_argument_spec()
        argument_spec.update(kwargs.get('argument_spec', dict()))
        kwargs['argument_spec'] = argument_spec

        super(VcdAnsibleModule, self).__init__(*args, **kwargs)
        self.login()

    def login(self):
        try:
            user = self.params.get('user')
            password = self.params.get('password')
            org = self.params.get('org')
            host = self.params.get('host')
            api_version = self.params.get('api_version')
            verify_ssl_certs = self.params.get('verify_ssl_certs')

            # giving more precedence to module level details
            user = user if user else os.environ['env_user']
            password = password if password else os.environ['env_password']
            host = host if host else os.environ['env_host']
            org = org if org else os.environ['env_org']
            api_version = api_version if api_version else os.environ['env_api_version']
            verify_ssl_certs = verify_ssl_certs if verify_ssl_certs else os.environ['env_verify_ssl_certs']
            verify_ssl_certs = False if verify_ssl_certs == "False" else True

            self.client = Client(host,
                            api_version=api_version,
                            verify_ssl_certs=verify_ssl_certs)

            self.client.set_credentials(BasicLoginCredentials(user, org, password))

        except Exception as error:
            error = 'Login failed for user {} to org {}'
            raise VCDLoginError(error.format(user, org))
