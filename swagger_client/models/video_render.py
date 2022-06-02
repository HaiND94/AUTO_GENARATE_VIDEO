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


class VideoRender(object):
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
        'link_source': 'str',
        'type_source': 'str',
        'type_render': 'str',
        'video_id': 'str',
        'status': 'bool',
        'is_live': 'bool',
        'id': 'float',
        'channel_id': 'float',
        'account_id': 'float',
        'created_at': 'datetime',
        'updated_at': 'datetime'
    }

    attribute_map = {
        'link_source': 'linkSource',
        'type_source': 'typeSource',
        'type_render': 'typeRender',
        'video_id': 'videoId',
        'status': 'status',
        'is_live': 'isLive',
        'id': 'id',
        'channel_id': 'channelId',
        'account_id': 'accountId',
        'created_at': 'createdAt',
        'updated_at': 'updatedAt'
    }

    def __init__(self, link_source=None, type_source=None, type_render=None, video_id=None, status=None, is_live=None, id=None, channel_id=None, account_id=None, created_at=None, updated_at=None):
        """
        VideoRender - a model defined in Swagger
        """

        self._link_source = None
        self._type_source = None
        self._type_render = None
        self._video_id = None
        self._status = None
        self._is_live = None
        self._id = None
        self._channel_id = None
        self._account_id = None
        self._created_at = None
        self._updated_at = None

        if link_source is not None:
          self.link_source = link_source
        if type_source is not None:
          self.type_source = type_source
        if type_render is not None:
          self.type_render = type_render
        if video_id is not None:
          self.video_id = video_id
        if status is not None:
          self.status = status
        if is_live is not None:
          self.is_live = is_live
        if id is not None:
          self.id = id
        if channel_id is not None:
          self.channel_id = channel_id
        if account_id is not None:
          self.account_id = account_id
        if created_at is not None:
          self.created_at = created_at
        if updated_at is not None:
          self.updated_at = updated_at

    @property
    def link_source(self):
        """
        Gets the link_source of this VideoRender.

        :return: The link_source of this VideoRender.
        :rtype: str
        """
        return self._link_source

    @link_source.setter
    def link_source(self, link_source):
        """
        Sets the link_source of this VideoRender.

        :param link_source: The link_source of this VideoRender.
        :type: str
        """

        self._link_source = link_source

    @property
    def type_source(self):
        """
        Gets the type_source of this VideoRender.

        :return: The type_source of this VideoRender.
        :rtype: str
        """
        return self._type_source

    @type_source.setter
    def type_source(self, type_source):
        """
        Sets the type_source of this VideoRender.

        :param type_source: The type_source of this VideoRender.
        :type: str
        """

        self._type_source = type_source

    @property
    def type_render(self):
        """
        Gets the type_render of this VideoRender.

        :return: The type_render of this VideoRender.
        :rtype: str
        """
        return self._type_render

    @type_render.setter
    def type_render(self, type_render):
        """
        Sets the type_render of this VideoRender.

        :param type_render: The type_render of this VideoRender.
        :type: str
        """

        self._type_render = type_render

    @property
    def video_id(self):
        """
        Gets the video_id of this VideoRender.

        :return: The video_id of this VideoRender.
        :rtype: str
        """
        return self._video_id

    @video_id.setter
    def video_id(self, video_id):
        """
        Sets the video_id of this VideoRender.

        :param video_id: The video_id of this VideoRender.
        :type: str
        """

        self._video_id = video_id

    @property
    def status(self):
        """
        Gets the status of this VideoRender.

        :return: The status of this VideoRender.
        :rtype: bool
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        Sets the status of this VideoRender.

        :param status: The status of this VideoRender.
        :type: bool
        """

        self._status = status

    @property
    def is_live(self):
        """
        Gets the is_live of this VideoRender.

        :return: The is_live of this VideoRender.
        :rtype: bool
        """
        return self._is_live

    @is_live.setter
    def is_live(self, is_live):
        """
        Sets the is_live of this VideoRender.

        :param is_live: The is_live of this VideoRender.
        :type: bool
        """

        self._is_live = is_live

    @property
    def id(self):
        """
        Gets the id of this VideoRender.

        :return: The id of this VideoRender.
        :rtype: float
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this VideoRender.

        :param id: The id of this VideoRender.
        :type: float
        """

        self._id = id

    @property
    def channel_id(self):
        """
        Gets the channel_id of this VideoRender.

        :return: The channel_id of this VideoRender.
        :rtype: float
        """
        return self._channel_id

    @channel_id.setter
    def channel_id(self, channel_id):
        """
        Sets the channel_id of this VideoRender.

        :param channel_id: The channel_id of this VideoRender.
        :type: float
        """

        self._channel_id = channel_id

    @property
    def account_id(self):
        """
        Gets the account_id of this VideoRender.

        :return: The account_id of this VideoRender.
        :rtype: float
        """
        return self._account_id

    @account_id.setter
    def account_id(self, account_id):
        """
        Sets the account_id of this VideoRender.

        :param account_id: The account_id of this VideoRender.
        :type: float
        """

        self._account_id = account_id

    @property
    def created_at(self):
        """
        Gets the created_at of this VideoRender.

        :return: The created_at of this VideoRender.
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """
        Sets the created_at of this VideoRender.

        :param created_at: The created_at of this VideoRender.
        :type: datetime
        """

        self._created_at = created_at

    @property
    def updated_at(self):
        """
        Gets the updated_at of this VideoRender.

        :return: The updated_at of this VideoRender.
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """
        Sets the updated_at of this VideoRender.

        :param updated_at: The updated_at of this VideoRender.
        :type: datetime
        """

        self._updated_at = updated_at

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
        if not isinstance(other, VideoRender):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other