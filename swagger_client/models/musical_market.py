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


class MusicalMarket(object):
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
        'number_of_views': 'str',
        'id': 'float',
        'country_id': 'float',
        'singer_id': 'float'
    }

    attribute_map = {
        'number_of_views': 'numberOfViews',
        'id': 'id',
        'country_id': 'countryId',
        'singer_id': 'singerId'
    }

    def __init__(self, number_of_views=None, id=None, country_id=None, singer_id=None):
        """
        MusicalMarket - a model defined in Swagger
        """

        self._number_of_views = None
        self._id = None
        self._country_id = None
        self._singer_id = None

        if number_of_views is not None:
          self.number_of_views = number_of_views
        if id is not None:
          self.id = id
        if country_id is not None:
          self.country_id = country_id
        if singer_id is not None:
          self.singer_id = singer_id

    @property
    def number_of_views(self):
        """
        Gets the number_of_views of this MusicalMarket.

        :return: The number_of_views of this MusicalMarket.
        :rtype: str
        """
        return self._number_of_views

    @number_of_views.setter
    def number_of_views(self, number_of_views):
        """
        Sets the number_of_views of this MusicalMarket.

        :param number_of_views: The number_of_views of this MusicalMarket.
        :type: str
        """

        self._number_of_views = number_of_views

    @property
    def id(self):
        """
        Gets the id of this MusicalMarket.

        :return: The id of this MusicalMarket.
        :rtype: float
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this MusicalMarket.

        :param id: The id of this MusicalMarket.
        :type: float
        """

        self._id = id

    @property
    def country_id(self):
        """
        Gets the country_id of this MusicalMarket.

        :return: The country_id of this MusicalMarket.
        :rtype: float
        """
        return self._country_id

    @country_id.setter
    def country_id(self, country_id):
        """
        Sets the country_id of this MusicalMarket.

        :param country_id: The country_id of this MusicalMarket.
        :type: float
        """

        self._country_id = country_id

    @property
    def singer_id(self):
        """
        Gets the singer_id of this MusicalMarket.

        :return: The singer_id of this MusicalMarket.
        :rtype: float
        """
        return self._singer_id

    @singer_id.setter
    def singer_id(self, singer_id):
        """
        Sets the singer_id of this MusicalMarket.

        :param singer_id: The singer_id of this MusicalMarket.
        :type: float
        """

        self._singer_id = singer_id

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
        if not isinstance(other, MusicalMarket):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other