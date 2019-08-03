# -*- coding: utf-8 -*-

from journal import journal
from figall import figall
from figday import figday
from datetime import datetime

journal()
if int(datetime.today().strftime('%H')) == 0: figday()
figall()

