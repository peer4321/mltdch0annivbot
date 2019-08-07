# -*- coding: utf-8 -*-

from datetime import date, timedelta, datetime
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.font_manager import FontProperties
from matplotlib.ticker import AutoMinorLocator
matplotlib.use('Agg')

def plot(figname, title, records, fname='./NotoSansTC-Regular.otf', interval=None, maxticks=None):

    x = [datetime.strptime(rec[0], '%Y-%m-%d %H:%M:%S') for rec in records]
    ranks = [(1, 0), (2, 1), (3, 2), (12, 3), (13, 4), (52, 5), (53, 6)]
    y = {}
    for r, idx in ranks:
        y[r] = [int(rec[1][idx]) for rec in records]

    fig = plt.figure(figsize=(8, 5))
    ax = fig.add_subplot(1, 1, 1)
    fp = FontProperties(fname=fname)
    fptitle = FontProperties(fname=fname, size=16)
    cmap = lambda i: ['#6495cf', '#fed552', '#ea5b76', '#afa690', '#788bc5', '#d7a96b', '#454341'][i] if i < 7 else plt.get_cmap('tab10')(i)
    ls = lambda i: ':' if i == 2 or i == 4 or i == 6 else '-'
    lw = lambda i: 2 if i == 4 or i == 6 else 2

    for r, idx in ranks:
        ax.plot(x, y[r], ls=ls(idx), lw=lw(idx), color=cmap(idx), label='%d位'%r)

    locator = mdates.AutoDateLocator(minticks=6, maxticks=20 if not maxticks else maxticks)
    formatter = mdates.ConciseDateFormatter(locator)
    ax.xaxis.set(
        major_locator=locator,
        major_formatter=formatter
    )
    if interval is not None:
        ax.xaxis.set_minor_locator(mdates.HourLocator(0 if interval is 0 else list(range(0, 24, interval))))
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
    ax.set_title(title, fontproperties=fptitle)
    ax.text(1, 1.1, '更新: %s'%(x[-1].strftime('%Y-%m-%d %H:%M:%S')), color='dimgray', ha='center', transform=ax.transAxes, fontproperties=fp, size=8)
    ax.text(1, -0.25, 'plurk: mltdch0annivbot', color='gray', ha='center', size=7, transform=ax.transAxes)
    fig.autofmt_xdate()
    plt.savefig(figname)
    
    return True

