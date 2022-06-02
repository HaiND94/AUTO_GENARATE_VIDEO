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


class AudioTemplateVideo(object):
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
        'audio_clean_id': 'float',
        'account_id': 'float',
        'template_video_id': 'float'
    }

    attribute_map = {
        'id': 'id',
        'audio_clean_id': 'audioCleanId',
        'account_id': 'accountId',
        'template_video_id': 'templateVideoId'
    }

    def __init__(self, id=None, audio_clean_id=None, account_id=None, template_video_id=None):
        """
        AudioTemplateVideo - a model defined in Swagger
        """

        self._id = None
        self._audio_clean_id = None
        self._account_id = None
        self._template_video_id = None

        if id is not None:
          self.id = id
        if audio_clean_id is not None:
          self.audio_clean_id = audio_clean_id
        if account_id is not None:
          self.account_id = account_id
        if template_video_id is not None:
          self.template_video_id = template_video_id

    @property
    def id(self):
        """
        Gets the id of this AudioTemplateVideo.

        :return: The id of this AudioTemplateVideo.
        :rtype: float
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this AudioTemplateVideo.

        :param id: The id of this AudioTemplateVideo.
        :type: float
        """

        self._id = id

    @property
    def audio_clean_id(self):
        """
        Gets the audio_clean_id of this AudioTemplateVideo.

        :return: The audio_clean_id of this AudioTemplateVideo.
        :rtype: float
        """
        return self._audio_clean_id

    @audio_clean_id.setter
    def audio_clean_id(self, audio_clean_id):
        """
        Sets the audio_clean_id of this AudioTemplateVideo.

        :param audio_clean_id: The audio_clean_id of this AudioTemplateVideo.
        :type: float
        """

        self._audio_clean_id = audio_clean_id

    @property
    def account_id(self):
        """
        Gets the account_id of this AudioTemplateVideo.

        :return: The account_id of this AudioTemplateVideo.
        :rtype: float
        """
        return self._account_id

    @account_id.setter
    def account_id(self, account_id):
        """
        Sets the account_id of this AudioTemplateVideo.

        :param account_id: The account_id of this AudioTemplateVideo.
        :type: float
        """

        self._account_id = account_id

    @property
    def template_video_id(self):
        """
        Gets the template_video_id of this AudioTemplateVideo.

        :return: The template_video_id of this AudioTemplateVideo.
        :rtype: float
        """
        return self._template_video_id

    @template_video_id.setter
    def template_video_id(self, template_video_id):
        """
        Sets the template_video_id of this AudioTemplateVideo.

        :param template_video_id: The template_video_id of this AudioTemplateVideo.
        :type: float
        """

        self._template_video_id = template_video_id

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
        if not isinstance(other, AudioTemplateVideo):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
