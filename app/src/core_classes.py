# better struct available ?
class Coordinate:
    def __init__(self, x: int, y: int):
        if not (type(x) is int
                and type(y) is int):
            raise ValueError('Invalid coordinate parameter')
        self.x = x
        self.y = y

    def __eq__(self, other) -> bool:
        if isinstance(other, Coordinate):
            if self.x == other.x and self.y == other.y:
                return True
        return False

    def __repr__(self):
        return f'{self.x}x{self.y}'


class Position(Coordinate):
    def __init__(self, x: int, y: int, z: int, xy: int, xz: int):  # xy and xz are the number of the corresponding faces (0...5)
        if not (type(x) is int
                and type(y) is int
                and type(z) is int
                and type(xy) is int
                and type(xz) is int):
            raise ValueError('Invalid position parameter')
        super().__init__(x, y)
        self.z = z
        self.xy = xy
        self.xz = xz

    def __eq__(self, other) -> bool:
        if isinstance(other, Position):
            if (super().__eq__(other)
                    and self.z == other.z
                    and self.xy == other.xy
                    and self.xz == other.xz):
                return True
            else:
                return False
        else:
            raise ValueError('Invalid parameter')

    def __repr__(self):
        return f'{self.x}x{self.y}x{self.z} xy:{self.xy} xz:{self.xz}'


class Message:
    def __init__(self, bus_channel_id: str):
        if type(bus_channel_id) is not str:
            raise ValueError('Invalid message parameter')
        self.bus_channel = bus_channel_id

    def write_message_to_bus(self, msg: str):  # placeholder function, just a print for now
        if type(msg) is not str:
            raise ValueError('Invalid message parameter')
        print(msg)
        pass

    def read_message_from_bus(self):  # placeholder function
        pass


class Pole(Message):  # async can be disabled (read on confluence, assumed to be True by default)
    def __init__(self, pole_id, async_work=True, bus_channel_id=''):
        if not (type(pole_id) is str
                and type(async_work) is bool):
            raise ValueError('Invalid pole parameter')
        super().__init__(bus_channel_id)
        self.id = pole_id  # raise error if not str, note for later
        self.armoires = []
        self.assigned_orders = list()
        self.async_work = async_work

    def add_armoire(self, armoire, setup: bool = False):
        if isinstance(armoire, Armoire):  # input is an armoire
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
        for packet in order.packet_list:
            for armoire in self.armoires:
                for drawer in armoire.drawers:
                    drawer.take_out_packet(packet)
        return order

    def get_order_completion_rate(self, order):
        if isinstance(order, Order):
            for assigned_order in self.assigned_orders:
                if assigned_order == order:
                    return sum(assigned_order.registered_packet_list) / len(assigned_order.registered_packet_list)
        else:
            raise ValueError('Invalid order parameter')

    def add_packet(self, packet, order, coordinate):  # not complete ?
        if isinstance(packet, Packet) and isinstance(order, Order) and isinstance(coordinate, Coordinate):
            for armoire in self.armoires:
                if armoire.add_packet(packet, coordinate):
                    order.register_packet(packet, coordinate)
                    return True
            return False

    def find_suitable_position(self, packet):  # not complete
        if isinstance(packet, Packet):
            for armoire in self.armoires:
                suitable_position = armoire.find_suitable_position(packet)
                if suitable_position is not None:
                    return suitable_position
        else:
            raise ValueError('Invalid packet parameter')


class Armoire:
    def __init__(self, armoire_id, capacity):
        if not (type(armoire_id) is str
                and type(capacity) is int):
            raise ValueError('Invalid armoire parameter')
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

    def add_packet(self, packet, coordinate):
        for drawer in self.drawers:
            if drawer.add_packet(packet, coordinate):
                return True
        return False

    def find_suitable_position(self, packet):
        for drawer in self.drawers:
            suitable_position = drawer.find_suitable_position(packet)
            if suitable_position is not None:
                return suitable_position
        return None





class Drawer:
    def __init__(self, drawer_id, length: int, width: int, height: int, margin: int, safety_margin: float = 1.1):
        if not (isinstance(drawer_id, str)
                and isinstance(length, int)
                and isinstance(width, int)
                and isinstance(height, int)
                and isinstance(margin, int)
                and isinstance(safety_margin, float)):
            raise ValueError('Invalid drawer parameter')
        self.id = drawer_id
        self.length = length
        self.width = width
        self.height = height
        self.margin = margin    # should be equal to half of the space needed for the robot arm to grab the packet
                                # (this way, even if double the value is set as input, the packets' integrity will be maintained)
        self.safety_margin = safety_margin
        self.packets = []

    def find_suitable_position(self, packet) -> Coordinate | None:  # to complete
        padded_dimension = packet.get_padded_dimension(self.margin, self.safety_margin)
        if (self.get_drawer_area() - self.get_used_area() > padded_dimension.x * padded_dimension.y
                and packet.real_dimension.z < self.height):
            # for position in (padded_dimension, packet.rotate('x', self.margin, self.safety_margin), packet.rotate('y', self.margin, self.safety_margin), packet.rotate('z', self.margin, self.safety_margin)):
            if len(self.packets) != 0:
                for x in range(self.length - padded_dimension.x):
                    for y in range(self.width - padded_dimension.y):
                        temp_bool = True
                        for stored_packet in self.packets:
                            if not (stored_packet.stored_position.x <= x <= stored_packet.stored_position.x + stored_packet.padded_dimension.x
                                    and stored_packet.stored_position.y <= y <= stored_packet.stored_position.y + stored_packet.padded_dimension.y
                                    or
                                    stored_packet.stored_position.x <= x + padded_dimension.x <= stored_packet.stored_position.x + stored_packet.padded_dimension.x
                                    and stored_packet.stored_position.y <= y + padded_dimension.y <= stored_packet.stored_position.y + stored_packet.padded_dimension.y
                                    and x + padded_dimension.x < self.length
                                    and y + padded_dimension.y < self.width):
                                temp_bool &= True
                            else:
                                temp_bool &= False
                        if temp_bool:
                            packet.padded_dimension = padded_dimension
                            return Coordinate(x, y)
                        else:
                            continue
            else:
                packet.padded_dimension = padded_dimension
                return Coordinate(0, 0)
        return None  # not enough space or no suitable place found

    def add_packet(self, packet, coordinate):
        packet.stored_position = coordinate
        self.packets.append(packet)
        return True

    def take_out_packet(self, packet):
        if isinstance(packet, Packet):
            if packet in self.packets:
                self.packets.remove(packet)
        else:
            raise ValueError('Invalid parameter')

    def get_used_area(self):
        return sum(packet.get_padded_area() for packet in self.packets)

    def get_drawer_area(self):
        return self.length * self.width


# type, dimension propre (Xc, Yc, Zc),
# dimension réelle (Xr, Yr, Zr),
# position (X, Y, Z, face XY, face XZ),
# id (optional)
class Packet:
    def __init__(self, packet_type, absolute_dimension, real_dimension, ko_face=(1, 5), xy_rotation_enabled=True, yz_rotation_enabled=True, zx_rotation_enabled=True):
        if not (isinstance(packet_type, str)
                and isinstance(absolute_dimension, Position)
                and (isinstance(real_dimension, Position) or real_dimension is None)
                and isinstance(ko_face, tuple)
                and type(xy_rotation_enabled) is bool
                and type(yz_rotation_enabled) is bool
                and type(zx_rotation_enabled) is bool):
            raise ValueError('Invalid packet parameter')
        self.packet_type = packet_type
        self.absolute_dimension = absolute_dimension
        self.real_dimension = real_dimension
        self.ko_face = ko_face
        self.padded_dimension = None
        self.xy_rotation_enabled = xy_rotation_enabled
        self.yz_rotation_enabled = yz_rotation_enabled
        self.zx_rotation_enabled = zx_rotation_enabled
        self.stored_position = ()

    def __eq__(self, other) -> bool:
        if isinstance(other, Packet) \
                and self.packet_type == other.packet_type \
                and self.absolute_dimension == other.absolute_dimension \
                and self.real_dimension == other.real_dimension \
                and ((self.stored_position is None and other.stored_position is None) or self.stored_position == other.stored_position):
            return True
        else:
            return False

    def set_real_dimension(self, real_dimension: Position, margin: int, safety_margin: float ):
        if isinstance(real_dimension, Position):
            self.real_dimension = real_dimension
            self.set_padded_dimension(margin, safety_margin)
        else:
            raise ValueError('Invalid parameter')

    def get_padded_area(self) -> int | None:
        if self.padded_dimension is not None:
            return self.padded_dimension.x * self.padded_dimension.y

    def set_position(self, coordinate):
        if isinstance(coordinate, Coordinate):
            self.stored_position = coordinate
            return True
        else:
            return False

    def get_padded_dimension(self, margin: int, safety_margin: float):
        return Position(round(self.real_dimension.x + 2 * margin * safety_margin),
                        round(self.real_dimension.y + 2 * margin * safety_margin),
                        round(self.real_dimension.z + 2 * margin * safety_margin),
                        self.real_dimension.xy,
                        self.real_dimension.xz)

    def set_padded_dimension(self, margin: int, safety_margin: float):
        self.padded_dimension = self.get_padded_dimension(margin, safety_margin)

    def rotate(self, axis, margin: int, safety_margin: float, clockwise: bool = True):  # need to finish
        if type(axis) is str and axis in ('x', 'y', 'z'):
            if axis == 'x' and self.yz_rotation_enabled:
                if clockwise:
                    self.set_real_dimension(Position(self.real_dimension.x, self.real_dimension.z, self.real_dimension.y, 4, 0), margin, safety_margin)
            elif axis == 'y' and self.zx_rotation_enabled:
                if clockwise:
                    self.set_real_dimension(Position(self.real_dimension.z, self.real_dimension.y, self.real_dimension.x, 3, 1), margin, safety_margin)
                else:
                    self.set_real_dimension(Position(self.real_dimension.x, self.real_dimension.z, self.real_dimension.y, 2, 1), margin, safety_margin)
            elif axis == 'z' and self.xy_rotation_enabled:
                if clockwise:
                    self.set_real_dimension(Position(self.real_dimension.y, self.real_dimension.x, self.real_dimension.z, 0, 2), margin, safety_margin)
                else:
                    self.set_real_dimension(Position(self.real_dimension.x, self.real_dimension.z, self.real_dimension.y, 0, 3), margin, safety_margin)
        else:
            raise ValueError('Invalid parameter')


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

    def contain_packet(self, packet: Packet):
        if isinstance(packet, Packet) and packet in self.packet_list and packet.stored_position is None:  # packet shouldn't have stored_position assigned at this stage, otherwise it's an anomaly
            return True
        else:
            return False

    def register_packet(self, packet, coordinate):  # need to handle position (real and padded dimension) as well
        if self.contain_packet(packet):
            self.registered_packet_list[self.packet_list.index(packet)] = True
            self.packet_list[self.packet_list.index(packet)].stored_position = coordinate
            print('Packet has been stored')
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



