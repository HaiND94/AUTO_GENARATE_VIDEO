"""""""""""""""""""""""
Author : NGUYEN DINH HAI
VER    : 1.0
DATE   : 2021, JUL 12
"""""""""""""""""""""""


from swagger_client import ChannelApi
from swagger_client import NotificationApi
from swagger_client import TemplateVideoApi

from swagger_client import ApiClient

from utility import generate_directory, clear_data, check_created_video, \
    check_env, auth_token, get_manual_video, get_data_handle_video


from update import auto_update

from src.log_status import log

from image_processing import load_model
from datetime import date, datetime
from decouple import config
# from func_timeout import func_set_timeout
from threading import Thread
# from multiprocessing import Process
# from timeout_decorator import timeout
from func_timeout import func_timeout

import os
import time
import shutil
import json
import urllib
import numpy
import random
import math
import gc
import pathlib
import subprocess

# Config for multi thread
token = None
start_time = time.time()

DURATION_MAX = 500

special_digit = ["*", "/", "[", "]", "{", "}", "|", "-", "," "&", "^", "%", "$", "#", "@", "!", "~"]

# Global variable 
error_channels = []
config_channels = []


def run_thread(api_cli, model, base_dir, token, template_api):
    """

    :param api_cli:
    :param model:
    :param base_dir:
    :param token:
    :param template_api:
    :return:
    """
    global config_channels
    global error_channels
    count = 0
    no_video_channels = config_channels.copy()

    while len(no_video_channels) != 0:
        count += 1
        if count > 120:
            break
        print(f"Have {len(config_channels) - len(error_channels)} need to create video")
        _channel_id = None

        no_video_channels = []
        for channel in config_channels:
            if channel in error_channels:
                continue
            no_video_channels.append(channel)

        _filter = json.dumps({"where": {"status": {'inq': ['NEW', 'RUNNING']},
                                        'channelId': {'inq': [no_video_channels]}
                                        }
                              })
        try:
            template_videos = template_api.template_video_find(filter=_filter)
        except Exception as e:
            print(e)
            template_videos = []

        if len(template_videos) != 0:
            print(f"Have {len(template_videos)} manual videos need to create")
            for video in template_videos:
                try:
                    _channel_id = video.channel_id
                    if not _channel_id:
                        continue
                except Exception as e:
                    print(e)
                    continue

                if _channel_id in error_channels:
                    continue
                else:
                    try:
                        data = {"status": 'RUNNING'}
                        template_api.template_video_prototype_patch_attributes(id=video.id, data=data)
                    except Exception as e:
                        _content = "Can not set attribute status for video template"
                        print(f'{_content}\n {e}')
                        pass

                    try:
                        error_channels.append(_channel_id)
                        result = func_timeout(150 * 60, get_manual_video, args=(api_cli, model, base_dir,
                                                                                _channel_id, error_channels,
                                                                                video, token))
                        if result is False:
                            print(f"Can not create video for channel {_channel_id}")
                        else:
                            error_channels.append(_channel_id)

                    except Exception as e:
                        print(e)
                        continue

        for channel_id in no_video_channels:
            if channel_id in error_channels:
                continue
            else:
                _channel_id = channel_id
                break

        if _channel_id:
            error_channels.append(_channel_id)
        else:
            break

        try:
            result = func_timeout(150 * 60, get_data_handle_video, args=(api_cli, model, base_dir,
                                                                         _channel_id, error_channels, token))
            if result is False:
                print(f"Can not create video for channel {_channel_id}")
            error_channels.append(_channel_id)

        except Exception as e:
            print(e)
            continue

        gc.collect()

    return True


def main(model, base_dir, api_cli):
    """

    :param model:
    :param base_dir:
    :param api_cli:
    :return:
    """

    if not api_cli:
        print("api_cli was not found")
        return False
    else:
        templateApi = False
        try:
            max_thread = int(config('NUMBER_THREAD'))
            channelApi = ChannelApi(api_client=api_cli)
            templateApi = TemplateVideoApi(api_client=api_cli)
            # serverApi = ServerApi(api_client=apiCLI)
            server_str = config("SERVER")
            SERVER_IDS = server_str.split(",")
            # channelServerApi = ChannelServerApi(api_client=apiCLI)
        except Exception as e:
            print(e)
            return False

        global error_channels
        global config_channels
        try:
            config_channels.clear()
            error_channels.clear()
        except Exception as e:
            print(e)

        _filter = json.dumps(
            {
                "fields": ['id', 'nameOfChannel'],
                "where": {'active': True,
                          'status': 'NORMAL',
                          'run': 'START',
                          "serverId": {"inq": SERVER_IDS},
                          "cookieState": "UPDATED"
                          },
                "order": 'lastUploadTime ASC'
            })

        channels = channelApi.channel_find(filter=_filter)
        # random.shuffle(channels)

        print(f'Find {len(channels)} channels was configured in this server')

        _channels = []

        for channel in channels:

            if check_created_video(base_dir, channel.id) is False:
                print(f"Video was created for channel {channel.name_of_channel}")
                continue

            config_channels.append(channel.id)
            # Use for test channel 
            config_channels = [953]

        # run_thread(api_cli, model, base_dir, token)

        thread = dict()
        # thread = Process(target=run_thread, args=(api_cli, model, base_dir,
        #                  token, templateApi))
        # thread.start()
        # thread.join()
        try:
            for idx in range(int(max_thread)):
                try:
                    thread[f'thread_{idx}'] = Thread(target=run_thread, args=(api_cli, model, base_dir,
                                                                              token, templateApi))
                    thread[f'thread_{idx}'].daemon = True
                    thread[f'thread_{idx}'].start()

                    time.sleep(5)
                except Exception as e:
                    print(e)
                    continue
            for idx in range(len(thread)):
                try:
                    thread[f'thread_{idx}'].join(timeout=12*60*60)
                except Exception as e:
                    print(e)

            gc.collect()
        except Exception as e:
            print(e)
            return False

        error_channels.clear()
        config_channels.clear()

        return True


if __name__ == '__main__':
    while True:
        # base_dir = os.path.abspath('..') + '/youtube-python'  # dev
        base_dir = os.path.abspath('..') + '/VIDEO_GENERATION'  # server
        path = base_dir + '/model/' + 'u2net.pth'
        log_sys = "./log_sys.txt"

        if not os.path.isfile(path):
            print(f"Model was not found at {path}")
        net = load_model(path)
        if check_env():
            # clear_data(base_dir)
            try:
                generate_directory(base_dir)
                api_cli, token = auth_token()
            except Exception as e:
                log(log_sys, "Can not authenticate")
                time.sleep(10)
                continue

            if not api_cli:
                log(log_sys, "Can not authenticate")
                time.sleep(10)
                continue

            else:
                count = 0
                while True:
                    # print(count)
                    try:
                        log(log_sys, "run auto update")
                        try:
                            func_timeout(8 * 60, auto_update, args=(api_cli,))
                        except Exception as e:
                            log(f"Can not update \n{e}")

                    except Exception as e:
                        print(e)
                        pass
                    count += 1
                    if count % 20 == 0:
                        count = 1
                        try:
                            log(log_sys, "Run clear data")
                            clear_data(base_dir)
                            generate_directory(base_dir)
                        except Exception as e:
                            print(e)
                            pass

                    try:
                        log(log_sys, f"count variable is {count}")
                        main(net, base_dir, api_cli)
                    except Exception as error:
                        print(error)

                    gc.collect()
                    time.sleep(0.5)
