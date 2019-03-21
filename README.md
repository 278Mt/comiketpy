# comiketpy

Comic Market is one of the most famous event in Japan. (Underconstruction)

## register

If you use this program, you have to sign up Twitter API Developper and Circle.ms account.

## CAUTION!!

1. Twitter official says no one allows to scrape her contents without permission.
2. Even though you use the tool, me thinking about loading to servers supported by Twitter and Circle.ms, it takes you ONE DAY to compliete calibration relating Twitter and Circle.ms data. If you scrape faster than the program and refurblish, YOU HAVE TO THINK ABOUT LOADING TO SERVERS SUPPORTED BY TWITTER, CIRCLE.MS AND SO ON (I EXPLICITLY DECLARE HERE). In the concrete, you just write program to scrape one page per one second, et cetra.

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
