"""""""""""""""""""""""
Author : NGUYEN DINH HAI
VER    : 1.0
DATE   : 2021, JUL 12
"""""""""""""""""""""""

from src.log_status import log
from src.utilitys import Struct, download
from src.notification import notice_error, notice_warning
from src.font import Font, get_font_by_id

from .utility import Template

# from func_timeout import func_set_timeout

import json
import os
import time
import random
import urllib


# Get data for template to create image
def get_data_templates(channel_img_list, token, base_dir, base_url,
                       font_api, image_api, log_file, notification_api, channel):

    if len(channel_img_list) == 0:
        _content = "Can not find template in channel"
        log(log_file, "Can not find template in channel")
        try:
            notice_error(notification_api, channel, _content)
        except Exception as e:
            print(e)

        return []

    # Find image was config in channel
    images = []

    for channel_img in channel_img_list:
        try:
            image_clean_id = int(channel_img.image_clean_id)
            img = image_api.image_clean_find_by_id(image_clean_id)
            images.append(img)
        except Exception as error:
            _content = f"Image was not found for template, please check image of template again"
            log(log_file, f"Image was not found for template\n {error}")
            try:
                notice_warning(notification_api, channel, _content)
            except Exception as e:
                print(e)
            continue

    if len(images) == 0:
        _content = "Can not find image of template in channel"
        log(log_file, f"Can not find image of template in channel")
        try:
            notice_error(notification_api, channel, _content)
        except Exception as e:
            print(e)

        return []

    # sum_template = 0
    #
    # for x in images:
    #     if x.meta_data:
    #         sum_template += 1

    data_templates = []

    for img in images:
        template = Template(font_api, base_dir, base_url, img, log_file, token, notification_api, channel)

        try:
            _meta_style = img.meta_data['typeTemplate']
        except Exception as e:
            print(e)
            continue

        if _meta_style == 'template_grayscale':
            _data = {
                'id': int(img.id),
                'typeTemplate': 'template_grayscale'
            }
            data = Struct(**_data)
            data_templates.append(data)

        elif _meta_style == 'template_auto':
            _data = {
                'id': int(img.id),
                'typeTemplate': 'template_auto'
            }
            data = Struct(**_data)
            data_templates.append(data)

        elif _meta_style == 'template_generation_worship':
            try:
                img_txt = img.meta_data['list']
                song_font_id = img.meta_data['songFontId']
                singer_font_id = img.meta_data['singerFontId']
                img_frame = img.meta_data['source']
                type_template = img.meta_data['typeTemplate']
                _data = template.template_worship(img_txt, song_font_id, singer_font_id,
                                                  img_frame, type_template)

                if _data:
                    _data['id'] = int(img.id)
                    _data['title_font_id'] = None
                    _data['song_font_id'] = song_font_id

                    data = Struct(**_data)
                    data_templates.append(data)

            except Exception as error:
                print(error)

        elif _meta_style in ["template_topsong", "template_top_songs_no_edge",
                             'template_generation_multi', 'top_songs_no_edge']:

            try:
                img_txt = img.meta_data['list']
                list_img_ob = img.meta_data['object']
                song_font_id = img.meta_data['songFontId']
                singer_font_id = img.meta_data['singerFontId']
                img_frame = img.meta_data['source']
                type_template = img.meta_data['typeTemplate']
                _data = template.template_top_song(img_txt, list_img_ob,
                                                   song_font_id, singer_font_id,
                                                   img_frame, type_template)

                if _data is False:
                    continue
                else:
                    _data['id'] = int(img.id)
                    _data['title_font_id'] = None
                    _data['song_font_id'] = song_font_id

                    data = Struct(**_data)
                    data_templates.append(data)

            except Exception as error:
                print(error)
                continue

    return data_templates
