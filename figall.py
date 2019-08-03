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
    import matplotlib
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from matplotlib.font_manager import FontProperties
    from matplotlib.ticker import AutoMinorLocator
    matplotlib.use('Agg')
    
    x = [datetime.strptime(rec[0], '%Y-%m-%d %H:%M:%S') for rec in records]
    ranks = [(1, 0), (2, 1), (3, 2), (12, 3), (52, 5)]
    y = {}
    for r, idx in ranks:
        y[r] = [int(rec[1][idx]) for rec in records]
    
    fig = plt.figure(figsize=(8, 5))
    ax = fig.add_subplot(1, 1, 1)
    fname = './NotoSansTC-Regular.otf'
    fp = FontProperties(fname=fname)
    fptitle = FontProperties(fname=fname, size=16)
    cmap = plt.get_cmap('tab10')

    for r, idx in ranks:
        ax.plot(x, y[r], ls='-', lw=2, color=cmap(idx), label='%d位'%r)
    
    locator = mdates.AutoDateLocator(minticks=6, maxticks=12)
    formatter = mdates.ConciseDateFormatter(locator)
    ax.xaxis.set(
        major_locator=locator,
        major_formatter=formatter,
        minor_locator=mdates.HourLocator((0, 6, 12, 18))
    )
    ax.yaxis.set(
        minor_locator=AutoMinorLocator()
    )
    ax.grid(which='both')
    ax.grid(which='minor', alpha=0.3)
    
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])
    ax.legend(loc='upper center', bbox_to_anchor=(0.45, -0.15), ncol=5, fancybox=True, shadow=True, prop=fp)
    ax.set_title('"劇場時光"宣傳製作人應援計畫　排名走勢', fontproperties=fptitle)
    ax.text(1, 1.1, '更新: %s'%(x[-1].strftime('%Y-%m-%d %H:%M:%S')), color='dimgray', ha='center', transform=ax.transAxes, fontproperties=fp, size=8)
    ax.text(1, -0.25, 'plurk: mltdch0annivbot', color='gray', ha='center', size=7, transform=ax.transAxes)
    plt.grid(True)
    fig.autofmt_xdate()
    plt.savefig(figname)
    
    if not post: return
    
    def post_img(private=False, retry=5):
        from plurk_oauth import PlurkAPI
        plurk = PlurkAPI.fromfile('./API.keys')
        res = None
        for i in range(retry):
            try: res = plurk.callAPI('/APP/Timeline/uploadPicture', fpath=figname)
            except: pass
            else: break
        if not res: return None
        options = {'content': '"劇場時光"宣傳製作人應援計畫\n排名走勢圖\n%s\n更新時間: %s' % (res['full'], x[-1].strftime('%Y-%m-%d %H:%M:%S')), 'qualifier': ':'}
        if private: options['limited_to'] = '[]'
        for i in range(retry):
            try: return plurk.callAPI('/APP/Timeline/plurkAdd', options=options)
            except: pass
        return None
    
    retry = 5
    for i in range(retry):
        res = post_img(private=private, retry=retry)
        if res:
            print('Success')
            with open('./log.txt', 'a') as f: f.write('%s\n'%str(res))
            break
        if i == retry:
            print('Failed')
            msg = 'Failed after %d tries: %s' % (retry, str(date.today()))
            with open('./log.txt', 'a') as f: f.write('%s\n'%str(msg))
            break

if __name__ == '__main__':
    import sys
    private, post = len(sys.argv) > 1, True
    if private and 'local' == sys.argv[1]: post = False
    figall(private=private, post=post)

