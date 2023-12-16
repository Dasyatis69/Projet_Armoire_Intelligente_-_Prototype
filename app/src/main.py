import core_classes as core
from time import time


def measure_runtime(func):
    def wrapper():
        t = time()
        func()
        t = time() - t
        print(f'{func.__name__} took {t} seconds to run')
    return wrapper


def setup():
    pole_1 = (core.Pole(pole_id='0001')
              .add_armoire([core.Armoire('0001', 6)
                           .add_drawer([core.Drawer('0001', 27),
                                        core.Drawer('0002', 30),
                                        core.Drawer('0003', 25)],
                                       setup=True),
                            core.Armoire('0002', 7)
                           .add_drawer([core.Drawer('0004', 31),
                                        core.Drawer('0005', 32),
                                        core.Drawer('0006', 28)],
                                       setup=True)]))
    pole_2 = (core.Pole(pole_id='0002')
              .add_armoire([core.Armoire('0003', 8)
                           .add_drawer([core.Drawer('0007', 27),
                                        core.Drawer('0008', 30),
                                        core.Drawer('0009', 25)],
                                       setup=True),
                            core.Armoire('0004', 9)
                           .add_drawer([core.Drawer('0010', 31),
                                        core.Drawer('0011', 32),
                                        core.Drawer('0012', 28)],
                                       setup=True)]))


def wait_for_packet_placeholder(packet_type):  # only here for prototype, real packet receive ing syteme will be implemented later
    packet = core.Packet(packet_type=packet_type,
                         absolute_dimension=core.Coordinate(1, 2, 1),
                         reel_dimension=core.Coordinate(2, 1, 1))
    return packet


def pole_switch(packet):
    pass


@measure_runtime
def main():
    setup()  # create poles, drawer, order_queue etc

    packet_type_list_for_demo = ['AAAA', 'BBBB', 'CCCC', 'DDDD', 'AAAA', 'EEEE', 'FFFF', 'CCCC', 'GGGG', 'HHHH', 'AAAA', 'EEEE', 'IIII', 'JJJJ']
    for packet_type in packet_type_list_for_demo:
        packet = wait_for_packet_placeholder(packet_type)  # idk how yet but when we receive a packet from message bus, placeholder function for demo purpose
        pole_switch(packet)
    return 0


if __name__ == "__main__":
    main()
