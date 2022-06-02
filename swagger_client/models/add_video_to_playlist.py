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


class AddVideoToPlaylist(object):
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
        'video_ids': 'list[str]',
        'number_of_playlist': 'float',
        'status': 'str',
        'id': 'float',
        'sub_category_id': 'float',
        'account_id': 'float',
        'created_at': 'datetime',
        'updated_at': 'datetime'
    }

    attribute_map = {
        'video_ids': 'videoIds',
        'number_of_playlist': 'numberOfPlaylist',
        'status': 'status',
        'id': 'id',
        'sub_category_id': 'subCategoryId',
        'account_id': 'accountId',
        'created_at': 'createdAt',
        'updated_at': 'updatedAt'
    }

    def __init__(self, video_ids=None, number_of_playlist=None, status=None, id=None, sub_category_id=None, account_id=None, created_at=None, updated_at=None):
        """
        AddVideoToPlaylist - a model defined in Swagger
        """

        self._video_ids = None
        self._number_of_playlist = None
        self._status = None
        self._id = None
        self._sub_category_id = None
        self._account_id = None
        self._created_at = None
        self._updated_at = None

        if video_ids is not None:
          self.video_ids = video_ids
        if number_of_playlist is not None:
          self.number_of_playlist = number_of_playlist
        if status is not None:
          self.status = status
        if id is not None:
          self.id = id
        if sub_category_id is not None:
          self.sub_category_id = sub_category_id
        if account_id is not None:
          self.account_id = account_id
        if created_at is not None:
          self.created_at = created_at
        if updated_at is not None:
          self.updated_at = updated_at

    @property
    def video_ids(self):
        """
        Gets the video_ids of this AddVideoToPlaylist.

        :return: The video_ids of this AddVideoToPlaylist.
        :rtype: list[str]
        """
        return self._video_ids

    @video_ids.setter
    def video_ids(self, video_ids):
        """
        Sets the video_ids of this AddVideoToPlaylist.

        :param video_ids: The video_ids of this AddVideoToPlaylist.
        :type: list[str]
        """

        self._video_ids = video_ids

    @property
    def number_of_playlist(self):
        """
        Gets the number_of_playlist of this AddVideoToPlaylist.

        :return: The number_of_playlist of this AddVideoToPlaylist.
        :rtype: float
        """
        return self._number_of_playlist

    @number_of_playlist.setter
    def number_of_playlist(self, number_of_playlist):
        """
        Sets the number_of_playlist of this AddVideoToPlaylist.

        :param number_of_playlist: The number_of_playlist of this AddVideoToPlaylist.
        :type: float
        """

        self._number_of_playlist = number_of_playlist

    @property
    def status(self):
        """
        Gets the status of this AddVideoToPlaylist.

        :return: The status of this AddVideoToPlaylist.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        Sets the status of this AddVideoToPlaylist.

        :param status: The status of this AddVideoToPlaylist.
        :type: str
        """

        self._status = status

    @property
    def id(self):
        """
        Gets the id of this AddVideoToPlaylist.

        :return: The id of this AddVideoToPlaylist.
        :rtype: float
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this AddVideoToPlaylist.

        :param id: The id of this AddVideoToPlaylist.
        :type: float
        """

        self._id = id

    @property
    def sub_category_id(self):
        """
        Gets the sub_category_id of this AddVideoToPlaylist.

        :return: The sub_category_id of this AddVideoToPlaylist.
        :rtype: float
        """
        return self._sub_category_id

    @sub_category_id.setter
    def sub_category_id(self, sub_category_id):
        """
        Sets the sub_category_id of this AddVideoToPlaylist.

        :param sub_category_id: The sub_category_id of this AddVideoToPlaylist.
        :type: float
        """

        self._sub_category_id = sub_category_id

    @property
    def account_id(self):
        """
        Gets the account_id of this AddVideoToPlaylist.

        :return: The account_id of this AddVideoToPlaylist.
        :rtype: float
        """
        return self._account_id

    @account_id.setter
    def account_id(self, account_id):
        """
        Sets the account_id of this AddVideoToPlaylist.

        :param account_id: The account_id of this AddVideoToPlaylist.
        :type: float
        """

        self._account_id = account_id

    @property
    def created_at(self):
        """
        Gets the created_at of this AddVideoToPlaylist.

        :return: The created_at of this AddVideoToPlaylist.
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """
        Sets the created_at of this AddVideoToPlaylist.

        :param created_at: The created_at of this AddVideoToPlaylist.
        :type: datetime
        """

        self._created_at = created_at

    @property
    def updated_at(self):
        """
        Gets the updated_at of this AddVideoToPlaylist.

        :return: The updated_at of this AddVideoToPlaylist.
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """
        Sets the updated_at of this AddVideoToPlaylist.

        :param updated_at: The updated_at of this AddVideoToPlaylist.
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
        if not isinstance(other, AddVideoToPlaylist):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other