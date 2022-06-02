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

from func_timeout import func_timeout

from image_processing import image_processing

import json
import os
import logging
import time
import random
import urllib


class Image:
    path_local = False

    def __init__(self, img, api_cli, base_dir, base_url, token, log_file):
        self.img = img
        self.api_cli = api_cli
        self.base_dir = base_dir
        self.base_url = base_url
        self.token = token
        self.log_file = log_file

    def id(self):
        try:
            _id = int(self.img.id)
        except Exception as error:
            log(self.log_file, f"Have no id for image\n {error}")
            return False
        return _id

    def path(self):
        _extend = "jpg"
        try:
            _tmp_name = self.img.url.split(".")
            _extend = _tmp_name[len(_tmp_name)-1]
        except Exception as error:
            log(self.log_file, f"Have no url for image\n {error}")
            return False

        _path = f'{self.base_dir}/data/images/{int(self.img.id)}.{_extend}'

        if os.path.isfile(_path):
            # self.path_local = _path
            return _path

        try:
            print(f"Downloading image: {_path}")
            url = str(self.base_url) + 'images/download/' + str(self.img.url)

            try:
                path = func_timeout(5 * 60, download, args=(f"{str(url)}?access_token={self.token}", _path))
                # self.path_local = _path
                try:
                    return path
                except Exception as e:
                    print(e)
                    return str(path)

            except Exception as e:
                print(e)
                try:
                    urllib.request.urlretrieve(str(url) + '?access_token=' + self.token, _path)
                    # self.path_local = _path
                    return _path
                except Exception as e:
                    log(self.log_file, e)
                    return False

        except Exception as e:
            log(self.log_file, e)
            return False


def _get_background(img_api, base_dir, base_url, api_cli, token, log_file):

    if not img_api:
        return False
    if not base_dir:
        return False

    if not base_url:
        return False
    if not token:
        return False

    if not os.path.isdir(base_dir):
        try:
            os.mkdir(base_dir)
        except:
            return False

    _filter = json.dumps({'where': {'type': 'BACKGROUND', 'url': {'neq': None}}})
    backgrounds = img_api.image_clean_find(filter=_filter)

    if len(backgrounds) == 0:
        log(log_file, "Can not find background image from BD")
        return False

    random.shuffle(backgrounds)

    path = base_dir + '/data/images'

    if os.path.isdir(path) is False:

        try:
            os.mkdir(base_dir + '/data')
        except:
            pass
        try:
            os.mkdir(path)
        except Exception as e:
            log(log_file, f"Can not create {path}\n {e}")
            return False

    for indx in range(10):
        secure_choose = random.SystemRandom()
        img = secure_choose.choice(backgrounds)
        
        image_background = Image(img, api_cli, base_dir, base_url, token, log_file)
        _id = image_background.id()
        _path_local = image_background.path()
        
        if _id is False or _path_local is False:
            continue
            
        return _path_local

    return False


def get_data_auto(model, title, channel, api_cli, base_dir, base_url, token,
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

    path_output = f'{base_dir}/output_image'

    if not os.path.isdir(path_output):
        try:
            os.mkdir(path_output)
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
        language_id = channel.language_id

        if os.path.isdir(f"{base_dir}/logger") is False:
            try:
                os.mkdir(f"{base_dir}/logger")
            except Exception as e:
                print(e)

            log(log_file, f"Can not creat {base_dir}/logger")
            data = Struct(**data_image)
            data.set_error()

            return data
        log(log_file, f"Start create image template auto for channel {channel_id}")

    except Exception as error:
        log(log_file, f"Can not get channel id and status\n or {error}")
        data = Struct(**data_image)
        data.set_error()

        return data

    if _error_status:
        log(log_file, "Can not get channel information")
        data = Struct(**data_image)
        data.set_error()

        return data

    try:
        imageApi = ImageCleanApi(api_client=api_cli)
        # channelSingerApi = ChannelSingerApi(api_client=api_cli)
        notificationApi = NotificationApi(api_client=api_cli)
        # channelCountryApi = ChannelCountryApi(api_client=api_cli)
        fontApi = FontFamilyApi(api_client=api_cli)

    except Exception as error:
        log(log_file, f"could be not pass api client\n or {error}")
        data = Struct(**data_image)
        data.set_error()

        return data

    # Get title font and song font for template auto
    fonts_list = get_fonts(fontApi, language_id, base_dir, base_url, log_file, 'List', token)
    fonts_title = get_fonts(fontApi, language_id, base_dir, base_url, log_file, 'Title', token)

    if len(fonts_title) == 0 or len(fonts_list) == 0:
        _content = f"could be not download font for channel {channel_id}"
        log(log_file, _content)
        data = Struct(**data_image)
        data.set_error()

        try:
            notice_error(notificationApi, channel, _content)
        except:
            pass

        return data

    # Get background for template auto
    img_background = _get_background(imageApi, base_dir, base_url, api_cli, token, log_file)
    if not img_background:
        _content = "could be not download background image for template auto"
        log(log_file, _content)
        data = Struct(**data_image)
        data.set_error()

        try:
            notice_error(notificationApi, channel, _content)
        except:
            pass

        return data

    # Random choose color for title and list song
    sys_random = random.SystemRandom()
    list_color_title = [(255, 255, 255), (255, 255, 0),
                        (0, 208, 0), (255, 48, 0),
                        (0, 17, 0), (0, 48, 144)]

    color_title = sys_random.choice(list_color_title)
    color_title_secondary = sys_random.choice(list_color_title)
    color_text = (250, 250, 250)
    color_singer = (250, 250, 250)

    # Random choose title font
    _min_loop = min(len(fonts_title), len(fonts_list))
    font_title = False
    font_song = False
    font_title_secondary = False

    for i in range(_min_loop):
        secure_random = random.SystemRandom()
        _font_title = secure_random.choice(fonts_title)
        _font_title_secondary = secure_random.choice(fonts_title)
        _font_song = secure_random.choice(fonts_list)

        try:
            font_title = _font_title.path_local
            id_font_title = _font_title.id

            font_title_secondary = _font_title_secondary.path_local
            id_font_title_secondary = _font_title_secondary.id

            font_song = _font_song.path_local
            id_font_song = _font_song.id

        except Exception as e:
            log(log_file, e)
            if i == (_min_loop - 1):
                _content = f"could be not download font for channel"
                log(log_file, f'{_content}\n{e}')
                data = Struct(**data_image)
                data.set_error()

                try:
                    notice_error(notificationApi, channel, _content)
                except:
                    pass

                return data
            continue
        break

# Random choose title
    _titles = [title, '']
    title = sys_random.choice(_titles)

# Create image
    _status = 'error'
    _count_max = len(list_object)
    _count = 0
    path = {"status": "error"}

    while _status == "error":
        if _count > _count_max:
            break
        _count += 1

    # Random choose image singer
        sys_random = random.SystemRandom()
        singer_img = sys_random.choice(list_object)

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
            mode = False

        if mode is False:
            aligns = ['center', 'left', 'right']
            align = secure_random.choice(aligns)
        else:
            aligns = ['left', 'right']
            align = secure_random.choice(aligns)

        positions = ["left", "right"]
        ob_position = secure_random.choice(positions)

        _list_singers = []
        for singer in list_singers:
            _list_singers.append({"name": singer})

        _list_songs = []
        for song in list_songs:
            _list_songs.append({"name": song})

        _data = {"style": "auto",
                 "mode": mode,
                 "path_img_origin": singer_img,
                 "background": img_background,
                 "collum_mode": col_mod,
                 "ob_position": ob_position,
                 "data_list": {
                        "title": title,
                        "sum": len(list_songs),
                        "list_songs": _list_songs.copy(),
                        "list_singer": _list_singers.copy(),
                        "size_title": 100,
                        "size_txt": 28,
                        "align": align,
                        "path_font_song": font_song,
                        "path_font_singer": font_song,
                        "path_font_title": font_title,
                        "path_font_title_secondary": font_title_secondary,
                        "color_title": color_title,
                        "color_title_secondary": color_title_secondary,
                        "color_song": color_text,
                        "color_singer": color_singer,
                    }

        }

        try:
            path = image_processing(data=_data, net=model, path_output=path_output)
            _status = path["status"]
        except Exception as error:
            log(log_file, f"Can not create image for template auto {error} with data is \n {_data}")
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
    data_image['id_font_title'] = id_font_title

    data = Struct(**data_image)

    return data










