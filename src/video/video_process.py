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
from decouple import config

from moviepy.editor import ImageClip, VideoFileClip, concatenate_audioclips, concatenate_videoclips
from datetime import date, datetime

from src.log_status import log
from src.utilitys import gen_description
from io import BytesIO

import json
import os
import logging
import time

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filemode='w')


def handle_video(datas, base_dir, video_title, title_singer, channel_id,
                 status_song, song_font_id, title_font_id, live_status=False):
    """

    :param datas:
    :param base_dir:
    :param video_title:
    :param title_singer:
    :param channel_id:
    :param status_song:
    :param song_font_id:
    :param title_font_id:
    :param live_status:
    :return:
    """

    cnt = int(0)
    list_path_video = []
    sum = 0
    log_file = f"{base_dir}/logger/channel_{int(channel_id)}.log"
    bitrate = None

    if os.path.isfile(log_file) is False:
        try:
            os.mkdir(f"{base_dir}/logger")
        except Exception as error:
            print(error)
            pass

    if live_status:
        # Live video set bitrate is 2,6M
        bitrate = 2600000

    for dataProduct in datas:
        cnt += 1
        audio_files = dataProduct['audiosFile']

        if not len(audio_files):
            log(log_file, 'could be not find audios file')
            return "error"

        sum = sum + len(audio_files)

        try:
            audio = concatenate_audioclips(audio_files)
            image = ImageClip(dataProduct['path_bg']).set_duration(audio.duration)
            video = image.set_audio(audio)
            if len(datas) > 1:
                path_local = base_dir + '/products/videos/' + str(date.today().strftime("%b-%d-%Y")) + '-' + str(
                    datetime.now().time()) + '-' + str(cnt) + '.flv'
            else:
                path_local = base_dir + f'/products/videos/channel_id={str(channel_id)}.flv'

            tmp_url_audio = str(date.today().strftime("%b-%d-%Y")) + '-' + str(datetime.now().time()) + '.m4a'

            video.to_videofile(path_local, fps=1, codec="libx264",
                               temp_audiofile=base_dir + '/tmp_audio/' + tmp_url_audio,
                               remove_temp=True,
                               bitrate=bitrate,
                               audio_codec='aac')

            list_path_video.append(path_local)

        except Exception as error:
            log(log_file, f"Cant not create this video because {error}")
            continue

    path_local = base_dir + f'/products/videos/channel_id={str(channel_id)}.flv'
    status_false = False

    # concatenate video
    if len(list_path_video) > 1:
        tmp_video = []

        for path_video in list_path_video:
            try:
                tmp_video.append(VideoFileClip(path_video))
            except Exception as error:
                log(log_file, error)
                status_false = True
                break

        if len(tmp_video) == 0:
            _content = "Render process is wrong"
            log(log_file, _content)
            # return False

        try:
            path_local = base_dir + f'/products/videos/channel_id={str(channel_id)}.flv'
            final_video = concatenate_videoclips(tmp_video)
            final_video.write_videofile(path_local, fps=1, codec="libx264", bitrate=bitrate)

        except Exception as error:
            _content = "Render process is wrong"
            log(log_file, f'{_content} \n {error}')
            # return False

        try:
            # delete video item
            for path in list_path_video:
                try:
                    os.remove(path)
                except Exception as error:
                    log(log_file, error)

        except Exception as error:
            log(log_file, error)

        if status_false:
            _content = "Render process is wrong"
            log(log_file, _content)
            return False

    else:
        path_local = list_path_video[0]

    dataProduct = datas[0]

    try:
        try:
            description, name_song = gen_description(datas)
        except:
            description = ''
            name_song = ''

        video_title = video_title.replace("*", str(sum))
        video_title = video_title.replace("=", '')

        title_singer = title_singer.replace("*", str(sum))
        title_singer = title_singer.replace("=", name_song)

        if status_song:
            data = {
                "channel_id": dataProduct['channel_id'],
                "path_video": path_local,
                "path_img": dataProduct['path_img'],
                "title": video_title,
                "title_singer": title_singer,
                "description": description,
                "des_status": 'no',
                "song_font_id": song_font_id,
                "title_font_id": title_font_id
            }
        else:
            data = {
                "channel_id": dataProduct['channel_id'],
                "path_video": path_local,
                "path_img": dataProduct['path_img'],
                "title": video_title,
                "title_singer": title_singer,
                "description": description,
                "des_status": 'no',
                "song_font_id": song_font_id,
                "title_font_id": title_font_id
            }
        channel_str = "channel=" + str(int(dataProduct['channel_id']))
        filename = str(base_dir + "/products/infos/" + channel_str + ".txt")

        with open(filename, 'w', encoding="utf-8") as outfile:
            json.dump(data, outfile)

        if len(datas) > 1:
            for i in range(1, len(datas)):
                try:
                    path = datas[i]['path_img']
                    os.remove(path)
                except Exception as error:
                    log(log_file, error)

    except Exception as error:
        log(log_file, error)
        return "error"

    return "success"
