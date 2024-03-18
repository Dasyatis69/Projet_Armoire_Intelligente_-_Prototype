import core_classes as core

# equility test between instances (imply __eq__ in Packet, Coordinate, Position) :
packet1 = core.Packet(packet_type='ABCD', absolute_dimension=core.Position(0, 0, 0, 1, 5), real_dimension=None)
packet2 = core.Packet(packet_type='ABCD', absolute_dimension=core.Position(0, 0, 0, 1, 5), real_dimension=None)
packet3 = core.Packet(packet_type='EFGH', absolute_dimension=core.Position(0, 0, 1, 1, 5), real_dimension=None)
packet4 = packet1
print(packet1 == packet2)
print(packet1 == packet3)
print(packet1 == packet4)

# Manual setup (1st iteration)
# pole_1 = (core.Pole(pole_id='0001')
#           .add_armoire([core.Armoire('0001', 6)
#                        .add_drawer([core.Drawer('0001', 27),
#                                     core.Drawer('0002', 30),
#                                     core.Drawer('0003', 25)],
#                                    setup=True),
#                         core.Armoire('0002', 7)
#                        .add_drawer([core.Drawer('0004', 31),
#                                     core.Drawer('0005', 32),
#                                     core.Drawer('0006', 28)],
#                                    setup=True)]))
# pole_2 = (core.Pole(pole_id='0002')
#           .add_armoire([core.Armoire('0003', 8)
#                        .add_drawer([core.Drawer('0007', 27),
#                                     core.Drawer('0008', 30),
#                                     core.Drawer('0009', 25)],
#                                    setup=True),
#                         core.Armoire('0004', 9)
#                        .add_drawer([core.Drawer('0010', 31),
#                                     core.Drawer('0011', 32),
#                                     core.Drawer('0012', 28)],
#                                    setup=True)]))
# return [pole_1, pole_2]

# Manual setup (2nd iteration, for demo) :
# poles = list()
# last_armoire_id = 0
# last_drawer_id = 0
# for i in range(2):
#     poles.append(core.Pole(pole_id=str(i).zfill(4)))
#     for j in range(2):
#         poles[i].add_armoire(core.Armoire(str(j + last_armoire_id).zfill(4), randint(6, 9)))
#         for k in range(3):
#             poles[i].armoires[j].add_drawer(core.Drawer(str(k + last_drawer_id).zfill(4), randint(27, 35)))
#         last_drawer_id += 3
#     last_armoire_id += 2