"""""""""""""""""""""""
Author : NGUYEN DINH HAI
VER    : 1.0
DATE   : 2021, JUL 12
"""""""""""""""""""""""

from swagger_client import AccountApi, ApiClient
from swagger_client import ImageCleanApi, FontFamilyApi, LanguageApi
from swagger_client import AudioCleanApi, SingerApi
from swagger_client import ChannelApi, ChannelCountryApi, ChannelSingerApi, ChannelImageApi
from swagger_client import NotificationApi

from moviepy.editor import ImageClip, VideoFileClip, concatenate_audioclips, concatenate_videoclips
from datetime import date, datetime
from src.log_status import log
from src.notification import notice_error, notice_warning
from src.utilitys import Struct
from src.utilitys import gen_description
from collections import namedtuple

import json
import os
import logging
import time
import random


# Get data of channel from database
def get_data_channel(api_cli, base_dir, channel_id, error_channels, log_file):
    data_channel = dict()
    data_channel['id'] = int(channel_id)
    data_channel['error_status'] = False

    country_ids = []

    log(log_file, f"Start get data channel {channel_id}")

    if os.path.isdir(f"{base_dir}/logger") is False:
        try:
            os.mkdir(f"{base_dir}/logger")
        except Exception as e:
            print(e)
            data = Struct(**data_channel)
            data.set_error()

            return data

    try:
        imageApi = ImageCleanApi(api_client=api_cli)
        audioApi = AudioCleanApi(api_client=api_cli)
        channelApi = ChannelApi(api_client=api_cli)
        channelSingerApi = ChannelSingerApi(api_client=api_cli)
        notificationApi = NotificationApi(api_client=api_cli)
        channelCountryApi = ChannelCountryApi(api_client=api_cli)
        languageApi = LanguageApi(api_cli)
        singerApi = SingerApi(api_client=api_cli)
        channel_id = int(channel_id)

    except Exception as error:
        log(log_file, f"could be not pass api client\n or {error}")
        data = Struct(**data_channel)
        data.set_error()

        return data

    try:
        channel = channelApi.channel_find_by_id(str(channel_id))
    except Exception as error:
        _content = f"Channel was not found with channel id {channel_id}"
        log(log_file, f'{_content}\n{error}')

        data = Struct(**data_channel)
        data.set_error()
        try:
            notice_error(notificationApi, channel, _content)
        except:
            pass

        return data

    try:
        _filter = json.dumps({"where": {'channelId': channel_id}})
        countries = channelCountryApi.channel_country_find(filter=_filter)

    except Exception as e:
        _content = f'could be not find country id in channel {channel_id}'
        log(log_file, _content)
        log(log_file, e)

        data = Struct(**data_channel)
        data.set_error()
        try:
            notice_error(notificationApi, channel, _content)
        except:
            pass

        return data

    # Get country id of channel
    for country in countries:
        try:
            country_ids.append(country.country_id)
        except:
            log(log_file, "could be not find country id in channel country api")
            pass

    # Check country of channel
    if len(country_ids) == 0:
        _content = "could be not find country id in channel"

        log(log_file, _content)

        data = Struct(**data_channel)
        data.set_error()

        try:
            notice_error(notificationApi, channel, _content)
        except:
            pass

        return data
    else:
        data_channel['country_ids'] = country_ids

    # Get language for channel
    _language_id = None
    try:
        _language_id = channel.language_id

    except Exception as error:
        _content = "Language id was not find"
        log(log_file, f"{_content}\n {error}")
        data = Struct(**data_channel)
        data.set_error()
        try:
            notice_error(notificationApi, channel, _content)
        except:
            pass

        return data

    if not _language_id:
        _content = "Language id was not find"
        log(log_file, f"{_content}")
        data = Struct(**data_channel)
        data.set_error()
        try:
            notice_error(notificationApi, channel, _content)
        except:
            pass

        return data

    else:
        data_channel['language_id'] = _language_id
        try:

            language = languageApi.language_find_by_id(id=channel.language_id)
            _language_code = language.code
            if not _language_code:
                data_channel['language_code'] = language.code
            else:
                data_channel['language_code'] = None
        except:
            _content = "Language code was not found"
            log(log_file, f"{_content}")
            data = Struct(**data_channel)

            data.set_error()
            try:
                notice_error(notificationApi, channel, _content)
            except:
                pass

            return data

    _singer_mode = None
    _include_singer_name = False
    _duration_min = 0
    _duration_max = 150

    try:
        if channel.meta_data:
            data_channel['meta_data'] = channel.meta_data

            meta_data = json.loads(channel.meta_data)
            try:
                _singer_mode = meta_data['singerMode']
            except:
                pass

            try:
                _duration_min = int(meta_data['durationMin'])
                _duration_max = int(meta_data['durationMax'])
                _include_singer_name = meta_data['includeSingerName']
            except:
                pass

    except:
        pass

    # Check singer mode config in channel
    if not _singer_mode:
        _content = f'singer mode was not config in channel {channel_id}'
        log(log_file, _content)

        data = Struct(**data_channel)
        data.set_error()
        try:
            notice_error(notificationApi, channel, _content)
        except:
            pass

        return data

    else:
        data_channel['singer_mode'] = _singer_mode
        data_channel['include_singer_name'] = _include_singer_name
        data_channel['duration_min'] = _duration_min
        data_channel['duration_max'] = _duration_max
        data_channel['account_id'] = channel.account_id

    # Check image of singer in channel
    # logging.info(f'CHANNEL {channel_id} CONTENT SINGER')

    singer_ids = []
    singer_names = []
    _img_types = []

    # Get image type of channel
    try:
        _img_types = channel.img_types
    except:
        pass

    # Check image type was config in channel
    if len(_img_types) == 0:
        _content = f'could be not find image type for channel {channel_id}'
        log(log_file, _content)

        data = Struct(**data_channel)
        data.set_error()

        try:
            notice_error(notificationApi, channel, _content)
        except:
            pass

        return data
    else:
        data_channel['img_types'] = _img_types

    # Check audio and image for singer in channel
    try:
        filter = json.dumps({"where": {'channelId': channel_id,
                                       'active': True,
                                       }
                             })
        channel_singers = channelSingerApi.channel_singer_find(filter=filter)

        if len(channel_singers) != 0:
            random.shuffle(channel_singers)
            for channel_singer in channel_singers:
                _id = None
                try:
                    _id = channel_singer.singer_id
                except:
                    continue

                if _id:
                    try:
                        filter = json.dumps({'singerId': _id,
                                             'or': [{'url': {'neq': None}}, {'idYoutube': {'neq': None}}]
                                             })
                        _count_audio = audioApi.audio_clean_count(where=filter)
                        __count_audio = int(_count_audio.count)

                        if __count_audio != 0:
                            try:
                                singer = singerApi.singer_find_by_id(id=_id)

                            except:
                                continue

                            if len(_img_types) != 0 and _img_types in ['SINGERS', 'SINGER']:
                                __count_img = 0

                                try:
                                    filter = json.dumps({'type': 'NORMAL',
                                                         'singerId': _id,
                                                         'url': {'neq': None},
                                                         'objectType': {'inq': ['SINGERS']}
                                                         })

                                    _count_img = imageApi.image_clean_count(where=filter)
                                    __count_img = int(_count_img.count)
                                except:
                                    continue

                                if __count_img != 0:
                                    singer_ids.append(_id)
                                    singer_names.append(singer.name)
                                    continue
                            else:
                                singer_ids.append(_id)
                                singer_names.append(singer.name)
                                continue

                        _content = f"could be not find audio for channel with singer {_id}"

                        log(log_file, _content)

                        try:
                            notice_warning(notificationApi, channel, _content)
                        except:
                            pass
                        continue

                    except:
                        continue

                continue

    except Exception as error:
        _content = 'could be not find singer'

        log(log_file, f'{_content}\n{error}' )

        data = Struct(**data_channel)
        data.set_error()
        try:
            notice_error(notificationApi, channel, _content)
        except:
            pass

        return data

    if len(singer_ids) == 0 or len(singer_names) == 0:

        _content = f'could be not find singer was config for channel {channel_id} have song and have image'
        log(log_file, _content)

        data = Struct(**data_channel)

        data.set_error()

        try:
            notice_error(notificationApi, channel, _content)
        except Exception as e:
            print(e)
            pass

        return data

    try:
        copy_right_content = channel.copy_right_content
    except:
        copy_right_content = False

    if _singer_mode == 'SINGER' or _include_singer_name == "YES":
        index = random.randint(0, len(singer_ids) - 1)
        singer_ids = [singer_ids[index]]
        singer_names = [singer_names[index]]

    data_channel['singer_names'] = singer_names
    data_channel['singer_ids'] = singer_ids
    data_channel['copy_right_content'] = copy_right_content

    data = Struct(**data_channel)

    return data
