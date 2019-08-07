# -*- coding: utf-8 -*-

from plurk_oauth import PlurkAPI
import time

def url_img(figname, retry=5):
    plurk = PlurkAPI.fromfile('./API.keys')
    for i in range(retry):
        try: return plurk.callAPI('/APP/Timeline/uploadPicture', fpath=figname)['full']
        except: time.sleep(0.1)
    return None

def add_plurk(msg, private=False, retry=5):
    plurk = PlurkAPI.fromfile('./API.keys')
    options = {'content': msg, 'qualifier': ''}
    if private: options['limited_to'] = '[]'
    for i in range(retry):
        try: return plurk.callAPI('/APP/Timeline/plurkAdd', options=options)
        except: time.sleep(0.1)
    return None

