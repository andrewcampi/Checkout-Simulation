
#Andrew Campi
#Simulation.py
#04/11/20
#Phase 1

"""
General Info:
    - Customer arrives at register at average rate of 1/lambda customers per minute.
        - Interval is random number between 1 and lambda.
    - Customer spends average of mu*(1/2) at register.
        - Interval is random number between 1 and mu*1
    - There are n registers.


Process:
    - Customer enters check-out line (queue).
    - When there is an idle cashier, customer is dequeued and matched with cashier. 
    - Cashier is now occupied.
    - Customer spends time with the paired cashier.
    - When customer is finished:
        - Customer is deleted from the simulation.
        - Cashier is now idle.
        - Cashier looks checks if queue is not empty and gets next customer.


Events:
    - " CustomerArrival " event:
        - Customer arrives at cashier registers area at random time.
        - If a cashier is free, customer is served immediately.
        - Else, customer joins single waiting queue.
        - Program should generate the next " CustomerArival " event.
        - If current customer arrives at time t, the next customer arrives at time 
          " t + random.randint(1,lamda) ", where lambda is specified maximum inter-arrival 
          time as int.
        - Keeps counter of total customers arrived.
        
    - " CashierServiceBegin " event:
        - Customer begins getting served by cashier.
        - Cashier is set to "busy".
        - Amount of time the customer spends at the cashier register is " random.randint(1,mu) "
          where mu is the specified maximum service time.
        - " CashierServiceEnd " event should be scheduled at start of this event.
        - Keeps counter of total waiting time.
        
    - " CashierServiceEnd " event:
        - Increment total number of customers served.
        - Cashier is now free.
        - Check to see if anyone is waiting in the queue.
        - If queue is not empty, dequeue and start service immediately.
        - Else, cashier is set to "idle".
    
    
Collected Statistics:
    - Average waiting time in the cashier queue   =    Total waiting time / total number of customers who recieved service
    - Total number of customers who completed service
    - Total number of customers wo are left in the cashier waiting queue (when simulation ends).
    - Total number of cashiers
    - Total Simulation time
    - Total number of customers who arrived at store.
    
"""
import random
from EventQueue import *
from CustomerQueue import *
from PickupQueue import *


def setup():
    print("Setting things up...")
    n = int(input("Enter number of cashiers: "))
    m = int(input("Enter number of curb-side pickup helpers: "))
    l = int(input("Enter maximum customer inter-arrival time: "))
    mu = int(input("Enter maximum cashier service time: "))
    total_simulation_time = int(input("Enter total simulation time: "))
    
    return n, m, l, mu, total_simulation_time
    




def run(n, m, l, mu, total_simulation_time):
    print("Simualtion starts...")
    #init statistics
    wait_times = []
    pickup_wait_times = []
    average_wait_time = None
    average_pickup_wait_time = None
    total_customers_arrived = 0
    total_customers_served = 0
    total_pickup_customers_arrived = 0
    total_pickup_customers_served = 0
    total_number_cashiers = n
    total_number_pickup_helpers = m
    percent_chance_of_pickup = 10
    
    
    
    #Setup init events
    customer_queue = CustomerQueue()
    pickup_queue = PickupQueue()
    event_queue = EventQueue(total_simulation_time)
    
    cashiers = []        # Create cashiers list
    for x in range(n):   # Fill cashiers list with n cashiers (all are init "idle")
        cashiers.append("idle")
        
    pickup_helpers = []  # Create pickup helpers list
    for x in range(m):   # Fill pickup helpers list with m pickup helpers (all are init "idle")
        pickup_helpers.append("idle")
        

    
    current_time = 0
    total_time = total_simulation_time
    
    
    # Randomly add customer arrival events to event_queue
    while (current_time < total_time):
        time_to_next_customer = random.randint(1,l)
        next_customer_arrival_time = current_time + time_to_next_customer
        if (next_customer_arrival_time < total_time): #If next customer arrival during time of simulation.
            event_queue.insert("CustomerArrival", next_customer_arrival_time)
            current_time = next_customer_arrival_time
            total_customers_arrived += 1
            
        else:
            current_time = total_time
    
    
    
    
    
    #run the simulation for "total_time"
    current_time = 0
    while (event_queue.is_empty() == False) and (current_time < total_time):
        #next_event_time = event_queue.peek_next()
        #current_time += next_event_time
        
        
        while (len(event_queue.data[current_time]) > 0):       #while priority is not empty in event queue.
            current_event, event_time = event_queue.delete()   #Dequeue event from event queue.
            #current_time = event_time
            """CustomerArrival Event"""
            if (current_event == "CustomerArrival"):
                for x in range(len(cashiers)):                 #Make the cashiers work if customers are in line
                    if (cashiers[x] == "idle"):
                        if (customer_queue.is_empty() == False):       #if customer in line
                            this_customer = customer_queue.dequeue() #Dequeue customer from line
                            task_and_cashier_number = "CashierServiceBegin#" + str(x)
                            cashiers[x] = "busy"                                   # Cashier is now busy
                            event_queue.insert(task_and_cashier_number,event_time) # Begin Service
                            wait_times.append(event_time - this_customer)                                
                            
                idle_index = None
                for x in range(len(cashiers)):                 # look for idle cashier in cashier list
                    if (cashiers[x] == "idle"): 
                        idle_index = x
                if (idle_index != None):                                   # if an idle cashier is found
                    task_and_cashier_number = "CashierServiceBegin#" + str(idle_index)
                    cashiers[idle_index] = "busy"                          # Cashier is now busy
                    event_queue.insert(task_and_cashier_number,event_time) # Begin Service
                    wait_times.append(0)
                if (idle_index == None):                                   # all cashiers are busy (customer gets in line)
                    customer_queue.enqueue(event_time) # add the event time of the customer arriving to the customer queue
            
            
            """PickupArrival Event"""
            if (current_event == "PickupArrival"):
                for x in range(len(pickup_helpers)):                 #Make the pickup helpers work if customers are in line
                    if (pickup_helpers[x] == "idle"):
                        if (pickup_queue.is_empty() == False):       #if pickup customer in line
                            this_pickup_customer = pickup_queue.dequeue() #Dequeue pickup customer from line
                            task_and_pickup_helper_number = "PickupServiceBegin#" + str(x)
                            pickup_helpers[x] = "busy"                                   # pickup helper is now busy
                            event_queue.insert(task_and_pickup_helper_number,event_time) # Begin Service
                            pickup_wait_times.append(event_time - this_pickup_customer)                                
                            
                idle_index = None
                for x in range(len(pickup_helpers)):                 # look for idle pickup helper in pickup helper list
                    if (pickup_helpers[x] == "idle"): 
                        idle_index = x
                if (idle_index != None):                                   # if an idle pickup helper is found
                    task_and_pickup_helper_number = "PickupServiceBegin#" + str(idle_index)
                    pickup_helpers[idle_index] = "busy"                          # pickup helper is now busy
                    event_queue.insert(task_and_pickup_helper_number,event_time) # Begin Service
                    pickup_wait_times.append(0)
                if (idle_index == None):                                   # all pickup helpers are busy (customer gets in line)
                    pickup_queue.enqueue(event_time) # add the event time of the pickup customer arriving to the customer queue
    
            
            
            
            
            #find number in string
            pound_found = False
            pound_index = None
            for x in range(len(current_event)):
                if (current_event[x] == "#"):
                    pound_found = True
                    pound_index = x
            if pound_found:
                
                """CashierServiceBegin Event"""
                if (current_event[0:pound_index] == "CashierServiceBegin"):
                    cashier_number = current_event[pound_index+1:]
                    service_time = random.randint(1,mu)
                    task_and_cashier_number = "CashierServiceEnd#"+ str(cashier_number)
                    event_queue.insert(task_and_cashier_number, event_time + service_time)
                

                """CashierServiceEnd Event"""
                if (current_event[0:pound_index] == "CashierServiceEnd"):
                    cashier_number = current_event[pound_index+1:]
                    total_customers_served += 1
                    cashiers[int(cashier_number)] = "idle"
                    this_chance = random.randint(1,100)
                    if (this_chance <= percent_chance_of_pickup):         # Customer needs pickup
                        event_queue.insert("PickupArrival",event_time)
                        total_pickup_customers_arrived += 1
                    
                """PickupServiceBegin Event"""
                if (current_event[0:pound_index] == "PickupServiceBegin"):
                    pickup_helper_number = current_event[pound_index+1:]
                    service_time = random.randint(1,mu)
                    task_and_pickup_helper_number = "PickupServiceEnd#"+ str(pickup_helper_number)
                    event_queue.insert(task_and_pickup_helper_number, event_time + service_time)
                
                """PickupServiceEnd Event"""
                if (current_event[0:pound_index] == "PickupServiceEnd"):
                    pickup_helper_number = current_event[pound_index+1:]
                    total_pickup_customers_served += 1
                    pickup_helpers[int(pickup_helper_number)] = "idle"
                
                    
            
        current_time += 1
            
    
    #compute average wait time
    sum_of_wait_times = 0
    number_of_wait_times = len(wait_times)
    for x in range(number_of_wait_times):
        sum_of_wait_times += wait_times[x]
    average_wait_time = sum_of_wait_times / number_of_wait_times

    #compute average pickup wait time
    sum_of_pickup_wait_times = 0
    number_of_pickup_wait_times = len(pickup_wait_times)
    for x in range(number_of_pickup_wait_times):
        sum_of_pickup_wait_times += pickup_wait_times[x]
    average_pickup_wait_time = sum_of_pickup_wait_times / number_of_pickup_wait_times
    
    
    
    #print and return statistics
    print("\n====== Simulation Statistics ==========")
    print("  - Total Cashiers:                   ", total_number_cashiers)
    print("  - Total Pickup Helpers:             ", total_number_pickup_helpers)
    print("  - Total Simulation Time:            ", total_simulation_time)
    print("  - Maximum Interarrival Time:        ", l)
    print("  - Maximum Service Time:             ", mu)
    print("  - Total Customers Arrived:          ", total_customers_arrived)
    print("  - Total Customers Served:           ", total_customers_served)
    print("  - Total Pickup Customers Arrived:   ", total_pickup_customers_arrived)
    print("  - Total Pickup Customers Served:    ", total_pickup_customers_served)
    print("  - Customers Not Served:             ", total_customers_arrived-total_customers_served)
    print("  - Average Wait Time:                ", round(average_wait_time,2))
    print("  - Average Pickup Wait Time:         ", round(average_pickup_wait_time,2))
    print("========================================\n")
    print("Simulation ends ...")
    
    
    return average_wait_time, total_customers_arrived, total_customers_served, total_pickup_customers_arrived, total_pickup_customers_served, total_number_cashiers, total_simulation_time, len(customer_queue)
                
        
    
    
def main():
    n, m, l, mu, total_simulation_time = setup()
    input("Press [ENTER] to run simulation. ")
    run(n, m, l, mu, total_simulation_time)



main()