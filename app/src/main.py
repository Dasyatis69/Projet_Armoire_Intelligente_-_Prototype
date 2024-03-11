import atexit

import core_classes as core
from time import time
from random import randint
import json

# logging
import logging.config
import logging.handlers
import pathlib

logger = logging.getLogger("storage_and_palletization")


def measure_runtime(func):
    def wrapper():
        t = time()
        func()
        t = time() - t
        print(f'{func.__name__} took {t:.5f} seconds to run')
    return wrapper


def setup_logging():
    config_file = pathlib.Path("../configuration_files/logger_config.json")
    with open(config_file) as file:
        config = json.load(file)
    logging.config.dictConfig(config)
    queue_handler = logging.getHandlerByName("queue_handler")
    if queue_handler is not None:
        queue_handler.listener.start()
        atexit.register(queue_handler.listener.stop)


def setup():
    message_bus = core.Message('simulation_channel:0001')

    order_queue = core.OrderQueue()
    order_list_for_demo = [
        core.Order('aaaa', [  # commande n°1
            core.Packet(packet_type='AAAA',
                        absolute_dimension=core.Coordinate(0, 0, 0),
                        real_dimension=core.Coordinate(0, 0, 0)),
            core.Packet(packet_type='AAAA',
                        absolute_dimension=core.Coordinate(0, 0, 0),
                        real_dimension=core.Coordinate(0, 0, 0)),
            core.Packet(packet_type='DDDD',
                        absolute_dimension=core.Coordinate(0, 0, 0),
                        real_dimension=core.Coordinate(0, 0, 0))
                        ]),
        core.Order('bbbb', [  # commande n°2
            core.Packet(packet_type='AAAA',
                        absolute_dimension=core.Coordinate(0, 0, 0),
                        real_dimension=core.Coordinate(0, 0, 0)),
            core.Packet(packet_type='BBBB',
                        absolute_dimension=core.Coordinate(0, 0, 0),
                        real_dimension=core.Coordinate(0, 0, 0)),
            core.Packet(packet_type='CCCC',
                        absolute_dimension=core.Coordinate(0, 0, 0),
                        real_dimension=core.Coordinate(0, 0, 0)),
            core.Packet(packet_type='CCCC',
                        absolute_dimension=core.Coordinate(0, 0, 0),
                        real_dimension=core.Coordinate(0, 0, 0)),
            core.Packet(packet_type='JJJJ',
                        absolute_dimension=core.Coordinate(0, 0, 0),
                        real_dimension=core.Coordinate(0, 0, 0)
                        )]),
        core.Order('cccc', [  # commande n°3
            core.Packet(packet_type='EEEE',
                        absolute_dimension=core.Coordinate(0, 0, 0),
                        real_dimension=core.Coordinate(0, 0, 0)),
            core.Packet(packet_type='FFFF',
                        absolute_dimension=core.Coordinate(0, 0, 0),
                        real_dimension=core.Coordinate(0, 0, 0)),
            core.Packet(packet_type='GGGG',
                        absolute_dimension=core.Coordinate(0, 0, 0),
                        real_dimension=core.Coordinate(0, 0, 0)),
            core.Packet(packet_type='IIII',
                        absolute_dimension=core.Coordinate(0, 0, 0),
                        real_dimension=core.Coordinate(0, 0, 0)),
            core.Packet(packet_type='HHHH',
                        absolute_dimension=core.Coordinate(0, 0, 0),
                        real_dimension=core.Coordinate(0, 0, 0)),
            core.Packet(packet_type='EEEE',
                        absolute_dimension=core.Coordinate(0, 0, 0),
                        real_dimension=core.Coordinate(0, 0, 0))
        ])
    ]
    # [order_queue.add_order(order) for order in order_list_for_demo]

    print('Start Setup'.center(40, '-'))
    for order in order_list_for_demo:
        print(f'\nOrder of id {order.id}')
        order_queue.add_order(order)
        for packet in order.packet_list:
            print(f'Packet of type {packet.packet_type}')
    print('\n' + 'End Setup'.center(40, '-') + '\n')


    # orders should be palletized in order : 1, 3, 2

    poles = list()
    last_armoire_id = 0
    last_drawer_id = 0
    for i in range(2):
        poles.append(core.Pole(pole_id=str(i).zfill(4)))
        for j in range(2):
            poles[i].add_armoire(core.Armoire(str(j + last_armoire_id).zfill(4), randint(6, 9)))
            for k in range(3):
                poles[i].armoires[j].add_drawer(core.Drawer(str(k + last_drawer_id).zfill(4), randint(27, 35)))
            last_drawer_id += 3
        last_armoire_id += 2
    return poles, order_queue, message_bus


# def setup():
#     pole_1 = (core.Pole(pole_id='0001')
#               .add_armoire([core.Armoire('0001', 6)
#                            .add_drawer([core.Drawer('0001', 27),
#                                         core.Drawer('0002', 30),
#                                         core.Drawer('0003', 25)],
#                                        setup=True),
#                             core.Armoire('0002', 7)
#                            .add_drawer([core.Drawer('0004', 31),
#                                         core.Drawer('0005', 32),
#                                         core.Drawer('0006', 28)],
#                                        setup=True)]))
#     pole_2 = (core.Pole(pole_id='0002')
#               .add_armoire([core.Armoire('0003', 8)
#                            .add_drawer([core.Drawer('0007', 27),
#                                         core.Drawer('0008', 30),
#                                         core.Drawer('0009', 25)],
#                                        setup=True),
#                             core.Armoire('0004', 9)
#                            .add_drawer([core.Drawer('0010', 31),
#                                         core.Drawer('0011', 32),
#                                         core.Drawer('0012', 28)],
#                                        setup=True)]))
#     return pole_1, pole_2


def wait_for_packet_placeholder(packet_type):  # only here for prototype, real packet receive ing syteme will be implemented later
    # sleep(0.1)
    return core.Packet(packet_type=packet_type,
                         absolute_dimension=core.Coordinate(0, 0, 0),
                         real_dimension=core.Coordinate(0, 0, 0))


def pole_switch(poles, order_queue, message_bus_channel, packet):
    default_position_for_demo = core.Position(0, 0, 0, 1, 1)
    poles_with_packet_in_assigned_order = []
    for pole in poles:
        if pole.is_packet_in_assigned_orders(packet):
            poles_with_packet_in_assigned_order.append(pole)

    print(f'Is the packet in an order of order_queue : {order_queue.is_packet_in_queue(packet)}')
    print(f'Pole that has the packet in its assigned order : {[pole.id for pole in poles_with_packet_in_assigned_order]}')

    if len(poles_with_packet_in_assigned_order) == 1:
        print('One pole has the packet in its assigned order')
        order = poles_with_packet_in_assigned_order[0].is_packet_in_assigned_orders(packet, get_order=True)
        poles_with_packet_in_assigned_order[0].add_packet(packet, order, default_position_for_demo)

    elif len(poles_with_packet_in_assigned_order) > 1:
        print('More than one pole has the packet in its assigned order')
        pole_order_with_highest_completion_rate = list()  # currently not the highest but the 1st, change will be made beyond prototype
        for pole in poles_with_packet_in_assigned_order:
            pole_order_with_highest_completion_rate.append(
                pole.get_order_completion_rate(
                    pole.is_packet_in_assigned_orders(packet, get_order=True) ))
        order = poles_with_packet_in_assigned_order[ max(enumerate(pole_order_with_highest_completion_rate), key=lambda x: x[1])[0] ].is_packet_in_assigned_orders(packet, get_order=True)
        poles_with_packet_in_assigned_order[ max(enumerate(pole_order_with_highest_completion_rate), key=lambda x: x[1])[0] ].add_packet(packet, order, default_position_for_demo)

    else:  # len(poles_with_packet_in_assigned_order) == 0:
        if order_queue.is_packet_in_queue(packet):
            print("Packet isn't in any pole but is in order_queue")
            pole_amounts_of_assigned_order = list()
            for pole in poles:
                pole_amounts_of_assigned_order.append(pole.get_number_of_assigned_order())
            order = order_queue.is_packet_in_queue(packet, get_order=True)
            poles[ min(enumerate(pole_amounts_of_assigned_order), key=lambda x: x[1])[0] if pole_amounts_of_assigned_order != [] else 0].assign_order(order)  # assign order to relevant pole
            order_queue.take_out_order_from_queue(order)
            print(f'nbr of order left in order_queue : {len(order_queue.order_list)}')
            poles[ min(enumerate(pole_amounts_of_assigned_order), key=lambda x: x[1])[0] if pole_amounts_of_assigned_order != [] else 0].add_packet(packet, order, default_position_for_demo)  # add packet to said pole
        else:
            message_bus_channel.write_message_to_bus("Error : packet doesn't belong to any known order")
            return False


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


#@measure_runtime
def main():
    # logging setup
    setup_logging()
    logger.debug("debug msg")
    logger.info("info msg")
    logger.warning("warning msg")
    logger.error("error msg")
    logger.critical("critical msg")
    try:
        1/0
    except ZeroDivisionError:
        logger.exception("exception msg")

    # sys setup
    poles, order_queue, message_bus_chanel = setup()  # create poles, drawer, order_queue etc

    palletized_order_list_for_demo = list()
    packet_type_list_for_demo = ['AAAA', 'BBBB', 'CCCC', 'DDDD', 'AAAA', 'EEEE', 'FFFF', 'CCCC', 'GGGG', 'HHHH', 'AAAA', 'EEEE', 'IIII', 'JJJJ']  # 14 packets to be palettized for demo
    for packet_type in packet_type_list_for_demo:
        packet = wait_for_packet_placeholder(packet_type)  # idk how yet but when we receive a packet from message bus, placeholder function for demo purpose
        print(f'Packet of type {packet.packet_type} is waiting for redirection')
        pole_switch(poles, order_queue, message_bus_chanel, packet)
        print(f'pole_switch finished')
        print(f'can palletize : {can_order_be_palletized(poles)}')
        if can_order_be_palletized(poles):
            palletized_order_list_for_demo.append(start_palletization(poles))
            print(f'List of palettized order : {[order.id for order in palletized_order_list_for_demo]}')
        print('\n')
    return 0


if __name__ == "__main__":
    main()
