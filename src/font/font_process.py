"""""""""""""""""""""""
Author : NGUYEN DINH HAI
VER    : 1.0
DATE   : 2021, JUL 12
"""""""""""""""""""""""

from src.log_status import log
from src.utilitys import download, Struct
from func_timeout import func_timeout

import os
import requests
import urllib.request
import json
import random


class Font:
    path_local = None
    id = None

    def __init__(self, font, log_file, base_dir, base_url, token):
        self.font = font
        self.log_file = log_file
        self.base_url = base_url
        self.base_dir = base_dir
        self.token = token

    def get_id(self):
        try:
            _id = int(self.font.id)
            self.id = _id
            return _id
        except Exception as e:
            _content = f"Can not get id font\n{e}"
            log(self.log_file, _content)
            return False

    def path(self):
        try:
            __extend = self.font.url.split(".")[-1]
        except Exception as e:
            _content = f"Can not get url font\n{e}"
            log(self.log_file, _content)
            return False
        __path = f'{self.base_dir}/data/fonts/{int(self.font.id)}.{__extend}'

        if os.path.isfile(__path):
            return __path

        try:
            print(f"Downloading font: {__path}")
            url = str(self.base_url) + 'fonts/download/' + str(self.font.url)

            try:
                urllib.request.urlretrieve(str(url) + '?access_token=' + self.token, __path)
                self.path_local = __path
                return __path
            except:
                try:
                    __path = func_timeout(3 * 60, download, args=(str(url) + '?access_token=' + self.token,
                                                                  __path))
                    self.path_local = __path
                    return __path
                except Exception as e:
                    log(self.log_file, e)
                    return False

        except Exception as e:
            log(self.log_file, e)
            return False


def get_font_by_id(fontApi, id_font, base_dir, base_url, log_file, token):
    """

    :param fontApi:
    :param id_font:
    :param base_dir:
    :param base_url:
    :param log_file:
    :param token:
    :return:
    """
    if fontApi is None:
        return []

    _path_font = f"{base_dir}/data/fonts"

    if not os.path.isdir(_path_font):
        try:
            os.mkdir(base_dir)
        except:
            pass

        try:
            os.mkdir(f'{base_dir}/data')
        except:
            pass

        try:
            os.mkdir(_path_font)
        except Exception as e:
            log(log_file, f"Can not create {_path_font}\n {e}")
            return []

    try:
        font = fontApi.font_family_find_by_id(id=id_font)
    except Exception as e:
        log(log_file, f"Font {id_font} was not found\n {e}")
        return False

    font_ob = Font(font, log_file, base_dir, base_url, token)
    _id = font_ob.get_id()
    _path = font_ob.path()

    if _id is False or _path is False:
        log(log_file, f"Font {id_font} can not download")
        return False

    return _path


def get_fonts(font_api, language_id, base_dir, base_url, log_file, kind, token):
    """

    :param font_api:
    :param language_id:
    :param base_dir:
    :param base_url:
    :param log_file:
    :param kind:
    :param token:
    :return:
    """
    if font_api is None:
        return []

    _path_font = f"{base_dir}/data/fonts"

    if not os.path.isdir(_path_font):
        try:
            os.mkdir(base_dir)
        except:
            pass

        try:
            os.mkdir(f'{base_dir}/data')
        except:
            pass

        try:
            os.mkdir(_path_font)
        except Exception as e:
            log(log_file, f"Can not create {_path_font}\n {e}")
            return []

    if kind is None:
        return []

    data_fonts = []

    _filter = json.dumps({"where": {"languageId": language_id, "kind": kind}})
    _fonts = font_api.font_family_find(filter=_filter)

    if len(_fonts) == 0:
        return []
    elif len(_fonts) <= 5:
        random.shuffle(_fonts)
    else:
        random.shuffle(_fonts)
        _fonts = _fonts[:5]

    for font in _fonts:
        tmp_data = dict()
        if font.url is None:
            continue

        font_ob = Font(font, log_file, base_dir, base_url, token)
        _id = font_ob.get_id()
        _path = font_ob.path()
        if _id is False or _path is False:
            continue
        tmp_data['id'] = _id
        tmp_data['path_local'] = _path

        data = Struct(**tmp_data)
        data_fonts.append(data)

    return data_fonts
