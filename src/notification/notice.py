"""""""""""""""""""""""
Author : NGUYEN DINH HAI
VER    : 1.0
DATE   : 2021, JUL 12
"""""""""""""""""""""""

import json


def notice_error(notificationApi, channel, content):
    """

    :param notificationApi:
    :param channel:
    :param content:
    :return:
    """
    account_id = channel.account_id
    channel_id = channel.id

    content = json.dumps({"title": content})

    data = {'message': 'ERROR CREATE VIDEO',
            'content': content,
            'accountId': account_id,
            'channelId': channel_id
            }

    filter = json.dumps({"where": {'message': 'ERROR CREATE VIDEO',
                                   'content': content,
                                   'accountId': account_id,
                                   'channelId': channel_id},
                         "order": 'id DESC'})

    noties = notificationApi.notification_find(filter=filter)
    if len(noties) != 0:
        notice = noties[0]
        if notice.status == "DONE":
            notificationApi.notification_create(data=data)
        else:
            print(f"This mistake was noticed for channel {channel_id}")
            return True
    else:
        try:
            notificationApi.notification_create(data=data)
        except Exception as e:
            print("can not create notice for channel")
            return False


def notice_warning(notificationApi, channel, content):
    """
    Detail:
    :param notificationApi:
    :param channel:
    :param content:
    :return:
    """
    account_id = channel.account_id
    channel_id = channel.id

    content = json.dumps({"title": content})

    data = {'message': 'WARNING CREATE VIDEO',
            'content': content,
            'accountId': account_id,
            'channelId': channel_id
            }
    try:
        notificationApi.notification_create(data=data)
        return True
    except:
        print(f"cannot create warning notice for channel {channel_id}")
        return False

