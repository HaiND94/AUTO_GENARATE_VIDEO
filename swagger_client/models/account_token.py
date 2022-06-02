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


class AccountToken(object):
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
        'id': 'str',
        'ttl': 'float',
        'scopes': 'list[str]',
        'created': 'datetime',
        'user_id': 'float',
        'created_at': 'datetime',
        'updated_at': 'datetime'
    }

    attribute_map = {
        'id': 'id',
        'ttl': 'ttl',
        'scopes': 'scopes',
        'created': 'created',
        'user_id': 'userId',
        'created_at': 'createdAt',
        'updated_at': 'updatedAt'
    }

    def __init__(self, id=None, ttl=1209600.0, scopes=None, created=None, user_id=None, created_at=None, updated_at=None):
        """
        AccountToken - a model defined in Swagger
        """

        self._id = None
        self._ttl = None
        self._scopes = None
        self._created = None
        self._user_id = None
        self._created_at = None
        self._updated_at = None

        self.id = id
        if ttl is not None:
          self.ttl = ttl
        if scopes is not None:
          self.scopes = scopes
        if created is not None:
          self.created = created
        if user_id is not None:
          self.user_id = user_id
        if created_at is not None:
          self.created_at = created_at
        if updated_at is not None:
          self.updated_at = updated_at

    @property
    def id(self):
        """
        Gets the id of this AccountToken.

        :return: The id of this AccountToken.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this AccountToken.

        :param id: The id of this AccountToken.
        :type: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")

        self._id = id

    @property
    def ttl(self):
        """
        Gets the ttl of this AccountToken.
        time to live in seconds (2 weeks by default)

        :return: The ttl of this AccountToken.
        :rtype: float
        """
        return self._ttl

    @ttl.setter
    def ttl(self, ttl):
        """
        Sets the ttl of this AccountToken.
        time to live in seconds (2 weeks by default)

        :param ttl: The ttl of this AccountToken.
        :type: float
        """

        self._ttl = ttl

    @property
    def scopes(self):
        """
        Gets the scopes of this AccountToken.
        Array of scopes granted to this access token.

        :return: The scopes of this AccountToken.
        :rtype: list[str]
        """
        return self._scopes

    @scopes.setter
    def scopes(self, scopes):
        """
        Sets the scopes of this AccountToken.
        Array of scopes granted to this access token.

        :param scopes: The scopes of this AccountToken.
        :type: list[str]
        """

        self._scopes = scopes

    @property
    def created(self):
        """
        Gets the created of this AccountToken.

        :return: The created of this AccountToken.
        :rtype: datetime
        """
        return self._created

    @created.setter
    def created(self, created):
        """
        Sets the created of this AccountToken.

        :param created: The created of this AccountToken.
        :type: datetime
        """

        self._created = created

    @property
    def user_id(self):
        """
        Gets the user_id of this AccountToken.

        :return: The user_id of this AccountToken.
        :rtype: float
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        """
        Sets the user_id of this AccountToken.

        :param user_id: The user_id of this AccountToken.
        :type: float
        """

        self._user_id = user_id

    @property
    def created_at(self):
        """
        Gets the created_at of this AccountToken.

        :return: The created_at of this AccountToken.
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """
        Sets the created_at of this AccountToken.

        :param created_at: The created_at of this AccountToken.
        :type: datetime
        """

        self._created_at = created_at

    @property
    def updated_at(self):
        """
        Gets the updated_at of this AccountToken.

        :return: The updated_at of this AccountToken.
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """
        Sets the updated_at of this AccountToken.

        :param updated_at: The updated_at of this AccountToken.
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
        if not isinstance(other, AccountToken):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other