"""""""""""""""""""""""
Author : NGUYEN DINH HAI
VER    : 1.0
DATE   : 2021, JUL 12
"""""""""""""""""""""""


from image_processing import image_processing
from decouple import config
from datetime import datetime, timezone
from dateutil.tz import tzlocal
from random import randint
from requests import get
from func_timeout import func_set_timeout
from src.log_status import log
from src.notification import notice_error, notice_warning

# from wrapt_timeout_decorator import timeout

import random
import time
import requests
import os
import json
import re
import shutil
import urllib.request
import youtube_dl
import logging


# Set logging to print status
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

    def set_error(self):
        error_status = {"error_status": True}
        self.__dict__.update(error_status)


# check exist video for channel
def get_video_for_channel(base_dir):
    video_created = []

    if not os.path.isdir(base_dir + '/products'):
        return video_created

    if not os.path.isdir(base_dir + '/products/infos/'):
        return video_created

    for path in os.listdir(base_dir + '/products/infos/'):
        channel_id = path.split('.')[0].split('=')[-1]
        video_created.append(float(channel_id))

    return video_created


def extract_name(name):
    if name is None:
        return ""
    check = False
    res = ""

    for i in name:
        if i == '(':
            check = True
            continue
        if i == ')':
            check = False
            continue
        if check:
            continue
        res += i

    res = res.translate({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|~-=_+"})
    res = re.sub(' +', ' ', res)
    final_names = []

    for word in res.split(' '):
        try:
            if len(word) > 1:
                new_word = word[0].upper() + word[1:].lower()
            else:
                new_word = word[0].upper()
            final_names.append(new_word)
        except:
            pass

    final_name = " ".join(final_names)
    return final_name


def check_created_video(base_dir, channel_id):
    if base_dir is None:
        return True

    if channel_id is None:
        return True

    log_file = f"{base_dir}/logger/channel_{int(channel_id)}.log"

    path_folder_info = base_dir + '/products/infos'
    for path in os.listdir(path_folder_info):
        path_tmp = path
        _channel_id = path.split('.')[0].split('=')[-1]
        if int(channel_id) == int(_channel_id):
            channel_file_info = f'{path_folder_info}/{path_tmp}'

            try:
                with open(channel_file_info) as json_file:
                    data = json.load(json_file)
                    # print(data)
            except ValueError as error:
                print(error)
                log(log_file, error)

                try:
                    os.remove(channel_file_info)
                except Exception as error:
                    print(error)
                    log(log_file, error)
                return True
            try:
                path_video = data['path_video']
                if os.path.isfile(path_video) is False:
                    try:
                        os.remove(channel_file_info)
                    except Exception as error:
                        print(error)
                        log(log_file, error)
                    return True

            except Exception as error:
                print(error)
                log(log_file, error)

                try:
                    os.remove(channel_file_info)
                except Exception as error:
                    print(error)
                    log(log_file, error)

                return True

            return False

    return True


def sort_rank_audio(list_obj):
    for i in range(0, len(list_obj)):
        for j in range(i + 1, len(list_obj) - 1):
            if not list_obj[j]:
                continue

            if not list_obj[i]:
                continue

            if list_obj[i].rank > list_obj[j].rank:
                list_obj[i], list_obj[j] = list_obj[j], list_obj[i]

    return list_obj


def sort_list(list_obj):
    for i in range(0, len(list_obj)):
        for j in range(i + 1, len(list_obj) - 1):
            try:
                if not list_obj[i].views and not list_obj[j].views:
                    if list_obj[i].total_rating * list_obj[j].numbers_of_rating > \
                            list_obj[j].total_rating * list_obj[i].numbers_of_rating:
                        list_obj[i], list_obj[j] = list_obj[j], list_obj[i]
                elif not list_obj[j].views:
                    continue
                elif not list_obj[i].views:
                    list_obj[i], list_obj[j] = list_obj[j], list_obj[i]
                elif list_obj[j].views == 0:
                    list_obj[i], list_obj[j] = list_obj[j], list_obj[i]
                elif list_obj[i].views == 0 or \
                        list_obj[i].views < list_obj[j].views:
                    list_obj[i], list_obj[j] = list_obj[j], list_obj[i]
            except:
                pass

    return list_obj


# # @func_set_timeout(500)
# @timeout(500)
# def download_audio_from_youtube(path_local, id_youtube):
#     if path_local is None:
#         return None
#
#     if id_youtube is None:
#         return None
#
#     try:
#         url = 'https://www.youtube.com/watch?v=' + id_youtube
#
#         ydl_opts = {
#             'format': 'bestaudio/best',
#             'outtmpl': path_local,
#             'postprocessors': [{
#                 'key': 'FFmpegExtractAudio',
#                 'preferredcodec': 'mp3',
#                 'preferredquality': '192',
#             }],
#         }
#         with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#             ydl.download([url])
#
#         return path_local
#     except Exception as error:
#         print(error)
#
#     return None

# @timeout(10*60)
def download(url, file_name):
    print(f"Downloading {file_name}")
    try:
        with open(file_name, "wb") as file:
            response = requests.get(url)
            if response.status_code == 200:
                file.write(response.content)
            else:
                print(f"Can not download {file_name} {response}")
                return False

    except Exception as error:
        print(error)
        return False

    return file_name


def convert_second_to_time(time_seconds):
    try:
        m, s = divmod(time_seconds, 60)
        h, m = divmod(m, 60)
        time_start = "%02d:%02d:%02d" % (h, m, s)
    except:
        h = time_seconds / 3600
        time_seconds = time_seconds % 3600
        m = time_seconds / 60
        s = time_seconds % 60
        time_start = "%02d:%02d:%02d" % (h, m, s)
    return time_start


def gen_description(datas):
    description = ''
    start_audio = 0
    songs = []
    stt = 1
    for data in datas:
        for des in data['description']:
            duration = des['duration']
            name = des['name']
            time_start = convert_second_to_time(start_audio)
            line_i = f'[{time_start}] - {stt}. {name}\n'
            stt += 1
            if len(songs) < 3:
                songs.append(name.split('-')[0])
            start_audio += duration
            description += line_i
        break
    return description, ", ".join(songs)


def extract_data_response(notification_api, channel,
                          res, data_worship, video_title,
                          duration_min, duration_max, log_file):
    data = []
    len_song = 0
    description = []
    durations = 0
    try:
        channel_id = channel.id
    except Exception as e:
        log(log_file, f"Can not get channel id from channel\n{e}")
        return data

    try:
        for data_res in res.data:
            if durations // 60 >= duration_max:
                break
            try:
                path_img = data_res['path_img']
                url_audios = []
                audio_files = []

                for song in data_res['list_songs']:
                    check_false = False
                    for item in data_worship:
                        if item.name == song:
                            check_false = False
                            url_audios.append(item.path)
                            audio_files.append(item.audio)
                            duration = item.duration
                            durations += duration
                            song_singer = f'{song} - {item.singer}'
                            description.append({'duration': duration, 'name': song_singer})
                            break
                        else:
                            check_false = True

                    if check_false:
                        log(log_file, f"Can not find  {song} in data")
                        if durations // 60 < duration_min:
                            log(log_file, f'DURATION VIDEO {durations // 60} < duration_min {duration_min}')
                            return []
                    if durations // 60 >= duration_max:
                        break

                if len(url_audios) == 0:
                    break

                len_song = len_song + len(audio_files)

                data.append({
                    'audiosFile': audio_files,
                    'listUrlAudio': url_audios,
                    'path_bg': path_img,
                    'channel_id': channel_id,
                    'path_img': path_img,
                    'title': video_title,
                    'description': description
                })

                if durations / 60 >= 1.3 * duration_max:
                    _content = "Duration of video too big"
                    log(log_file, _content)
                    try:
                        notice_error(notification_api, channel, _content)
                    except Exception as e:
                        print(e)
                    data = []

                    return data

            except Exception as error:
                print(error)
                break

    except Exception as error:
        print(error)

    if int(durations / 60) < 0.7 * duration_min:
        _content = f"Duration of video is {durations//60} minute too small"
        log(log_file, _content)
        try:
            notice_error(notification_api, channel, _content)
        except Exception as e:
            print(e)

        data = []

        return data

    return data


# Get color from Database
def get_color_collum_align(img):
    """

    :param img:
    :return:
    """
    try:
        collum = img.meta_data['listCol']
    except Exception as error:
        logger.info(error)
        collum = 1

    try:
        align = img.meta_data['listAlign']
        align = align.lower()
    except Exception as error:
        logger.info(error)
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
        logger.info(error)
        color_text = (255, 255, 255)
        color_singer = (255, 255, 255)

    return collum, color_text, color_singer, align


# Get data for template to create image
def _get_template(channel_images, image_api):

    templates = []

    if not len(channel_images):
        return []

    images = []
    for channel_img in channel_images:
        try:
            image_clean_id = int(channel_img.image_clean_id)
            img = image_api.image_clean_find_by_id(image_clean_id)
            images.append(img)
        except Exception as error:
            logger.info(error)
            continue

    if not len(images):
        return []

    for img in images:
        if img.meta_data:
            _template = img.meta_data['typeTemplate']
            if _template in templates:
                continue
            templates.append(_template)

    return templates


def get_manual_images(list_img_input, base_dir, channel_id, token):
    if list_img_input is None:
        return []
    if base_dir is None:
        return []
    if channel_id is None:
        return []

    try:
        random.shuffle(list_img_input)
        random.shuffle(list_img_input)
        # random.shuffle(list_img_input)
    except:
        pass

    ids = []
    list_img_input = list_img_input[0: min(40, len(list_img_input))]
    base_url = config("BASE_URL")
    images = []
    path = base_dir + '/data/images/channel_id=' + str(int(channel_id))

    if os.path.isdir(path) is False:
        os.mkdir(path)

    list_img = list_img_input.copy()

    for i in range(0, len(list_img)):
        filename = path + '/' + list_img[i]
        print(f"Downloading image: {filename}")

        try:
            url = str(base_url) + 'images/download/' + str(list_img[i])
            urllib.request.urlretrieve(str(url) + '?access_token=' + token, filename)
            images.append(str(filename))
        except Exception as error:
            url = download(str(url) + '?access_token=' + token, filename)
            images.append(str(filename))

        time.sleep(.5)

    return images
