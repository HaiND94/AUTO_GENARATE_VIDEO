"""""""""""""""""""""""
Author : NGUYEN DINH HAI
VER    : 1.0
DATE   : 2021, JUL 12
"""""""""""""""""""""""

from moviepy.editor import AudioFileClip, ImageClip, VideoFileClip, concatenate_audioclips, concatenate_videoclips

from swagger_client import AccountApi, ApiClient
from swagger_client import ImageCleanApi, FontFamilyApi, LanguageApi
from swagger_client import AudioCleanApi, SingerApi
from swagger_client import ChannelApi, ChannelCountryApi, ChannelSingerApi, ChannelImageApi
from swagger_client import NotificationApi

from src.log_status import log
from src.utilitys import Struct, download
from src.notification import notice_error, notice_warning

from .get_template import get_data_templates
from .auto_data import get_data_auto
from .topsong_data import get_data_top_song
from .worship_data import get_data_worship
from .auto_data import Image


from func_timeout import func_set_timeout

import json
import os
import logging
import time
import random

import urllib.request


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filemode='w')


DURATION_MAX = 90


def get_data_images(title, model, channel, api_cli, base_dir, base_url, token, error_channels,
                    list_singers, list_songs):

    data_images = dict()
    data_images['error_status'] = False

    # Get information from channel
    try:
        channel_id = channel.id
        _error_status = channel.error_status
        singer_ids = channel.singer_ids
        # meta_data = channel.meta_data
        img_types = channel.img_types
        country_ids = channel.country_ids

        if os.path.isdir(f"{base_dir}/logger") is False:
            try:
                os.mkdir(f"{base_dir}/logger")
            except Exception as e:
                print(e)

        log_file = f"{base_dir}/logger/channel_{int(channel_id)}.log"
        log(log_file, f"Start start getting image data for channel {channel_id}")

    except Exception as error:
        logging.info(f"Can not get channel id and status\n or {error}")
        data = Struct(**data_images)
        data.set_error()

        return data

    try:
        imageApi = ImageCleanApi(api_client=api_cli)
        # channelSingerApi = ChannelSingerApi(api_client=api_cli)
        notificationApi = NotificationApi(api_client=api_cli)
        channelImgApi = ChannelImageApi(api_client=api_cli)
        fontApi = FontFamilyApi(api_client=api_cli)

    except Exception as error:
        log(log_file, f"could be not pass api client\n or {error}")
        data = Struct(**data_images)
        data.set_error()

        return data

    if not os.path.isdir(base_dir):
        try:
            os.mkdir(base_dir)
        except Exception as e:
            _content = f"Can not find folder {base_dir} in server\n{e}"
            logging.info(_content)
            data = Struct(**data_images)
            data.set_error()

            return data

    # Check path save audio
    _path_save = f'{base_dir}/data/images'

    if not os.path.isdir(_path_save):
        if not os.path.isdir(f'{base_dir}/data'):
            try:
                os.mkdir(f'{base_dir}/data')
            except Exception as e:
                log(log_file, e)
        try:
            os.mkdir(_path_save)
        except Exception as e:
            log(log_file, f"Can not crate {_path_save}\n {e}")

        data = Struct(**data_images)
        data.set_error()

        return data

    _object_status = False

    if len(img_types) == 0:
        _content = "Image type must config in channel"
        log(log_file, _content)
        data = Struct(**data_images)
        data.set_error()

        try:
            notice_error(notificationApi, channel, _content)
        except:
            pass

        return data

    # Check MEN and WOMEN was config in channel
    if "MEN" in img_types or "WOMEN" in img_types:
        _object_status = True

    # Find image object in DB
    limit = 20
    rand_limit = 0
    _count_sum = 0
    _count_img = 0
    images = []

    # Check image it has available
    if _object_status:
        _filter = json.dumps({'type': 'NORMAL',
                              'countryId': {'inq': country_ids},
                              'singerId': None,
                              'url': {'neq': None},
                              'objectType': {'inq': img_types}
                              })
        try:
            _count_img = imageApi.image_clean_count(where=_filter)
            __count_img = int(_count_img.count)
            _count_sum += __count_img
        except Exception as e:
            logging.info(e)
            log(log_file, e)
            pass

    _filter = json.dumps({'type': 'NORMAL',
                          'singerId': {'inq': singer_ids},
                          'url': {'neq': None},
                          'objectType': {'inq': img_types}
                          })

    try:
        _count_img = imageApi.image_clean_count(where=_filter)
        __count_img = int(_count_img.count)
        _count_sum += __count_img
    except:
        pass

    if _count_sum > limit:
        rand_limit = random.randint(0, _count_sum - limit)

    # Find image MEN or WOMEN
    if _object_status:
        _filter = json.dumps({"skip": rand_limit, "limit": limit,
                             "where": {'type': 'NORMAL',
                                       'countryId': {'inq': country_ids},
                                       'singerId': None,
                                       'url': {'neq': None},
                                       'objectType': {'inq': img_types}}})
        try:
            _images = imageApi.image_clean_find(filter=_filter)
            if len(_images) != 0:
                images += _images
        except:
            pass

    # Find image singer
    _filter = json.dumps({"skip": rand_limit, "limit": limit,
                         "where": {'type': 'NORMAL',
                                   'singerId': {'inq': singer_ids},
                                   'url': {'neq': None},
                                   'objectType': {'inq': img_types}}})
    try:
        _images = imageApi.image_clean_find(filter=_filter)
        if len(_images) != 0:
            images += _images
    except:
        pass

    # Get images
    images_final = []
    for image in images:
        # _tmp = dict()
        _image = Image(image, api_cli, base_dir, base_url, token, log_file)
        _id = _image.id()
        _path = _image.path()
        if _id is False or _path is False:
            continue

        images_final.append(_path)

    # Check images was downloads
    if len(images_final) == 0:
        _content = "Can not download image in channel"
        log(log_file, _content)
        data = Struct(**data_images)
        data.set_error()

        try:
            notice_error(notificationApi, channel, _content)
        except:
            pass

        return data

    # Get template from channel
    logging.info(f"Get data template for {int(channel_id)}")
    try:
        _filter = json.dumps({"where": {'channelId': channel_id}})
        channel_img_list = channelImgApi.channel_image_find(filter=_filter)

        if len(channel_img_list) == 0:
            _content = "Template must be choose in channel config"
            log(log_file, _content)
            data = Struct(**data_images)
            data.set_error()

            try:
                notice_error(notificationApi, channel, _content)
            except:
                pass

            return data

        data_templates = get_data_templates(channel_img_list, token, base_dir, base_url,
                                            fontApi, imageApi, log_file, notificationApi, channel)

        random.shuffle(data_templates)

    except Exception as error:
        _content = f"Can not get data template from channel"

        log(log_file, f'{_content}\n{error}')
        data = Struct(**data_images)
        data.set_error()

        try:
            notice_error(notificationApi, channel, _content)
        except:
            pass

        return data

    if len(data_templates) == 0:
        _content = "Can not get template data"
        log(log_file, _content)

        data = Struct(**data_images)
        data.set_error()

        try:
            notice_error(notificationApi, channel, _content)
        except:
            pass

        return data

    _img_data = dict()
    _img_data['error_status'] = True
    img_data = Struct(**_img_data)

    for template in data_templates:
        try:
            _style = template.typeTemplate
        except Exception as error:
            log(log_file, f"Can not get style in template\n{error}")
            continue

        if _style == "template_auto":
            img_data = get_data_auto(model, title, channel, api_cli, base_dir, base_url, token, images_final,
                                     list_singers=list_singers, list_songs=list_songs, log_file=log_file)
            if img_data.error_status:
                continue
            else:
                break

        elif _style == "template_generation_worship":
            img_data = get_data_worship(template, model, channel, api_cli, base_dir,
                                        list_singers=list_singers, list_songs=list_songs, log_file=log_file)

            if img_data.error_status:
                continue
            else:
                break

        elif _style in ["template_topsong", "template_top_songs_no_edge",
                        'template_generation_multi', "top_songs_no_edge",
                        'top_songs']:
            img_data = get_data_top_song(template, model, _style, channel, api_cli, base_dir, images_final,
                                         list_singers=list_singers, list_songs=list_songs, log_file=log_file)
            if img_data.error_status:
                continue
            else:
                break

        else:
            log(log_file, f"style of template is {_style} not True")

    if img_data.error_status:
        _content = f"Can not create image for channel {channel_id}"
        log(log_file, _content)

        data = Struct(**data_images)
        data.set_error()

        try:
            notice_error(notificationApi, channel, _content)
        except:
            pass

        return data

    return img_data








