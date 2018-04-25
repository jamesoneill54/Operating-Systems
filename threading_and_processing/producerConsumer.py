import threading
import random
import time

queue = []
queue_size = 5
condition = threading.Condition()

class producerThread(threading.Thread):
   def run(self):
      while True:
         condition.acquire()
         if len(queue) == queue_size:
            print('Queue full, producer waiting')
            condition.wait()
         num = random.randint(1, 5)
         queue.append(num)
         print('Produced', num, '- queue is', queue)
         condition.notify()
         condition.release()
         time.sleep(random.random())

class consumerThread(threading.Thread):
   def run(self):
      while True:
         condition.acquire()
         if not queue:
            print('Nothing in queue, consumer waiting')
            condition.wait()
            print('Consuming, om nom nom...')
         num = queue.pop(0)
         print('Consumed', num)
         condition.notify()
         condition.release()
         time.sleep(random.random())

producerThread().start()
consumerThread().start()