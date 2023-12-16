import core_classes as core

# equility test between instances (imply __eq__ in Packet, Coordinate, Position) :
packet1 = core.Packet(packet_type='ABCD',
                      absolute_dimension=core.Coordinate(0, 0, 0),
                      reel_dimension=core.Coordinate(0, 0, 0))
packet2 = core.Packet(packet_type='ABCD',
                      absolute_dimension=core.Coordinate(0, 0, 0),
                      reel_dimension=core.Coordinate(0, 0, 0))
packet3 = core.Packet(packet_type='EFGH',
                      absolute_dimension=core.Coordinate(0, 0, 1),
                      reel_dimension=core.Coordinate(0, 0, 1))
packet4 = packet1
print(packet1 == packet2)
print(packet1 == packet3)
print(packet1 == packet4)
