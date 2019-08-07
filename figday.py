# -*- coding: utf-8 -*-

def figday(post=True, private=False):
    import os, sys
    from datetime import date, timedelta, datetime
    os.chdir(sys.path[0])
    figdir = './figures'
    figname = figdir + '/figday.png'
    os.makedirs(figdir, exist_ok=True)
    
    _date_1 = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    _date_2 = (date.today() - timedelta(days=2)).strftime('%Y-%m-%d')
    records = []
    with open('./journal.txt', 'r') as f:
        for line in f.readlines():
            if _date_2 in line:
                ts, pts = line.strip().split('|')
                records = [(ts, pts.split())]
            if _date_1 in line:
                ts, pts = line.strip().split('|')
                records.append((ts, pts.split()))
    
    from plot import plot
    if not plot(figname, '%s 單日走勢'%_date_1, records, interval=1, maxticks=12):
        with open('./log.txt', 'a') as f: f.write('Failed to plot (daily) %s\n'%date.today().strftime('%Y-%m-%d %H:%M:%S'))
        return
    
    if not post: return
    
    from plurk import url_img, add_plurk
    url = url_img(figname)
    if not url:
        with open('./log.txt', 'a') as f: f.write('Failed to upload image %s\n'%date.today().strftime('%Y-%m-%d %H:%M:%S'))
        return
    msg = '"劇場時光"宣傳製作人應援計畫\n%s 單日走勢\n%s' % (_date_1, url)
    res = add_plurk(msg, private=private)
    if not res:
        with open('./log.txt', 'a') as f: f.write('Failed to add plurk %s\n'%date.today().strftime('%Y-%m-%d %H:%M:%S'))
        return
    with open('./log.txt', 'a') as f: f.write('%s\n'%str(res))

if __name__ == '__main__':
    import sys
    private, post = len(sys.argv) > 1, True
    if private and 'local' == sys.argv[1]: post = False
    figday(private=private, post=post)

