import struct
from typing import ClassVar

from pydantic import BaseModel, computed_field
from pydantic_extra_types.mac_address import MacAddress

from aiolifx.resources.const import BROADCAST_MAC, HEADER_SIZE_BYTES
from aiolifx.resources.message_types import MessageType

# reverses bytes for little endian, then converts to int


def little_endian(bs):
    return bytes(reversed(bs.bytes))


class Message(BaseModel):
    message_type: MessageType
    # Frame

    size_struct: ClassVar[struct.Struct] = struct.Struct("<H")
    flags_struct: ClassVar[struct.Struct] = struct.Struct("<H")
    source_id_struct: ClassVar[struct.Struct] = struct.Struct("<L")
    size: int | None = None  # 16 bits/uint16
    origin: int = 0  # 2 bits/uint8, must be zero
    addressable: bool = 1  # 1 bit/bool, must be one
    protocol: int = 1024  # 12 bits/uint16
    source_id: int  # 32 bits/uint32, unique ID set by client. If zero, broadcast reply requested. If non-zero, unicast reply requested.

    # Frame Address
    mac_addr_struct: ClassVar[struct.Struct] = struct.Struct("<Q")
    reserved_48_struct: ClassVar[struct.Struct] = struct.Struct("<BBBBBB")
    response_flags_struct: ClassVar[struct.Struct] = struct.Struct("<B")
    seq_num_struct: ClassVar[struct.Struct] = struct.Struct("<B")
    target_addr: MacAddress = BROADCAST_MAC  # 64 bits/uint64, either single MAC address or all zeroes for broadcast.
    reserved: int = 0  # 48 bits/uint8 x 6, all zero
    ack_requested: bool = False  # 1 bit/bool, 1 = yes
    response_requested: bool = False  # 1 bit/bool, 1 = yes
    seq_num: int  # 8 bits/uint8, wraparound

    # Protocol Header
    reserved_64_struct: ClassVar[struct.Struct] = struct.Struct("<Q")
    message_type_struct: ClassVar[struct.Struct] = struct.Struct("<H")
    reserved_16_struct: ClassVar[struct.Struct] = struct.Struct("<H")

    _packed_message = None

    @computed_field
    @property
    def tagged(self) -> int:
        return self.target_addr == BROADCAST_MAC

    @property
    def packed_message(self):
        if self._packed_message is None:
            self._packed_message = self.generate_packed_message()
        return self._packed_message

    @packed_message.setter
    def packed_message(self, value) -> None:
        self._packed_message = value

    def target_address_int(self) -> int:
        reverse_bytes_str = self.target_addr.split(":")
        reverse_bytes_str.reverse()
        addr_str = "".join(reverse_bytes_str)
        return int(addr_str, 16)

    def generate_packed_message(self) -> bytes:
        payload = self.get_payload()
        header = self.get_header()
        return header + payload

    # frame (and thus header) needs to be generated after payload (for size field)
    def get_header(self) -> bytes:
        if self.size is None:
            self.size = self.get_msg_size()
        frame_addr = self.get_frame_addr()
        frame = self.get_frame()
        protocol_header = self.get_protocol_header()
        return frame + frame_addr + protocol_header

    # Default: No payload unless method overridden
    def get_payload(self) -> bytes:
        return struct.pack("")

    def get_frame(self) -> bytes:
        size = self.size_struct.pack(self.size)
        flags = self.flags_struct.pack(((self.origin & 0b11) << 14) | ((self.tagged & 0b1) << 13) | ((self.addressable & 0b1) << 12) | (self.protocol & 0b111111111111))
        source_id = self.source_id_struct.pack(self.source_id)
        return size + flags + source_id

    def get_frame_addr(self) -> bytes:
        mac_addr = self.mac_addr_struct.pack(self.target_address_int())
        reserved_48 = self.reserved_48_struct.pack(*([self.reserved] * 6))
        response_flags = self.response_flags_struct.pack(((self.reserved & 0b111111) << 2) | ((self.ack_requested & 0b1) << 1) | (self.response_requested & 0b1))
        seq_num = self.seq_num_struct.pack(self.seq_num)
        return mac_addr + reserved_48 + response_flags + seq_num

    def get_protocol_header(self) -> bytes:
        reserved_64 = self.reserved_64_struct.pack(self.reserved)
        message_type = self.message_type_struct.pack(self.message_type)
        reserved_16 = self.reserved_16_struct.pack(self.reserved)
        return reserved_64 + message_type + reserved_16

    def get_msg_size(self) -> int:
        payload_size_bytes = len(self.payload)
        return HEADER_SIZE_BYTES + payload_size_bytes
