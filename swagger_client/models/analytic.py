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


class Analytic(object):
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
        'total_video': 'float',
        'total_video_upload': 'float',
        'total_video_error': 'float',
        'view': 'float',
        'id': 'float',
        'channel_id': 'float',
        'account_id': 'float',
        'created_at': 'datetime',
        'updated_at': 'datetime'
    }

    attribute_map = {
        'total_video': 'totalVideo',
        'total_video_upload': 'totalVideoUpload',
        'total_video_error': 'totalVideoError',
        'view': 'view',
        'id': 'id',
        'channel_id': 'channelId',
        'account_id': 'accountId',
        'created_at': 'createdAt',
        'updated_at': 'updatedAt'
    }

    def __init__(self, total_video=None, total_video_upload=None, total_video_error=None, view=None, id=None, channel_id=None, account_id=None, created_at=None, updated_at=None):
        """
        Analytic - a model defined in Swagger
        """

        self._total_video = None
        self._total_video_upload = None
        self._total_video_error = None
        self._view = None
        self._id = None
        self._channel_id = None
        self._account_id = None
        self._created_at = None
        self._updated_at = None

        if total_video is not None:
          self.total_video = total_video
        if total_video_upload is not None:
          self.total_video_upload = total_video_upload
        if total_video_error is not None:
          self.total_video_error = total_video_error
        if view is not None:
          self.view = view
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
    def total_video(self):
        """
        Gets the total_video of this Analytic.

        :return: The total_video of this Analytic.
        :rtype: float
        """
        return self._total_video

    @total_video.setter
    def total_video(self, total_video):
        """
        Sets the total_video of this Analytic.

        :param total_video: The total_video of this Analytic.
        :type: float
        """

        self._total_video = total_video

    @property
    def total_video_upload(self):
        """
        Gets the total_video_upload of this Analytic.

        :return: The total_video_upload of this Analytic.
        :rtype: float
        """
        return self._total_video_upload

    @total_video_upload.setter
    def total_video_upload(self, total_video_upload):
        """
        Sets the total_video_upload of this Analytic.

        :param total_video_upload: The total_video_upload of this Analytic.
        :type: float
        """

        self._total_video_upload = total_video_upload

    @property
    def total_video_error(self):
        """
        Gets the total_video_error of this Analytic.

        :return: The total_video_error of this Analytic.
        :rtype: float
        """
        return self._total_video_error

    @total_video_error.setter
    def total_video_error(self, total_video_error):
        """
        Sets the total_video_error of this Analytic.

        :param total_video_error: The total_video_error of this Analytic.
        :type: float
        """

        self._total_video_error = total_video_error

    @property
    def view(self):
        """
        Gets the view of this Analytic.

        :return: The view of this Analytic.
        :rtype: float
        """
        return self._view

    @view.setter
    def view(self, view):
        """
        Sets the view of this Analytic.

        :param view: The view of this Analytic.
        :type: float
        """

        self._view = view

    @property
    def id(self):
        """
        Gets the id of this Analytic.

        :return: The id of this Analytic.
        :rtype: float
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this Analytic.

        :param id: The id of this Analytic.
        :type: float
        """

        self._id = id

    @property
    def channel_id(self):
        """
        Gets the channel_id of this Analytic.

        :return: The channel_id of this Analytic.
        :rtype: float
        """
        return self._channel_id

    @channel_id.setter
    def channel_id(self, channel_id):
        """
        Sets the channel_id of this Analytic.

        :param channel_id: The channel_id of this Analytic.
        :type: float
        """

        self._channel_id = channel_id

    @property
    def account_id(self):
        """
        Gets the account_id of this Analytic.

        :return: The account_id of this Analytic.
        :rtype: float
        """
        return self._account_id

    @account_id.setter
    def account_id(self, account_id):
        """
        Sets the account_id of this Analytic.

        :param account_id: The account_id of this Analytic.
        :type: float
        """

        self._account_id = account_id

    @property
    def created_at(self):
        """
        Gets the created_at of this Analytic.

        :return: The created_at of this Analytic.
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """
        Sets the created_at of this Analytic.

        :param created_at: The created_at of this Analytic.
        :type: datetime
        """

        self._created_at = created_at

    @property
    def updated_at(self):
        """
        Gets the updated_at of this Analytic.

        :return: The updated_at of this Analytic.
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """
        Sets the updated_at of this Analytic.

        :param updated_at: The updated_at of this Analytic.
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
        if not isinstance(other, Analytic):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other