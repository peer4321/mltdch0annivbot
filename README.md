# MLTD.ch Campaign Scoreboard Plurk Bot

This is a [Plurk](https://www.plurk.com) bot to monitor the scoreboard of the [pre-release campaign](https://prj.gamer.com.tw/2019/theaterdays/) of THE IDOLM@STER MILLION LIVE! THEATER DAYS! (TC ver.) held by [Bahamut](https://www.gamers.com.tw).

## Requirements ##

* Access Tokens received from [Plurk API](https://www.plurk.com/API)
* Python 3
* `pip install matplotlib 'plurk-oauth==0.9.2'`
* (Optional) Fonts supporting Unicode, e.g. [Noto Sans TC](https://fonts.google.com/specimen/Noto+Sans+TC)

## Execution ##

* `$ python main.py`: Normal execution, sends text message, also figures at specific time.
* `$ python main.py test`: Sends private plurks.
* `$ python main.py local`: Excecute without sending plurks.
* Other `.py` files with `main` have the same usage.
* You can use `crontab` to schedule the updates.
