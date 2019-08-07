# -*- coding: utf-8 -*-

def figall(post=True, private=False):
    import os, sys
    from datetime import date, timedelta, datetime
    os.chdir(sys.path[0])
    figdir = './figures'
    figname = figdir + '/figall.png'
    os.makedirs(figdir, exist_ok=True)
    
    records = []
    with open('./journal.txt', 'r') as f:
        for line in f.readlines():
            ts, pts = line.strip().split('|')
            records.append((ts, pts.split()))
    
    interval, date = 6, int(datetime.today().strftime('%d'))
    if date >= 11: interval = 12
    if date >= 16: interval = 24
    from plot import plot
    if not plot(figname, '"劇場時光"宣傳製作人應援計畫　排名走勢', records, interval=interval):
        with open('./log.txt', 'a') as f: f.write('\n[Failed]\nFailed to plot (all time) %s\n'%date.today().strftime('%Y-%m-%d %H:%M:%S'))
        return
    
    if not post: return
    
    from plurk import url_img, add_plurk
    url = url_img(figname)
    if not url:
        with open('./log.txt', 'a') as f: f.write('\n[Failed]\nFailed to upload image %s\n'%date.today().strftime('%Y-%m-%d %H:%M:%S'))
        return
    msg = '"劇場時光"宣傳製作人應援計畫\n排名走勢: %s\n%s\n' % (records[-1][0], url)
    res = add_plurk(msg, private=private)
    if not res:
        with open('./log.txt', 'a') as f: f.write('\n[Failed]\nFailed to add plurk %s\n'%date.today().strftime('%Y-%m-%d %H:%M:%S'))
        return
    with open('./log.txt', 'a') as f: f.write('\n[Success]\n%s\n'%str(res))

if __name__ == '__main__':
    import sys
    private, post = len(sys.argv) > 1, True
    if private and 'local' == sys.argv[1]: post = False
    figall(private=private, post=post)

