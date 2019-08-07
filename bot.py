# -*- coding: utf-8 -*-

def get_msg():
    import json, urllib.request, os, sys, time
    
    os.chdir(sys.path[0])
    os.makedirs('./logs', exist_ok=True)
    os.makedirs('./json', exist_ok=True)
    
    _url = 'https://prj.gamer.com.tw/2019/theaterdays/ajax/rank.php?page='
    headers = { 'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' }
    
    def get_ranks(url):
        req = urllib.request.Request(url, None, headers)
        time.sleep(0.1)
        with urllib.request.urlopen(req) as res:
            return json.loads(res.read().decode('utf-8'))['data']['rank']
    
    data = []
    for url in [_url+str(i) for i in range(1, 6)]: data.extend(get_ranks(url))
    
    ranks = [1, 2, 3, 12, 13, 52, 53]
    ids = [data[r-1]['username'] for r in ranks]
    pts = [int(data[r-1]['count']) for r in ranks]
    
    index = 0
    try: index = max([int(x.split('.')[0]) for x in os.listdir('./logs')])+1
    except ValueError: pass
    p_index = index-1
    pp_index = index-48
    has_24 = os.path.exists('./logs/%d.txt' % pp_index)
    has_30 = os.path.exists('./logs/%d.txt' % p_index)
    
    if has_24:
        with open('./logs/%d.txt' % pp_index, 'r') as f:
            pts_24 = list(map(int, f.readline().strip().split()))
        delta_24 = [pts[i] - pts_24[i] for i in range(len(pts))]

    if has_30:
        with open('./logs/%d.txt' % p_index, 'r') as f:
            pts_30 = list(map(int, f.readline().strip().split()))
        delta_30 = [pts[i] - pts_30[i] for i in range(len(pts))]
    
    req = urllib.request.Request('https://prj.gamer.com.tw/2019/theaterdays/', None, headers)
    with urllib.request.urlopen(req) as res:
        uptime = res.read().decode('utf-8').split('last-upd')[1].split('<span>')[1].split('</span>')[0]
    
    with open('./json/%d.json' % index, 'w') as f:
        json.dump({'uptime': uptime, 'data': data}, f)
    
    with open('./logs/%d.txt' % index, 'w') as f:
        for pt in pts: f.write(str(pt)+' ')
        f.write('\n')
        f.write('%s\n' % uptime)
    
    msg = '"劇場時光"宣傳製作人應援計畫\n'
    msg = msg + '更新時間: %s\n' % uptime
    loops = [('金賞', [0,1]), ('銀賞', [2,3]), ('銅賞', [4,5]), ('殘念', [6])]
    for prize, r in loops:
        for i in r:
            msg = msg + '%s %d位: %s | %d次' % (prize, ranks[i], ids[i], pts[i])
            if has_30: msg = msg + ' (+%d' % delta_30[i]
            if has_24: msg = msg + '/%d' % delta_24[i]
            msg = msg + ')\n'
    msg = msg + '[emo1]\n'
    return msg


def bot(post=True, private=False, retry=5):
    from plurk import add_plurk
    msg = get_msg()
    if not post: return
    res = add_plurk(msg, private=private)
    if not res:
        with open('./log.txt', 'a') as f: f.write('Failed to add plurk %s\n'%date.today().strftime('%Y-%m-%d %H:%M:%S'))
        return
    with open('./log.txt', 'a') as f: f.write('%s\n'%str(res))


if __name__ == '__main__':
    import sys
    bot(private=(len(sys.argv) > 1))

