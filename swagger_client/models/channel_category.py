# coding: utf-8

"""
    YTB-CRAWLER

    YTB-CRAWLER

    OpenAPI spec version: 1.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class ChannelCategory(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
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
        'id': 'float',
        'sub_category_id': 'float',
        'channel_pll_id': 'float'
    }

    attribute_map = {
        'id': 'id',
        'sub_category_id': 'subCategoryId',
        'channel_pll_id': 'channelPllId'
    }

    def __init__(self, id=None, sub_category_id=None, channel_pll_id=None):
        """
        ChannelCategory - a model defined in Swagger
        """

        self._id = None
        self._sub_category_id = None
        self._channel_pll_id = None

        if id is not None:
          self.id = id
        if sub_category_id is not None:
          self.sub_category_id = sub_category_id
        if channel_pll_id is not None:
          self.channel_pll_id = channel_pll_id

    @property
    def id(self):
        """
        Gets the id of this ChannelCategory.

        :return: The id of this ChannelCategory.
        :rtype: float
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this ChannelCategory.

        :param id: The id of this ChannelCategory.
        :type: float
        """

        self._id = id

    @property
    def sub_category_id(self):
        """
        Gets the sub_category_id of this ChannelCategory.

        :return: The sub_category_id of this ChannelCategory.
        :rtype: float
        """
        return self._sub_category_id

    @sub_category_id.setter
    def sub_category_id(self, sub_category_id):
        """
        Sets the sub_category_id of this ChannelCategory.

        :param sub_category_id: The sub_category_id of this ChannelCategory.
        :type: float
        """

        self._sub_category_id = sub_category_id

    @property
    def channel_pll_id(self):
        """
        Gets the channel_pll_id of this ChannelCategory.

        :return: The channel_pll_id of this ChannelCategory.
        :rtype: float
        """
        return self._channel_pll_id

    @channel_pll_id.setter
    def channel_pll_id(self, channel_pll_id):
        """
        Sets the channel_pll_id of this ChannelCategory.

        :param channel_pll_id: The channel_pll_id of this ChannelCategory.
        :type: float
        """

        self._channel_pll_id = channel_pll_id

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
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
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        if not isinstance(other, ChannelCategory):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other