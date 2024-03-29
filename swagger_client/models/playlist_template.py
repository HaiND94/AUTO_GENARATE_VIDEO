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


class PlaylistTemplate(object):
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
        'name': 'str',
        'playlist_id': 'str',
        'views': 'float',
        'is_created': 'bool',
        'id': 'float',
        'created_at': 'datetime',
        'updated_at': 'datetime',
        'sub_category_id': 'float'
    }

    attribute_map = {
        'name': 'name',
        'playlist_id': 'playlistId',
        'views': 'views',
        'is_created': 'isCreated',
        'id': 'id',
        'created_at': 'createdAt',
        'updated_at': 'updatedAt',
        'sub_category_id': 'subCategoryId'
    }

    def __init__(self, name=None, playlist_id=None, views=None, is_created=None, id=None, created_at=None, updated_at=None, sub_category_id=None):
        """
        PlaylistTemplate - a model defined in Swagger
        """

        self._name = None
        self._playlist_id = None
        self._views = None
        self._is_created = None
        self._id = None
        self._created_at = None
        self._updated_at = None
        self._sub_category_id = None

        if name is not None:
          self.name = name
        if playlist_id is not None:
          self.playlist_id = playlist_id
        if views is not None:
          self.views = views
        if is_created is not None:
          self.is_created = is_created
        if id is not None:
          self.id = id
        if created_at is not None:
          self.created_at = created_at
        if updated_at is not None:
          self.updated_at = updated_at
        if sub_category_id is not None:
          self.sub_category_id = sub_category_id

    @property
    def name(self):
        """
        Gets the name of this PlaylistTemplate.

        :return: The name of this PlaylistTemplate.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this PlaylistTemplate.

        :param name: The name of this PlaylistTemplate.
        :type: str
        """

        self._name = name

    @property
    def playlist_id(self):
        """
        Gets the playlist_id of this PlaylistTemplate.

        :return: The playlist_id of this PlaylistTemplate.
        :rtype: str
        """
        return self._playlist_id

    @playlist_id.setter
    def playlist_id(self, playlist_id):
        """
        Sets the playlist_id of this PlaylistTemplate.

        :param playlist_id: The playlist_id of this PlaylistTemplate.
        :type: str
        """

        self._playlist_id = playlist_id

    @property
    def views(self):
        """
        Gets the views of this PlaylistTemplate.

        :return: The views of this PlaylistTemplate.
        :rtype: float
        """
        return self._views

    @views.setter
    def views(self, views):
        """
        Sets the views of this PlaylistTemplate.

        :param views: The views of this PlaylistTemplate.
        :type: float
        """

        self._views = views

    @property
    def is_created(self):
        """
        Gets the is_created of this PlaylistTemplate.

        :return: The is_created of this PlaylistTemplate.
        :rtype: bool
        """
        return self._is_created

    @is_created.setter
    def is_created(self, is_created):
        """
        Sets the is_created of this PlaylistTemplate.

        :param is_created: The is_created of this PlaylistTemplate.
        :type: bool
        """

        self._is_created = is_created

    @property
    def id(self):
        """
        Gets the id of this PlaylistTemplate.

        :return: The id of this PlaylistTemplate.
        :rtype: float
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this PlaylistTemplate.

        :param id: The id of this PlaylistTemplate.
        :type: float
        """

        self._id = id

    @property
    def created_at(self):
        """
        Gets the created_at of this PlaylistTemplate.

        :return: The created_at of this PlaylistTemplate.
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """
        Sets the created_at of this PlaylistTemplate.

        :param created_at: The created_at of this PlaylistTemplate.
        :type: datetime
        """

        self._created_at = created_at

    @property
    def updated_at(self):
        """
        Gets the updated_at of this PlaylistTemplate.

        :return: The updated_at of this PlaylistTemplate.
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """
        Sets the updated_at of this PlaylistTemplate.

        :param updated_at: The updated_at of this PlaylistTemplate.
        :type: datetime
        """

        self._updated_at = updated_at

    @property
    def sub_category_id(self):
        """
        Gets the sub_category_id of this PlaylistTemplate.

        :return: The sub_category_id of this PlaylistTemplate.
        :rtype: float
        """
        return self._sub_category_id

    @sub_category_id.setter
    def sub_category_id(self, sub_category_id):
        """
        Sets the sub_category_id of this PlaylistTemplate.

        :param sub_category_id: The sub_category_id of this PlaylistTemplate.
        :type: float
        """

        self._sub_category_id = sub_category_id

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
        if not isinstance(other, PlaylistTemplate):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
