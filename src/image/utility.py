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

from src.log_status import log
from src.utilitys import Struct, download
from src.notification import notice_error, notice_warning
from src.font import get_fonts, get_font_by_id

# from wrapt_timeout_decorator import timeout

from func_timeout import func_set_timeout

import json
import os
import time
import random
import urllib


# Get color from Database
def _get_color_collum_align(img):
    """

    :param img:
    :return:
    """
    try:
        collum = img.meta_data['listCol']
    except Exception as error:
        print(error)
        collum = 1

    try:
        align = img.meta_data['listAlign']
        align = align.lower()
    except Exception as error:
        print(error)
        align = 'left'
    try:
        # print(type(img.meta_data['textColor']), img.meta_data['textColor'])
        if not img.meta_data['textColor']:
            color_text = (255, 255, 255)
            color_singer = (255, 255, 255)
        else:
            color_hex = img.meta_data['textColor'].split(',')

            if len(color_hex) == 1:
                color_singer = (255, 255, 255)
            else:
                hex_singer = str(color_hex[1].strip()).lstrip('#')
                color_singer = tuple(int(hex_singer[i:i + 2], 16) for i in (0, 2, 4))

            hex_text = str(color_hex[0].strip()).lstrip('#')
            color_text = tuple(int(hex_text[i:i + 2], 16) for i in (0, 2, 4))

    except Exception as error:
        print(error)
        color_text = (255, 255, 255)
        color_singer = (255, 255, 255)

    return collum, color_text, color_singer, align


def _path_img(base_dir, log_file):
    if not os.path.isdir(base_dir):
        try:
            os.mkdir(base_dir)
        except Exception as error:
            log(log_file, f"{base_dir} was not find")
            return False

    path = base_dir + '/data/images'

    if not os.path.isdir(path):
        if not os.path.isdir(base_dir + '/data'):
            try:
                os.mkdir(base_dir + '/data')
            except Exception as error:
                log(log_file, f"can not create {base_dir}/data\n{error}")
                return False
        try:
            os.mkdir(path)
        except Exception as error:
            log(log_file, f"can not create {base_dir}/data\n{error}")
            return False

    return path


# @timeout(10 * 60)
def _download_image(path, url, base_url, token):
    filename = path + '/' + str(url)
    if os.path.isfile(filename):
        return filename

    try:
        path_local = download(str(url) + '?access_token=' + token, filename)

    except Exception as error:
        print(error)

    if not path_local:
        try:
            url = str(base_url) + 'images/download/' + str(url)
            urllib.request.urlretrieve(str(url) + '?access_token=' + token, filename)
            return filename

        except Exception as e:
            print(e)
            return False

    return path_local


class Template:
    def __init__(self, font_api, base_dir, base_url, img, log_file, token, notification_api, channel=False):
        self.font_api = font_api
        self.base_dir = base_dir
        self.base_url = base_url
        self.log_file = log_file
        self.token = token
        self.img = img
        self.notification_api = notification_api
        self.channel = channel

    def template_top_song(self,
                          path_img_txt, list_path_img_ob,
                          song_font_id, singer_font_id,
                          path_img_frame, type_template):
        font_api = self.font_api
        base_dir = self.base_dir
        base_url = self.base_url
        log_file = self.log_file
        token = self.token

        path = _path_img(base_dir, log_file)
        if not path:
            return False

        try:
            collum, color_text, color_singer, align = _get_color_collum_align(self.img)
        except Exception as error:
            print(error)
            collum, color_text, color_singer, align = 1, (255, 255, 255), (255, 255, 255), 'left'
        try:
            img_txt = _download_image(path, path_img_txt, base_url, token)
            img_frame = _download_image(path, path_img_frame, base_url, token)
        except Exception as e:
            print(e)
            log(log_file, f"Can not download image {path_img_frame}, {path_img_txt}")
            return False

        if img_txt is False or img_frame is False:
            log(log_file, f"Can not download image {path_img_frame}, {path_img_txt}")
            return False

        list_path_img_ob_tmp = list_path_img_ob.copy()
        list_path_img_ob = []

        for url in list_path_img_ob_tmp:
            try:
                path_local = _download_image(path, url, base_url, token)
            except Exception as e:
                print(e)
                list_path_img_ob = []
                break

            if not path_local:
                list_path_img_ob = []
                break

            list_path_img_ob.append(path_local)

        if len(list_path_img_ob) == 0:
            return False

        try:
            singer_font = get_font_by_id(font_api, singer_font_id, base_dir, base_url, log_file, token)

        except Exception as e:
            _content = "Singer font was not found"
            log(log_file, _content)
            notice_warning(self.notification_api, self.channel, _content)
            print(e)
            pass

        try:
            song_font = get_font_by_id(font_api, song_font_id, base_dir, base_url, log_file, token)
        except Exception as e:
            print(e)
            _content = "Song font was not found"
            log(log_file, _content)
            notice_error(self.notification_api, self.channel, _content)
            return False

        if song_font is False:
            return False

        # try:
        #     singer_font = _singer_font.path_local
        #     song_font = _song_font.path_local
        # except Exception as e:
        #     _content = f"Can not download font with id {song_font_id} {singer_font_id}"
        #     log(log_file, f"{_content}\n {e}")
        #     return False

        data = {
            'img_txt': img_txt,
            'img_frame': img_frame,
            'list_path_img_ob': list_path_img_ob,
            'singer_font': singer_font,
            'song_font': song_font,
            'collum': collum,
            'align': align,
            'color_text': color_text,
            'color_singer': color_singer,
            'typeTemplate': 'top_songs_no_edge'
        }

        return data

    def template_worship(self, url_img_txt,
                         song_font_id, singer_font_id,
                         url_img_frame, type_template):
        """

        :param url_img_txt:
        :param song_font_id:
        :param singer_font_id:
        :param url_img_frame:
        :param type_template:
        :return:
        """

        try:
            collum, color_text, color_singer, align = _get_color_collum_align(self.img)
        except Exception as error:
            print(error)
            collum, color_text, color_singer, align = 1, (255, 255, 255), (255, 255, 255), 'left'

        font_api = self.font_api
        base_dir = self.base_dir
        base_url = self.base_url
        log_file = self.log_file
        token = self.token

        path = _path_img(base_dir, log_file)
        if not path:
            return False
        try:
            img_txt = _download_image(path, url_img_txt, base_url, token)
            img_frame = _download_image(path, url_img_frame, base_url, token)
        except Exception as e:
            log(log_file, f"Can not downloads image tempalte\n{e}")
            return False

        if img_txt is False or img_frame is False:
            return False

        try:
            song_font = get_font_by_id(font_api, song_font_id, base_dir, base_url, log_file, token)
            # song_font = _song_font.path_local
            singer_font = get_font_by_id(font_api, singer_font_id, base_dir, base_url, log_file, token)
            # singer_font = _singer_font.path_local
        except Exception as e:
            log(log_file, f"Can not download font for template\n{e}")
            return False

        if singer_font is False or song_font is False:
            return False

        data = {
            'img_txt': img_txt,
            'img_frame': img_frame,
            'singer_font': singer_font,
            'song_font': song_font,
            'collum': collum,
            'align': align,
            'color_text': color_text,
            'color_singer': color_singer,
            'typeTemplate': 'template_generation_worship'
        }

        return data
