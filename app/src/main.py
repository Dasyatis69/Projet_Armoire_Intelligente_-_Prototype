import core_classes as core
from time import time
from random import randint


def measure_runtime(func):
    def wrapper():
        t = time()
        func()
        t = time() - t
        print(f'{func.__name__} took {t} seconds to run')
    return wrapper


def setup():
    poles = list()
    for i in range(2):
        poles.append(core.Pole(pole_id=str(i).zfill(4)))
        for j in range(2):
            poles[i].add_armoire(core.Armoire(str(j).zfill(4), randint(6, 9)))
            for k in range(3):
                poles[i].armoires[k].add_drawer(core.Drawer(str(k).zfill(4), randint(27, 35)))
    return poles


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
    packet = core.Packet(packet_type=packet_type,
                         absolute_dimension=core.Coordinate(1, 2, 1),
                         reel_dimension=core.Coordinate(2, 1, 1))
    return packet


def pole_switch(poles, packet):
    '''
    check si le packet est dans les commmandes attribué
    on l'aiguille vers le pôle ayant la commande ayant besoin du colis qui est le plus proche de la complétion
    (ratio de paquet de la commande completé) s'il peut stocker le colis

    sinon, on va chercher une commande qui correspond
    et on l'attribut au pôle ayant le moins de commandes attibués et/ou le moins de colis en stock
    et on aiguille le paquet vers ce pôle s'il peut stocker le colis, sinon rebelotte

    si personne ayant besoin du colis peut le sotcker, et qu'il n'y a plus d'order ayant besoin de ce colis -> erreur
    '''
    pass


@measure_runtime
def main():
    poles = setup()  # create poles, drawer, order_queue etc

    packet_type_list_for_demo = ['AAAA', 'BBBB', 'CCCC', 'DDDD', 'AAAA', 'EEEE', 'FFFF', 'CCCC', 'GGGG', 'HHHH', 'AAAA', 'EEEE', 'IIII', 'JJJJ']
    for packet_type in packet_type_list_for_demo:
        packet = wait_for_packet_placeholder(packet_type)  # idk how yet but when we receive a packet from message bus, placeholder function for demo purpose
        pole_switch(poles, packet)
    return 0


if __name__ == "__main__":
    main()
