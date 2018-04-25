import threading
import time

def sleeper(n):
   print('I will sleep for {} seconds'.format(n))
   time.sleep(n)

threads = []

t = threading.Thread(target = sleeper, args = (5,))
threads.append(t)

t = threading.Thread(target = sleeper, args = (2,))
threads.append(t)


for t in threads:
   t.start()

print('Hello')