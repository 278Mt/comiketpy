# comiketpy_public

Comic Market is one of the most famous event in Japan. (Underconstruction)

## register

If you use this program, you have to sign up Twitter API Developper and Circle.ms account.

## CAUTION ABOUT SCRAPING IN TWITTER!!

Twitter official says no one allows to scrape her contents without permission.

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
