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


class ChannelServer(object):
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
        'channel_id': 'float',
        'server_id': 'float'
    }

    attribute_map = {
        'id': 'id',
        'channel_id': 'channelId',
        'server_id': 'serverId'
    }

    def __init__(self, id=None, channel_id=None, server_id=None):
        """
        ChannelServer - a model defined in Swagger
        """

        self._id = None
        self._channel_id = None
        self._server_id = None

        if id is not None:
          self.id = id
        if channel_id is not None:
          self.channel_id = channel_id
        if server_id is not None:
          self.server_id = server_id

    @property
    def id(self):
        """
        Gets the id of this ChannelServer.

        :return: The id of this ChannelServer.
        :rtype: float
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this ChannelServer.

        :param id: The id of this ChannelServer.
        :type: float
        """

        self._id = id

    @property
    def channel_id(self):
        """
        Gets the channel_id of this ChannelServer.

        :return: The channel_id of this ChannelServer.
        :rtype: float
        """
        return self._channel_id

    @channel_id.setter
    def channel_id(self, channel_id):
        """
        Sets the channel_id of this ChannelServer.

        :param channel_id: The channel_id of this ChannelServer.
        :type: float
        """

        self._channel_id = channel_id

    @property
    def server_id(self):
        """
        Gets the server_id of this ChannelServer.

        :return: The server_id of this ChannelServer.
        :rtype: float
        """
        return self._server_id

    @server_id.setter
    def server_id(self, server_id):
        """
        Sets the server_id of this ChannelServer.

        :param server_id: The server_id of this ChannelServer.
        :type: float
        """

        self._server_id = server_id

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
        if not isinstance(other, ChannelServer):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
