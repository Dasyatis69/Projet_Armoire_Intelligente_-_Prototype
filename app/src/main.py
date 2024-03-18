import core_classes as core
import config
from time import time#, sleep
from random import randint


def measure_runtime(func):
    def wrapper():
        t = time()
        func()
        t = time() - t
        print(f'{func.__name__} took {t:.5f} seconds to run')
    return wrapper


def setup():
    message_bus = core.Message('simulation_channel:0001')

    order_queue = core.OrderQueue()
    # [order_queue.add_order(order) for order in order_list_for_demo]
    order_list_for_demo = [
        core.Order('aaaa', [  # commande n°1
            core.Packet(packet_type='AAAA', absolute_dimension=core.Position(30, 20, 15, 0, 1),
                        real_dimension=core.Position(30, 20, 15, 0, 1)),
            core.Packet(packet_type='AAAA', absolute_dimension=core.Position(30, 20, 15, 0, 1),
                        real_dimension=core.Position(30, 20, 15, 0, 1)),
            core.Packet(packet_type='DDDD', absolute_dimension=core.Position(20, 20, 20, 0, 1),
                        real_dimension=core.Position(20, 20, 20, 0, 1))
                        ]),
        core.Order('bbbb', [  # commande n°2
            core.Packet(packet_type='AAAA', absolute_dimension=core.Position(30, 20, 15, 0, 1),
                        real_dimension=core.Position(30, 20, 15, 0, 1)),
            core.Packet(packet_type='BBBB', absolute_dimension=core.Position(50, 15, 15, 0, 1),
                        real_dimension=core.Position(50, 15, 15, 0, 1)),
            core.Packet(packet_type='CCCC', absolute_dimension=core.Position(15, 10, 8, 0, 1),
                        real_dimension=core.Position(15, 10, 8, 0, 1)),
            core.Packet(packet_type='CCCC', absolute_dimension=core.Position(15, 10, 8, 0, 1),
                        real_dimension=core.Position(15, 10, 8, 0, 1)),
            core.Packet(packet_type='JJJJ', absolute_dimension=core.Position(40, 25, 30, 0, 1),
                        real_dimension=core.Position(40, 25, 30, 0, 1))]),
        core.Order('cccc', [  # commande n°3
            core.Packet(packet_type='EEEE', absolute_dimension=core.Position(20, 35, 30, 0, 1),
                        real_dimension=core.Position(20, 35, 30, 0, 1)),
            core.Packet(packet_type='FFFF', absolute_dimension=core.Position(10, 10, 5, 0, 1),
                        real_dimension=core.Position(10, 10, 5, 0, 1)),
            core.Packet(packet_type='GGGG', absolute_dimension=core.Position(20, 25, 20, 0, 1),
                        real_dimension=core.Position(20, 25, 20, 0, 1)),
            core.Packet(packet_type='IIII', absolute_dimension=core.Position(8, 10, 4, 0, 1),
                        real_dimension=core.Position(8, 10, 4, 0, 1)),
            core.Packet(packet_type='HHHH', absolute_dimension=core.Position(50, 70, 45, 0, 1),
                        real_dimension=core.Position(50, 70, 45, 0, 1)),
            core.Packet(packet_type='EEEE', absolute_dimension=core.Position(20, 35, 30, 0, 1),
                        real_dimension=core.Position(20, 35, 30, 0, 1))
        ])
    ]

    print('Start Setup'.center(40, '-'))
    for order in order_list_for_demo:
        print(f'\nOrder of id {order.id}')
        order_queue.add_order(order)
        for packet in order.packet_list:
            print(f'Packet of type {packet.packet_type} and dimension {packet.real_dimension.x}x{packet.real_dimension.y}x{packet.real_dimension.z}')
    print('\n' + 'End Setup'.center(40, '-') + '\n')

    # orders should be palletized in order : 1, 3, 2

    # New setup (3rd iteration, through config file) :
    poles = config.load_config_from_file('../configuration_files/sys_config.json')

    return poles, order_queue, message_bus


def wait_for_packet_placeholder(i: int):  # for simulation purpose
    packet_type_list_for_demo = ['AAAA', 'BBBB', 'CCCC', 'DDDD', 'AAAA', 'EEEE', 'FFFF', 'CCCC', 'GGGG', 'HHHH', 'AAAA', 'EEEE', 'IIII', 'JJJJ']  # 14 packets to be palettized for demo
    packet_list_for_2nd_demo = [
        core.Packet(packet_type='AAAA', absolute_dimension=core.Position(30, 20, 15, 0, 1),
                    real_dimension=core.Position(30, 20, 15, 0, 1)),
        core.Packet(packet_type='BBBB', absolute_dimension=core.Position(50, 15, 15, 0, 1),
                    real_dimension=core.Position(50, 15, 15, 0, 1)),
        core.Packet(packet_type='CCCC', absolute_dimension=core.Position(15, 10, 8, 0, 1),
                    real_dimension=core.Position(15, 10, 8, 0, 1)),
        core.Packet(packet_type='DDDD', absolute_dimension=core.Position(20, 20, 20, 0, 1),
                    real_dimension=core.Position(20, 20, 20, 0, 1)),
        core.Packet(packet_type='AAAA', absolute_dimension=core.Position(30, 20, 15, 0, 1),
                    real_dimension=core.Position(30, 20, 15, 0, 1)),
        core.Packet(packet_type='EEEE', absolute_dimension=core.Position(20, 35, 30, 0, 1),
                    real_dimension=core.Position(20, 35, 30, 0, 1)),
        core.Packet(packet_type='FFFF', absolute_dimension=core.Position(10, 10, 5, 0, 1),
                    real_dimension=core.Position(10, 10, 5, 0, 1)),
        core.Packet(packet_type='CCCC', absolute_dimension=core.Position(15, 10, 8, 0, 1),
                    real_dimension=core.Position(15, 10, 8, 0, 1)),
        core.Packet(packet_type='GGGG', absolute_dimension=core.Position(20, 25, 20, 0, 1),
                    real_dimension=core.Position(20, 25, 20, 0, 1)),
        core.Packet(packet_type='HHHH', absolute_dimension=core.Position(50, 70, 45, 0, 1),
                    real_dimension=core.Position(50, 70, 45, 0, 1)),
        core.Packet(packet_type='AAAA', absolute_dimension=core.Position(30, 20, 15, 0, 1),
                    real_dimension=core.Position(30, 20, 15, 0, 1)),
        core.Packet(packet_type='EEEE', absolute_dimension=core.Position(20, 35, 30, 0, 1),
                    real_dimension=core.Position(20, 35, 30, 0, 1)),
        core.Packet(packet_type='IIII', absolute_dimension=core.Position(8, 10, 4, 0, 1),
                    real_dimension=core.Position(8, 10, 4, 0, 1)),
        core.Packet(packet_type='JJJJ', absolute_dimension=core.Position(40, 25, 30, 0, 1),
                    real_dimension=core.Position(40, 25, 30, 0, 1))
    ]
    return packet_list_for_2nd_demo[i]


def pole_switch(poles, order_queue, message_bus_channel, packet):
    poles_with_packet_in_assigned_order = []
    for pole in poles:
        if pole.is_packet_in_assigned_orders(packet):
            poles_with_packet_in_assigned_order.append(pole)

    # print(f'Is the packet in an order of order_queue : {order_queue.is_packet_in_queue(packet)}')
    # print(f'Pole that has the packet in its assigned order : {[pole.id for pole in poles_with_packet_in_assigned_order]}')

    if len(poles_with_packet_in_assigned_order) == 1:
        print('One pole has the packet in its assigned order')
        order = poles_with_packet_in_assigned_order[0].is_packet_in_assigned_orders(packet, get_order=True)
        coordinate = poles_with_packet_in_assigned_order[0].find_suitable_position(packet)
        poles_with_packet_in_assigned_order[0].add_packet(packet, order, coordinate)

    elif len(poles_with_packet_in_assigned_order) > 1:
        print('More than one pole has the packet in its assigned order')
        pole_order_with_highest_completion_rate = list()  # currently not the highest but the 1st, change will be made
        for pole in poles_with_packet_in_assigned_order:
            pole_order_with_highest_completion_rate.append(
                pole.get_order_completion_rate(
                    pole.is_packet_in_assigned_orders(packet, get_order=True) ))
        index_pole_highest_completion_rate = max(enumerate(pole_order_with_highest_completion_rate), key=lambda x: x[1])[0]
        order = poles_with_packet_in_assigned_order[index_pole_highest_completion_rate].is_packet_in_assigned_orders(packet, get_order=True)
        coordinate = poles_with_packet_in_assigned_order[index_pole_highest_completion_rate].find_suitable_position(packet)
        poles_with_packet_in_assigned_order[index_pole_highest_completion_rate].add_packet(packet, order, coordinate)

    else:  # len(poles_with_packet_in_assigned_order) == 0:
        if order_queue.is_packet_in_queue(packet):
            print("Packet isn't in any pole but is in order_queue")
            pole_amounts_of_assigned_order = list()
            for pole in poles:
                pole_amounts_of_assigned_order.append(pole.get_number_of_assigned_order())
            order = order_queue.is_packet_in_queue(packet, get_order=True)
            index_pole_lowest_assigned_order = min(enumerate(pole_amounts_of_assigned_order), key=lambda x: x[1])[0] if pole_amounts_of_assigned_order != [] else 0
            poles[index_pole_lowest_assigned_order].assign_order(order)  # assign order to relevant pole
            order_queue.take_out_order_from_queue(order)
            # print(f'nbr of order left in order_queue : {len(order_queue.order_list)}')
            coordinate = poles[index_pole_lowest_assigned_order].find_suitable_position(packet)
            poles[index_pole_lowest_assigned_order].add_packet(packet, order, coordinate)  # add packet to said pole
        else:
            message_bus_channel.write_message_to_bus("Error : packet doesn't belong to any known order")


def start_palletization(pole_list):  # no need for else case since we only call if we know we can palletize
    for pole in pole_list:
        if pole.can_palletize():
            order = pole.can_palletize(get_order=True)
            return pole.palletize(order)


def can_order_be_palletized(pole_list):
    for pole in pole_list:
        if pole.can_palletize():
            return True
    return False


def display_drawer_state(poles):
    print('\n--- Drawer States ---')
    for pole in poles:
        print(f"pole : {pole.id}")
        # for assigned_order in pole.assigned_orders:
        #     print(assigned_order.registered_packet_list)
        for armoire in pole.armoires:
            print(f"-- armoire : {armoire.id}")
            for drawer in armoire.drawers:
                if len(drawer.packets) > 0:
                    print(f"--|- drawer : {drawer.id}")
                    for packet in drawer.packets:
                        print(f"--|-|- packet of type {packet.packet_type} is stored at {packet.stored_position} as {packet.padded_dimension}")
    print('---------------------\n')


@measure_runtime
def main():
    poles, order_queue, message_bus_chanel = setup()  # create poles, drawer, order_queue etc

    config.display_config(poles)

    if config.display_config(poles, check_only=True):
        palletized_order_list_for_demo = list()

        for i in range(14):
            packet = wait_for_packet_placeholder(i)  # when we receive a packet from message bus, placeholder function for demo purpose
            print(f'Packet of type {packet.packet_type} is waiting for redirection')
            pole_switch(poles, order_queue, message_bus_chanel, packet)
            display_drawer_state(poles)
            print(f'can palletize : {can_order_be_palletized(poles)}')
            if can_order_be_palletized(poles):
                palletized_order_list_for_demo.append(start_palletization(poles))
                print(f'List of palettized order : {[order.id for order in palletized_order_list_for_demo]}')
            print('\n')
    return 0


if __name__ == "__main__":
    main()
