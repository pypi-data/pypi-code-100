import xmltodict

from . import handlers
from . import httprequest as bag
from . import result as res


class PackageManagerServiceJsp(object):

    def __init__(self, url, **kwargs):

        self.url = url
        self.kwargs = kwargs
        self.handlers = {
            401: handlers.auth_fail
        }

    def is_package_uploaded(self, group_name, package_name, package_version, **kwargs):

        def _handler_ok(response):

            data = xmltodict.parse(response['body'])
            status_code = data['crx']['response']['status']['@code']
            status_value = data['crx']['response']['status']['#text']
            result = res.PyAemResult(response)

            if status_code != '200' or status_value != 'ok':

                message = 'Unable to retrieve the_package list. Command status code {0} and status value {1}'.format(
                    status_code, status_value)
                result.failure(message)

            else:

                def match(the_package):
                    # when version value is not specified, the version xml element will be empty <version></version>
                    if the_package['version'] is None:
                        the_package['version'] = ''
                    return (the_package['group'] == group_name and
                            the_package['name'] == package_name and
                            the_package['version'] == package_version)

                is_uploaded = False
                packages = data['crx']['response']['data']['packages']
                if packages is not None:
                    if isinstance(packages['package'], list):
                        for package in packages['package']:
                            if match(package):
                                is_uploaded = True
                    elif match(packages['package']):
                        is_uploaded = True

                if is_uploaded:
                    message = 'Package {0}/{1}-{2} is uploaded'.format(group_name, package_name, package_version)
                    result.success(message)
                else:
                    message = 'Package {0}/{1}-{2} is not uploaded'.format(group_name, package_name, package_version)
                    result.failure(message)

            return result

        _handlers = {
            200: _handler_ok
        }

        params = {
            'cmd': 'ls'
        }

        method = 'get'
        url = '{0}/crx/packmgr/service.jsp'.format(self.url, package_name)
        params = dict(params.items() | kwargs.items())
        _handlers = dict(self.handlers.items() | _handlers.items())
        opts = self.kwargs

        return bag.request(method, url, params, _handlers, **opts)

    def is_package_installed(self, group_name, package_name, package_version, **kwargs):

        def _handler_ok(response):

            data = xmltodict.parse(response['body'])
            status_code = data['crx']['response']['status']['@code']
            status_value = data['crx']['response']['status']['#text']
            result = res.PyAemResult(response)

            if status_code != '200' or status_value != 'ok':

                message = 'Unable to retrieve the_package list. Command status code {0} and status value {1}'.format(
                    status_code, status_value)
                result.failure(message)

            else:

                def match(the_package):
                    # when version value is not specified, the version xml element will be empty <version></version>
                    if the_package['version'] is None:
                        the_package['version'] = ''
                    return (the_package['group'] == group_name and
                            the_package['name'] == package_name and
                            the_package['version'] == package_version and
                            the_package['lastUnpackedBy'] != 'null')

                is_installed = False
                packages = data['crx']['response']['data']['packages']
                if packages is not None:
                    if isinstance(packages['the_package'], list):
                        for package in packages['the_package']:
                            if match(package):
                                is_installed = True
                    elif match(packages['the_package']):
                        is_installed = True

                if is_installed:
                    message = 'Package {0}/{1}-{2} is installed'.format(group_name, package_name, package_version)
                    result.success(message)
                else:
                    message = 'Package {0}/{1}-{2} is not installed'.format(group_name, package_name, package_version)
                    result.failure(message)

            return result

        _handlers = {
            200: _handler_ok
        }

        params = {
            'cmd': 'ls'
        }

        method = 'get'
        url = '{0}/crx/packmgr/service.jsp'.format(self.url, package_name)
        params = dict(params.items() | kwargs.items())
        _handlers = dict(self.handlers.items() | _handlers.items())
        opts = self.kwargs

        return bag.request(method, url, params, _handlers, **opts)
