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


class UploadCreateParameters(object):
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
        'branch': 'str',
        'file': 'file',
        'file_format': 'str',
        'locale_id': 'str',
        'tags': 'str',
        'update_translations': 'bool',
        'update_descriptions': 'bool',
        'convert_emoji': 'bool',
        'skip_upload_tags': 'bool',
        'skip_unverification': 'bool',
        'file_encoding': 'str',
        'locale_mapping': 'object',
        'format_options': 'object',
        'autotranslate': 'bool',
        'mark_reviewed': 'bool'
    }

    attribute_map = {
        'branch': 'branch',
        'file': 'file',
        'file_format': 'file_format',
        'locale_id': 'locale_id',
        'tags': 'tags',
        'update_translations': 'update_translations',
        'update_descriptions': 'update_descriptions',
        'convert_emoji': 'convert_emoji',
        'skip_upload_tags': 'skip_upload_tags',
        'skip_unverification': 'skip_unverification',
        'file_encoding': 'file_encoding',
        'locale_mapping': 'locale_mapping',
        'format_options': 'format_options',
        'autotranslate': 'autotranslate',
        'mark_reviewed': 'mark_reviewed'
    }

    def __init__(self, branch=None, file=None, file_format=None, locale_id=None, tags=None, update_translations=None, update_descriptions=None, convert_emoji=None, skip_upload_tags=None, skip_unverification=None, file_encoding=None, locale_mapping=None, format_options=None, autotranslate=None, mark_reviewed=None, local_vars_configuration=None):  # noqa: E501
        """UploadCreateParameters - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._branch = None
        self._file = None
        self._file_format = None
        self._locale_id = None
        self._tags = None
        self._update_translations = None
        self._update_descriptions = None
        self._convert_emoji = None
        self._skip_upload_tags = None
        self._skip_unverification = None
        self._file_encoding = None
        self._locale_mapping = None
        self._format_options = None
        self._autotranslate = None
        self._mark_reviewed = None
        self.discriminator = None

        if branch is not None:
            self.branch = branch
        if file is not None:
            self.file = file
        if file_format is not None:
            self.file_format = file_format
        if locale_id is not None:
            self.locale_id = locale_id
        if tags is not None:
            self.tags = tags
        if update_translations is not None:
            self.update_translations = update_translations
        if update_descriptions is not None:
            self.update_descriptions = update_descriptions
        if convert_emoji is not None:
            self.convert_emoji = convert_emoji
        if skip_upload_tags is not None:
            self.skip_upload_tags = skip_upload_tags
        if skip_unverification is not None:
            self.skip_unverification = skip_unverification
        if file_encoding is not None:
            self.file_encoding = file_encoding
        if locale_mapping is not None:
            self.locale_mapping = locale_mapping
        if format_options is not None:
            self.format_options = format_options
        if autotranslate is not None:
            self.autotranslate = autotranslate
        if mark_reviewed is not None:
            self.mark_reviewed = mark_reviewed

    @property
    def branch(self):
        """Gets the branch of this UploadCreateParameters.  # noqa: E501

        specify the branch to use  # noqa: E501

        :return: The branch of this UploadCreateParameters.  # noqa: E501
        :rtype: str
        """
        return self._branch

    @branch.setter
    def branch(self, branch):
        """Sets the branch of this UploadCreateParameters.

        specify the branch to use  # noqa: E501

        :param branch: The branch of this UploadCreateParameters.  # noqa: E501
        :type: str
        """

        self._branch = branch

    @property
    def file(self):
        """Gets the file of this UploadCreateParameters.  # noqa: E501

        File to be imported  # noqa: E501

        :return: The file of this UploadCreateParameters.  # noqa: E501
        :rtype: file
        """
        return self._file

    @file.setter
    def file(self, file):
        """Sets the file of this UploadCreateParameters.

        File to be imported  # noqa: E501

        :param file: The file of this UploadCreateParameters.  # noqa: E501
        :type: file
        """

        self._file = file

    @property
    def file_format(self):
        """Gets the file_format of this UploadCreateParameters.  # noqa: E501

        File format. Auto-detected when possible and not specified.  # noqa: E501

        :return: The file_format of this UploadCreateParameters.  # noqa: E501
        :rtype: str
        """
        return self._file_format

    @file_format.setter
    def file_format(self, file_format):
        """Sets the file_format of this UploadCreateParameters.

        File format. Auto-detected when possible and not specified.  # noqa: E501

        :param file_format: The file_format of this UploadCreateParameters.  # noqa: E501
        :type: str
        """

        self._file_format = file_format

    @property
    def locale_id(self):
        """Gets the locale_id of this UploadCreateParameters.  # noqa: E501

        Locale of the file's content. Can be the name or public id of the locale. Preferred is the public id.  # noqa: E501

        :return: The locale_id of this UploadCreateParameters.  # noqa: E501
        :rtype: str
        """
        return self._locale_id

    @locale_id.setter
    def locale_id(self, locale_id):
        """Sets the locale_id of this UploadCreateParameters.

        Locale of the file's content. Can be the name or public id of the locale. Preferred is the public id.  # noqa: E501

        :param locale_id: The locale_id of this UploadCreateParameters.  # noqa: E501
        :type: str
        """

        self._locale_id = locale_id

    @property
    def tags(self):
        """Gets the tags of this UploadCreateParameters.  # noqa: E501

        List of tags separated by comma to be associated with the new keys contained in the upload.  # noqa: E501

        :return: The tags of this UploadCreateParameters.  # noqa: E501
        :rtype: str
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this UploadCreateParameters.

        List of tags separated by comma to be associated with the new keys contained in the upload.  # noqa: E501

        :param tags: The tags of this UploadCreateParameters.  # noqa: E501
        :type: str
        """

        self._tags = tags

    @property
    def update_translations(self):
        """Gets the update_translations of this UploadCreateParameters.  # noqa: E501

        Indicates whether existing translations should be updated with the file content.  # noqa: E501

        :return: The update_translations of this UploadCreateParameters.  # noqa: E501
        :rtype: bool
        """
        return self._update_translations

    @update_translations.setter
    def update_translations(self, update_translations):
        """Sets the update_translations of this UploadCreateParameters.

        Indicates whether existing translations should be updated with the file content.  # noqa: E501

        :param update_translations: The update_translations of this UploadCreateParameters.  # noqa: E501
        :type: bool
        """

        self._update_translations = update_translations

    @property
    def update_descriptions(self):
        """Gets the update_descriptions of this UploadCreateParameters.  # noqa: E501

        Existing key descriptions will be updated with the file content. Empty descriptions overwrite existing descriptions.  # noqa: E501

        :return: The update_descriptions of this UploadCreateParameters.  # noqa: E501
        :rtype: bool
        """
        return self._update_descriptions

    @update_descriptions.setter
    def update_descriptions(self, update_descriptions):
        """Sets the update_descriptions of this UploadCreateParameters.

        Existing key descriptions will be updated with the file content. Empty descriptions overwrite existing descriptions.  # noqa: E501

        :param update_descriptions: The update_descriptions of this UploadCreateParameters.  # noqa: E501
        :type: bool
        """

        self._update_descriptions = update_descriptions

    @property
    def convert_emoji(self):
        """Gets the convert_emoji of this UploadCreateParameters.  # noqa: E501

        This option is obsolete. Providing the option will cause a bad request error.  # noqa: E501

        :return: The convert_emoji of this UploadCreateParameters.  # noqa: E501
        :rtype: bool
        """
        return self._convert_emoji

    @convert_emoji.setter
    def convert_emoji(self, convert_emoji):
        """Sets the convert_emoji of this UploadCreateParameters.

        This option is obsolete. Providing the option will cause a bad request error.  # noqa: E501

        :param convert_emoji: The convert_emoji of this UploadCreateParameters.  # noqa: E501
        :type: bool
        """

        self._convert_emoji = convert_emoji

    @property
    def skip_upload_tags(self):
        """Gets the skip_upload_tags of this UploadCreateParameters.  # noqa: E501

        Indicates whether the upload should not create upload tags.  # noqa: E501

        :return: The skip_upload_tags of this UploadCreateParameters.  # noqa: E501
        :rtype: bool
        """
        return self._skip_upload_tags

    @skip_upload_tags.setter
    def skip_upload_tags(self, skip_upload_tags):
        """Sets the skip_upload_tags of this UploadCreateParameters.

        Indicates whether the upload should not create upload tags.  # noqa: E501

        :param skip_upload_tags: The skip_upload_tags of this UploadCreateParameters.  # noqa: E501
        :type: bool
        """

        self._skip_upload_tags = skip_upload_tags

    @property
    def skip_unverification(self):
        """Gets the skip_unverification of this UploadCreateParameters.  # noqa: E501

        Indicates whether the upload should unverify updated translations.  # noqa: E501

        :return: The skip_unverification of this UploadCreateParameters.  # noqa: E501
        :rtype: bool
        """
        return self._skip_unverification

    @skip_unverification.setter
    def skip_unverification(self, skip_unverification):
        """Sets the skip_unverification of this UploadCreateParameters.

        Indicates whether the upload should unverify updated translations.  # noqa: E501

        :param skip_unverification: The skip_unverification of this UploadCreateParameters.  # noqa: E501
        :type: bool
        """

        self._skip_unverification = skip_unverification

    @property
    def file_encoding(self):
        """Gets the file_encoding of this UploadCreateParameters.  # noqa: E501

        Enforces a specific encoding on the file contents. Valid options are \"UTF-8\", \"UTF-16\" and \"ISO-8859-1\".  # noqa: E501

        :return: The file_encoding of this UploadCreateParameters.  # noqa: E501
        :rtype: str
        """
        return self._file_encoding

    @file_encoding.setter
    def file_encoding(self, file_encoding):
        """Sets the file_encoding of this UploadCreateParameters.

        Enforces a specific encoding on the file contents. Valid options are \"UTF-8\", \"UTF-16\" and \"ISO-8859-1\".  # noqa: E501

        :param file_encoding: The file_encoding of this UploadCreateParameters.  # noqa: E501
        :type: str
        """

        self._file_encoding = file_encoding

    @property
    def locale_mapping(self):
        """Gets the locale_mapping of this UploadCreateParameters.  # noqa: E501

        Optional, format specific mapping between locale names and the columns the translations to those locales are contained in.  # noqa: E501

        :return: The locale_mapping of this UploadCreateParameters.  # noqa: E501
        :rtype: object
        """
        return self._locale_mapping

    @locale_mapping.setter
    def locale_mapping(self, locale_mapping):
        """Sets the locale_mapping of this UploadCreateParameters.

        Optional, format specific mapping between locale names and the columns the translations to those locales are contained in.  # noqa: E501

        :param locale_mapping: The locale_mapping of this UploadCreateParameters.  # noqa: E501
        :type: object
        """

        self._locale_mapping = locale_mapping

    @property
    def format_options(self):
        """Gets the format_options of this UploadCreateParameters.  # noqa: E501

        Additional options available for specific formats. See our format guide for complete list.  # noqa: E501

        :return: The format_options of this UploadCreateParameters.  # noqa: E501
        :rtype: object
        """
        return self._format_options

    @format_options.setter
    def format_options(self, format_options):
        """Sets the format_options of this UploadCreateParameters.

        Additional options available for specific formats. See our format guide for complete list.  # noqa: E501

        :param format_options: The format_options of this UploadCreateParameters.  # noqa: E501
        :type: object
        """

        self._format_options = format_options

    @property
    def autotranslate(self):
        """Gets the autotranslate of this UploadCreateParameters.  # noqa: E501

        If set, translations for the uploaded language will be fetched automatically.  # noqa: E501

        :return: The autotranslate of this UploadCreateParameters.  # noqa: E501
        :rtype: bool
        """
        return self._autotranslate

    @autotranslate.setter
    def autotranslate(self, autotranslate):
        """Sets the autotranslate of this UploadCreateParameters.

        If set, translations for the uploaded language will be fetched automatically.  # noqa: E501

        :param autotranslate: The autotranslate of this UploadCreateParameters.  # noqa: E501
        :type: bool
        """

        self._autotranslate = autotranslate

    @property
    def mark_reviewed(self):
        """Gets the mark_reviewed of this UploadCreateParameters.  # noqa: E501

        Indicated whether the imported translations should be marked as reviewed. This setting is available if the review workflow (currently beta) is enabled for the project.  # noqa: E501

        :return: The mark_reviewed of this UploadCreateParameters.  # noqa: E501
        :rtype: bool
        """
        return self._mark_reviewed

    @mark_reviewed.setter
    def mark_reviewed(self, mark_reviewed):
        """Sets the mark_reviewed of this UploadCreateParameters.

        Indicated whether the imported translations should be marked as reviewed. This setting is available if the review workflow (currently beta) is enabled for the project.  # noqa: E501

        :param mark_reviewed: The mark_reviewed of this UploadCreateParameters.  # noqa: E501
        :type: bool
        """

        self._mark_reviewed = mark_reviewed

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
        if not isinstance(other, UploadCreateParameters):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, UploadCreateParameters):
            return True

        return self.to_dict() != other.to_dict()
