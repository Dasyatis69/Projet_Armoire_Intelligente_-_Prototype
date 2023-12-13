class Message:
    def __init__(self, bus_channel):
        pass

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
        self.drawers = [drawer] if drawer.isinstance(drawer) else drawer if drawer.isintance(list) else []
        # à modifier, accepte drawer ou une liste de drawer

    def get_packet_list_for_order(self, order):
        return self.orders[order]

    def send_message(self):
        pass


class Drawer:
    def __init__(self):
        pass


# type, dimension propre (Xc, Yc, Zc), dimension réelle (Xr, Yr, Zr), position (X, Y, Z, face XY, face XZ), id (optional)
class Packet:
    def __init__(self):
        pass


class Order:
    def __init__(self):
        pass


# better struct available ?
class Coordinate:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def volume(self):
        return self.x * self.y * self.z

    def rotate(self, angle, axis):  # 90, 180, -90 in each axis only (clockwise, counterclockwise, mirror as choice ?)
        pass
