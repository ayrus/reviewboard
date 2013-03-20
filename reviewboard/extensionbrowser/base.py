from urllib import urlencode
from urllib2 import Request, urlopen

import django.utils.simplejson as json

from reviewboard.settings import EXTENSION_STORE_ENDPOINT


class StoreExtensionInfo(object):
    """A class for depicting an extension from the store."""
    def __init__(self, id, name, description, version, author, package, installed):
        self.id = id
        self.name = name
        self.description = description
        self.version = version
        self.author = author
        self.package_name = package
        self.installed = installed


class ExtensionStoreQuery(object):
    """Allows querying the extension store for a possible list of extensions.

    A supported extension store can be queried (with or without parameters)
    for a list of extensions available.
    """
    def __init__(self, extension_manager):
        self.store_url = EXTENSION_STORE_ENDPOINT
        self.installed_extensions = None

        # Populate package names of all extensions presently installed.
        self.installed_extensions = [
            ext.dist.project_name.lower()
            for ext in extension_manager._entrypoint_iterator()
        ]

    def _query(self, endpoint, params=None):
        """Query the store.

        Perform the actual HTTP request to the store with parameters (if any).
        """
        request_url = '%s/%s' % (self.store_url, endpoint)

        if params:
            url_params = urlencode(params)
            request_url = '%s?%s' % (request_url, url_params)

        request = Request(request_url)
        response = urlopen(request)

        return json.loads(response.read())

    def populate_extensions(self, params):
        """Query and populate the result of extensions.

        Query for a list of extensions with the given params against the
        extension store and return a list of StoreExtensionInfo class objects.
        """
        response = self._query("list", params)
        extlist = []
        extensions = response['extensions']

        for ext in extensions:
            installed = ext['package_name'] in self.installed_extensions
            extlist.append(StoreExtensionInfo(id=ext['id'], 
                                            name=ext['name'], 
                                            description=ext['description'], 
                                            version=ext['version'], 
                                            author=ext['author'],
                                            package=ext['package_name'], 
                                            installed=installed))

        return extlist

    def get_extension_info(self, package_name):
        """Fetch more information about an extension."""
        response = self._query("details", {"ext": package_name})

        if "error" in response:
            return {"error": response["error"]}
        else:
            response['extension_info']['installed'] = package_name in self.installed_extensions
            return response['extension_info']
