# Please use python 3 to run this code. 


import threading, time, random

BARBERS = 0
barber_list = []
customer_in_chair = {}
barber_condition = {}
ALL_CUSTOMERS = []
waiting_room_size = 15
waiting_room = []
waiting_room_lock = threading.Lock()
shop_closed = threading.Event()
new_customer_for = {}

def shop_closing(closing_time):
   time.sleep(closing_time)
   # sets event flag to true to tell everyone that the shop is closed
   shop_closed.set()



class Barber(threading.Thread):
   def run(self):
      barber_condition[self.name].acquire()
      
      while not shop_closed.is_set():
         if len(waiting_room) == 0:
            # waiting room empty, go to sleep
            print('No one in waiting room,', self.name, 'sleeping...')
            barber_condition[self.name].wait()
            # customer has woken barber
            print(new_customer_for[self.name].name, 'enters, wakes', self.name)
            customer = new_customer_for[self.name]
         
         else:
            # waiting room has at least one customer, so go get
            # them from the waiting room. 
            waiting_room_lock.acquire()
            customer = waiting_room.pop(0)
            waiting_room_lock.release()
            print(self.name, 'calls new customer')

         customer_in_chair[self.name].set()
         # begin cutting the customer's hair
         cutting = threading.Thread(target = customer.trim(self.name))
         cutting.start()
         # barber waits for cut to be finished
         cutting.join()
         # cut is complete, customer leaves
         customer_in_chair[self.name].clear()

      barber_condition[self.name].release()


class Customer(threading.Thread):

   def run(self):
      if len(waiting_room) == 0:
         # no one in the waiting room, check each barber's chair
         i = 0
         while i < len(barber_list):
            b = barber_list[i]

            if customer_in_chair[b.name].is_set():
               # someone in barbers chair, so check the next one
               i += 1
               continue

            else:
               # no one in chair and no one in waiting room
               # wake the barber and sit in chair
               new_customer_for[b.name] = self
               barber_condition[b.name].acquire()
               barber_condition[b.name].notify()
               barber_condition[b.name].release()
               break

            i += 1

         # all of the barbers' chairs are full, so go 
         # to the waiting room. 
         if i == len(barber_list):
            waiting_room_lock.acquire()
            waiting_room.append(self)
            waiting_room_lock.release()
            print(self.name, 'in waiting room')
            print(len(waiting_room), 'customer(s) waiting')

      elif len(waiting_room) > 0 and len(waiting_room) < waiting_room_size:
         # people already in the waiting room, so wait with them
         waiting_room_lock.acquire()
         waiting_room.append(self)
         waiting_room_lock.release()
         print(self.name, 'in waiting room')
         print(len(waiting_room), 'customer(s) waiting')

      elif len(waiting_room) == waiting_room_size:
         # waiting room is full, so the new customer is turned away
         print('Waiting room full!!', self.name, 'leaving...')

   def trim(self, barb_name):
      print(self.name, 'getting a trim from', barb_name)
      # sleep to simulate hair being cut
      time.sleep(5 * random.random())
      # trim is finished
      print(barb_name, 'finished', self.name + '\'s trim!')



def main():
   # user input to decide how long the shop will stay open for,
   # and how many barbers there will be in the shop. 
   closing = int(input('How long should the shop stay open for: '))
   BARBERS = int(input('How many barbers: '))
   print('\n----- BARBER SHOP OPEN -----\n')
   
   # counter thread to tell everyone when the shop is closed. 
   shop_thread = threading.Thread(target = shop_closing, args = (closing,))
   shop_thread.start()

   # make instances for all the barbers. 
   for i in range(BARBERS):
      barber_name = 'Barber ' + str(i)
      barber_list.append(Barber(name = barber_name, daemon = True))
   
   for b in barber_list:
      # adding the seperate conditions and events for each of the
      # barbers, that will be changed by customers and by the 
      # barbers themselves. 
      customer_in_chair[b.name] = threading.Event()
      barber_condition[b.name] = threading.Condition()
      new_customer_for[b.name] = None

   for b in barber_list:
      # starts all the barber threads
      b.start()

   i = 0
   while not shop_closed.is_set():
      # create customer threads until the shop closes
      time.sleep(1 * random.random())
      cust_name = 'Customer ' + str(i)
      c = Customer(name = cust_name)
      ALL_CUSTOMERS.append(c)
      c.start()
      i += 1

   for cust in ALL_CUSTOMERS:
      # wait for all customer threads to finish trimming
      cust.join()

   for b in barber_list:
      # wait for all barber threads to finish 
      b.join()

   print('\n----- BARBER SHOP CLOSED -----\n')

if __name__ == '__main__':
   main()