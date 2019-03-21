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
################################################################

import json
import tweepy
import requests
import re
import os
import pandas as pd
from getpass import getpass
from bs4 import BeautifulSoup
from time import sleep
from datetime import datetime
from statistics import mean

Base_dir = os.path.abspath("./../")

################################################################
#
# initilaize Twitter's keys and Circle.ms's ones
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
        res.raise_for_status()

        self.session = session

    def make_csv_all_id(self):

        print("コミックマーケット参加者 ID （落選を含む）を取得します。")

        session = self.session

        Days = (1,2,3,99)

        all_id = []

        target_csv = Base_dir+"/resources/circle_ms_all_id.csv"
        with open(target_csv, mode="w") as file:
            file.write("Id\n")
        for day in Days:

            Target_url = "https://webcatalog-free.circle.ms/Circle?Day=" + str(day)
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

        session = self.session

        Series = pd.read_csv(target_csv, dtype="object")["Id"]

        all_circle_info = []

        target_csv = Base_dir+"/resources/all_circle_info.csv"
        header = {}
        for i in ["Name","Id","TwitterId","PixivId","Day","Hall","Block","Space"]:
            header[i] = i

        df = pd.io.json.json_normalize(header)
        df.to_csv(target_csv, mode="w", header=False, index=False)

        pages = len(Series)
        for i in range(pages):

            Target_url = "https://webcatalog-free.circle.ms/Circle/" + str(Series[i])
            Target_html = session.get(Target_url).text

            Soup = BeautifulSoup(Target_html, "html.parser")

            Title = Soup.find("title").text

            if "Comike Web Catalog" not in Title:

                print(datetime.today(), "Wait 5 minutes....")

                df = pd.io.json.json_normalize(all_circle_info)
                df.to_csv(target_csv, mode="a", header=False, index=False)

                all_circle_info = []
                sleep(301)

                Target_html = session.get(Target_url).text

            all_circle_info.append(self.circle_info(Target_html))

            if (pages-i-1) % 20 == 0:
                print(datetime.today(), "Circle.ms のデータは残り", pages-i-1, "ページあります。")

        df = pd.io.json.json_normalize(all_circle_info)
        df.to_csv(target_csv, mode="a", header=False, index=False)

        print("全てのコミックマーケット参加者の情報（落選を含む）を取得しました。")

    def circle_info(self, Target_html):

        Current_circle = re.search("ComiketWebCatalog.CurrentCircle(.|\s)*?};", Target_html).group(0)
        Name, Id, TwitterId, PixivId = (string[1:-1] for string in re.findall("'.*?'", Current_circle))

        Location = re.search("ComiketWebCatalog.CurrentCircle.Location(.|\s)*?};", Target_html).group(0)
        Day, Hall, Block, Space = (string[1:-1] for string in re.findall("'.*?'", Location))

        res = {
            "Name"     : Name,
            "Id"       : Id,
            "TwitterId": TwitterId,
            "PixivId"  : PixivId,
            "Day"      : Day,
            "Hall"     : Hall,
            "Block"    : Block,
            "Space"    : Space,
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
# how to sign up Twitter API developper account? you google it
#
# !!! CAUTION !!!
#
# you have to wait so many hours (about half a day)
# during getting all circle.ms's ids of participants of comiket
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
        df = pd.read_csv(target_csv, dtype="object")
        Series = df["TwitterId"]

        target_csv = Base_dir+"/resources/all_circle_info_twitter.csv"
        pages = len(Series)

        for i in range(start, pages):
            if (pages-i-1) % 20 == 0:
                print(datetime.today(), "Twitter のデータは残り", pages-i-1, "ページあります。")
                df.to_csv(target_csv, mode="w", index=False)

            try:
                df.loc[i,"TwitterFollowers"] = int(self.get_followers_count(user_id=int(Series[i])))
            except:
                df.loc[i,"TwitterFollowers"] = ""

        df.to_csv(target_csv, mode="w", index=False)

    def get_followers_count(self, user_id):

        api = self.api

        userInfo = api.get_user(user_id=user_id)
        res = userInfo.followers_count

        # technical avoidant time because of Twitter Followers count only one request per one sec.
        sleep(1)

        return res

if __name__ == '__main__':

    # ACM = AnalyzeCircleMs()
    # ACM.make_csv_all_id()
    # ACM.make_csv_all_circle_info()

    MCT = AnalyzeTwitter()
    MCT.get_all_followers_count()

    #AP = AnalyzePixiv()
    #AP.get_all_favors_count()


