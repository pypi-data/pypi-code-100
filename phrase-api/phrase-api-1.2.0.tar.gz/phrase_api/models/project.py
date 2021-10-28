# coding: utf-8

"""
    Phrase API Reference

    The version of the OpenAPI document: 2.0.0
    Contact: support@phrase.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from phrase_api.configuration import Configuration


class Project(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'id': 'str',
        'name': 'str',
        'slug': 'str',
        'main_format': 'str',
        'project_image_url': 'str',
        'account': 'Account',
        'space': 'Space1',
        'created_at': 'datetime',
        'updated_at': 'datetime'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'slug': 'slug',
        'main_format': 'main_format',
        'project_image_url': 'project_image_url',
        'account': 'account',
        'space': 'space',
        'created_at': 'created_at',
        'updated_at': 'updated_at'
    }

    def __init__(self, id=None, name=None, slug=None, main_format=None, project_image_url=None, account=None, space=None, created_at=None, updated_at=None, local_vars_configuration=None):  # noqa: E501
        """Project - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._name = None
        self._slug = None
        self._main_format = None
        self._project_image_url = None
        self._account = None
        self._space = None
        self._created_at = None
        self._updated_at = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if slug is not None:
            self.slug = slug
        if main_format is not None:
            self.main_format = main_format
        if project_image_url is not None:
            self.project_image_url = project_image_url
        if account is not None:
            self.account = account
        if space is not None:
            self.space = space
        if created_at is not None:
            self.created_at = created_at
        if updated_at is not None:
            self.updated_at = updated_at

    @property
    def id(self):
        """Gets the id of this Project.  # noqa: E501


        :return: The id of this Project.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Project.


        :param id: The id of this Project.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this Project.  # noqa: E501


        :return: The name of this Project.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Project.


        :param name: The name of this Project.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def slug(self):
        """Gets the slug of this Project.  # noqa: E501


        :return: The slug of this Project.  # noqa: E501
        :rtype: str
        """
        return self._slug

    @slug.setter
    def slug(self, slug):
        """Sets the slug of this Project.


        :param slug: The slug of this Project.  # noqa: E501
        :type: str
        """

        self._slug = slug

    @property
    def main_format(self):
        """Gets the main_format of this Project.  # noqa: E501


        :return: The main_format of this Project.  # noqa: E501
        :rtype: str
        """
        return self._main_format

    @main_format.setter
    def main_format(self, main_format):
        """Sets the main_format of this Project.


        :param main_format: The main_format of this Project.  # noqa: E501
        :type: str
        """

        self._main_format = main_format

    @property
    def project_image_url(self):
        """Gets the project_image_url of this Project.  # noqa: E501


        :return: The project_image_url of this Project.  # noqa: E501
        :rtype: str
        """
        return self._project_image_url

    @project_image_url.setter
    def project_image_url(self, project_image_url):
        """Sets the project_image_url of this Project.


        :param project_image_url: The project_image_url of this Project.  # noqa: E501
        :type: str
        """

        self._project_image_url = project_image_url

    @property
    def account(self):
        """Gets the account of this Project.  # noqa: E501


        :return: The account of this Project.  # noqa: E501
        :rtype: Account
        """
        return self._account

    @account.setter
    def account(self, account):
        """Sets the account of this Project.


        :param account: The account of this Project.  # noqa: E501
        :type: Account
        """

        self._account = account

    @property
    def space(self):
        """Gets the space of this Project.  # noqa: E501


        :return: The space of this Project.  # noqa: E501
        :rtype: Space1
        """
        return self._space

    @space.setter
    def space(self, space):
        """Sets the space of this Project.


        :param space: The space of this Project.  # noqa: E501
        :type: Space1
        """

        self._space = space

    @property
    def created_at(self):
        """Gets the created_at of this Project.  # noqa: E501


        :return: The created_at of this Project.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this Project.


        :param created_at: The created_at of this Project.  # noqa: E501
        :type: datetime
        """

        self._created_at = created_at

    @property
    def updated_at(self):
        """Gets the updated_at of this Project.  # noqa: E501


        :return: The updated_at of this Project.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this Project.


        :param updated_at: The updated_at of this Project.  # noqa: E501
        :type: datetime
        """

        self._updated_at = updated_at

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Project):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Project):
            return True

        return self.to_dict() != other.to_dict()
