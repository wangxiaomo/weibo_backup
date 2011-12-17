#-*- coding: utf-8 -*-

import sys
from time import sleep

from config import *
from weibopy.auth import OAuthHandler
from weibopy.api import API
from writer import Writer

class WeiboBackup(object):
    """
    新浪微博自动备份.
    """
    def __init__(self):
        self.hdl = OAuthHandler(APP_KEY, APP_SECRET)
        self.api = None
        self.writer = None
        self.token  = {}

    def auth(self, pin):
        try:
            token = self.hdl.get_access_token(pin)
            """
            self.token = dict(parse_qsl(token))
            self.hdl.setToken(
                self.token['oauth_token'],
                self.token['oauth_token_secret']
            )
            self.hdl.setToken(
                ACCESS_TOKEN,
                ACCESS_SECRET
            )
            """
            self.api = API(self.hdl)
        except Exception as e:
            print e

    def get_auth_url(self):
        return self.hdl.get_authorization_url()

    def get_data(self, screen_name, page):
        count = 200
        while True:
            try:
                res = self.api.user_timeline(
                    screen_name=screen_name,
                    count=count,
                    page=page
                )
                if len(res)==0:
                    return page
                else:
                    for status in res:
                        text = status.text
                        retweet = getattr(
                            status,
                            "retweeted_status",
                            False
                        )
                        if retweet:
                            text = text+"//"+retweet.text
                        text = text.encode("utf-8")
                        self.writer.append(text)
                page = page+1
            except Exception as e:
                print e
            

    def backup(self, screen_name, filename):
        self.writer = Writer(filename)
        page,alert_num = 1,0
        while alert_num<ALERT_MAX_TIMES:
            page = self.get_data(screen_name, page)
            alert_num += 1

if __name__ == '__main__':
    obj = WeiboBackup()
    print obj.get_auth_url()
    pin = raw_input("PIN:")
    obj.auth(pin)
    obj.backup(sys.argv[1], sys.argv[2])
