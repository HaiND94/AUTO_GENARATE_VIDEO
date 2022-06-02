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
from swagger_client import TemplateVideoApi

from decouple import config
# from func_timeout import func_set_timeout
# from timeout_decorator import timeout
from func_timeout import func_timeout

from src.title import gen_title_one_singer, gen_title_collection
from src.notification import notice_error, notice_warning
from src.video import handle_video
from src.channel import get_data_channel
from src.image import get_data_images
from src.audio import get_data_audios
from src.log_status import log
from src.utilitys import extract_data_response, Struct, get_manual_images
from src.audio import Audio
from src.font import get_fonts

# from wrapt_timeout_decorator import timeout

from image_processing import image_processing

import os
import time
import shutil
import random
import json
import logging
import gc
import pathlib


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filemode='w')


# Get token from authn function
def auth_token():
    email = config('EMAIL')
    password = config('PASSWORD')

    try:
        my_account = AccountApi().account_login(credentials={"email": email,
                                                             "password": password})
        token_id = my_account['id']
        api_cli = ApiClient(header_name='Authorization',
                            header_value=my_account['id'])
        return api_cli, token_id

    except Exception as e:
        logging.info(e)

        return False, False


def check_env():
    """
    Detail: check file .env in project
    :return:
    """
    _path_folder = pathlib.Path().absolute()
    name_repo = str(_path_folder).split("/")[-1]
    path_temp = f"../tempo/{name_repo}"
    path_temp_env = f"{path_temp}/.env"

    if not os.path.isfile("./.env"):
        if not os.path.isdir(path_temp_env):
            return False

        try:
            shutil.move(path_temp_env, "./.env")
            return True
        except Exception as e:
            logging.info(e)
            return False

    return True


def generate_directory(base_dir):
    if base_dir is None:
        return
    try:
        if not os.path.isdir(base_dir):
            os.mkdir(base_dir)

        if os.path.isdir(base_dir + '/output') is False:
            os.mkdir(base_dir + '/output')

        if os.path.isdir(base_dir + '/tmp_audio') is False:
            os.mkdir(base_dir + '/tmp_audio')

        if os.path.isdir(base_dir + '/products') is False:
            os.mkdir(base_dir + '/products')

        if (os.path.isdir(base_dir + '/products/infos')) is False:
            os.mkdir(base_dir + '/products/infos')

        if (os.path.isdir(base_dir + '/products/videos')) is False:
            os.mkdir(base_dir + '/products/videos')

        if os.path.isdir(base_dir + '/data') is False:
            os.mkdir(base_dir + '/data')

        if os.path.isdir(base_dir + '/data/fonts') is False:
            os.mkdir(base_dir + '/data/fonts')

        if os.path.isdir(base_dir + '/data/images') is False:
            os.mkdir(base_dir + '/data/images')

        if os.path.isdir(base_dir + '/data/audios') is False:
            os.mkdir(base_dir + '/data/audios')

    except Exception as error:
        print(error)
        return False

    return True


def clear_data(base_dir):
    try:
        path = base_dir + '/data/images'
        shutil.rmtree(path)
        path = base_dir + '/data/fonts'
        shutil.rmtree(path)
        path = base_dir + '/data/audios'
        shutil.rmtree(path)
    except Exception as error:
        print(error)
        return False

    return True


def check_created_video(base_dir, channel_id):
    if not os.path.isdir(base_dir):
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


# Create video and set time out is 100'
# @func_set_timeout(120 * 60)
# @timeout(120*60)
def get_data_handle_video(api_cli, model, base_dir, channel_id, error_channels, token):
    # global config_channels
    # global error_channels

    base_url = config("BASE_URL")
    song_font_id = None
    title_font_id = None

    # Check input conditional
    if not os.path.isdir(base_dir):
        try:
            os.mkdir(base_dir)
        except Exception as e:
            print(e)
            return False

    if os.path.isdir(f"{base_dir}/logger") is False:
        try:
            os.mkdir(f"{base_dir}/logger")
        except Exception as e:
            print(e)
            return False
    # Log file
    log_file = f"{base_dir}/logger/channel_{int(channel_id)}.log"
    log(log_file, f"Start thread for channel {int(channel_id)}")

    # Get api
    try:
        notificationApi = NotificationApi(api_client=api_cli)

    except Exception as e:
        log(log_file, f"could be not pass api client\n {e}")
        return False

    # Check channel id must be a number
    try:
        channel_id = int(channel_id)
    except Exception as e:
        _content = f"Channel_id is wrong"
        log(log_file, f'{_content}\n {e}')
        return False

    # Get data channel
    try:
        channel = get_data_channel(api_cli=api_cli, base_dir=base_dir,
                                   channel_id=channel_id, error_channels=error_channels, log_file=log_file)
        error_status = channel.error_status

    except Exception as e:
        _content = "Can not get channel information"
        log(log_file, f"{_content}\n{e}")
        return False

    if error_status:
        _content = "Can not get channel information"
        log(log_file, f'{_content}\n')
        try:
            notice_error(notificationApi, channel, _content)
        except Exception as e:
            print(e)

        return False

    # Get title suggest
    try:
        suggest_titles = json.loads(channel.meta_data)
        try:
            start_titles = suggest_titles['startTitle'].split(',')
        except:
            start_titles = []

        try:
            mid_titles = suggest_titles['midTitle'].split(',')
        except:
            mid_titles = []

        try:
            stop_titles = suggest_titles['stopTitle'].split(',')
        except:
            stop_titles = []

    except Exception as e:
        log(log_file, e)

        start_titles = []
        mid_titles = []
        stop_titles = []

    # Get attribute from channel
    try:
        singer_mode = channel.singer_mode
        include_singer_name = channel.include_singer_name
        language_code = channel.language_code
        singer_names = channel.singer_names
        duration_max = channel.duration_max

    except Exception as e:
        _content = "Can not get data from audio object"
        log(log_file, f"Can not get data from audio object\n{e}")
        try:
            notice_error(notificationApi, channel, _content)
        except Exception as e:
            print(e)
        return False

    # Generation title
    _singer_name = singer_names[0]
    try:
        if singer_mode == 'SINGER' or include_singer_name == "YES":
            video_title, title_singer, title_auto = gen_title_one_singer(start_titles, language_code,
                                                                         _singer_name)
            title_auto = _singer_name
        else:
            if len(singer_names) > 3:
                tmp_singers = singer_names[:3]
            else:
                tmp_singers = singer_names.copy()

            video_title, title_singer, title_auto = gen_title_collection(tmp_singers,
                                                                         start_titles, mid_titles, stop_titles,
                                                                         language_code, include_singer_name)
    except Exception as e:
        _content = "Can not generation title"
        log(log_file, f"{_content}\n{e}")
        try:
            notice_error(notificationApi, channel, _content)
        except Exception as e:
            print(e)

        return False

    if len(video_title) == 0 or video_title is None:
        _content = "Can not generation title"
        log(log_file, f"{_content}\n{e}")
        try:
            notice_error(notificationApi, channel, _content)
        except Exception as e:
            print(e)

        return False

    # Get audio data
    try:
        audios_data = get_data_audios(channel, api_cli, base_dir, base_url, token, error_channels)
        error_status = audios_data.error_status
    except Exception as e:
        _content = "Can not get audio from database"
        log(log_file, f'{_content}\n{e}')
        try:
            notice_error(notificationApi, channel, _content)
        except Exception as e:
            print(e)

        return False

    if error_status:
        _content = "Can not get audio from database"
        log(log_file, f'{_content}')
        try:
            notice_error(notificationApi, channel, _content)
        except Exception as e:
            print(e)

        return False

    # Generate image
    try:
        list_singers = audios_data.list_singers
        list_songs = audios_data.list_songs
    except Exception as e:
        _content = f"Can not get list singers and list songs "
        log(log_file, f"{_content}\n{e}")

        try:
            notice_error(notificationApi, channel, _content)
        except Exception as e:
            print(e)

        return False

    try:
        images_data = get_data_images(title_auto, model, channel, api_cli,
                                      base_dir, base_url, token, error_channels,
                                      list_singers, list_songs)
        res = images_data.data
        if res.status == 'error':
            _content = res.content
            log(log_file, _content)
            try:
                notice_warning(notificationApi, channel, _content)
            except:
                pass

        error_status = images_data.error_status
    except Exception as e:
        _content = "Can not generation image"
        log(log_file, f'{_content}\n{e}')
        try:
            notice_error(notificationApi, channel, _content)
        except Exception as e:
            print(e)

        return False

    if error_status:
        _content = "Can not get image from database"
        log(log_file, f'{_content}')
        try:
            notice_error(notificationApi, channel, _content)
        except Exception as e:
            print(e)

        return False

    # Extract data to generate video
    # Get data image, audio
    try:
        res = images_data.data
        if res.status == 'error':
            _content = res.content
            log(log_file, _content)
            try:
                notice_error(notificationApi, channel, _content)
            except Exception as e:
                print(e)
                pass

            return False

    except Exception as e:
        _content = "Can not get image from image data"
        log(log_file, f"{_content}\n{e}")
        try:
            notice_error(notificationApi, channel, _content)
        except:
            pass

        return False

    # Get data audio from audio object
    try:
        data_worship = audios_data.audios
    except Exception as e:
        _content = "Can not audio from audios data"
        log(log_file, f"{_content}\n{e}")
        try:
            notice_error(notificationApi, channel, _content)
        except:
            pass

        return False

    # Get duration from channel
    try:
        duration_min = channel.duration_min
        duration_max = channel.duration_max
    except Exception as e:
        _content = "Can not get duration from channel"
        log(log_file, _content)
        try:
            notice_warning(notificationApi, channel, _content)
        except:
            pass
        duration_min = 0
        duration_max = 90

    try:
        datas = extract_data_response(notificationApi, channel, res,
                                      data_worship, video_title,
                                      duration_min, duration_max, log_file)
    except Exception as e:
        _content = "Can not extract data to generate video"
        log(log_file, f'{_content}\n{e}')
        try:
            notice_error(notificationApi, channel, _content)
        except Exception as e:
            print(e)

        return False

    if len(datas) == 0:
        _content = "Can not extract data to generate video"
        log(log_file, f'{_content}\n{e}')
        try:
            notice_error(notificationApi, channel, _content)
        except Exception as e:
            print(e)

        return False

    # Generate video
    try:
        status_song = audios_data.status_song
    except Exception as e:
        log(log_file, "Can not get status_song")
        status_song = False

    try:
        song_font_id = images_data.id_font_song
        title_font_id = images_data.id_font_title
    except:
        pass

    try:
        result = handle_video(datas, base_dir, video_title, title_singer, channel_id, status_song,
                              song_font_id, title_font_id)
        # set_channel_active(channel_id)
    except Exception as e:
        _content = "Can not generate video"
        log(log_file, f'{_content}\n{e}')
        try:
            notice_error(notificationApi, channel, _content)
        except Exception as e:
            print(e)

        return False

    if result == "error":
        _content = f"Can't generate video for channel id {channel_id}"
        log(log_file, _content)

        try:
            notice_error(notificationApi, channel, _content)
        except Exception as e:
            print(e)

        return False

    else:
        log(log_file, f"Generate video success for channel id {channel_id}")


# @timeout(120*60)
def get_manual_video(api_cli, model, base_dir, channel_id, error_channels, video, token):
    base_url = config("BASE_URL")
    song_font_id = None
    title_font_id = None

    # Get api
    try:
        template_api = TemplateVideoApi(api_client=api_cli)
        notificationApi = NotificationApi(api_client=api_cli)
        # singerApi = SingerApi(api_client=api_cli)
        audioApi = AudioCleanApi(api_client=api_cli)
        fontApi = FontFamilyApi(api_client=api_cli)
    except Exception as e:
        print("Can not get template video api or notification video")
        print(e)
        return False

    # Check input conditional
    if not os.path.isdir(base_dir):
        try:
            os.mkdir(base_dir)
        except Exception as e:
            print(e)
            return False

    if os.path.isdir(f"{base_dir}/logger") is False:
        try:
            os.mkdir(f"{base_dir}/logger")
        except Exception as e:
            print(e)
            return False
    # Log file
    log_file = f"{base_dir}/logger/channel_{int(channel_id)}.log"
    log(log_file, f"Start thread for channel {int(channel_id)}")

    # Check channel id must be a number
    try:
        channel_id = int(channel_id)
    except Exception as e:
        _content = f"Channel_id is wrong"
        log(log_file, f'{_content}\n {e}')
        return False

    # Get data channel
    try:
        channel = get_data_channel(api_cli=api_cli, base_dir=base_dir,
                                   channel_id=channel_id, error_channels=error_channels, log_file=log_file)
        error_status = channel.error_status

    except Exception as e:
        _content = "Can not get channel information"
        log(log_file, f"{_content}\n{e}")
        return False

    if error_status:
        _content = "Can not get channel information"
        log(log_file, f'{_content}\n')
        try:
            notice_error(notificationApi, channel, _content)
        except Exception as e:
            print(e)

        return False

    # Get title suggest
    try:
        suggest_titles = json.loads(channel.meta_data)
        try:
            start_titles = suggest_titles['startTitle'].split(',')
        except:
            start_titles = []

        try:
            mid_titles = suggest_titles['midTitle'].split(',')
        except:
            mid_titles = []

        try:
            stop_titles = suggest_titles['stopTitle'].split(',')
        except:
            stop_titles = []

    except Exception as e:
        log(log_file, e)

        start_titles = []
        mid_titles = []
        stop_titles = []

    # Get attribute from channel
    try:
        singer_mode = channel.singer_mode
        include_singer_name = channel.include_singer_name
        language_code = channel.language_code
        duration_max = channel.duration_max

    except Exception as e:
        _content = "Can not get data from audio object"
        log(log_file, f"Can not get data from audio object\n{e}")
        try:
            notice_error(notificationApi, channel, _content)
        except Exception as e:
            print(e)
        return False


# Get video template information
    type_image = False
    id_language = False
    attribute_audios = []
    list_songs = []
    list_img = []
    list_singers = []
    audio_ids = []
    audios = []
    urls_img = []
    audio_error = []
    live_status = False

    # Get audio ids
    try:
        audio_ids = video.audio_ids
        id_language = video.language_id
        _live_status = video.is_live
        if _live_status:
            live_status = True
    except Exception as e:
        log(log_file, e)
        pass

    if not id_language:
        _content = f'id language was not config in video {video.id}'
        log(log_file, _content)
        try:
            data = {"status": 'ERROR',
                    "description": _content}
            template_api.template_video_prototype_patch_attributes(id=video.id, data=data)
        except Exception as e:
            logging.info("Can not set attribute status for video template")
            logging.info(e)
        return False

    # check len audio
    if len(audio_ids) == 0:
        _content = f"Can not find audio in video {video.id}"
        log(log_file, _content)
        try:
            data = {"status": 'ERROR',
                    "description": _content}
            template_api.template_video_prototype_patch_attributes(id=video.id, data=data)
        except Exception as e:
            logging.info("Can not set attribute status for video template")
            logging.info(e)
        return False

    try:
        _filter = json.dumps({"where": {'id': {'inq': audio_ids}}})
        audios = audioApi.audio_clean_find(filter=_filter)
    except Exception as e:
        log(log_file, e)

    if len(audios) == 0:
        _content = 'Audio was not found'
        log(log_file, _content)
        try:
            data = {"status": 'ERROR',
                    "description": _content}
            template_api.template_video_prototype_patch_attributes(id=video.id, data=data)
        except Exception as e:
            logging.info("Can not set attribute status for video template")
            logging.info(e)
        return False

    # Extras data audio from audios
    for index, audio in enumerate(audios):
        _tmp = dict()
        try:
            _audio = Audio(audio, api_cli, base_dir, base_url, token, log_file)
            _id = Audio.id(_audio)
            _singer = Audio.singer(_audio)
            _name = Audio.title(_audio)
            _path = Audio.path(_audio)
            _audio_clip = Audio.audio(_audio)
        except Exception as e:
            _content = f"Can not download audio {audio} for video {video.id}"
            log(log_file, e)
            try:
                audio_error.append(audio.id)
            except Exception as e:
                print(e)
                pass

            continue

        if _id is False or _name is False or _path is False or _audio_clip is False or _singer is False:
            try:
                audio_error.append(audio.id)
            except Exception as e:
                print(e)
                pass

            continue

        list_singers.append(_singer)
        list_songs.append(_name)

        _tmp['id'] = _id
        _tmp['singer'] = _singer
        _tmp['name'] = _name
        _tmp['path'] = _path
        _tmp['audio'] = _audio_clip
        _tmp['duration'] = _audio_clip.duration

        _data = Struct(**_tmp)
        attribute_audios.append(_data)

    # Get type of image
    try:
        type_image = video.type_image
    except Exception as e:
        print(e)

    if not type_image:
        _content = f"Can not find type image for video {video.id}"
        log(log_file, _content)

        try:
            data = {"status": 'ERROR',
                    "description": _content}

            template_api.template_video_prototype_patch_attributes(id=video.id, data=data)
        except Exception as e:
            logging.info("Can not set attribute status for video template")
            logging.info(e)

        return False

    elif type_image == "NO_LIST":
        image_template = False
        image = False

        try:
            image_template = video.image_template_url
            image = video.image_url
        except Exception as e:
            print(e)

        if not image or not image_template:
            log(log_file, f"Can not find image for video {video.id}")

            try:
                data = {"status": 'ERROR',
                        "description": "Image was not found"}
                template_api.template_video_prototype_patch_attributes(id=video.id, data=data)
            except Exception as e:
                _content = "Can not set attribute status for video template"
                log(log_file, _content)
            return False

        urls_img.append(image)
        urls_img.append(image_template)

    elif type_image == "HAS_LIST":
        image = False
        try:
            image = video.image_url
        except Exception as e:
            print(e)

        if not image:
            _content = f"Can not find image for video {video.id}"
            log(log_file, _content)

            try:
                data = {"status": 'ERROR',
                        "description": "Image was not found"}
                template_api.template_video_prototype_patch_attributes(id=video.id, data=data)
            except Exception as e:
                logging.info("Can not set attribute status for video template")
                logging.info(e)
            return False

        urls_img.append(image)

    else:
        _content = f"Type image for video {video.id} not True, must be HAVE_LIST or NO_LIST"
        log(log_file, _content)

        try:
            data = {"status": 'ERROR',
                    "description": _content}
            template_api.template_video_prototype_patch_attributes(id=video.id, data=data)
        except Exception as e:
            _content = f"Can not set attribute status for video template {video.id}"
            log(log_file, f"{_content}\n{e}")

        return False

    # Generation title
    try:
        random_choose = random.SystemRandom()
        singer_name = random_choose.choice(list_singers)

        if singer_mode == 'SINGER' or singer_mode == 'SINGERS' or include_singer_name == "YES":
            video_title, title_singer, title_auto = gen_title_one_singer(start_titles, language_code,
                                                                         singer_name)
            title_auto = singer_name
        else:
            if len(list_singers) > 3:
                tmp_singers = list_singers[:3]
            else:
                tmp_singers = list_singers.copy()

            video_title, title_singer, title_auto = gen_title_collection(tmp_singers,
                                                                         start_titles, mid_titles, stop_titles,
                                                                         language_code, include_singer_name)
    except Exception as e:
        _content = "Can not generation title"
        log(log_file, f"{_content}\n{e}")
        try:
            notice_error(notificationApi, channel, _content)
        except Exception as e:
            print(e)

        return False

    if len(video_title) == 0 or video_title is None:
        _content = "Can not generation title"
        log(log_file, f"{_content}\n{e}")
        try:
            notice_error(notificationApi, channel, _content)
        except Exception as e:
            print(e)

        return False

    try:
        list_img = get_manual_images(urls_img, base_dir, channel_id, token)
    except Exception as error:
        print(error)

    if len(list_img) == 0:
        _content = f"Can not download images object for video {video.id}"
        log(log_file, _content)

        try:
            data = {"status": 'ERROR',
                    "description": _content}
            template_api.template_video_prototype_patch_attributes(id=video.id, data=data)
        except Exception as e:
            logging.info(f"Can not set attribute status for video template\n{e}")

        return False

    data_video = []
    data_template = ['template_generation_worship']

    if type_image == "NO_LIST":

        for data_tem in data_template:
            type_template = data_tem

            if len(list_img) != 2:
                _content = f"Image need to create are 2 image, has {len(list_img)}"
                log(log_file, _content)

                data = {"status": 'ERROR',
                        "description": _content}
                try:
                    template_api.template_video_prototype_patch_attributes(id=video.id, data=data)
                except Exception as e:
                    print(e)
                    pass
                return False

            if type_template == 'template_generation_worship':
                logging.info(f"Generate image channel {channel_id} for video...")

                secure_random = random.SystemRandom()
                list_collum_mode = [1, 2]
                col_mod = secure_random.choice(list_collum_mode)
                modes = ['no_line', 'singer']

                if col_mod == 1:
                    modes = ['no_line', 'singer']
                    mode = secure_random.choice(modes)
                    aligns = ['left', 'right']
                    align = secure_random.choice(aligns)
                else:
                    aligns = ['center', 'left', 'right']
                    align = secure_random.choice(aligns)
                    mode = 'singer'

                list_colors = [(255, 255, 255), (255, 255, 0),
                              (0, 208, 0), (255, 48, 0),
                              (0, 17, 0), (0, 48, 144)]

            # Get font
                # Get song font for template
                fonts_list = get_fonts(fontApi, id_language, base_dir, base_url, log_file, 'List', token)

                if len(fonts_list) == 0:
                    _content = f"could be not download font for channel {channel_id}"
                    log(log_file, _content)

                    try:
                        notice_error(notificationApi, channel, _content)
                    except:
                        pass

                    try:
                        data = {"status": 'ERROR',
                                "description": _content}
                        template_api.template_video_prototype_patch_attributes(id=video.id, data=data)
                    except Exception as e:
                        logging.info("Can not set attribute status for video template")
                        logging.info(e)

                    return False

                # Random choose title font
                _min_loop = len(fonts_list)
                font_singer = False
                font_song = False

                for i in range(_min_loop):
                    secure_random = random.SystemRandom()

                    _font_song = secure_random.choice(fonts_list)
                    _font_singer = secure_random.choice(fonts_list)

                    try:
                        font_song = _font_song.path_local
                        id_font_song = _font_song.id

                        font_singer = _font_singer.path_local

                    except Exception as e:
                        print(e)
                        continue
                    break

                if not font_song:
                    _content = f"Can not download font for video {video.id}"
                    log(log_file, _content)

                    try:
                        data = {"status": 'ERROR',
                                "description": _content}
                        template_api.template_video_prototype_patch_attributes(id=video.id, data=data)
                    except Exception as e:
                        logging.info("Can not set attribute status for video template")
                        logging.info(e)
                    return "error"

                # Get list song and list singer follow format
                _list_singers = []
                for singer in list_singers:
                    _list_singers.append({"name": singer})

                _list_songs = []
                for song in list_songs:
                    _list_songs.append({"name": song})

                _count = 0
                img_txt = list_img[1]
                img_frame = list_img[0]

                random_choice = random.SystemRandom()
                color_text = random_choice.choice(list_colors)
                color_singer = random_choice.choice(list_colors)

                img = {"status": "error"}

                while _count < 3:
                    _count += 1
                    _data = {
                        "style": "template_generation_worship",
                        "path_img_txt": img_txt,  # no name copy
                        'img_frame': img_frame,
                        'collum_mode': col_mod,
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
                        img = image_processing(data=_data, net=model, path_output=base_dir)
                        _status = img["status"]
                    except Exception as error:
                        log(log_file,
                            f"Can not create image for template generation worship \n {error}\n with data is {_data}")
                        continue

                    try:
                        if img["status"] == 'success':
                            break
                        else:
                            col_mod = 1
                    except Exception as e:
                        print(e)
                        continue

                try:
                    if img["status"] == "error":
                        log(log_file, img)
                        data = {"status": 'ERROR',
                                "description": f"{img['content']}"}

                        try:
                            template_api.template_video_prototype_patch_attributes(id=video.id, data=data)
                        except Exception as e:
                            print(e)
                            pass

                        if len(img["image_false"]) != 0:
                            source_file = img["image_false"]
                            destination_folder = f"{base_dir}/logger/channel_{channel_id}"

                            if os.path.isdir(destination_folder) is False:
                                try:
                                    os.mkdir(destination_folder)

                                except Exception as error:
                                    log(log_file, f"Can not make {destination_folder} because {error}")
                                    logging.info(f"Can not make {destination_folder} because {error}")
                                    continue

                            name_file = source_file.split("/")[-1]
                            destination_file = f"{destination_folder}/{name_file}"

                            try:
                                shutil.copy(source_file, destination_file)
                            except Exception as error:
                                log(log_file, f"Can remove {source_file} to {destination_folder} because {error}")
                                logging.info(f"Can remove {source_file} to {destination_folder} because {error}")

                        continue
                    else:
                        res = Struct(**img)
                        data_video = extract_data_response(notificationApi, channel,
                                                           res, attribute_audios, video_title,
                                                           0, duration_max, log_file)
                except Exception as error:
                    logging.info(error)
                    log(log_file, error)
                    data_video = []
                    continue
    else:
        _list_songs = []
        _name_audios = []
        if len(audio_error) != 0:
            _content = f'Have audios cannot download {audio_error}, please update it again'
            log(log_file, _content)

            try:
                notice_warning(notificationApi, channel, _content)
            except Exception as e:
                print(e)

        _res = {'status': 'success', 'content': '',
                'data': [
                       {'path_img': list_img[0],
                        'list_songs': list_songs
                        }],
                'image_false': ''}

        res = Struct(**_res)

        data_video = extract_data_response(notificationApi, channel,
                                           res, attribute_audios, video_title,
                                           0, duration_max, log_file)

    if len(data_video) == 0:
        _content = f'Can not crate image for video {video.id}'
        log(log_file, _content)

        data = {"status": 'ERROR',
                "description": _content}

        try:
            template_api.template_video_prototype_patch_attributes(id=video.id, data=data)
        except Exception as e:
            print(e)
        return False

    try:
        result = handle_video(data_video, base_dir, video_title, title_singer,
                              channel_id, False, song_font_id, title_font_id,
                              live_status=live_status)
    except Exception as e:
        _content = "Can not generate video"
        log(log_file, f'{_content}\n{e}')
        try:
            notice_error(notificationApi, channel, _content)
        except Exception as e:
            print(e)

        return False

    if result == "error":
        _content = f"Can't generate video for channel id {channel_id}"
        log(log_file, _content)

        try:
            notice_error(notificationApi, channel, _content)
        except Exception as e:
            print(e)

        return False

    else:
        data = {"status": 'DONE'}

        try:
            template_api.template_video_prototype_patch_attributes(id=video.id, data=data)
        except Exception as e:
            print(e)
        log(log_file, f"Generate video success for channel id {channel_id}")

    return True
