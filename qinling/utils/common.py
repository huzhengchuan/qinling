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
import functools
import warnings

from oslo_utils import uuidutils
import six


def convert_dict_to_string(d):
    temp_list = ['%s=%s' % (k, v) for k, v in d.items()]

    return ','.join(temp_list)


def datetime_to_str(dct, attr_name):
    """Convert datetime object in dict to string."""
    if (dct.get(attr_name) is not None and
            not isinstance(dct.get(attr_name), six.string_types)):
        dct[attr_name] = dct[attr_name].isoformat(' ')


def generate_unicode_uuid(dashed=True):
    return uuidutils.generate_uuid(dashed=dashed)


def disable_ssl_warnings(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with warnings.catch_warnings():
            warnings.filterwarnings(
                "ignore",
                message="A true SSLContext object is not available"
            )
            warnings.filterwarnings(
                "ignore",
                message="Unverified HTTPS request is being made"
            )
            return func(*args, **kwargs)

    return wrapper
