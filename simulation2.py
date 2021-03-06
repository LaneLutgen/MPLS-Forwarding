'''
Created on Oct 12, 2016

@author: mwitt_000
'''
import network2
import link2
import threading
from time import sleep
import sys

##configuration parameters
router_queue_size = 0 #0 means unlimited
simulation_time = 20 #give the network sufficient time to transfer all packets before quitting

if __name__ == '__main__':
    object_L = [] #keeps track of objects, so we can kill their threads
    
    #create network hosts
    client = network2.Host(1)
    object_L.append(client)
    client2 = network2.Host(2)
    object_L.append(client2)
    server = network2.Host(3)
    object_L.append(server)
    
    #create routers and routing tables for connected clients (subnets)
    router_a_rt_tbl_D = {} # packet to host 1 through interface 0 for cost 1
    router_a_rt_tbl_D['in_label'] = [0, 0]
    router_a_rt_tbl_D['out_label'] = [8, 10]
    router_a_rt_tbl_D['in_intf'] = [0, 1]
    router_a_rt_tbl_D['out_intf'] = [2, 3]
    router_a = network2.Router(name='A', 
                              intf_cost_L=[1,1,1,1], 
                              intf_capacity_L=[500,500,500,500],
                              rt_tbl_D = router_a_rt_tbl_D, 
                              max_queue_size=router_queue_size)
    object_L.append(router_a)
    router_b_rt_tbl_D = {} # packet to host 2 through interface 1 for cost 3
    router_b_rt_tbl_D['in_label'] = [10]
    router_b_rt_tbl_D['out_label'] = [6]
    router_b_rt_tbl_D['in_intf'] = [0]
    router_b_rt_tbl_D['out_intf'] = [1]
    router_b = network2.Router(name='B', 
                              intf_cost_L=[1,3], 
                              intf_capacity_L=[500,100],
                              rt_tbl_D = router_b_rt_tbl_D, 
                              max_queue_size=router_queue_size)
    object_L.append(router_b)
    router_c_rt_tbl_D = {}
    router_c_rt_tbl_D['in_label'] = [8]
    router_c_rt_tbl_D['out_label'] = [6]
    router_c_rt_tbl_D['in_intf'] = [0]
    router_c_rt_tbl_D['out_intf'] = [1]
    router_c = network2.Router(name='C', 
                              intf_cost_L=[1,3], 
                              intf_capacity_L=[500,100],
                              rt_tbl_D = router_c_rt_tbl_D, 
                              max_queue_size=router_queue_size)
    object_L.append(router_c)
    router_d_rt_tbl_D = {}
    router_d_rt_tbl_D['in_label'] = [6, 6]
    router_d_rt_tbl_D['out_label'] = [0, 0]
    router_d_rt_tbl_D['in_intf'] = [0, 1]
    router_d_rt_tbl_D['out_intf'] = [2, 2]
    router_d = network2.Router(name='D', 
                              intf_cost_L=[1,3,1], 
                              intf_capacity_L=[500,100,500],
                              rt_tbl_D = router_d_rt_tbl_D, 
                              max_queue_size=router_queue_size)
    object_L.append(router_d)
    
    #create a Link Layer to keep track of links between network nodes
    link_layer = link2.LinkLayer()
    object_L.append(link_layer)
    
    #add all the links
    link_layer.add_link(link2.Link(client, 0, router_a, 0)) #1 to a
    link_layer.add_link(link2.Link(client2, 0, router_a, 1)) #2 to a
    link_layer.add_link(link2.Link(router_a, 2, router_b, 0)) #a to b
    link_layer.add_link(link2.Link(router_a, 3, router_c, 0)) #a to c
    link_layer.add_link(link2.Link(router_b, 1, router_d, 0)) #b to d
    link_layer.add_link(link2.Link(router_c, 1, router_d, 1)) #c to d    
    link_layer.add_link(link2.Link(router_d, 2, server, 0))
    
    
    #start all the objects
    thread_L = []
    for obj in object_L:
        thread_L.append(threading.Thread(name=obj.__str__(), target=obj.run)) 
    
    for t in thread_L:
        t.start()
    
    #create some send events    
    for i in range(3):
        priority = i%2
        print(priority)
        client.udt_send(3, 1, 'From Host 1 Sample %d' % i, priority)

    for i in range(3):
        priority = i%2
        print(priority)
        client2.udt_send(3, 2, 'From Host 2 SAMPLE %d' % i, priority)
        
    #give the network sufficient time to transfer all packets before quitting
    sleep(simulation_time)
    
    #print the final routing tables
    for obj in object_L:
        if str(type(obj)) == "<class 'network.Router'>":
            obj.print_routes()
    
    #join all threads
    for o in object_L:
        o.stop = True
    for t in thread_L:
        t.join()
        
    print("All simulation threads joined")



# writes to host periodically
