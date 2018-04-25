import threading, time, random

BARBERS = 3
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
   shop_closed.set()



class Barber(threading.Thread):
   def run(self):
      barber_condition[self.name].acquire()
      
      while not shop_closed.is_set():
         if len(waiting_room) == 0:
            print('No one in waiting room,', self.name, 'sleeping...')
            barber_condition[self.name].wait()
            print(new_customer_for[self.name].name, 'enters, wakes', self.name)
            customer = new_customer_for[self.name]
         
         else:
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
         # no one in the waiting room, check each barber chair
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
      time.sleep(5 * random.random())
      # notify the barber that the trim is finished
      print(barb_name, 'finished', self.name + '\'s trim!')



def main():
   closing = int(input('How long should the shop stay open for: '))
   BARBERS = int(input('How many barbers: '))
   print('\n----- BARBER SHOP OPEN -----\n')
   
   shop_thread = threading.Thread(target = shop_closing, args = (closing,))
   shop_thread.start()


   for i in range(BARBERS):
      barber_name = 'Barber ' + str(i)
      barber_list.append(Barber(name = barber_name, daemon = True))
   
   for b in barber_list:
      customer_in_chair[b.name] = threading.Event()
      barber_condition[b.name] = threading.Condition()
      new_customer_for[b.name] = None

   for b in barber_list:
      b.start()

   i = 0
   while not shop_closed.is_set():
      time.sleep(1 * random.random())
      cust_name = 'Customer ' + str(i)
      c = Customer(name = cust_name)
      ALL_CUSTOMERS.append(c)
      c.start()
      i += 1

   for cust in ALL_CUSTOMERS:
      cust.join()

   for b in barber_list:
      b.join()

   print('\n----- BARBER SHOP CLOSED -----\n')

if __name__ == '__main__':
   main()







