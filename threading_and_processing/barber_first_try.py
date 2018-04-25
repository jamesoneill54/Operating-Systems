import time
import threading
import random

BARBERS = 1
CUSTOMERS = 5
waiting_room = []
condition = threading.Condition()
customer_in_chair = False
customer = None

class Barber(threading.Thread):
   def run(self):
      condition.acquire()
      while True:
         # begins by sleeping in the chair
         if not waiting_room:
            condition.wait()
            print('No one in waiting room, barber is sleeping')
         # get someone from the waiting room
         else:
            customer = waiting_room.pop(0)

         # tell the customer to begin trim
         customer_in_chair = True
         customer.trim()
         # wait for customer to finish trim
         condition.wait()
         customer_in_chair = False
      condition.release()

class Customer(threading.Thread):
   def run(self):
      condition.acquire()
      if not waiting_room:
         if customer_in_chair:
            waiting_room.append(self)
            condition.wait()
         else:
            customer = self
            condition.notify()

