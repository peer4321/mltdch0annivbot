# -*- coding: utf-8 -*-

if __name__ == '__main__':
    import sys
    from bot import bot
    from journal import journal
    from figday import figday
    from figall import figall
    from datetime import datetime

    private, post = len(sys.argv) > 1, True
    if private and 'local' == sys.argv[1]: post = False
    bot(private=private, post=post)
    
    now = datetime.today()
    mm = int(now.strftime('%M'))
    hh = int(now.strftime('%H'))
    
    if hh % 6 == 0 and mm < 30:
        journal()
        figall(private=private, post=post)
        if hh == 0: figday(private=private, post=post)

