# coding: utf-8

"""
    College Football Data API

    This is an API for accessing all sorts of college football data.  Please note that API keys should be supplied with \"Bearer \" prepended (e.g. \"Bearer your_key\"). API keys can be acquired from the CollegeFootballData.com website.  # noqa: E501

    OpenAPI spec version: 4.2.2
    Contact: admin@collegefootballdata.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from cfbd.configuration import Configuration


class Team(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'id': 'int',
        'school': 'str',
        'mascot': 'str',
        'abbreviation': 'str',
        'alt_name_1': 'str',
        'alt_name_2': 'str',
        'alt_name_3': 'str',
        'conference': 'str',
        'division': 'str',
        'color': 'str',
        'alt_color': 'str',
        'logos': 'list[str]',
        'location': 'object'
    }

    attribute_map = {
        'id': 'id',
        'school': 'school',
        'mascot': 'mascot',
        'abbreviation': 'abbreviation',
        'alt_name_1': 'alt_name_1',
        'alt_name_2': 'alt_name_2',
        'alt_name_3': 'alt_name_3',
        'conference': 'conference',
        'division': 'division',
        'color': 'color',
        'alt_color': 'alt_color',
        'logos': 'logos',
        'location': 'location'
    }

    def __init__(self, id=None, school=None, mascot=None, abbreviation=None, alt_name_1=None, alt_name_2=None, alt_name_3=None, conference=None, division=None, color=None, alt_color=None, logos=None, location=None, _configuration=None):  # noqa: E501
        """Team - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._id = None
        self._school = None
        self._mascot = None
        self._abbreviation = None
        self._alt_name_1 = None
        self._alt_name_2 = None
        self._alt_name_3 = None
        self._conference = None
        self._division = None
        self._color = None
        self._alt_color = None
        self._logos = None
        self._location = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if school is not None:
            self.school = school
        if mascot is not None:
            self.mascot = mascot
        if abbreviation is not None:
            self.abbreviation = abbreviation
        if alt_name_1 is not None:
            self.alt_name_1 = alt_name_1
        if alt_name_2 is not None:
            self.alt_name_2 = alt_name_2
        if alt_name_3 is not None:
            self.alt_name_3 = alt_name_3
        if conference is not None:
            self.conference = conference
        if division is not None:
            self.division = division
        if color is not None:
            self.color = color
        if alt_color is not None:
            self.alt_color = alt_color
        if logos is not None:
            self.logos = logos
        if location is not None:
            self.location = location

    @property
    def id(self):
        """Gets the id of this Team.  # noqa: E501


        :return: The id of this Team.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Team.


        :param id: The id of this Team.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def school(self):
        """Gets the school of this Team.  # noqa: E501


        :return: The school of this Team.  # noqa: E501
        :rtype: str
        """
        return self._school

    @school.setter
    def school(self, school):
        """Sets the school of this Team.


        :param school: The school of this Team.  # noqa: E501
        :type: str
        """

        self._school = school

    @property
    def mascot(self):
        """Gets the mascot of this Team.  # noqa: E501


        :return: The mascot of this Team.  # noqa: E501
        :rtype: str
        """
        return self._mascot

    @mascot.setter
    def mascot(self, mascot):
        """Sets the mascot of this Team.


        :param mascot: The mascot of this Team.  # noqa: E501
        :type: str
        """

        self._mascot = mascot

    @property
    def abbreviation(self):
        """Gets the abbreviation of this Team.  # noqa: E501


        :return: The abbreviation of this Team.  # noqa: E501
        :rtype: str
        """
        return self._abbreviation

    @abbreviation.setter
    def abbreviation(self, abbreviation):
        """Sets the abbreviation of this Team.


        :param abbreviation: The abbreviation of this Team.  # noqa: E501
        :type: str
        """

        self._abbreviation = abbreviation

    @property
    def alt_name_1(self):
        """Gets the alt_name_1 of this Team.  # noqa: E501


        :return: The alt_name_1 of this Team.  # noqa: E501
        :rtype: str
        """
        return self._alt_name_1

    @alt_name_1.setter
    def alt_name_1(self, alt_name_1):
        """Sets the alt_name_1 of this Team.


        :param alt_name_1: The alt_name_1 of this Team.  # noqa: E501
        :type: str
        """

        self._alt_name_1 = alt_name_1

    @property
    def alt_name_2(self):
        """Gets the alt_name_2 of this Team.  # noqa: E501


        :return: The alt_name_2 of this Team.  # noqa: E501
        :rtype: str
        """
        return self._alt_name_2

    @alt_name_2.setter
    def alt_name_2(self, alt_name_2):
        """Sets the alt_name_2 of this Team.


        :param alt_name_2: The alt_name_2 of this Team.  # noqa: E501
        :type: str
        """

        self._alt_name_2 = alt_name_2

    @property
    def alt_name_3(self):
        """Gets the alt_name_3 of this Team.  # noqa: E501


        :return: The alt_name_3 of this Team.  # noqa: E501
        :rtype: str
        """
        return self._alt_name_3

    @alt_name_3.setter
    def alt_name_3(self, alt_name_3):
        """Sets the alt_name_3 of this Team.


        :param alt_name_3: The alt_name_3 of this Team.  # noqa: E501
        :type: str
        """

        self._alt_name_3 = alt_name_3

    @property
    def conference(self):
        """Gets the conference of this Team.  # noqa: E501


        :return: The conference of this Team.  # noqa: E501
        :rtype: str
        """
        return self._conference

    @conference.setter
    def conference(self, conference):
        """Sets the conference of this Team.


        :param conference: The conference of this Team.  # noqa: E501
        :type: str
        """

        self._conference = conference

    @property
    def division(self):
        """Gets the division of this Team.  # noqa: E501


        :return: The division of this Team.  # noqa: E501
        :rtype: str
        """
        return self._division

    @division.setter
    def division(self, division):
        """Sets the division of this Team.


        :param division: The division of this Team.  # noqa: E501
        :type: str
        """

        self._division = division

    @property
    def color(self):
        """Gets the color of this Team.  # noqa: E501


        :return: The color of this Team.  # noqa: E501
        :rtype: str
        """
        return self._color

    @color.setter
    def color(self, color):
        """Sets the color of this Team.


        :param color: The color of this Team.  # noqa: E501
        :type: str
        """

        self._color = color

    @property
    def alt_color(self):
        """Gets the alt_color of this Team.  # noqa: E501


        :return: The alt_color of this Team.  # noqa: E501
        :rtype: str
        """
        return self._alt_color

    @alt_color.setter
    def alt_color(self, alt_color):
        """Sets the alt_color of this Team.


        :param alt_color: The alt_color of this Team.  # noqa: E501
        :type: str
        """

        self._alt_color = alt_color

    @property
    def logos(self):
        """Gets the logos of this Team.  # noqa: E501


        :return: The logos of this Team.  # noqa: E501
        :rtype: list[str]
        """
        return self._logos

    @logos.setter
    def logos(self, logos):
        """Sets the logos of this Team.


        :param logos: The logos of this Team.  # noqa: E501
        :type: list[str]
        """

        self._logos = logos

    @property
    def location(self):
        """Gets the location of this Team.  # noqa: E501


        :return: The location of this Team.  # noqa: E501
        :rtype: object
        """
        return self._location

    @location.setter
    def location(self, location):
        """Sets the location of this Team.


        :param location: The location of this Team.  # noqa: E501
        :type: object
        """

        self._location = location

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
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
        if issubclass(Team, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Team):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Team):
            return True

        return self.to_dict() != other.to_dict()
