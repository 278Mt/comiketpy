# comiketpy

Comic Market (日本語: コミックマーケット), every one calls Comiket (日本語: コミケ) is one of the most famous event in Japan. Comiket's official page is [HERE](https://www.comiket.co.jp/).
About thirty thousand of circles and half an hundred of visitors participate in Tokyo Big Sight, Ariake Tokyo Japan, summer (about middle August) and winter (about end Decembre). There are so crowded by so many hot-blooded otakus crazy about manga, anime, computer game, and so on.
I think it will be convinient if I get approximiate waiting time to purchase objects I want, so I made the program.

## register

If you use this program, you have to sign up Twitter API Developper and Circle.ms account.

## CAUTION!!

1. Twitter official says no one allows to scrape her contents without permission. The program follows the rule, but if you remake sth from the program, you have to follow [her rule](https://help.twitter.com/en/rules-and-policies/twitter-rules).
2. Even though you use the tool, me thinking about loading to servers supported by Twitter and Circle.ms, it takes you ONE DAY to complete calibration relating Twitter and Circle.ms data. If you scrape faster than the program and refurblish, YOU HAVE TO THINK ABOUT LOADING TO SERVERS SUPPORTED BY TWITTER, CIRCLE.MS AND SO ON (I EXPLICITLY DECLARE HERE). In the concrete, you just write program to scrape one page per one second, et cetra.

## copyright
You can use this program on your terminal: e.g. your laptop, personal computer et cetra. However, only do I have the copyright of this program [comiketpy](http://github.com/278Mt/comiketpy). All rights reserved. If you upload, distribute, and share some website a program of your downloading here or refurblishing this program and so on, you must get permission of mine.

## spcification

```python
import comiketpy as cmp

cmp.init_keys()                # register Twitter API keys and Circle.ms keys on json file

cmp.make_csv_all_id()          # get all IDs of participant in Comiket
                               # If you use it, you have to sign up Circle.ms account
                               # about: https://portal.circle.ms/Account/Register1

cmp.make_csv_all_circle_info() # get all information of participant in Comiket

cmp.get_all_followers_count()  # get all followers count of participants in Comiket
                               # If you use it, you have to sign up Twitter API Developper
                               # about: https://developer.twitter.com/en/apply-for-access

# underconstruction....
```
