import threading, time, random

BARBERS = 1
CUSTOMERS = 10
ALL_CUSTOMERS = []
waiting_room = []
barber_condition = threading.Condition()
customer_in_chair = threading.Event()
shop_closed = threading.Event()

def wait():
   time.sleep(5 * random.random())

class Barber(threading.Thread):
   def run(self):
      barber_condition.acquire()
      
      while not shop_closed.is_set():
         if len(waiting_room) == 0:
            print('No one in waiting room, sleeping...')
            barber_condition.wait()
            print('Customer enters, wakes barber')
            customer = waiting_room.pop(0)
         
         else:
            customer = waiting_room.pop(0)
            print('Barber calls new customer')

         customer_in_chair.set()
         # begin cutting the customer's hair
         customer.trim()
         # barber waits for cut to be finished
         barber_condition.wait()
         # cut is complete, customer notifies barber
         # customer leaves
         customer_in_chair.clear()

      print('Barber finished for the day!')
      barber_condition.release()


class Customer(threading.Thread):

   def run(self):
      if len(waiting_room) == 0:
         # no one in the waiting room, check barber chair
         if customer_in_chair.is_set():
            # someone in barbers chair, so wait in waiting room   
            waiting_room.append(self)
            print('New customer in waiting room')
            print('waiting room:', waiting_room)

         else:
            # no one in chair and no one in waiting room
            # wake the barber and sit in chair
            waiting_room.append(self)
            barber_condition.acquire()
            barber_condition.notify()
            barber_condition.release()

      else:
         # people already in the waiting room, so wait with them
         waiting_room.append(self)
         print('New customer in waiting room')
         print('waiting room:', waiting_room)

   def trim(self):
      barber_condition.acquire()
      print('Customer', self.name, 'getting a trim...')
      time.sleep(2 * random.random())
      # notify the barber that the trim is finished
      print('Finished trim!')
      barber_condition.notify()
      barber_condition.release()



def main():
   print('\n----- BARBER SHOP OPEN -----\n')
   
   barber = Barber()
   barber.start()
   for i in range(CUSTOMERS):
      wait()
      c = Customer()
      ALL_CUSTOMERS.append(c)
      c.start()

   shop_closed.set()
   barber.join()
   print('\n----- BARBER SHOP CLOSED -----\n')
   print('waiting room:', waiting_room)

if __name__ == '__main__':
   main()







