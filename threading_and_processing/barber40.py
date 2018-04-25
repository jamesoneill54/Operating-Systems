import threading, time, random

BARBERS = 1
CUSTOMERS = 10
ALL_CUSTOMERS = []
waiting_room = []
barber_condition = threading.Condition()
customer_in_chair = threading.Event()
shop_closed = threading.Event()

def shop_closing(closing_time):
   time.sleep(closing_time)
   shop_closed.set()



class Barber(threading.Thread):
   def run(self):
      barber_condition.acquire()
      
      while not shop_closed.is_set():
         if len(waiting_room) == 0:
            print('No one in waiting room, sleeping...\n')
            barber_condition.wait()
            print('Customer enters, wakes barber')
            customer = waiting_room.pop(0)
         
         else:
            customer = waiting_room.pop(0)
            print('Barber calls new customer')

         customer_in_chair.set()
         # begin cutting the customer's hair
         cutting = threading.Thread(target = customer.trim())
         cutting.start()
         # barber waits for cut to be finished
         cutting.join()
         # cut is complete, customer leaves
         customer_in_chair.clear()

      barber_condition.release()


class Customer(threading.Thread):

   def run(self):
      if len(waiting_room) == 0:
         # no one in the waiting room, check barber chair
         if customer_in_chair.is_set():
            # someone in barbers chair, so wait in waiting room   
            waiting_room.append(self)
            print('New customer in waiting room')
            print(len(waiting_room), 'customer(s) waiting')

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
         print(len(waiting_room), 'customer(s) waiting')

   def trim(self):
      print('Customer', self.name, 'getting a trim...')
      time.sleep(2 * random.random())
      # notify the barber that the trim is finished
      print('Finished', self.name + '\'s trim!\n')



def main():
   closing = int(input('How long should the shop stay open for: '))
   print('\n----- BARBER SHOP OPEN -----\n')
   
   shop_thread = threading.Thread(target = shop_closing, args = (closing,))
   shop_thread.start()

   barber = Barber()
   barber.start()
   while not shop_closed.is_set():
      time.sleep(2 * random.random())
      c = Customer()
      ALL_CUSTOMERS.append(c)
      c.start()

   for cust in ALL_CUSTOMERS:
      cust.join()

   barber.join()
   print('\n----- BARBER SHOP CLOSED -----\n')

if __name__ == '__main__':
   main()







