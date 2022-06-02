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
from src.utilitys import Struct
from src.notification import notice_error

from func_timeout import func_set_timeout

from image_processing import image_processing

import json
import os
import logging
import random


def get_data_top_song(data_template, model, type_template, channel, api_cli, base_dir,
                      list_object, list_singers, list_songs, log_file):

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

    if len(list_object) == 0:
        _content = "Can not find singer image"
        log(log_file, _content)
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
        singer_ids = channel.singer_ids
        singer_mode = channel.singer_mode

        if os.path.isdir(f"{base_dir}/logger") is False:
            try:
                os.mkdir(f"{base_dir}/logger")
            except Exception as e:
                print(e)

        log(log_file, f"Start generation image  data for channel {channel_id}")

    except Exception as error:
        logging.info(f"Can not get channel id and status\n or {error}")
        data = Struct(**data_image)
        data.set_error()

        return data

    try:
        # imageApi = ImageCleanApi(api_client=api_cli)
        # channelSingerApi = ChannelSingerApi(api_client=api_cli)
        notificationApi = NotificationApi(api_client=api_cli)
        # channelCountryApi = ChannelCountryApi(api_client=api_cli)
        # fontApi = FontFamilyApi(api_client=api_cli)

    except Exception as error:
        log(log_file, f"could be not pass api client\n or {error}")
        data = Struct(**data_image)
        data.set_error()

        return data

    # Get attribute for template
    try:
        path_img_txt = data_template.img_txt
        list_path_img_ob = data_template.list_path_img_ob
        _img_frame = data_template.img_frame

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
        data.set_error()

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
    _count_max = len(list_object) if len(list_object) < 8 else 8
    _count = 0
    _tmp_list = list_object.copy()
    list_path_img_origin = []
    path = {"status": "error"}

    while _status == "error":
        if _count > _count_max:
            break
        _count += 1

    # Random choose image object
        for idx in range(len(list_path_img_ob)):
            random_sys = random.SystemRandom()
            _tmp_img = random_sys.choice(_tmp_list)
            _tmp_list.remove(_tmp_img)
            list_path_img_origin.append(_tmp_img)
        # Check len image singer and len image list mark object
        if len(list_path_img_ob) != len(list_path_img_origin):
            list_path_img_origin.clear()
            _tmp_list = list_object.copy()
            continue

    # Random style for text
        secure_random = random.SystemRandom()
        list_collum_mode = [1, 2, "title_style"]
        col_mod = secure_random.choice(list_collum_mode)

        if col_mod != "title_style":
            col_mod = secure_random.choice(list_collum_mode)

        if col_mod == 1:
            modes = ['no_line', 'singer']
            mode = secure_random.choice(modes)
        else:
            mode = False

        if singer_mode == 'SINGER' or singer_mode == 'SINGERS':
            mode = 'singer'

        _data = {
                "style": type_template,
                "list_path_img_origin": list_path_img_origin,
                "path_img_txt": path_img_txt,
                "list_path_img_ob": list_path_img_ob,
                "img_frame": _img_frame,
                "collum_mode": collum_mode,
                "data_list": {
                            "path_font_song": font_song,
                            "path_font_singer": font_singer,
                            "size_txt": 25,
                            "color_song": color_text,
                            "color_singer": color_singer,
                            "offset": int(1),
                            "mode": mode,
                            "align": align,
                            "sum": len(_list_songs),
                            "list_songs": _list_songs.copy(),
                            "list_singer": _list_singers.copy()
                            }
                }

        try:
            path = image_processing(data=_data, net=model, path_output=base_dir)
            _status = path["status"]
        except Exception as error:
            log(log_file, f"Can not create image for template top song \n {error}\n with data is {_data}")
            continue

    if _status == 'error':
        _content = "can not create image for template auto"
        log(log_file, _content)
        data = Struct(**data_image)
        data.set_error()

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
