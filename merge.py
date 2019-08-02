# -*- coding: utf-8 -*-

import os, sys
from datetime import date, timedelta, datetime

_date = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')
records = []
logs = sorted([int(x.split('.')[0]) for x in os.listdir('./logs/')])
with open('./journal.txt', 'w') as fout:
    for log in logs:
        with open('./logs/%d.txt' % log) as fin:
            pts = fin.readline().strip()
            ts = fin.readline().strip()
        fout.write('%s|%s\n' % (ts, pts))
        if _date in ts:
            records.append((ts, pts.split()))

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.font_manager import FontProperties

# prepare plot data
x = [datetime.strptime(rec[0].split()[1], '%H:%M:%S') for rec in records]
ranks = [(1, 0), (2, 1), (3, 2), (12, 3), (52, 5)]
y = {}
for r, idx in ranks:
    y[r] = [int(rec[1][idx]) for rec in records]

# figure initialize
fig = plt.figure(figsize=(8,5))
ax = fig.add_subplot(1, 1, 1)

fname = 'C:\WINDOWS\Fonts\msjh.ttc'
fname = './NotoSansTC-Regular.otf'

fp = FontProperties(fname=fname)
fptitle = FontProperties(fname=fname, size=16)

# plot
cmap = plt.get_cmap('tab10')
for r, idx in ranks:
    ax.plot(x, y[r], linestyle='-', lw=2, marker='s', ms=4, color=cmap(idx), label='%d位'%r)

ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax.set_xlim([datetime.strptime('0:00:00', '%H:%M:%S'), datetime.strptime('0:00:00', '%H:%M:%S')+timedelta(days=1)])

# shrink plot area
box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])

# add legend
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=5, fancybox=True, shadow=True, prop=fp)
ax.set_title('%s 走勢圖' % _date, fontproperties=fptitle)
ax.text(1, -0.25, 'plurk: mltdch0annivbot', color='gray', ha='center', size=7, transform=ax.transAxes)

plt.grid(True)
fig.autofmt_xdate()
plt.savefig('figure.png')

def post_img(private=False):
    from plurk_oauth import PlurkAPI
    plurk = PlurkAPI.fromfile('./API.keys')
    res = plurk.callAPI('/APP/Timeline/uploadPicture', fpath='./figure.png')
    if not res: return None
    options = {'content': '"劇場時光"宣傳製作人應援計畫\n%s 走勢圖\n%s' % (_date, res['full']), 'qualifier': ':'}
    if private: options['limited_to'] = '[]'
    return plurk.callAPI('/APP/Timeline/plurkAdd', options=options)

i, res = 0, None
retry = 5
while i < retry:
    res = post_img(len(sys.argv) > 1)
    if res:
        print('Success')
        with open('./log.txt', 'a') as f: f.write('%s\n' % str(res))
        break
    i += 1
    if i == retry:
        print('Failed')
        msg = 'Failed after %d tries: %s' % (retry, str(date.today()))
        with open('./log.txt', 'a') as f: f.write('%s\n' % msg)
        break

