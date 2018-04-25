import threading, random, time

condition = threading.Condition()
can_write = True
words = [
'hello', 'bean', 'family', 'fork', 'the', 'lightbulb', 
'attempt', 'cri', 'rocket', 'cloud', 'owl', 'jame', 'peeb', 
'sprout', 'comfy', 'puff', 'poot', 'boof', 'mlem', 'blep', 'bep'
]

class readerThread(threading.Thread):
   def run(self):
      can_write = False
      condition.acquire()
      with open('textfile.txt', 'r') as f:
         from_file = f.read()
      print('This just in:\n' + from_file + '\n' + '------- END -------')
      can_write = True
      condition.notify()
      condition.release()


class writerThread(threading.Thread):
   def run(self):
      for i in range(100):
         condition.acquire()
         if not can_write:
            condition.wait()
         with open('textfile.txt', 'a') as f:
            index = random.randint(0, len(words) - 1)
            f.write(words[index] + ' ')
         time.sleep(0.05)
         condition.release()


with open('textfile.txt', 'w') as f:
   f.write('')

writerThread().start()
time.sleep(random.random())

for i in range(5):
   readerThread().start()
   time.sleep(2 * random.random())
