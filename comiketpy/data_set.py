#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 18:00:00 2019

get Circle.ms Data and Twitter Data
@author: nozomi_toba
"""
################################################################
#
# you can get Circle.ms's data by this program, made by csv files
# if you use the program, you have to sign up Circle.ms's
# and Twitter API accounts
# after that you can use this program
#
# filename:
#     circle_ms_all_id.csv       : all ids of participant in comiket
#     all_circle_info.csv        : all information of participant in comiket
#     all_circle_info_twitter.csv: all information with Twitter followers count of participant in comiket
#
################################################################

import json
import pandas as pd
import os
import re
import requests
import tweepy
from bs4 import BeautifulSoup
from datetime import datetime
from getpass import getpass
from statistics import mean
from time import sleep

Base_dir = os.path.abspath("./")

################################################################
#
# initilaize Twitter's keys and Circle.ms's ones
#
# meaning of functions and arguments:
#     init_keys(): initialize keys of Twitter API and Circle.ms
#         Ck: Twitter API consumer key
#         Cs: Twitter API consumer secret
#         At: Twttier API access token
#         As: Twitter API access secret
#         Un: Circle.ms username
#         Pw: Circle.ms password
#
# eg(interactive mode):
# >>> import comiketpy as cmp
# >>> cmp.init_keys()
# ### Twitter_API Consumer_key   : /* input your Twitter API consumer key by password mode */
# ### Twitter_API Consumer_secret: /* input yout Twitter API consumer secret by password mode */
# ### Twitter_API Access_token   : /* input your Twitter API access token by password mode */
# ### Twitter_API Access_secret  : /* input your Twitter API access secret by password mode */
# ### Circle_ms   Username       : /* input your Circle.ms username by input mode */
# ### Circle_ms   Password       : /* input your Circle.ms password by password mode */
# ### キーの初期化をしました。
#
# eg(script mode):
# >>> import comiketpy as cmp
# >>> Ck = /* input your Twitter API consumer key by password mode */
# >>> Cs = /* input yout Twitter API consumer secret by password mode */
# >>> At = /* input your Twitter API access token by password mode */
# >>> As = /* input your Twitter API access secret by password mode */
# >>> Un = /* input your Circle.ms username by input mode */
# >>> Pw = /* input your Circle.ms password by password mode */
# >>> cmp.init_keys(Ck=Ck, Cs=Cs, At=At, As=As, Un=Un, Pw=Pw)
# ### キーの初期化をしました。
#
################################################################
class InitComiketpyKey(object):

    def __init__(self):
        pass

    def init_keys(self, Ck="", Cs="", At="", As="", Un="", Pw=""):
        # input Twitter's keys by password mode.
        if Ck == "":
            Ck = getpass("Twitter_API Consumer_key   : ")
        if Cs == "":
            Cs = getpass("Twitter_API Consumer_secret: ")
        if At == "":
            At = getpass("Twitter_API Access_token   : ")
        if As == "":
            As = getpass("Twitter_API Access_secret  : ")

        # input Circle.mcs's keys by password mode and input mode.
        if Un == "":
            Un =   input("Circle_ms   Username       : ")
        if Pw == "":
            Pw = getpass("Circle_ms   Password       : ")

        output = {
            "Twitter_API": {
                "Consumer_key": Ck,
                "Consumer_secret": Cs,
                "Access_token": At,
                "Access_secret": As
            },
            "Circle_ms": {
                "Username": Un,
                "Password": Pw
            }
        }

        # register their keys
        with open(Base_dir+"/resources/login_info.json", mode="w") as file:
            json.dump(output, file)

        print("キーの初期化をしました。")

################################################################
#
# get Circle.ms information
#
# !!! CAUTION !!!
# if you don't register subscribed account on Circle.ms,
# you have to wait so many hours (about half a day)
# during getting all circle.ms's ids of participants of comiket
#
# meaning of functions and arguments:
#     make_csv_all_id()         : get all ids of participant in comiket
#     make_csv_all_circle_info(): get one id of participant in comiket
#     circle_info()             : get circle information from htmls of participant in comiket
#         Target_html: html of participant in comiket
#
# eg:
# >>> import comiketpy as cmp
# >>> cmp.make_csv_all_id()
# ### コミックマーケット参加者 ID （落選を含む）を取得します。
# ### 1 日目のデータは 127 ページあります。
# ### 現在 20 ページのデータを取得中です。
# ### ...
# ### 現在 120 ページのデータを取得中です。
# ### 全てのコミックマーケット参加者 ID （落選を含む）を取得しました。
# >>> cmp.make_csv_all_circle_info()
# ### コミックマーケット参加者の情報（落選を含む）を取得します。
# ### Circle.ms のデータは残り 37000 ページあります。
# ### ...
# ### Wait 5 minutes....
# ### ...
# ### Circle.ms のデータは残り 0 ページあります。
# ### 全てのコミックマーケット参加者の情報（落選を含む）を取得しました。
#
################################################################
class AnalyzeCircleMs(object):

    def __init__(self):

        # set login key via json file
        Target_json = Base_dir+"/resources/login_info.json"
        with open(Target_json) as file:
            Login_info = json.loads(file.read())["Circle_ms"]

        # login on Circle.ms page
        Target_url = "https://webcatalog-free.circle.ms/Account/Login"
        Target_html = requests.get(Target_url).text
        Soup = BeautifulSoup(Target_html, "html.parser")

        Form_action = Soup.find("form")["action"]

        Input_list = Soup.find_all("input")
        for li in Input_list:
            try:
                key = li["name"]
                val = li["value"]
            except:
                continue
            if key not in Login_info:
                Login_info[key] = val

        session = requests.session()
        res = session.post(Form_action, data=Login_info)
        # if session of login is failed, raise for status
        res.raise_for_status()

        # creating Circle.ms login instance
        self.session = session

    def make_csv_all_id(self):

        print("コミックマーケット参加者 ID （落選を含む）を取得します。")

        # held days of comiket as of 2018 winter
        # in 2019 comiket will be held 4 days, so Days will be rewritten Days = (1,2,3,4,99)
        # they mean participants of 1st day, 2nd day, 3rd day, and rejected ones in comiket
        Days = (1,2,3,99)

        all_id = []

        target_csv = Base_dir+"/resources/circle_ms_all_id.csv"
        with open(target_csv, mode="w") as file:
            file.write("Id\n")

        session = self.session

        for day in Days:

            Target_url = "https://webcatalog-free.circle.ms/Circle?Day=" + str(day)
            Target_html = session.get(Target_url).text

            Soup = BeautifulSoup(Target_html, "html.parser")

            Title = Soup.find("title").text

            # only 3 minutes serially you can connect comiket web catalog
            # so if you connect the page over 3 minutes serially, wait 5 minutes
            # if you don't want to wait, you register subscribed account on Circle.ms
            if "Comike Web Catalog" not in Title:

                print(datetime.today(), "Wait 5 minutes....")

                with open(target_csv, mode="a") as file:
                    for one_id in all_id:
                        file.write(one_id+"\n")

                all_id = []
                # wait 5 minutes before next connecting
                sleep(301)

                Target_html = session.get(Target_url).text

            pre_pages = Soup.find_all("div", attrs={"class": "m-pagination-item m-pagination-nav"})[-1]
            pages = int(re.search("[0-9]+", pre_pages.find("a")["href"][-3:]).group(0))

            print(datetime.today(), day, "日目のデータは", pages,"ページあります。")

            for page in range(1, pages+1):

                Target_url = "https://webcatalog-free.circle.ms/Circle?Day=" + str(day) + "&page=" + str(page)
                Target_html = session.get(Target_url).text

                Soup = BeautifulSoup(Target_html, "html.parser")

                Title = Soup.find("title").text

                if "Comike Web Catalog" not in Title:

                    print(datetime.today(), "Wait 5 minutes....")

                    with open(target_csv, mode="a") as file:
                        for one_id in all_id:
                            file.write(one_id+"\n")

                    all_id = []
                    sleep(301)

                    Target_html = session.get(Target_url).text

                if page % 20 == 0:
                    print(datetime.today(), "現在", page, "ページのデータを取得中です。")

                Soup = BeautifulSoup(Target_html, "html.parser")

                pre_current_all_id = Soup.find("script", attrs={"type": "application/json"}).text
                Current_all_id = [one_id[len("\"Id\":"):-1] for one_id in re.findall("\"Id\":[0-9]*?,", pre_current_all_id)]

                all_id.extend(Current_all_id)

        with open(target_csv, mode="a") as file:
            for one_id in all_id:
                file.write(one_id+"\n")

        print("全てのコミックマーケット参加者 ID （落選を含む）を取得しました。")

    def make_csv_all_circle_info(self):

        print(datetime.today(), "コミックマーケット参加者の情報（落選を含む）を取得します。")
        target_csv = Base_dir+"/resources/circle_ms_all_id.csv"

        Series = pd.read_csv(target_csv, dtype="object")["Id"]

        target_csv = Base_dir+"/resources/all_circle_info.csv"

        with open(target_csv, mode="w") as file:
            file.write("")

        columns = ["Id","Day","Hall","Block","Space","Name","Author","Genre","PixivId","TwitterId"]
        all_circle_info = [{i: i for i in columns}]

        pages = len(Series)

        session = self.session

        for i in range(pages):

            Target_url = "https://webcatalog-free.circle.ms/Circle/" + str(Series[i])
            Target_html = session.get(Target_url).text

            Soup = BeautifulSoup(Target_html, "html.parser")

            Title = Soup.find("title").text

            # only 3 minutes serially you can connect comiket web catalog
            # so if you connect the page over 3 minutes serially, wait 5 minutes
            # if you don't want to wait, you register subscribed account on Circle.ms
            if "Comike Web Catalog" not in Title:

                print(datetime.today(), "Wait 5 minutes....")

                # write csv file by mode of adding a postscript
                pre_df = pd.io.json.json_normalize(all_circle_info)
                df = pre_df.loc[:,["Id","Day","Hall","Block","Space","Name","Author","Genre","PixivId","TwitterId"]]
                df.to_csv(target_csv, mode="a", header=False, index=False)

                all_circle_info = []

                # wait 5 minutes before next connecting
                sleep(301)

                Target_html = session.get(Target_url).text

            all_circle_info.append(self.circle_info(Target_html))

            if (pages-i-1) % 20 == 0:
                print(datetime.today(), "Circle.ms のデータは残り", pages-i-1, "ページあります。")

        # write csv file by mode of adding a postscript
        pre_df = pd.io.json.json_normalize(all_circle_info)
        df = pre_df.loc[:,["Id","Day","Hall","Block","Space","Name","Author","Genre","PixivId","TwitterId"]]
        df.to_csv(target_csv, mode="a", header=False, index=False)

        print("全てのコミックマーケット参加者の情報（落選を含む）を取得しました。")

    def circle_info(self, Target_html):

        Current_circle = re.search("ComiketWebCatalog.CurrentCircle(.|\s)*?};", Target_html).group(0)
        Name, Id, TwitterId, PixivId = (string[1:-1] for string in re.findall("'.*?'", Current_circle))

        Location = re.search("ComiketWebCatalog.CurrentCircle.Location(.|\s)*?};", Target_html).group(0)
        Day, Hall, Block, Space = (string[1:-1] for string in re.findall("'.*?'", Location))

        # get author information
        target_th = re.search('<th>執筆者名</th>(.|\s)*?</td>', Target_html).group(0)
        soup = BeautifulSoup(target_th, "html.parser")
        Author = re.search(".*", soup.find("td").text).group(0)[:-1]

        # get genre information
        target_th = re.search('<th.*?>ジャンル</th>(.|\s)*?</td>', Target_html).group(0)
        soup = BeautifulSoup(target_th, "html.parser")
        Genre = soup.find("td").text.split("\n")[1][:-1]

        res = {
            "Name"     : Name,
            "Id"       : Id,
            "TwitterId": TwitterId,
            "PixivId"  : PixivId,
            "Day"      : Day,
            "Hall"     : Hall,
            "Block"    : Block,
            "Space"    : Space,
            "Author"   : Author,
            "Genre"    : Genre,
        }

        return res

################################################################
#
# get Twitter information of participants in comiket
#
# !!! CAUTION !!!
# it is explicitly prohibitten to scrape any Twitter pages without Twitter API
# cf https://help.twitter.com/en/rules-and-policies/twitter-rules
# if you scrape some Twitter pages, you have to sign up Twitter API developper account
# why don't you know how to sign up Twitter API developper account? you google it
#
# !!! CAUTION !!!
# you have to wait so many hours (about half a day) because of the twitter rules
#
# meaning of functions and arguments:
#     get_all_followers_count(): get all followers counts of participant in comiket
#         start  : index of all_circle_info.csv, even if you interrupt running function get_all_followers_count(), you can restart the program
#     get_followers_count()    : get one followers count fo participant in comiket
#         user_id: Twitter user id of participant in comiket
#
# eg:
# >>> import comiketpy as cmp
# >>> cmp.get_all_followers_count()
# ### Twitter のフォロワー数を取得します。")
# ### Twitter のデータは残り 30000 ページあります。
# ### ...
# ### Twitter のデータは残り 0 ページあります。
# ### 全てのコミックマーケット参加者のフォロワー数（落選を含む）を取得しました。
#
################################################################
class AnalyzeTwitter(object):

    def __init__(self):

        # set login key via json file
        Target_json = Base_dir+"/resources/login_info.json"
        with open(Target_json) as file:
            Login_info = json.loads(file.read())["Twitter_API"]

        Ck = Login_info["Consumer_key"]
        Cs = Login_info["Consumer_secret"]
        At = Login_info["Access_token"]
        As = Login_info["Access_secret"]

        # authority recognition
        auth = tweepy.OAuthHandler(Ck, Cs)
        auth.set_access_token(At, As)

        # creating API instance
        self.api = tweepy.API(auth)

    def get_all_followers_count(self, start=0):

        print(datetime.today(), "Twitter のフォロワー数を取得します。")

        target_csv = Base_dir+"/resources/all_circle_info.csv"
        # write csv file by mode of new writing
        df = pd.read_csv(target_csv, dtype="object")
        Series = df["TwitterId"]

        target_csv = Base_dir+"/resources/all_circle_info_twitter.csv"
        pages = len(Series)

        for i in range(start, pages):
            if (pages-i-1) % 20 == 0:
                print(datetime.today(), "Twitter のデータは残り", pages-i-1, "ページあります。")
                # write csv file by mode of new writing
                df.to_csv(target_csv, mode="w", index=False)

            try:
                df.loc[i,"TwitterFollowers"] = str(self.get_followers_count(user_id=int(Series[i])))
            except:
                df.loc[i,"TwitterFollowers"] = ""

        # write csv file by mode of new writing
        df.to_csv(target_csv, mode="w", index=False)

        print(datetime.today(), "全てのコミックマーケット参加者のフォロワー数（落選を含む）を取得しました。")

    def get_followers_count(self, user_id):

        api = self.api

        userInfo = api.get_user(user_id=user_id)
        res = userInfo.followers_count

        # technical avoidant time because of Twitter Followers count only one request per one sec.
        sleep(1)

        return res

