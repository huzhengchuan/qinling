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

from oslo_config import cfg
from oslo_log import log as logging
import pecan

from qinling.api import access_control
from qinling import context as ctx
from qinling.db import api as db_api
from qinling.services import periodics

LOG = logging.getLogger(__name__)


def get_pecan_config():
    # Set up the pecan configuration.
    opts = cfg.CONF.pecan

    cfg_dict = {
        "app": {
            "root": opts.root,
            "modules": opts.modules,
            "debug": opts.debug,
            "auth_enable": opts.auth_enable
        }
    }

    return pecan.configuration.conf_from_dict(cfg_dict)


def setup_app(config=None):
    if not config:
        config = get_pecan_config()
    app_conf = dict(config.app)

    db_api.setup_db()

    LOG.info('Starting periodic tasks...')
    periodics.start_job_handler()

    app = pecan.make_app(
        app_conf.pop('root'),
        hooks=lambda: [ctx.ContextHook(), ctx.AuthHook()],
        logging=getattr(config, 'logging', {}),
        **app_conf
    )

    # Set up access control.
    app = access_control.setup(app)

    return app
