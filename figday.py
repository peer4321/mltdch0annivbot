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
    
    import matplotlib
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from matplotlib.font_manager import FontProperties
    from matplotlib.ticker import AutoMinorLocator
    matplotlib.use('Agg')
    
    x = [datetime.strptime(rec[0], '%Y-%m-%d %H:%M:%S') for rec in records]
    ranks = [(1, 0), (2, 1), (3, 2), (12, 3), (13, 4), (52, 5), (53, 6)]
    y = {}
    for r, idx in ranks:
        y[r] = [int(rec[1][idx]) for rec in records]
    
    fig = plt.figure(figsize=(8, 5))
    ax = fig.add_subplot(1, 1, 1)
    fname = './NotoSansTC-Regular.otf'
    fp = FontProperties(fname=fname)
    fptitle = FontProperties(fname=fname, size=16)
    cmap = lambda i: ['#6495cf', '#fed552', '#ea5b76', '#afa690', '#788bc5', '#d7a96b', '#454341'][i] if i < 7 else plt.get_cmap('tab10')(i)
    ls = lambda i: ':' if i == 2 or i == 4 or i == 6 else '-'
    lw = lambda i: 2 if i == 4 or i == 6 else 2
    ms = lambda i: 0 if i == 4 or i == 6 else 0
    
    for r, idx in ranks:
        ax.plot(x, y[r], ls=ls(idx), lw=lw(idx), marker='s', ms=ms(idx), color=cmap(idx), label='%d位'%r)
    
    locator = mdates.AutoDateLocator(minticks=6, maxticks=12)
    formatter = mdates.ConciseDateFormatter(locator)
    ax.xaxis.set(
        major_locator=locator,
        major_formatter=formatter,
        minor_locator=mdates.HourLocator()
    )
    ax.yaxis.set(
        minor_locator=AutoMinorLocator()
    )
    ax.set_ylim(ymin=0)
    ax.grid(which='both')
    ax.grid(which='minor', alpha=0.3)
    ax2 = ax.twinx()
    ax2.set_ylim(ax.get_ylim())
    ax2.set_yticks([y[r][-1] for r, idx in ranks])
    ax2.set_yticklabels([y[r][-1] for r, idx in ranks])
    
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])
    handles, labels = ax.get_legend_handles_labels()
    def flip(items, ncol):
        import itertools
        return itertools.chain(*[items[i::ncol] for i in range(ncol)])
    ax.legend(flip(handles, 4), flip(labels, 4), bbox_to_anchor=(0.5, -0.12), loc='upper center', ncol=4, fancybox=True, shadow=True, prop=fp)
    ax.set_title('%s 單日走勢'%_date_1, fontproperties=fptitle)
    ax.text(1, 1.1, '更新: %s'%(x[-1].strftime('%Y-%m-%d %H:%M:%S')), color='dimgray', ha='center', transform=ax.transAxes, fontproperties=fp, size=8)
    ax.text(1, -0.25, 'plurk: mltdch0annivbot', color='gray', ha='center', size=7, transform=ax.transAxes)
    fig.autofmt_xdate()
    plt.savefig(figname)
    
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

