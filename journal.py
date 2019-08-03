# -*- coding: utf-8 -*-

def journal():
    import os
    logs = sorted([int(x.split('.')[0]) for x in os.listdir('./logs/')])
    with open('./journal.txt', 'w') as fout:
        for log in logs:
            with open('./logs/%d.txt' % log) as fin:
                pts = fin.readline().strip()
                ts = fin.readline().strip()
            fout.write('%s|%s\n' % (ts, pts))

if __name__ == '__main__':
    journal()

