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


class Discussion(object):
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
        'title': 'str',
        'role_creator': 'str',
        'content': 'str',
        'status': 'str',
        'id': 'float',
        'account_id': 'float',
        'created_at': 'datetime',
        'updated_at': 'datetime'
    }

    attribute_map = {
        'title': 'title',
        'role_creator': 'roleCreator',
        'content': 'content',
        'status': 'status',
        'id': 'id',
        'account_id': 'accountId',
        'created_at': 'createdAt',
        'updated_at': 'updatedAt'
    }

    def __init__(self, title=None, role_creator=None, content=None, status=None, id=None, account_id=None, created_at=None, updated_at=None):
        """
        Discussion - a model defined in Swagger
        """

        self._title = None
        self._role_creator = None
        self._content = None
        self._status = None
        self._id = None
        self._account_id = None
        self._created_at = None
        self._updated_at = None

        if title is not None:
          self.title = title
        if role_creator is not None:
          self.role_creator = role_creator
        if content is not None:
          self.content = content
        if status is not None:
          self.status = status
        if id is not None:
          self.id = id
        if account_id is not None:
          self.account_id = account_id
        if created_at is not None:
          self.created_at = created_at
        if updated_at is not None:
          self.updated_at = updated_at

    @property
    def title(self):
        """
        Gets the title of this Discussion.

        :return: The title of this Discussion.
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """
        Sets the title of this Discussion.

        :param title: The title of this Discussion.
        :type: str
        """

        self._title = title

    @property
    def role_creator(self):
        """
        Gets the role_creator of this Discussion.

        :return: The role_creator of this Discussion.
        :rtype: str
        """
        return self._role_creator

    @role_creator.setter
    def role_creator(self, role_creator):
        """
        Sets the role_creator of this Discussion.

        :param role_creator: The role_creator of this Discussion.
        :type: str
        """

        self._role_creator = role_creator

    @property
    def content(self):
        """
        Gets the content of this Discussion.

        :return: The content of this Discussion.
        :rtype: str
        """
        return self._content

    @content.setter
    def content(self, content):
        """
        Sets the content of this Discussion.

        :param content: The content of this Discussion.
        :type: str
        """

        self._content = content

    @property
    def status(self):
        """
        Gets the status of this Discussion.

        :return: The status of this Discussion.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        Sets the status of this Discussion.

        :param status: The status of this Discussion.
        :type: str
        """

        self._status = status

    @property
    def id(self):
        """
        Gets the id of this Discussion.

        :return: The id of this Discussion.
        :rtype: float
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this Discussion.

        :param id: The id of this Discussion.
        :type: float
        """

        self._id = id

    @property
    def account_id(self):
        """
        Gets the account_id of this Discussion.

        :return: The account_id of this Discussion.
        :rtype: float
        """
        return self._account_id

    @account_id.setter
    def account_id(self, account_id):
        """
        Sets the account_id of this Discussion.

        :param account_id: The account_id of this Discussion.
        :type: float
        """

        self._account_id = account_id

    @property
    def created_at(self):
        """
        Gets the created_at of this Discussion.

        :return: The created_at of this Discussion.
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """
        Sets the created_at of this Discussion.

        :param created_at: The created_at of this Discussion.
        :type: datetime
        """

        self._created_at = created_at

    @property
    def updated_at(self):
        """
        Gets the updated_at of this Discussion.

        :return: The updated_at of this Discussion.
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """
        Sets the updated_at of this Discussion.

        :param updated_at: The updated_at of this Discussion.
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
        if not isinstance(other, Discussion):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
