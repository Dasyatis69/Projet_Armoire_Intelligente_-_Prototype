class Message:
    def __init__(self, bus_channel):
        self.bus_channel = bus_channel

    def write_to_message_bus(self):
        pass

    def read_from_message_bus(self):
        pass


class Pole(Message):  # async can be disabled (read on confluence, assumed to be True by default)
    def __init__(self, armoire, async_work=True, bus_channel=''):
        super().__init__(bus_channel)
        self.async_work = async_work
        self.armoires = [armoire] if armoire.isinstance(Armoire) else armoire if armoire.isintance(list) else []
        # à modifier, accepte armoire ou une liste d'armoire


class Armoire:
    def __init__(self, drawer):
        self.orders = dict()
        self.drawers = [drawer] if drawer.isinstance(Drawer) else drawer if drawer.isintance(list) else []
        # à modifier, accepte drawer ou une liste de drawer

    def get_packet_list_for_order(self, order):
        return self.orders[order]

    def send_message(self):
        pass


class Drawer:
    def __init__(self, packet):
        self.packets = [packet] if packet.isinstance(Packet) else packet if packet.isintance(list) else []

    def add_packet(self, packet):
        self.packets.append(packet)
        return 0

    def take__out_packet(self, packet):
        self.packets.remove(packet)
        return 0


# type, dimension propre (Xc, Yc, Zc),
# dimension réelle (Xr, Yr, Zr),
# position (X, Y, Z, face XY, face XZ),
# id (optional)
class Packet:
    def __init__(self, packet_type, absolute_dimension, reel_dimension, position, id=None):
        self.packet_type = packet_type
        self.absolute_dimension = absolute_dimension if absolute_dimension.isinstance(Coordinate) else ()
        self.reel_dimension = reel_dimension if reel_dimension.isinstance(Coordinate) else ()
        self.position = position if position.isinstance(Coordinate) and position.isposition else ()

    def volume(self):
        return self.absolute_dimension.x * self.absolute_dimension.y * self.absolute_dimension.z


class Order:
    def __init__(self):
        pass


# better struct available ?
class Coordinate:
    def __init__(self, x, y, z, xy=None, xz=None):
        self.x = x
        self.y = y
        self.z = z
        self.xy = xy
        self.xz = xz
        self.isposition = True if xy is not None and xz is not None else False

    def rotate(self, angle, axis):  # 90, 180, -90 in each axis only (clockwise, counterclockwise, mirror as choice ?)
        pass
