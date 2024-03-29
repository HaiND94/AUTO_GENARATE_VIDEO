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


class AudioClean(object):
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
        'url': 'str',
        'title': 'str',
        'total_rating': 'float',
        'numbers_of_rating': 'float',
        'audio_finger_print': 'str',
        'id_sound_cloud': 'str',
        'id_spotify': 'str',
        'id_youtube': 'str',
        'type': 'float',
        'license': 'str',
        'status': 'str',
        'views': 'float',
        'uploaded_at': 'str',
        'active': 'bool',
        'priority': 'float',
        'cover_status': 'str',
        'duration': 'float',
        'modifier': 'str',
        'modify_content': 'str',
        'name_translate': 'str',
        'id': 'float',
        'account_id': 'float',
        'created_at': 'datetime',
        'updated_at': 'datetime',
        'singer_id': 'float',
        'author_id': 'float',
        'category_id': 'float',
        'country_id': 'float',
        'music_genre_id': 'float'
    }

    attribute_map = {
        'url': 'url',
        'title': 'title',
        'total_rating': 'totalRating',
        'numbers_of_rating': 'numbersOfRating',
        'audio_finger_print': 'audioFingerPrint',
        'id_sound_cloud': 'idSoundCloud',
        'id_spotify': 'idSpotify',
        'id_youtube': 'idYoutube',
        'type': 'type',
        'license': 'license',
        'status': 'status',
        'views': 'views',
        'uploaded_at': 'uploadedAt',
        'active': 'active',
        'priority': 'priority',
        'cover_status': 'coverStatus',
        'duration': 'duration',
        'modifier': 'modifier',
        'modify_content': 'modifyContent',
        'name_translate': 'nameTranslate',
        'id': 'id',
        'account_id': 'accountId',
        'created_at': 'createdAt',
        'updated_at': 'updatedAt',
        'singer_id': 'singerId',
        'author_id': 'authorId',
        'category_id': 'categoryId',
        'country_id': 'countryId',
        'music_genre_id': 'musicGenreId'
    }

    def __init__(self, url=None, title=None, total_rating=0.0, numbers_of_rating=0.0, audio_finger_print=None, id_sound_cloud=None, id_spotify=None, id_youtube=None, type=None, license='NON BLOCK', status=None, views=None, uploaded_at=None, active=True, priority=None, cover_status=None, duration=None, modifier=None, modify_content=None, name_translate=None, id=None, account_id=None, created_at=None, updated_at=None, singer_id=None, author_id=None, category_id=None, country_id=None, music_genre_id=None):
        """
        AudioClean - a model defined in Swagger
        """

        self._url = None
        self._title = None
        self._total_rating = None
        self._numbers_of_rating = None
        self._audio_finger_print = None
        self._id_sound_cloud = None
        self._id_spotify = None
        self._id_youtube = None
        self._type = None
        self._license = None
        self._status = None
        self._views = None
        self._uploaded_at = None
        self._active = None
        self._priority = None
        self._cover_status = None
        self._duration = None
        self._modifier = None
        self._modify_content = None
        self._name_translate = None
        self._id = None
        self._account_id = None
        self._created_at = None
        self._updated_at = None
        self._singer_id = None
        self._author_id = None
        self._category_id = None
        self._country_id = None
        self._music_genre_id = None

        if url is not None:
          self.url = url
        if title is not None:
          self.title = title
        if total_rating is not None:
          self.total_rating = total_rating
        if numbers_of_rating is not None:
          self.numbers_of_rating = numbers_of_rating
        if audio_finger_print is not None:
          self.audio_finger_print = audio_finger_print
        if id_sound_cloud is not None:
          self.id_sound_cloud = id_sound_cloud
        if id_spotify is not None:
          self.id_spotify = id_spotify
        if id_youtube is not None:
          self.id_youtube = id_youtube
        if type is not None:
          self.type = type
        if license is not None:
          self.license = license
        if status is not None:
          self.status = status
        if views is not None:
          self.views = views
        if uploaded_at is not None:
          self.uploaded_at = uploaded_at
        if active is not None:
          self.active = active
        if priority is not None:
          self.priority = priority
        if cover_status is not None:
          self.cover_status = cover_status
        if duration is not None:
          self.duration = duration
        if modifier is not None:
          self.modifier = modifier
        if modify_content is not None:
          self.modify_content = modify_content
        if name_translate is not None:
          self.name_translate = name_translate
        if id is not None:
          self.id = id
        if account_id is not None:
          self.account_id = account_id
        if created_at is not None:
          self.created_at = created_at
        if updated_at is not None:
          self.updated_at = updated_at
        if singer_id is not None:
          self.singer_id = singer_id
        if author_id is not None:
          self.author_id = author_id
        if category_id is not None:
          self.category_id = category_id
        if country_id is not None:
          self.country_id = country_id
        if music_genre_id is not None:
          self.music_genre_id = music_genre_id

    @property
    def url(self):
        """
        Gets the url of this AudioClean.

        :return: The url of this AudioClean.
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """
        Sets the url of this AudioClean.

        :param url: The url of this AudioClean.
        :type: str
        """

        self._url = url

    @property
    def title(self):
        """
        Gets the title of this AudioClean.

        :return: The title of this AudioClean.
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """
        Sets the title of this AudioClean.

        :param title: The title of this AudioClean.
        :type: str
        """

        self._title = title

    @property
    def total_rating(self):
        """
        Gets the total_rating of this AudioClean.

        :return: The total_rating of this AudioClean.
        :rtype: float
        """
        return self._total_rating

    @total_rating.setter
    def total_rating(self, total_rating):
        """
        Sets the total_rating of this AudioClean.

        :param total_rating: The total_rating of this AudioClean.
        :type: float
        """

        self._total_rating = total_rating

    @property
    def numbers_of_rating(self):
        """
        Gets the numbers_of_rating of this AudioClean.

        :return: The numbers_of_rating of this AudioClean.
        :rtype: float
        """
        return self._numbers_of_rating

    @numbers_of_rating.setter
    def numbers_of_rating(self, numbers_of_rating):
        """
        Sets the numbers_of_rating of this AudioClean.

        :param numbers_of_rating: The numbers_of_rating of this AudioClean.
        :type: float
        """

        self._numbers_of_rating = numbers_of_rating

    @property
    def audio_finger_print(self):
        """
        Gets the audio_finger_print of this AudioClean.

        :return: The audio_finger_print of this AudioClean.
        :rtype: str
        """
        return self._audio_finger_print

    @audio_finger_print.setter
    def audio_finger_print(self, audio_finger_print):
        """
        Sets the audio_finger_print of this AudioClean.

        :param audio_finger_print: The audio_finger_print of this AudioClean.
        :type: str
        """

        self._audio_finger_print = audio_finger_print

    @property
    def id_sound_cloud(self):
        """
        Gets the id_sound_cloud of this AudioClean.

        :return: The id_sound_cloud of this AudioClean.
        :rtype: str
        """
        return self._id_sound_cloud

    @id_sound_cloud.setter
    def id_sound_cloud(self, id_sound_cloud):
        """
        Sets the id_sound_cloud of this AudioClean.

        :param id_sound_cloud: The id_sound_cloud of this AudioClean.
        :type: str
        """

        self._id_sound_cloud = id_sound_cloud

    @property
    def id_spotify(self):
        """
        Gets the id_spotify of this AudioClean.

        :return: The id_spotify of this AudioClean.
        :rtype: str
        """
        return self._id_spotify

    @id_spotify.setter
    def id_spotify(self, id_spotify):
        """
        Sets the id_spotify of this AudioClean.

        :param id_spotify: The id_spotify of this AudioClean.
        :type: str
        """

        self._id_spotify = id_spotify

    @property
    def id_youtube(self):
        """
        Gets the id_youtube of this AudioClean.

        :return: The id_youtube of this AudioClean.
        :rtype: str
        """
        return self._id_youtube

    @id_youtube.setter
    def id_youtube(self, id_youtube):
        """
        Sets the id_youtube of this AudioClean.

        :param id_youtube: The id_youtube of this AudioClean.
        :type: str
        """

        self._id_youtube = id_youtube

    @property
    def type(self):
        """
        Gets the type of this AudioClean.

        :return: The type of this AudioClean.
        :rtype: float
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this AudioClean.

        :param type: The type of this AudioClean.
        :type: float
        """

        self._type = type

    @property
    def license(self):
        """
        Gets the license of this AudioClean.

        :return: The license of this AudioClean.
        :rtype: str
        """
        return self._license

    @license.setter
    def license(self, license):
        """
        Sets the license of this AudioClean.

        :param license: The license of this AudioClean.
        :type: str
        """

        self._license = license

    @property
    def status(self):
        """
        Gets the status of this AudioClean.

        :return: The status of this AudioClean.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        Sets the status of this AudioClean.

        :param status: The status of this AudioClean.
        :type: str
        """

        self._status = status

    @property
    def views(self):
        """
        Gets the views of this AudioClean.

        :return: The views of this AudioClean.
        :rtype: float
        """
        return self._views

    @views.setter
    def views(self, views):
        """
        Sets the views of this AudioClean.

        :param views: The views of this AudioClean.
        :type: float
        """

        self._views = views

    @property
    def uploaded_at(self):
        """
        Gets the uploaded_at of this AudioClean.

        :return: The uploaded_at of this AudioClean.
        :rtype: str
        """
        return self._uploaded_at

    @uploaded_at.setter
    def uploaded_at(self, uploaded_at):
        """
        Sets the uploaded_at of this AudioClean.

        :param uploaded_at: The uploaded_at of this AudioClean.
        :type: str
        """

        self._uploaded_at = uploaded_at

    @property
    def active(self):
        """
        Gets the active of this AudioClean.

        :return: The active of this AudioClean.
        :rtype: bool
        """
        return self._active

    @active.setter
    def active(self, active):
        """
        Sets the active of this AudioClean.

        :param active: The active of this AudioClean.
        :type: bool
        """

        self._active = active

    @property
    def priority(self):
        """
        Gets the priority of this AudioClean.

        :return: The priority of this AudioClean.
        :rtype: float
        """
        return self._priority

    @priority.setter
    def priority(self, priority):
        """
        Sets the priority of this AudioClean.

        :param priority: The priority of this AudioClean.
        :type: float
        """

        self._priority = priority

    @property
    def cover_status(self):
        """
        Gets the cover_status of this AudioClean.

        :return: The cover_status of this AudioClean.
        :rtype: str
        """
        return self._cover_status

    @cover_status.setter
    def cover_status(self, cover_status):
        """
        Sets the cover_status of this AudioClean.

        :param cover_status: The cover_status of this AudioClean.
        :type: str
        """

        self._cover_status = cover_status

    @property
    def duration(self):
        """
        Gets the duration of this AudioClean.

        :return: The duration of this AudioClean.
        :rtype: float
        """
        return self._duration

    @duration.setter
    def duration(self, duration):
        """
        Sets the duration of this AudioClean.

        :param duration: The duration of this AudioClean.
        :type: float
        """

        self._duration = duration

    @property
    def modifier(self):
        """
        Gets the modifier of this AudioClean.

        :return: The modifier of this AudioClean.
        :rtype: str
        """
        return self._modifier

    @modifier.setter
    def modifier(self, modifier):
        """
        Sets the modifier of this AudioClean.

        :param modifier: The modifier of this AudioClean.
        :type: str
        """

        self._modifier = modifier

    @property
    def modify_content(self):
        """
        Gets the modify_content of this AudioClean.

        :return: The modify_content of this AudioClean.
        :rtype: str
        """
        return self._modify_content

    @modify_content.setter
    def modify_content(self, modify_content):
        """
        Sets the modify_content of this AudioClean.

        :param modify_content: The modify_content of this AudioClean.
        :type: str
        """

        self._modify_content = modify_content

    @property
    def name_translate(self):
        """
        Gets the name_translate of this AudioClean.

        :return: The name_translate of this AudioClean.
        :rtype: str
        """
        return self._name_translate

    @name_translate.setter
    def name_translate(self, name_translate):
        """
        Sets the name_translate of this AudioClean.

        :param name_translate: The name_translate of this AudioClean.
        :type: str
        """

        self._name_translate = name_translate

    @property
    def id(self):
        """
        Gets the id of this AudioClean.

        :return: The id of this AudioClean.
        :rtype: float
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this AudioClean.

        :param id: The id of this AudioClean.
        :type: float
        """

        self._id = id

    @property
    def account_id(self):
        """
        Gets the account_id of this AudioClean.

        :return: The account_id of this AudioClean.
        :rtype: float
        """
        return self._account_id

    @account_id.setter
    def account_id(self, account_id):
        """
        Sets the account_id of this AudioClean.

        :param account_id: The account_id of this AudioClean.
        :type: float
        """

        self._account_id = account_id

    @property
    def created_at(self):
        """
        Gets the created_at of this AudioClean.

        :return: The created_at of this AudioClean.
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """
        Sets the created_at of this AudioClean.

        :param created_at: The created_at of this AudioClean.
        :type: datetime
        """

        self._created_at = created_at

    @property
    def updated_at(self):
        """
        Gets the updated_at of this AudioClean.

        :return: The updated_at of this AudioClean.
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """
        Sets the updated_at of this AudioClean.

        :param updated_at: The updated_at of this AudioClean.
        :type: datetime
        """

        self._updated_at = updated_at

    @property
    def singer_id(self):
        """
        Gets the singer_id of this AudioClean.

        :return: The singer_id of this AudioClean.
        :rtype: float
        """
        return self._singer_id

    @singer_id.setter
    def singer_id(self, singer_id):
        """
        Sets the singer_id of this AudioClean.

        :param singer_id: The singer_id of this AudioClean.
        :type: float
        """

        self._singer_id = singer_id

    @property
    def author_id(self):
        """
        Gets the author_id of this AudioClean.

        :return: The author_id of this AudioClean.
        :rtype: float
        """
        return self._author_id

    @author_id.setter
    def author_id(self, author_id):
        """
        Sets the author_id of this AudioClean.

        :param author_id: The author_id of this AudioClean.
        :type: float
        """

        self._author_id = author_id

    @property
    def category_id(self):
        """
        Gets the category_id of this AudioClean.

        :return: The category_id of this AudioClean.
        :rtype: float
        """
        return self._category_id

    @category_id.setter
    def category_id(self, category_id):
        """
        Sets the category_id of this AudioClean.

        :param category_id: The category_id of this AudioClean.
        :type: float
        """

        self._category_id = category_id

    @property
    def country_id(self):
        """
        Gets the country_id of this AudioClean.

        :return: The country_id of this AudioClean.
        :rtype: float
        """
        return self._country_id

    @country_id.setter
    def country_id(self, country_id):
        """
        Sets the country_id of this AudioClean.

        :param country_id: The country_id of this AudioClean.
        :type: float
        """

        self._country_id = country_id

    @property
    def music_genre_id(self):
        """
        Gets the music_genre_id of this AudioClean.

        :return: The music_genre_id of this AudioClean.
        :rtype: float
        """
        return self._music_genre_id

    @music_genre_id.setter
    def music_genre_id(self, music_genre_id):
        """
        Sets the music_genre_id of this AudioClean.

        :param music_genre_id: The music_genre_id of this AudioClean.
        :type: float
        """

        self._music_genre_id = music_genre_id

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
        if not isinstance(other, AudioClean):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
