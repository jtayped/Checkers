import threading

threadResults = {}

def function(value):
    threadResults[value] = value*2

threads = []
for i in range(3):
    thread = threading.Thread(target=function, args=(i,))
    threads.append(thread)
    thread.start()

for t in threads:
    t.join()

print(threadResults)