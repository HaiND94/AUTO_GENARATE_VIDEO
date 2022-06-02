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

from func_timeout import func_timeout

from random import randint

from src.log_status import log
from src.utilitys import Struct, download, sort_list, extract_name
from src.notification import notice_error, notice_warning

from func_timeout import func_set_timeout

from pytube import YouTube

import json
import os
import math
import random
import logging
import numpy
import time


import urllib.request
import youtube_dl
import subprocess


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filemode='w')

DURATION_MAX = 600


# @func_set_timeout(600)
# @timeout(500)
def _download_audio_from_youtube_v0(path_local, id_youtube):
    """

    :param path_local:
    :param id_youtube:
    :return:
    """

    if path_local is None:
        return None

    if id_youtube is None:
        return None

    try:
        if 'https://www.youtube.com/' in id_youtube:
            url = id_youtube
        else:
            url = 'https://www.youtube.com/watch?v=' + id_youtube

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': path_local,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return path_local
    except Exception as error:
        print(error)

    return None


def _download_audio_from_youtube_v1(path_local, id_youtube):
    """
    :param path_local:
    :param id_youtube:
    :return:
    """

    if path_local is None:
        return None

    if id_youtube is None:
        return None

    try:
        if 'https://www.youtube.com/' in id_youtube:
            url = id_youtube
        else:
            url = 'https://www.youtube.com/watch?v=' + id_youtube

        # Get audio from youtube
        yt = YouTube(url)
        audio_path = (yt.streams\
                        .filter(only_audio=True)\
                        .order_by('abr')[-1]\
                        .download(filename=path_local))
        print(audio_path)

        return audio_path
    except Exception as error:
        print(error)

    return None



# Download audio with yt-dlp
def _download_audio_from_youtube(path_local, id_youtube):
    """
    :param path_local:
    :param id_youtube:
    :return:
    """

    if path_local is None:
        return None

    if id_youtube is None:
        return None

    try:
        if 'https://www.youtube.com/' in id_youtube:
            url = id_youtube
        else:
            url = 'https://www.youtube.com/watch?v=' + id_youtube

        # Get audio from youtube
        subprocess.run(f"yt-dlp -f 'ba' -x --audio-format mp3\
                        {url}  -o '{path_local}'",shell=True)
        if os.path.isfile(path_local):
            print(path_local)
            return path_local
        else:
            return None

    except Exception as error:
        print(error)

    return None


def _sort_audios(list_audios, limit_song_singer=5):
    """

    :param list_audio:
    :param limit_song_singer:
    :return:
    """
    if len(list_audios) == 0:
        return []

    try:
        list_audios.sort(key=lambda x: x.views, reverse=True)
    except:
        list_audios = sort_list(list_audios)

    if len(list_audios) > limit_song_singer:
        final_audios = [list_audios[0], list_audios[1], list_audios[2], list_audios[3], list_audios[4]]
        # final_audio = list_audio[0]
        random.shuffle(final_audios)

        if len(list_audios) >= 50:
            tmp = list_audios[5:50]
        else:
            tmp = list_audios[5:]
    else:
        random.shuffle(list_audios)
        return list_audios

    ids_audio = []

    try:
        random.shuffle(tmp)
    except Exception as error:
        print(error)

    for audio in tmp:
        if audio.id in ids_audio:
            continue
        final_audios.append(audio)

    return final_audios


class Audio:
    _id = None

    def __init__(self, audio, api_cli, base_dir, base_url, token, log_file):
        self.audio = audio
        self._id = int(audio.id)
        self.api_cli = api_cli
        self.base_dir = base_dir
        self.base_url = base_url
        self.log_file = log_file
        self.token = token

    def id(self):
        try:
            __id = self._id
        except Exception as e:
            log(self.log_file, e)
            return False

        return __id

    def title(self):
        try:
            __name = self.audio.title
        except Exception as e:
            log(self.log_file, e)
            return False

        return __name

    def singer(self):
        try:
            __singer_id = self.audio.singer_id
        except Exception as e:
            log(self.log_file, f"can not get id attribute of  audio\n {e}")
            return False

        try:
            singerApi = SingerApi(api_client=self.api_cli)
        except Exception as e:
            log(self.log_file, f"can not get singerAPi \n{e}")
            return False

        try:
            singer = singerApi.singer_find_by_id(__singer_id)
            name_singer = singer.name
        except Exception as e:
            log(self.log_file, f"can not get name of singer for song {self.id}\n {e}")
            return False

        return name_singer

    def path(self):
        __path = f'{self.base_dir}/data/audios/{self._id}.mp3'
        __path_m4a = f'{self.base_dir}/data/audios/{self._id}.m4a'

        if os.path.isfile(__path):

            print(f'Audio is available {__path}')
            return __path

        elif os.path.isfile(__path_m4a):
            print(f'Audio is available {__path_m4a}')
            return __path_m4a

        else:
            try:
                if self.audio.id_youtube:
                    file_name = __path_m4a
                    try:
                        file_name_tmp = func_timeout(10 * 60, _download_audio_from_youtube,
                                                     args=(file_name, self.audio.id_youtube))

                        # file_name_tmp = func_timeout(10 * 60, _download_audio_from_youtube_v0,
                        #                              args=(file_name, self.audio.id_youtube))

                    except Exception as error:
                        if not os.path.isdir(file_name):
                            try:
                                os.remove(file_name)
                            except Exception as e:
                                log(self.log_file, f"could be not remove audio {e}")
                        log(self.log_file, f"could be not download audio {error}")
                        return False

                    if not file_name_tmp:
                        return False

                    else:
                        return file_name_tmp

                elif self.audio.url and self.audio.url != 'error':
                    url = self.base_url + "audios/download/" + self.audio.url + '?access_token=' + self.token

                    try:
                        __path = func_timeout(10 * 60, download, args=(url, __path))
                        if not __path:
                            return False
                    except Exception as e:
                        if not os.path.isfile(__path):
                            try:
                                os.remove(__path)
                            except Exception as e:
                                log(self.log_file, f"could be not remove  {__path}\n {e}")
                        log(self.log_file, f"Can not download song {self.id} file, from DB\n {e}")
                        return False

                    return __path

                else:
                    log(self.log_file, f"Can not download song {self.id} file, no url not youtube_id")
                    return False
            except Exception as e:
                log(self.log_file, f"Can not download song {self.id} file\n {e}")
                return False
            # Download audio

    def audio(self):
        __path = f'{self.base_dir}/data/audios/{int(self.audio.id)}.mp3'
        __path_m4a = f'{self.base_dir}/data/audios/{int(self.audio.id)}.m4a'

        # Check file audio is available
        if os.path.isfile(__path):
            pass

        elif os.path.isfile(__path_m4a):
            __path = __path_m4a

        else:
            print(f"Can not found {__path}")
            print(f"Can not found {__path_m4a}")

            return False
        

        

        # Get duration of audio
        try:
            audio_file_clip = AudioFileClip(__path)
            if audio_file_clip.duration < DURATION_MAX:
                return audio_file_clip
            else:
                log(self.log_file, f"Duration of song {self.audio.title} too long")
                return False
        except Exception as e:
            log(self.log_file, f"Can not get duration {self.audio.title} file\n {e}")
            return False


def get_data_audios(channel, api_cli, base_dir, base_url, token, error_channels):

    data_audios = dict()
    data_audios['error_status'] = False

    try:
        channel_id = int(channel.id)
        _error_status = channel.error_status
        singer_ids = channel.singer_ids
        copy_right_content = channel.copy_right_content
        _duration_min = channel.duration_min
        _duration_max = channel.duration_max

        if os.path.isdir(f"{base_dir}/logger") is False:
            try:
                os.mkdir(f"{base_dir}/logger")
            except Exception as e:
                print(e)

        log_file = f"{base_dir}/logger/channel_{int(channel_id)}.log"
        log(log_file, f"Start start getting audio data for channel {channel_id}")

    except Exception as error:
        logging.info(f"Can not get channel id and status\n or {error}")
        data = Struct(**data_audios)
        data.set_error()

        return data

    if _error_status:
        log(log_file, "Channel config is wrong")
        data = Struct(**data_audios)
        data.set_error()

        return data

    try:
        audioApi = AudioCleanApi(api_client=api_cli)
        notificationApi = NotificationApi(api_client=api_cli)

    except Exception as error:
        log(log_file, f"could be not pass api client\n or {error}")
        data = Struct(**data_audios)
        data.set_error()

        return data

    if len(singer_ids) == 0:
        _content = f"Can not find singer in channel {channel_id}"
        logging.info(_content)
        data = Struct(**data_audios)
        data.set_error()
        try:
            notice_error(notificationApi, channel, _content)
        except Exception as e:
            print(e)
            pass

        return data

    if not os.path.isdir(base_dir):
        try:
            os.mkdir(base_dir)
        except Exception as e:
            _content = f"Can not find folder {base_dir} in server\n{e}"
            logging.info(_content)
            data = Struct(**data_audios)
            data.set_error()

            return data

    # Check path save audio
    _path_save = f'{base_dir}/data/audios'

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

        data = Struct(**data_audios)
        data.set_error()

        return data

    # Variable for filter audio
    limit = int(60 // len(singer_ids))
    rand_limit = randint(0, 20)
    audios = []

    # Get audio information from DB
    if copy_right_content:
        for id_singer in singer_ids:

            try:
                filter = json.dumps({"skip": rand_limit, "limit": limit,
                                     "where": {'singerId': id_singer, 'type': 2, 'active': True,
                                               'license': {'neq': 'BLOCK'},
                                               'or': [{'url': {'neq': None}}, {'idYoutube': {'neq': None}}]}})
                audio_tmp = audioApi.audio_clean_find(filter=filter)

                if len(audio_tmp) == 0:
                    _content = f"could be not find audio in DB for singer {id_singer}"
                    log(log_file, _content)
                    notice_warning(notificationApi, channel, _content)

                    continue

                if len(audios) == 0:
                    audios = audio_tmp
                else:
                    audios = numpy.concatenate((audios, audio_tmp), axis=0)
                    audios = audios.tolist()

            except Exception as error:
                logging.info(error)
                continue

        if len(audios) < 6:
            data_audios['status_song'] = True
            audios = []

            for id_singer in singer_ids:
                # audios = []

                try:
                    filter = json.dumps({"where": {'singerId': id_singer,
                                                   'type': 2,
                                                   'active': True,
                                                   'or': [{'url': {'neq': None}}, {'idYoutube': {'neq': None}}]}})

                    audio_tmp = audioApi.audio_clean_find(filter=filter)
                    if len(audio_tmp) == 0:
                        continue
                    if len(audios) == 0:
                        audios = audio_tmp
                    else:
                        audios = numpy.concatenate((audios, audio_tmp), axis=0)
                        audios = audios.tolist()
                except Exception as error:
                    log(log_file, error)
                    continue

    else:
        for id_singer in singer_ids:
            try:
                filter = json.dumps({"skip": rand_limit, "limit": limit,
                                     "where": {'singerId': id_singer,
                                               'type': 1,
                                               'active': True,
                                               'license': {'neq': 'BLOCK'},
                                               'or': [{'url': {'neq': None}}, {'idYoutube': {'neq': None}}]}})

                audio_tmp = audioApi.audio_clean_find(filter=filter)

                if len(audio_tmp) == 0:
                    continue

                if len(audios) == 0:
                    audios = audio_tmp
                else:
                    audios = numpy.concatenate((audios, audio_tmp), axis=0)
                    audios = audios.tolist()

            except Exception as error:
                logging.info(error)
                log(log_file, error)

        if len(audios) < 25:
            data_audios['status_song'] = True
            audios = []

            for id_singer in singer_ids:
                try:
                    _filter = json.dumps({
                        "where": {'singerId': id_singer,
                                  # 'license': {'neq': 'BLOCK'},
                                  'type': 1,
                                  'active': True,
                                  'or': [{'url': {'neq': None}}, {'idYoutube': {'neq': None}}]}})

                    audio_tmp = audioApi.audio_clean_find(filter=_filter)

                    if len(audio_tmp) == 0:
                        continue

                    if len(audios) == 0:
                        audios = audio_tmp
                    else:
                        audios = numpy.concatenate((audios, audio_tmp), axis=0)
                        audios = audios.tolist()

                except Exception as error:
                    logging.info(error)
                    log(log_file, error)

    # Check sum of audio must be diff 0
    if len(audios) == 0:
        _content = f"Can not find audio for channel {channel_id} with singers {singer_ids}"
        log(log_file, _content)
        notice_error(notificationApi, channel, _content)

        data = Struct(**data_audios)
        data.set_error()

        return data

    # Sort audios follow view
    audios_sort = _sort_audios(audios, 5)

    # Get attribute of audios
    attribute_audios = []
    list_singers = []
    list_songs = []
    _duration = 0

    # Extras data audio from audio was sort
    for index, audio in enumerate(audios_sort):
        _tmp = dict()
        try:
            _audio = Audio(audio, api_cli, base_dir, base_url, token, log_file)
            _id = Audio.id(_audio)
            _singer = Audio.singer(_audio)
            _name = Audio.title(_audio)
            _path = Audio.path(_audio)
            _audio_clip = Audio.audio(_audio)
        except:
            continue

        if _id is False or _name is False or _path is False or _audio_clip is False or _singer is False:
            continue

        list_singers.append(_singer)
        list_songs.append(_name)

        _tmp['id'] = _id
        _tmp['singer'] = _singer
        _tmp['name'] = _name
        _tmp['path'] = _path
        _tmp['audio'] = _audio_clip
        _tmp['duration'] = _audio_clip.duration

        _duration += _audio_clip.duration
        _data = Struct(**_tmp)
        attribute_audios.append(_data)

    # Create loop audio
    _tmp_audios = attribute_audios.copy()
    _tmp_duration = _duration
    _tmp_singers = list_singers.copy()
    _tmp_songs = list_songs.copy()
    _times_out = 0

    while (_duration/60) < _duration_max:
        _times_out += 1
        if _times_out == 10:
            break

        attribute_audios += _tmp_audios
        list_songs += _tmp_songs
        list_singers += _tmp_singers
        _duration += _tmp_duration

    if len(attribute_audios) == 0:
        _content = f"Can not find audio for channel {channel_id} with singers {singer_ids}"
        log(log_file, _content)
        notice_error(notificationApi, channel, _content)

        data = Struct(**data_audios)
        data.set_error()

        return data

    data_audios['audios'] = attribute_audios
    data_audios['list_singers'] = list_singers
    data_audios['list_songs'] = list_songs
    data_audios['error_status'] = False
    data = Struct(**data_audios)

    return data















