class Message:
    def __init__(self, bus_channel):
        self.bus_channel = bus_channel

    def write_message_to_bus(self, msg):
        pass

    def read_message_from_bus(self):  # need more info about how the bus message works
        pass


class Pole(Message):  # async can be disabled (read on confluence, assumed to be True by default)
    def __init__(self, pole_id, async_work=True, bus_channel=''):
        super().__init__(bus_channel)
        self.id = pole_id  # raise error if not str, note for later
        self.armoires = []
        self.assigned_orders = list()
        self.async_work = async_work

    def add_armoire(self, armoire, setup=False):
        if isinstance(armoire, Armoire):  # input is one armoire
            self.armoires.append(armoire)
            if setup:
                return self
            else:  # delete else when error handling is added
                return True
        elif len(armoire) > 0 and all(isinstance(item, Armoire) for item in armoire):  # input is a list, set, tuple or even an array of armoire (type safety to add later on)
            for armoire in armoire:
                self.armoires.append(armoire)
            if setup:
                return self
            else:  # delete else when error handling is added
                return True
        else:
            return False  # raise error

    def assign_order(self, order):
        if isinstance(order, Order):
            self.assigned_orders.append(order)
            self.write_message_to_bus(f'Order of id : {order.id} has been assigned to pole of id {self.id}')
            return True
        else:
            return False

    def get_number_of_assigned_order(self):
        return len(self.assigned_orders)

    def is_packet_in_assigned_orders(self, packet, get_order=False):
        if isinstance(packet, Packet):
            for assigned_order in self.assigned_orders:
                for order_packet in assigned_order.packet_list:
                    if order_packet == packet:  # if packet has been stored and thus have a position, it will return False which is correct, we are looking for packet that we can complete in orders
                        if get_order:  # will return the 1st found, it's not the best choice but since other details need to be added to go beyond a prototype, it will stay like this for now
                            return assigned_order
                        else:
                            return True
        return False

    def can_palletize(self, get_order=False):
        for assigned_order in self.assigned_orders:
            if all(assigned_order.registered_packet_list):
                if get_order:
                    return assigned_order
                else:
                    return True
            else:
                return False

    def palletize(self, order):
        self.assigned_orders.remove(order)
        return order

    def get_order_completion_rate(self, order):
        if isinstance(order, Order):
            for assigned_order in self.assigned_orders:
                if assigned_order == order:
                    return sum(assigned_order.registered_packet_list) / len(assigned_order.registered_packet_list)
        return False

    def add_packet(self, packet, order, position):  #temp methode for prototype
        if isinstance(packet, Packet) and isinstance(order, Order) and isinstance(position, Position):
            for armoire in self.armoires:
                if armoire.add_packet(packet):
                    order.register_packet(packet, position)

                    return True
            return False


class Armoire:
    def __init__(self, armoire_id, capacity):
        self.id = armoire_id
        self.capacity = capacity  # raise error if not int, note for later
        self.drawers = []

    def add_drawer(self, drawer, setup=False):
        if isinstance(drawer, Drawer) and len(self.drawers) < self.capacity:  # input is one drawer
            self.drawers.append(drawer)
            if setup:
                return self
            else:  # delete else when error handling is added
                return True
        elif len(drawer) > 0 \
                and all(isinstance(item, Drawer) for item in drawer) \
                and len(self.drawers) + len(drawer) < self.capacity:  # input is a list, set, tuple or even an array of drawer (type safety to add later on)
            for drawer in drawer:
                self.drawers.append(drawer)
            if setup:
                return self
            else:  # delete else when error handling is added
                return True
        else:
            return False  # raise error

    def add_packet(self, packet):  # will change to (self, packet (rotated if needed), drawer, position)
        for drawer in self.drawers:
            if not drawer.is_full():
                if drawer.add_packet(packet):
                    return True
        return False

    def send_message(self):
        pass


class Drawer:
    def __init__(self, drawer_id, capacity):
        self.id = drawer_id
        self.capacity = capacity  # simplified storage management for prototype (MVP)
        self.packets = []

    def add_packet(self, packet):
        if len(self.packets) < self.capacity:
            self.packets.append(packet)
            return True
        else:
            return False

    def take_out_packet(self, packet):
        if isinstance(packet, Packet) and packet in self.packets:
            self.packets.remove(packet)
            return True
        else:
            return False

    def is_full(self):
        return True if len(self.packets) == self.capacity else False


# type, dimension propre (Xc, Yc, Zc),
# dimension réelle (Xr, Yr, Zr),
# position (X, Y, Z, face XY, face XZ),
# id (optional)
class Packet:
    def __init__(self, packet_type, absolute_dimension, real_dimension, position=None, id=None):
        self.packet_type = packet_type
        self.absolute_dimension = absolute_dimension if isinstance(absolute_dimension, Coordinate) else ()
        self.real_dimension = real_dimension if isinstance(real_dimension, Coordinate) else ()
        self.position = position if isinstance(position, Position) or position is None else ()

    def __eq__(self, other):
        if isinstance(other, Packet) \
                and self.packet_type == other.packet_type \
                and self.absolute_dimension == other.absolute_dimension \
                and self.real_dimension == other.real_dimension \
                and ((self.position is None and other.position is None) or self.position == other.position):
            return True
        else:
            return False

    def volume(self):
        return self.absolute_dimension.x * self.absolute_dimension.y * self.absolute_dimension.z

    def set_position(self, position):
        if isinstance(position, Position):
            self.position = position
            return True
        else:
            return False


class Order:
    def __init__(self, order_id, packet_list):
        self.id = order_id
        self.packet_list = packet_list  # tracking of packet position need proper upgrade
        self.registered_packet_list = [False for i in range(len(packet_list))]

    def __eq__(self, other):
        if isinstance(other, Order):
            if self.id == other.id \
                    and self.packet_list == other.packet_list \
                    and self.registered_packet_list == other.registered_packet_list:
                return True
        return False

    def contain_packet(self, packet):
        if isinstance(packet, Packet) and packet in self.packet_list and packet.position is None:  # packet shouldn't have position assigned at this stage, otherwise it's an anomaly
            return True
        else:
            return False

    def register_packet(self, packet, position):
        if self.contain_packet(packet):
            self.registered_packet_list[self.packet_list.index(packet)] = True
            self.packet_list[self.packet_list.index(packet)].position = position
            print('Packet has been registered as stored')
        else:
            return False


class OrderQueue:
    def __init__(self):
        self.order_list = list()

    def add_order(self, order):  # need to be able to add list of order too
        if isinstance(order, Order):
            self.order_list.append(order)
            return True
        else:
            return False

    def take_out_order_from_queue(self, order):
        if isinstance(order, Order):
            for order_from_queue in self.order_list:
                if order == order_from_queue:
                    self.order_list.remove(order)
                    return order_from_queue
        return False

    def is_packet_in_queue(self, packet, get_order=False):  # will be possible to check if packet exist in queue from future interface, thus we don't always need to get the order
        if isinstance(packet, Packet):
            for order in self.order_list:
                for packet_from_order in order.packet_list:
                    if packet == packet_from_order:

                        if get_order:
                            return order
                        else:
                            return True
        return False


# better struct available ?
class Coordinate:
    def __init__(self, x, y, z, xy=None, xz=None):
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, other):
        if isinstance(other, Coordinate):
            if self.x == other.x \
                    and self.y == other.y \
                    and self.z == other.z:

                return True
        return False


class Position(Coordinate):
    def __init__(self, x, y, z, xy, xz):
        super().__init__(x, y, z)
        self.xy = xy
        self.xz = xz

    def __eq__(self, other):
        if isinstance(other, Position):
            if super().__eq__(other) \
                    and self.xy == other.xy \
                    and self.xz == other.xz:
                return True
        return False

    def rotate(self, angle, axis):  # 90, 180, -90 in each axis only (clockwise, counterclockwise, mirror as choice ?)
        pass
