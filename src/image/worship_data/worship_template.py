"""""""""""""""""""""""
Author : NGUYEN DINH HAI
VER    : 1.0
DATE   : 2021, JUL 12
"""""""""""""""""""""""

from moviepy.editor import AudioFileClip, ImageClip, VideoFileClip, concatenate_audioclips, concatenate_videoclips

from swagger_client import ImageCleanApi, FontFamilyApi, LanguageApi
from swagger_client import AudioCleanApi, SingerApi
from swagger_client import ChannelApi, ChannelCountryApi, ChannelSingerApi, ChannelImageApi
from swagger_client import NotificationApi

from src.log_status import log
from src.utilitys import Struct, download
from src.font import Font, get_fonts, get_font_by_id
from src.notification import notice_error, notice_warning
from ..auto_data import Image

from func_timeout import func_set_timeout

from image_processing import image_processing

import json
import os
import logging
import time
import random
import urllib


def get_data_worship(data_template, model, channel, api_cli, base_dir,
                     list_singers, list_songs, log_file):

    data_image = dict()
    data_image['error_status'] = False

    if not os.path.isdir(base_dir):
        try:
            os.mkdir(base_dir)
        except Exception as error:
            log(log_file, f"Can not find {base_dir}\n {error}")
            data = Struct(**data_image)
            data.set_error()
            return data

    base_dir = f'{base_dir}/output_image'

    if not os.path.isdir(base_dir):
        try:
            os.mkdir(base_dir)
        except Exception as error:
            log(log_file, f"Can not find {base_dir}\n {error}")
            data = Struct(**data_image)
            data.set_error()
            return data

    if not os.path.isdir(base_dir):
        try:
            os.mkdir(base_dir)
        except Exception as e:
            logging.info(f"{base_dir} was not found\n{e}")
            data = Struct(**data_image)
            data.set_error()
            return data

    try:
        channel_id = channel.id
        _error_status = channel.error_status
        # singer_ids = channel.singer_ids
        # meta_data = channel.meta_data
        # img_types = channel.img_types
        # country_ids = channel.country_ids
        # language_id = channel.language_id

        if os.path.isdir(f"{base_dir}/logger") is False:
            try:
                os.mkdir(f"{base_dir}/logger")
            except Exception as e:
                print(e)

    except Exception as error:
        logging.info(f"Can not get channel id and status\n or {error}")
        data = Struct(**data_image)
        data.set_error()

        return data

    try:
        notificationApi = NotificationApi(api_client=api_cli)

    except Exception as error:
        log(log_file, f"could be not pass api client\n or {error}")
        data = Struct(**data_image)
        data.set_error()

        return data

    # Get attribute for template
    try:
        logging.info(f"Generate image generation worship channel {channel_id} for video...")
        img_txt = data_template.img_txt
        img_frame = data_template.img_frame

        font_song = data_template.song_font
        id_font_song = data_template.song_font_id
        font_singer = data_template.singer_font

        color_text = data_template.color_text
        color_singer = data_template.color_singer

        align = data_template.align
        collum_mode = data_template.collum
    except Exception as error:
        _content = "Can not get attribute from template"
        log(log_file, f"{_content}\n{error}")
        data = Struct(**data_image)

        try:
            notice_error(notificationApi, channel, _content)
        except:
            pass

        return data

    # Get list song and list singer follow format
    _list_singers = []
    for singer in list_singers:
        _list_singers.append({"name": singer})

    _list_songs = []
    for song in list_songs:
        _list_songs.append({"name": song})

    # Create image
    _status = 'error'
    _count_max = 3
    _count = 0
    path = {"status": "error"}

    while _status == "error":
        if _count > _count_max:
            break
        _count += 1

        # Random style for text
        secure_random = random.SystemRandom()
        list_collum_mode = [1, 2, "title_style"]
        col_mod = secure_random.choice(list_collum_mode)
        modes = ['no_line', 'singer']

        if col_mod != "title_style":
            col_mod = secure_random.choice(list_collum_mode)

        if col_mod == 1:
            modes = ['no_line', 'singer']
            mode = secure_random.choice(modes)
        else:
            mode = "singer"

        _data = {
                "style": "template_generation_worship",
                "path_img_txt": img_txt,  # no name copy
                'img_frame': img_frame,
                'collum_mode': collum_mode,
                "data_list": {
                    "path_font_singer": font_singer,
                    "path_font_song": font_song,
                    "size_txt": 33,
                    "mode": mode,
                    "color_song": color_text,
                    "color_singer": color_singer,
                    "sum": len(list_songs),
                    "list_songs": _list_songs.copy(),
                    "align": align,
                    "list_singer": _list_singers.copy()
                    }
                }

        try:
            path = image_processing(data=_data, net=model, path_output=base_dir)
            _status = path["status"]
        except Exception as error:
            log(log_file, f"Can not create image for template generation worship \n {error}\n with data is {_data}")
            continue

    if _status == 'error':
        _content = "can not create image for template auto"
        log(log_file, _content)
        data = Struct(**data_image)

        try:
            notice_error(notificationApi, channel, _content)
        except:
            pass

        return data

    _path = Struct(**path)
    data_image['data'] = _path
    data_image['id_font_song'] = id_font_song
    data_image['id_font_title'] = None

    data = Struct(**data_image)

    return data
