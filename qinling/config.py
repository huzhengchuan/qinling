# Copyright 2017 Catalyst IT Limited
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

"""
Configuration options registration and useful routines.
"""
import itertools

from oslo_config import cfg
from oslo_log import log

from qinling import version

launch_opt = cfg.ListOpt(
    'server',
    default=['all'],
    help='Specifies which qinling server to start by the launch script.'
)

api_opts = [
    cfg.StrOpt('host', default='0.0.0.0', help='Qinling API server host.'),
    cfg.PortOpt('port', default=7070, help='Qinling API server port.'),
    cfg.BoolOpt(
        'enable_ssl_api',
        default=False,
        help='Enable the integrated stand-alone API to service requests'
             'via HTTPS instead of HTTP.'
    ),
    cfg.IntOpt(
        'api_workers',
        help='Number of workers for Qinling API service '
             'default is equal to the number of CPUs available if that can '
             'be determined, else a default worker count of 1 is returned.'
    )
]

pecan_opts = [
    cfg.StrOpt(
        'root',
        default='qinling.api.controllers.root.RootController',
        help='Pecan root controller'
    ),
    cfg.ListOpt(
        'modules',
        default=["qinling.api"],
        help='A list of modules where pecan will search for applications.'
    ),
    cfg.BoolOpt(
        'debug',
        default=False,
        help='Enables the ability to display tracebacks in the browser and'
             ' interactively debug during development.'
    ),
    cfg.BoolOpt(
        'auth_enable',
        default=True,
        help='Enables user authentication in pecan.'
    )
]

CONF = cfg.CONF
API_GROUP = 'api'
PECAN_GROUP = 'pecan'
CLI_OPTS = [launch_opt]

CONF.register_opts(api_opts, group=API_GROUP)
CONF.register_opts(pecan_opts, group=PECAN_GROUP)
CONF.register_cli_opts(CLI_OPTS)

default_group_opts = itertools.chain(
    CLI_OPTS,
    []
)


def list_opts():
    return [
        (API_GROUP, api_opts),
        (PECAN_GROUP, pecan_opts),
        (None, default_group_opts)
    ]


_DEFAULT_LOG_LEVELS = [
    'eventlet.wsgi.server=WARN',
    'oslo_service.periodic_task=INFO',
    'oslo_service.loopingcall=INFO',
    'oslo_db=WARN',
    'oslo_concurrency.lockutils=WARN'
]


def parse_args(args=None, usage=None, default_config_files=None):
    default_log_levels = log.get_default_log_levels()
    default_log_levels.extend(_DEFAULT_LOG_LEVELS)
    log.set_defaults(default_log_levels=default_log_levels)

    log.register_options(CONF)

    CONF(
        args=args,
        project='qinling',
        version=version,
        usage=usage,
        default_config_files=default_config_files
    )