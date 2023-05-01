# author: xiaomu18

from threading import Thread

header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}

def threads(target, thread_num:int=None, wait=False, args=None):

    mode = None

    if not thread_num:
        if isinstance(args, list):
            thread_num = len(args)
            mode = 1
        else:
            raise "if you don't use thread num to start threads, the args must be a list of tuple, every threads use a one of the list"
    else:
        mode = 0
        if not isinstance(args, tuple):
            raise "if you use thread num to start threads, the args must be a tuple"

    print("[ INFO ] Reptile Tools > begin to start", thread_num, "threads.")
        
    ts = []
    for i in range(0, thread_num):
        if mode:
            t = Thread(target=target, args=args[i])
        else:
            t = Thread(target=target, args=args)
        t.setDaemon(True)

        ts.append(t)
    
    del t

    for t in ts: t.start()
    
    print("[ INFO ] Reptile Tools >", len(args), "threads started done.")

    if wait:
        for t in ts: t.join()

    return ts

