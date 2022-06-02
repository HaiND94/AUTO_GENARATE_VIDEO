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

from moviepy.editor import ImageClip, VideoFileClip, concatenate_audioclips, concatenate_videoclips
from datetime import date, datetime
from src.log_status import log
from src.notification import notice_error, notice_warning
from src.utilitys import Struct
from src.utilitys import gen_description
from collections import namedtuple

import numpy
import random
import datetime
import requests
import json

fi = ['top', 'best']
mid = ['', 'hits', 'popular', 'greatest hits', 'collection']
mid_cover = ['Cover Of Popular', 'Cover']
mid_categr = []
se = ['right now', 'of all time']

n = len(mid) - 1
a = [0, 1, 2]
number_song = "10"
res = []
stop = 0


def generate_title(channel, api_cli, error_channels):
    video_title = None
    title_singer = None
    title_auto = None

    data_title = dict()
    data_title['error_status'] = False

    try:
        channel_id = channel.id
        log_file = channel.log_file
        singer_mode = channel.singer_mode
        include_singer_name = channel.include_singer_name

    except Exception as e:
        print(f'Can not get channel id for channel {e}')

        data = Struct(**data_title)
        data.set_error()

        return data

    log(log_file, f"Start thread for channel {channel_id}")


    try:
        imageApi = ImageCleanApi(api_client=api_cli)
        audioApi = AudioCleanApi(api_client=api_cli)
        channelApi = ChannelApi(api_client=api_cli)
        channelSingerApi = ChannelSingerApi(api_client=api_cli)
        notificationApi = NotificationApi(api_client=api_cli)
        channelCountryApi = ChannelCountryApi(api_client=api_cli)
    except Exception as error:
        log(log_file, f"could be not pass api client\n or {error}")
        data = Struct(**data_title)
        if channel_id in error_channels:
            pass
        else:
            data.set_error()

        return data

    try:
        language_code = channel.language_code
    except:
        __content = "Language code was not found"
        log(log_file, f"{__content}")
        data = Struct(**data_title)

        if channel_id in error_channels:
            pass
        else:
            data.set_error()
        try:
            notice_error(notificationApi, channel, __content)
        except:
            pass

        return data

    if not language_code:
        __content = "Language code was not found"
        log(log_file, f"{__content}")
        data = Struct(**data_title)

        if channel_id in error_channels:
            pass
        else:
            data.set_error()
        try:
            notice_error(notificationApi, channel, __content)
        except:
            pass

        return data

    try:
        name_singers = channel.singer_names
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

    except Exception as error:
        __content = "Language code was not found"
        log(log_file, f"{__content}")
        data = Struct(**data_title)

        if channel_id in error_channels:
            pass
        else:
            data.set_error()
        try:
            notice_error(notificationApi, channel, __content)
        except:
            pass

        return data

    if len(name_singers) == 0:

        log(log_file, "Name singer could not be find")

        if channel_id in error_channels:
            pass
        else:
            error_channels.append(channel_id)

        return "error"

    len_min_singer = min(3, len(name_singers))

    count = 10

    while count > 0:
        count -= 1
        try:
            if singer_mode == 'SINGER' or singer_mode == 'SINGERS' or include_singer_name == "YES":
                video_title, title_singer, title_auto = gen_title_one_singer(start_titles, language_code,
                                                                             name_singers[0])
            elif singer_mode == 'COLLECTION' and include_singer_name == "NO":
                if len(start_titles) == 0:
                    __content = "List start title was not find"
                    log(log_file, f"{__content}")

                    data = Struct(**data_title)

                    if channel_id in error_channels:
                        pass
                    else:
                        data.set_error()
                    try:
                        notice_error(notificationApi, channel, __content)
                    except:
                        pass

                    return data

                if len(mid_titles) == 0:
                    __content = "List mid title was not find"
                    log(log_file, f"{__content}")

                    data = Struct(**data_title)

                    if channel_id in error_channels:
                        pass
                    else:
                        data.set_error()
                    try:
                        notice_error(notificationApi, channel, __content)
                    except:
                        pass

                    return data

                if len(stop_titles) == 0:
                    __content = "List end titles was not find"
                    log(log_file, f"{__content}")

                    data = Struct(**data_title)

                    if channel_id in error_channels:
                        pass
                    else:
                        data.set_error()
                    try:
                        notice_error(notificationApi, channel, __content)
                    except:
                        pass

                    return data

                video_title, title_singer, title_auto = gen_title_collection(name_singers[0:len_min_singer],
                                                                             start_titles, mid_titles,
                                                                             stop_titles, language_code,
                                                                             include_singer_name)
        except:
            video_title = None

        if not video_title:
            continue
        elif len(video_title) < 95:
            break
        else:
            video_title = title_auto
            if len(video_title) < 95:
                break
            break

    if not video_title:
        __content = "Can not generate title"
        log(log_file, f"{__content}")

        data = Struct(**data_title)

        if channel_id in error_channels:
            pass
        else:
            data.set_error()
        try:
            notice_error(notificationApi, channel, __content)
        except:
            pass

        return data

    data_title['video_title'] = video_title
    data_title['title_singer'] = title_singer
    data_title['title_auto'] = title_auto
    data = Struct(**data_title)

    return data


def sinh_to_hop(k):
    global n
    i = k
    global stop
    global a
    while i >= 1 and a[i] == n - k + i:
        i = i - 1
    if i == 0:
        stop = 1
    else:
        a[i] += 1
        p = a[i]
        while i <= k:
            a[i] = p
            i += 1
            p += 1
    arr = a.copy()
    titles = []
    arr_se = []
    for k in fi:
        try:
            title_arr = [k, number_song, mid[arr[1]], mid[arr[2]], 'songs']
            title = " ".join(title_arr)
            titles.append(title)
            arr_se.append(title)
        except:
            pass
        try:
            title_arr = [k, number_song, mid[arr[2]], mid[arr[1]], 'songs']
            title = " ".join(title_arr)
            titles.append(title)
            arr_se.append(title)
        except:
            pass
        try:
            title_arr = [k, mid[arr[1]], mid[arr[2]], 'songs']
            title = " ".join(title_arr)
            titles.append(title)
            arr_se.append(title)
        except:
            pass
        try:
            title_arr = [k, mid[arr[2]], mid[arr[1]], 'songs']
            title = " ".join(title_arr)
            titles.append(title)
            arr_se.append(title)
        except:
            pass
        try:
            title_arr = [k, number_song, mid[arr[1]], 'songs']
            title = " ".join(title_arr)
            titles.append(title)
            arr_se.append(title)
        except:
            pass
        try:
            title_arr = [k, number_song, mid[arr[2]], 'songs']
            title = " ".join(title_arr)
            titles.append(title)
            arr_se.append(title)
        except:
            pass
        try:
            title_arr = [k, mid[arr[1]], 'songs']
            title = " ".join(title_arr)
            titles.append(title)
            arr_se.append(title)
        except:
            pass
        try:
            title_arr = [k, mid[arr[2]], 'songs']
            title = " ".join(title_arr)
            titles.append(title)
            arr_se.append(title)
        except:
            pass
        try:
            title_arr = [mid[arr[1]], mid[arr[2]], 'songs']
            title = " ".join(title_arr)
            titles.append(title)
            arr_se.append(title)
        except:
            pass
        try:
            title_arr = [mid[arr[2]], mid[arr[1]], 'songs']
            title = " ".join(title_arr)
            titles.append(title)
            arr_se.append(title)
        except:
            pass
        try:
            title_arr = [mid[arr[2]], 'songs']
            title = " ".join(title_arr)
            titles.append(title)
            arr_se.append(title)
        except:
            pass
        try:
            title_arr = [mid[arr[1]], 'songs']
            title = " ".join(title_arr)
            titles.append(title)
            arr_se.append(title)
        except:
            pass

    for x in arr_se:
        for k in se:
            titles.append(x + ' ' + k)
    global res
    if len(res) == 0:
        res = titles.copy()
    else:
        res = numpy.concatenate((res, titles), axis=0)


def to_hop():
    global res
    while stop == 0:
        sinh_to_hop(2)


def clean_title(title: str):
    title = title.lower()
    arr = title.split(' ')
    d = {}
    for x in arr:
        d[x] = 1
    new_title = ''
    for x in arr:
        if d[x] == 1:
            new_title = new_title + x + ' '
            d[x] = 0

    new_title = new_title[0].upper() + new_title[1:]
    return new_title


def generate_title(singers, is_cover, is_playlist, key, category, sum, start=None, mi=None, stop=None, codes=['en']):
    global mid_categr
    global mid_cover
    global mid
    global number_song
    global fi
    global se
    # singers_encode = []
    # for singer in singers:
    #     singer_encode = str(singer).encode("utf8")
    #     singers_encode.append(singer_encode)

    if start:
        fi_tmp = []
        for x in start.split(','):
            if len(x) > 0:
                fi_tmp.append(x)

        if len(fi_tmp) > 0:
            fi = fi_tmp.copy()

    if mi:
        mid_tmp = []
        for x in mi.split(','):
            if len(x) > 0:
                mid_tmp.append(x)

        if len(mid_tmp) > 0:
            mid = mid_tmp.copy()
            mid.append('Best')
            mid.append('Hot')
            mid.append('Greatest hits')

    if stop:
        se_tmp = []
        for x in stop.split(','):
            if len(x) > 0:
                se_tmp.append(x)

        if len(se_tmp) > 0:
            se = se_tmp.copy()

    try:
        random.shuffle(fi)
        random.shuffle(mid)
        random.shuffle(se)
    except Exception as error:
        print(error)

    fi = fi[0: min(5, len(fi) - 1)]
    mid = fi[0: min(5, len(mid) - 1)]
    se = fi[0: min(5, len(se) - 1)]
    if not fi or len(fi) == 0:
        return None
    if not mid or len(mid) == 0:
        return None
    if not se or len(se) == 0:
        return None
    if is_playlist:
        fi.append('playlist')
        mid.append('playlist')
    if type(sum) is str:
        number_song = sum
    elif type(sum) is int:
        if not sum or sum <= 0:
            number_song = ""
        number_song = str(sum)
    else:
        number_song = "*"
    if not is_cover:
        mid_cover = []
    else:
        mid = mid + mid_cover
    if key:
        for mi in mid:
            if key.lower() in str(mi).lower():
                mid.append(key)
    if category and len(category) > 0:
        mid = mid + category
    global n
    if not singers or len(singers) == 0:
        return None
    if len(singers) > 1:
        name_singers = ", ".join(singers) + "..."
    else:
        name_singers = singers[0]
    n = len(mid) - 1
    to_hop()
    titles = []
    titles_key = []
    titles_cate = []

    for title in res:
        title = clean_title(title)
        titles.append(title)
        if key and key.lower() in title.lower():
            titles_key.append(title)
        elif 'playlist' in title.lower():
            titles_key.append(title)
        if category and len(category) > 0:
            for categr in category:
                if categr.lower() in title.lower():
                    titles_cate.append(title)
    if len(titles_key) == 0:
        titles_key = titles
    if len(titles_cate) == 0:
        titles_cate = titles

    try:
        random.shuffle(titles_key)
        random.shuffle(titles_cate)
    except Exception as error:
        print(error)

    title_final = []
    index_1 = random.randint(0, len(titles_key))
    index_2 = random.randint(0, len(titles_cate))
    cnt = 0
    while True:
        title_key = titles_key[index_1]
        title_cate = titles_cate[index_2]
        cnt += 1
        if cnt > 1000:
            break
        if title_key != title_cate or cnt > 1000:
            title_final.append(title_key)
            title_final.append(name_singers)
            title_final.append(title_cate)
            break
    for i in range(0, len(title_final)):
        x = title_final[i].strip()
        title_final[i] = x

    now = datetime.datetime.now()
    fi_title = title_final[0]
    se_title = title_final[2]
    of = 'of'
    for code in codes:
        try:
            if code == 'en':
                break
            url_translate = 'http://vfast.tech:8000/translate'
            params = {'sourceCountry': 'auto', 'destinationCountry': code, 'text': fi_title}
            res_fi_title = requests.post(url=url_translate, data=params)
            if res_fi_title.status_code != 200:
                continue
            fi_title = res_fi_title.json()['textAfterTrans']
            if len(fi_title) == 0:
                continue
            params = {'sourceCountry': 'en', 'destinationCountry': code, 'text': se_title}
            res_se_title = requests.post(url=url_translate, data=params)
            if res_se_title.status_code != 200:
                continue

            se_title = res_se_title.json()['textAfterTrans']
            if len(se_title) == 0:
                continue
            params = {'sourceCountry': 'en', 'destinationCountry': code, 'text': of}
            res_of = requests.post(url=url_translate, data=params)
            of = res_of.json()['textAfterTrans']
            if res_of.status_code != 200:
                continue
            if len(singers) == 1 and len(of) == 0:
                continue
            title_final[0] = str(fi_title).strip()
            title_final[2] = str(se_title).strip()
            of = str(of).strip()

            break
        except Exception as error:
            print(error)

    if len(singers) == 1:
        title_final = [title_final[0], title_final[2] + ' ' + of + ' ' + name_singers, str(now.year)]
    else:
        title_final = [title_final[0], name_singers, title_final[2], str(now.year)]

    return " | ".join(title_final)


affter_singer = ['best songs', 'top songs', 'best of songs', 'New song', 'greatest hits full album',
                 'greatest hits right now',
                 'greatest hits collection', 'mix songs', 'mix collection songs', 'new song full album',
                 'best mix of popular songs', 'full album', 'style greatest hits playlist', 'all song']
title_insert_singer = ['Top * songs', 'Best * song', 'Best songs * playlist', 'Top * style', 'New song * style']


def gen_title_singer_or_group(singers, sum, affter_singer_input, title_insert_singerInput, category):
    titles = []
    # date = datetime.datetime()
    year = datetime.datetime.now().year
    if affter_singer_input and len(affter_singer_input) > 0:
        affter_singer_input = []
    if title_insert_singerInput and len(title_insert_singerInput) > 0:
        title_insert_singerInput = []
    affter_singer_input = affter_singer_input + affter_singer
    if len(category) > 0:
        affter_singer_input.append(category)
    title_insert_singerInput = title_insert_singerInput + title_insert_singer

    name_singer = singers[0]
    for word in affter_singer_input:
        title = word + " " + name_singer
        titles.append(title)
        title = name_singer + " " + word
        titles.append(title)
        title = word + " " + name_singer + " " + str(year)
        titles.append(title)
        title = name_singer + " " + word + " " + str(year)
        titles.append(title)

    if not sum:
        sum = ""

    sum = str(sum)
    name_singer = sum + " " + singers[0]
    titles_2 = []

    for word in title_insert_singerInput:
        if len(sum) > 0:
            title = word.replace("*", name_singer)
            titles_2.append(title)
            title = word.replace("*", name_singer) + " " + str(year)
            titles_2.append(title)
        title = word.replace("*", singers[0])
        titles_2.append(title)

        title = word.replace("*", singers[0]) + " " + str(year)
        titles_2.append(title)

    index = random.randint(0, len(titles) - 1)
    title_1 = titles[index]
    index = random.randint(0, len(titles_2) - 1)
    title_2 = titles_2[index]
    title = " | ".join([title_1, title_2])
    if title.split(" ")[-1] != str(year):
        title += " " + str(year)

    title = title[0].upper() + title[1:]
    return title


top_many_singer = ['best songs', 'top songs', 'New song', 'greatest hits', 'best top song',
                   'mix songs', 'Best hit song', 'Top hit song', 'best mix of songs',
                   'style greatest hits playlist']

mid_many_singer = ['popular', 'collection']
end_many_singer = ['full time', 'all time', 'of right now']


def translate(text, code):
    if code != 'en':
        url_translate = 'http://vfast.tech:8000/translate'
        params = {'sourceCountry': 'auto', 'destinationCountry': code, 'text': text}
        res_title = requests.post(url=url_translate, data=params)
        if res_title.status_code == 200:
            res_text = res_title.json()['textAfterTrans']

        if len(res_text) > 0:
            return res_text
    return text


def gen_title_collection(singers, top_many_singer_input,
                         mid_many_singer_input, end_many_singer_input,
                         code, include_singer_name):
    """
Detail:
    :param singers:
    :param top_many_singer_input:
    :param mid_many_singer_input:
    :param end_many_singer_input:
    :param code:
    :param include_singer_name:
    :return:
    """

    year = datetime.datetime.now().year

    if len(top_many_singer_input) == 0:
        # top_many_singer_input = []
        print("List top title was not found")
        return '', ''

    if len(mid_many_singer_input) == 0:
        # mid_many_singer_input = []
        print("List mid title was not found")
        return '', ''

    if len(end_many_singer_input) == 0:
        # end_many_singer_input = []
        print("List mid title was not found")
        return '', ''
    #
    # text_top = ",".join(top_many_singer_input)
    # text_top = translate(text_top, code)
    # if text_top:
    #     top_many_singer_input = text_top.split(',')

    # text_mid = ",".join(mid_many_singer_input)
    # text_mid = translate(text_mid, code)
    # if text_mid:
    #     mid_many_singer_input = text_mid.split(',')
    #
    # text_end = ",".join(end_many_singer_input)
    # text_end = translate(text_end, code)
    # if text_end:
    #     end_many_singer_input = text_end.split(',')

    year = str(year)
    top_titles = ['']
    mid_titles = ['']
    end_titles = ['']

    for top in top_many_singer_input:
        if 100 >= len(top) >= 90:
            continue

        top_titles.append(top)

        _year_title = top + " " + year
        if len(_year_title) < 90:
            end_titles.append(_year_title)

    for mid in mid_many_singer_input:
        if len(mid) >= 90:
            continue

        mid_titles.append(mid)

        _year_title = mid + " " + year
        if len(_year_title) < 90:
            end_titles.append(_year_title)

    for end_title in end_many_singer_input:
        if len(end_title) >= 90:
            continue

        end_titles.append(end_title)

        _year_title = end_title + " " + year

        if len(_year_title) < 90:
            end_titles.append(_year_title)

    emoji = [' | ', ' ♫ ', ' 💘 ', ' 💋 ', ' 💔 ', ' ☘️ ']
    random_choice = random.SystemRandom()
    # e = emoji[random.randint(0, len(emoji)-1)]
    e = random_choice.choice(emoji)
    e_1 = random_choice.choice(emoji)
    e_2 = random_choice.choice(emoji)

    top_title = random_choice.choice(top_titles)
    mid_title = random_choice.choice(mid_titles)
    end_title = random_choice.choice(end_titles)

    count_times = 0
    while len(top_title) == 0 and len(mid_title) == 0 and len(end_title) == 0:
        count_times += 1
        top_title = random_choice.choice(top_titles)
        mid_title = random_choice.choice(mid_titles)
        end_title = random_choice.choice(end_titles)
        if count_times > 100:
            break

    titles = [top_title, e, mid_title, e_1, end_title]
    title = top_title
    _times_out = len(titles)
    _count = 0

    while len(title) < 90:
        _count += 1
        if _count >= _times_out:
            break
        title += titles[_count]

    titles = [top_title, mid_title, end_title]
    count_times = 0
    title_audio = ''

    while len(title_audio) == 0:
        count_times += 1
        title_audio = random_choice.choice(titles)
        if count_times > 10:
            break

    if include_singer_name == 'YES':
        title_singer = title
        _title_singer = title + e

        if len(_title_singer) < 100:
            _title_singer += ", ".join(singers)
            if len(_title_singer) < 100:
                _title_singer += e_2

        title = _title_singer

    else:
        title_singer = title

    title = upper_title(title)
    title_singer = upper_title(title_singer)
    title_audio = upper_title(title_audio)

    return title, title_singer, title_audio


def gen_title_one_singer(one_singer_input, code='en', singer=None):
    _one_title = False

    if len(singer) == 0:
        return None

    if len(one_singer_input) < 2:
        _one_title = True

    if not one_singer_input or len(one_singer_input) == 0:
        one_singer_input = []
        default_title = ['Top * songs', 'Best * song', 'Best songs * playlist', 'Top * style', 'New song * style']

        if code != 'en':
            for text in default_title:
                url_translate = 'http://vfast.tech:8000/translate'
                params = {'sourceCountry': 'auto', 'destinationCountry': code, 'text': text}
                res_title = requests.post(url=url_translate, data=params)
                if res_title.status_code == 200:
                    res_text = res_title.json()['textAfterTrans']
                    res_text = res_text.replace('*', '')
                    one_singer_input.append(res_text)
                else:
                    print("Can not translate title")
        else:
            for title in default_title:
                new_title = title.replace("*", '')
                one_singer_input.append(new_title)

    end_one_singer = []
    # end_one_singer = ['Popular', 'Collection', 'Of all time']
    #
    # if code != 'en':
    #     end_titles = []
    #     for end_title in end_one_singer:
    #         url_translate = 'http://vfast.tech:8000/translate'
    #         params = {'sourceCountry': 'auto', 'destinationCountry': code, 'text': end_title}
    #
    #         res_title = requests.post(url=url_translate, data=params)
    #
    #         if res_title.status_code == 200:
    #             title = res_title.json()['textAfterTrans']
    #             if len(title) != 0:
    #                 end_titles.append(title)
    #
    #     end_one_singer = end_titles

    data_titles = []
    data_titles_singer = []

    for title in one_singer_input:
        new_title = title.lower()
        new_title_singer = new_title

        new_title_singer = new_title_singer.replace('singer', singer)
        new_title = new_title.replace('singer', '')

        new_title = new_title.replace('number', " * ")
        new_title_singer = new_title_singer.replace('number', " * ")

        data_titles.append(new_title)
        data_titles_singer.append(new_title_singer)

    titles = []
    titles_singer = []
    year = str(datetime.datetime.now().year)

    for title in data_titles:
        number_digit = len(title)
        if 100 >= number_digit >= 90:
            titles.append(title)
            continue

        elif number_digit > 100:
            continue

        else:
            title_year = title + ' ' + year
            if len(title_year) < 100:
                titles.append(title_year)
            else:
                titles.append(title)
                continue
        for end_title in end_one_singer:
            _title_tmp = title + ' ' + end_title
            if len(_title_tmp) < 100:
                titles.append(title + ' ' + end_title)
            else:
                continue

            _title_tmp = title + ' ' + end_title + ' ' + year
            if len(_title_tmp):
                titles.append(_title_tmp)

    for title in data_titles_singer:
        if 100 >= len(title) >= 90:
            titles_singer.append(title)
            continue

        elif len(title) > 100:
            continue

        else:
            title_year = title + ' ' + year
            if len(title_year) < 100:
                titles_singer.append(title_year)
            else:
                titles_singer.append(title)
                continue

        for end_title in end_one_singer:
            _title_tmp = title + ' ' + end_title
            if len(_title_tmp) < 100:
                titles_singer.append(title + ' ' + end_title)
            else:
                continue

            _title_tmp = title + ' ' + end_title + ' ' + year
            if len(_title_tmp):
                titles_singer.append(_title_tmp)

    titles_clean = []
    titles_singer_clean = []

    for title in titles:
        title_split = []
        for word in title.split(' '):
            new_word = None
            if len(word) > 1:
                new_word = word[0].upper() + word[1:].lower()
            elif len(word) == 1:
                new_word = word[0].upper()
            if new_word:
                title_split.append(new_word)

        if len(title_split):
            title_clean = " ".join(title_split)
            titles_clean.append(title_clean)

    # Check title too long with has singer in title singer
    if len(titles_singer) == 0:
        titles_singer = titles.copy()

    for title in titles_singer:
        title_split = []
        for word in title.split(' '):
            new_word = None
            if len(word) > 1:
                new_word = word[0].upper() + word[1:].lower()
            elif len(word) == 1:
                new_word = word[0].upper()
            if new_word:
                title_split.append(new_word)

        if len(title_split):
            title_singer_clean = " ".join(title_split)
            titles_singer_clean.append(title_singer_clean)

    emojis = [' | ', ' ♫ ', ' 💘 ', ' 💋 ', ' 💔 ', ' ☘️ ']
    _chose = random.SystemRandom()

    # Render title
    if not _one_title:
        _start_title = _chose.choice(titles_clean)
        _start_title = upper_title(_start_title)

        _end_title = _chose.choice(titles_clean)
        _end_title = upper_title(_end_title)

        emoji = _chose.choice(emojis)

        _titles = [_start_title, emoji, _end_title]
        title = _start_title
        _time_out = len(_titles)
        _count = 0

        while len(title) < 90:
            _count += 1
            if _count == _time_out:
                break

            _title = title + _titles[_count]
            if len(_title) >= 90:
                break
            else:
                title = _title

    else:
        _title = _chose.choice(titles_clean)
        emoji = _chose.choice(emojis)
        title = _title + emoji
        if len(title) >= 100:
            title = _title

    # Render title singer
    if len(titles_singer_clean) >= 8:
        _start_title = _chose.choice(titles_singer_clean)
        _start_title = upper_title(_start_title)

        _end_title = _chose.choice(titles_singer_clean)
        _end_title = upper_title(_end_title)

        emoji = _chose.choice(emojis)
        _titles_singer = [_start_title, emoji, _end_title]
        title_singer = _start_title
        _time_out = len(_titles_singer)
        _count = 0

        while len(title_singer) < 90:
            _count += 1
            if _count == _time_out:
                break

            _title_singer = title_singer + _titles_singer[_count]
            if len(_title_singer) >= 90:
                break
            else:
                title_singer = _title_singer

    else:
        _title = _chose.choice(titles_singer_clean)
        _title = upper_title(_title)

        emoji = _chose.choice(emojis)
        title_singer = _title + emoji

        if len(title_singer) >= 100:
            title_singer = _title

    title_audio = upper_title(_chose.choice(titles_clean))

    return title, title_singer, title_audio


def upper_title(title):
    try:
        arr_1 = []
        for word in title.split(' '):
            new_word = None
            if len(word) == 1:
                new_word = word[0].upper()
            elif len(word) > 1:
                new_word = word[0].upper() + word[1:].lower()
            if new_word:
                arr_1.append(new_word)
        return " ".join(arr_1)

    except:
        return title

