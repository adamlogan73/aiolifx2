from enum import Enum
from enum import IntEnum
from random import randrange
from typing import Any

import bitstring
from pydantic import BaseModel

from aiolifx.models.message import Message
from aiolifx.models.message import little_endian


def uint8_format(d: int) -> bytes:
    return little_endian(bitstring.pack("uint:8", d))


def int8_format(d: int) -> bytes:
    return little_endian(bitstring.pack("int:8", d))


def uint16_format(d: int) -> bytes:
    return little_endian(bitstring.pack("uint:16", d))


def int16_format(d: int) -> bytes:
    return little_endian(bitstring.pack("int:16", d))


def uint32_format(d: int) -> bytes:
    return little_endian(bitstring.pack("uint:32", d))


def int32_format(d: int) -> bytes:
    return little_endian(bitstring.pack("int:32", d))


def float32_format(d: float) -> bytes:
    return little_endian(bitstring.pack("float:32", d))


def float_format(d: float) -> bytes:
    return little_endian(bitstring.pack("float", d))


def uint64_format(d: int) -> bytes:
    return little_endian(bitstring.pack("uint:64", d))


class MessageType(IntEnum):
    GetService = 2
    StateService = 3
    GetHostInfo = 12
    StateHostInfo = 13
    GetHostFirmware = 14
    StateHostFirmware = 15
    GetWifiInfo = 16
    StateWifiInfo = 17
    GetWifiFirmware = 18
    StateWifiFirmware = 19
    GetPower = 20
    SetPower = 21
    StatePower = 22
    GetLabel = 23
    SetLabel = 24
    StateLabel = 25
    GetVersion = 32
    StateVersion = 33
    GetInfo = 34
    StateInfo = 35
    SetReboot = 38
    Acknowledgement = 45
    GetLocation = 48
    StateLocation = 50
    GetGroup = 51
    StateGroup = 53
    EchoRequest = 58
    EchoResponse = 59
    LightGet = 101
    LightSetColor = 102
    LightSetWaveform = 103
    LightState = 107
    LightGetPower = 116
    LightSetPower = 117
    LightStatePower = 118
    LightSetWaveformOptional = 119
    LightGetInfrared = 120
    LightStateInfrared = 121
    LightSetInfrared = 122
    GetHevCycle = 142
    SetHevCycle = 143
    StateHevCycle = 144
    GetHevCycleConfiguration = 145
    SetHevCycleConfiguration = 146
    StateHevCycleConfiguration = 147
    GetLastHevCycleResult = 148
    StateLastHevCycleResult = 149
    MultiZoneSetColorZones = 501
    MultiZoneGetColorZones = 502
    MultiZoneStateZone = 503
    MultiZoneStateMultiZone = 506
    MultiZoneGetMultiZoneEffect = 507
    MultiZoneSetMultiZoneEffect = 508
    MultiZoneStateMultiZoneEffect = 509
    MultiZoneSetExtendedColorZones = 510
    MultiZoneGetExtendedColorZones = 511
    MultiZoneStateExtendedColorZones = 512
    TileGetDeviceChain = 701
    TileStateDeviceChain = 702
    TileGet64 = 707
    TileState64 = 711
    TileSet64 = 715
    TileGetTileEffect = 718
    TileSetTileEffect = 719
    TileStateTileEffect = 720
    GetRPower = 816
    SetRPower = 817
    StateRPower = 818
    GetButton = 905
    SetButton = 906
    StateButton = 907
    GetButtonConfig = 909
    SetButtonConfig = 910
    StateButtonConfig = 911


class ButtonGesture(Enum):
    PRESS = 1
    HOLD = 2
    PRESS_PRESS = 3
    PRESS_HOLD = 4
    HOLD_HOLD = 5


class ButtonTargetType(Enum):
    RELAYS = 2
    DEVICE = 3
    LOCATION = 4
    GROUP = 5
    SCENE = 6
    DEVICE_RELAYS = 7


class MultiZoneEffectType(Enum):
    OFF = 0
    MOVE = 1
    RESERVED1 = 2
    RESERVED2 = 3


class MultiZoneDirection(Enum):
    RIGHT = 0
    LEFT = 1
    BACKWARD = 0
    FORWARD = 1


class TileEffectType(Enum):
    OFF = 0
    RESERVED1 = 1
    MORPH = 2
    FLAME = 3
    RESERVED2 = 4
    SKY = 5


class TileEffectSkyType(Enum):
    SUNRISE = 0
    SUNSET = 1
    CLOUDS = 2


class ButtonTargetRelays:
    def __init__(self, data) -> None:
        self.relays_count = data[0]
        self.relays = data[1 : 1 + self.relays_count]


class ButtonTargetDevice:
    def __init__(self, data) -> None:
        self.serial = data[0:6]
        self.reserved = data[6:16]


class ButtonTargetDeviceRelays:
    def __init__(self, data) -> None:
        self.serial = data[0:6]
        self.relays_count = data[6]
        self.relays = data[7 : 7 + self.relays_count]


class GetService(Message):
    message_type: MessageType = MessageType.GetService


class StateServicePayload(BaseModel):
    service: int
    port: int


class StateService(Message):
    message_type: MessageType = MessageType.StateService
    payload: StateServicePayload

    def get_payload(self) -> bytes:
        service = uint8_format(self.payload.service)
        port = uint32_format(self.payload.port)
        return service + port


class GetHostInfo(Message):
    message_type: MessageType = MessageType.GetHostInfo


class StateHostInfoPayload(BaseModel):
    signal: float
    tx: int
    rx: int
    reserved1: int


class StateHostInfo(Message):
    message_type: MessageType = MessageType.StateHostInfo
    payload: StateHostInfoPayload

    def get_payload(self) -> bytes:
        signal = float32_format(self.payload.signal)
        tx = uint32_format(self.payload.tx)
        rx = uint32_format(self.payload.rx)
        reserved1 = int16_format(self.payload.reserved1)
        return signal + tx + rx + reserved1


class GetHostFirmware(Message):
    message_type: MessageType = MessageType.GetHostFirmware


class StateHostFirmwarePayload(BaseModel):
    build: int
    reserved1: int
    version: int


class StateHostFirmware(Message):
    message_type: MessageType = MessageType.StateHostFirmware
    payload: StateHostFirmwarePayload

    def get_payload(self) -> bytes:
        build = uint64_format(self.payload.build)
        reserved1 = uint64_format(self.payload.reserved1)
        version = uint32_format(self.payload.version)
        return build + reserved1 + version


class GetWifiInfo(Message):
    message_type: MessageType = MessageType.GetWifiInfo


class StateWifiInfoPayload(BaseModel):
    signal: float
    tx: int
    rx: int
    reserved1: int


class StateWifiInfo(Message):
    message_type: MessageType = MessageType.StateWifiInfo
    payload: StateWifiInfoPayload

    def get_payload(self) -> bytes:
        signal = float32_format(self.payload.signal)
        tx = uint32_format(self.payload.tx)
        rx = uint32_format(self.payload.rx)
        reserved1 = int16_format(self.payload.reserved1)
        return signal + tx + rx + reserved1


class GetWifiFirmware(Message):
    message_type: MessageType = MessageType.GetWifiFirmware


class StateWifiFirmwarePayload(BaseModel):
    build: int
    reserved1: Any
    version: int


class StateWifiFirmware(Message):
    message_type: MessageType = MessageType.StateWifiFirmware
    payload: StateWifiFirmwarePayload

    def get_payload(self) -> bytes:
        build = uint64_format(self.payload.build)
        reserved1 = uint64_format(self.payload.reserved1)
        version = uint32_format(self.payload.version)
        return build + reserved1 + version


class GetPower(Message):
    message_type: MessageType = MessageType.GetPower


class PowerPayload(BaseModel):
    power_level: int


class SetPower(Message):
    message_type: MessageType = MessageType.SetPower
    payload: PowerPayload

    def get_payload(self) -> bytes:
        return uint16_format(self.payload.power_level)


class StatePower(Message):
    message_type: MessageType = MessageType.StatePower
    payload: PowerPayload

    def get_payload(self) -> bytes:
        return uint16_format(self.payload.power_level)


class GetLabel(Message):
    message_type: MessageType = MessageType.GetLabel


class LabelPayload(BaseModel):
    label: str


class SetLabel(Message):
    message_type: MessageType = MessageType.SetLabel
    payload: LabelPayload

    def get_payload(self) -> bytes:
        field_len_bytes = 32
        label = b"".join(uint8_format(ord(c)) for c in self.payload.label)
        padding = b"".join(
            uint8_format(0) for i in range(field_len_bytes - len(self.payload.label))
        )
        return label + padding


class StateLabel(Message):
    message_type: MessageType = MessageType.StateLabel
    payload: LabelPayload

    def get_payload(self) -> bytes:
        field_len_bytes = 32
        label = b"".join(uint8_format(c) for c in self.payload.label)
        padding = b"".join(
            uint8_format(0) for i in range(field_len_bytes - len(self.payload.label))
        )
        return label + padding


class GetVersion(Message):
    message_type: MessageType = MessageType.GetVersion


class StateVersionPayload(BaseModel):
    vendor: int
    product: int
    version: int


class StateVersion(Message):
    message_type: MessageType = MessageType.StateVersion
    payload: StateVersionPayload

    def get_payload(self) -> bytes:
        vendor = uint32_format(self.payload.vendor)
        product = uint32_format(self.payload.product)
        version = uint32_format(self.payload.version)
        return vendor + product + version


class GetInfo(Message):
    message_type: MessageType = MessageType.GetInfo


class StateInfoPayload(BaseModel):
    time: int
    uptime: int
    downtime: int


class StateInfo(Message):
    message_type: MessageType = MessageType.StateInfo
    payload: StateInfoPayload

    def get_payload(self) -> bytes:
        time = uint64_format(self.payload.time)
        uptime = uint64_format(self.payload.uptime)
        downtime = uint64_format(self.payload.downtime)
        return time + uptime + downtime


class GetLocation(Message):
    message_type: MessageType = MessageType.GetLocation


class LocationPayload(BaseModel):
    location: list[int]
    label: str
    updated_at: int


class StateLocation(Message):
    message_type: MessageType = MessageType.StateLocation
    payload: LocationPayload

    def get_payload(self) -> bytes:
        location = b"".join(uint8_format(b) for b in self.payload.location)
        label = b"".join(uint8_format(c) for c in self.payload.label)
        label_padding = b"".join(
            uint8_format(0) for i in range(32 - len(self.payload.label))
        )
        updated_at = uint64_format(self.payload.updated_at)
        return location + label + label_padding + updated_at


class GetGroup(Message):
    message_type: MessageType = MessageType.GetGroup


class GroupPayload(BaseModel):
    group: list[int]
    label: str
    updated_at: int


class StateGroup(Message):
    message_type: MessageType = MessageType.StateGroup
    payload: GroupPayload

    def get_payload(self) -> bytes:
        group = b"".join(uint8_format(b) for b in self.payload.group)
        label = b"".join(uint8_format(c) for c in self.payload.label)
        label_padding = b"".join(
            uint8_format(0) for i in range(32 - len(self.payload.label))
        )
        label += label_padding
        updated_at = uint64_format(self.payload.updated_at)
        return group + label + updated_at


class SetReboot(Message):
    message_type: MessageType = MessageType.SetReboot


class Acknowledgement(Message):
    message_type: MessageType = MessageType.Acknowledgement


class ByteArrayPayload(BaseModel):
    byte_array: str


class EchoRequest(Message):
    message_type: MessageType = MessageType.EchoRequest
    payload: ByteArrayPayload

    def get_payload(self) -> bytes:
        field_len = 64
        byte_array = b"".join(uint8_format(b) for b in self.payload.byte_array)
        byte_array_len = len(byte_array)
        if byte_array_len < field_len:
            byte_array += b"".join(
                uint8_format(0) for i in range(field_len - byte_array_len)
            )
        elif byte_array_len > field_len:
            byte_array = byte_array[:field_len]
        return byte_array


class EchoResponse(Message):
    message_type: MessageType = MessageType.EchoResponse
    payload: ByteArrayPayload

    def get_payload(self) -> bytes:
        return b"".join(uint8_format(b) for b in self.payload.byte_array)


##### LIGHT MESSAGES #####


class LightGet(Message):
    message_type: MessageType = MessageType.LightGet


class SetColorPayload(BaseModel):
    color: list[int]
    duration: int


class LightSetColor(Message):
    message_type: MessageType = MessageType.LightSetColor
    payload: SetColorPayload

    def get_payload(self) -> bytes:
        reserved_8 = uint8_format(self.reserved)
        color = b"".join(uint16_format(field) for field in self.payload.color)
        duration = uint32_format(self.payload.duration)
        return reserved_8 + color + duration


class WaveFormPayload(BaseModel):
    transient: int
    color: list[int]
    period: int
    cycles: int
    skew_ratio: int
    waveform: int


class LightSetWaveform(Message):
    message_type: MessageType = MessageType.LightSetWaveform
    payload: WaveFormPayload

    def get_payload(self) -> bytes:
        reserved_8 = uint8_format(self.reserved)
        transient = uint8_format(self.payload.transient)
        color = b"".join(uint16_format(field) for field in self.payload.color)
        period = uint32_format(self.payload.period)
        cycles = float32_format(self.payload.cycles)
        skew_ratio = int16_format(self.payload.skew_ratio)
        waveform = uint8_format(self.payload.waveform)

        return reserved_8 + transient + color + period + cycles + skew_ratio + waveform


class WaveFormPayloadOptional(WaveFormPayload):
    hue: int
    set_saturation: int
    set_brightness: int
    set_kelvin: int
    set_hue: int


class LightSetWaveformOptional(Message):
    message_type: MessageType = MessageType.LightSetWaveform
    payload: WaveFormPayloadOptional

    def get_payload(self) -> bytes:
        reserved_8 = uint8_format(self.reserved)
        transient = uint8_format(self.payload.transient)
        color = b"".join(uint16_format(field) for field in self.payload.color)
        period = uint32_format(self.payload.period)
        cycles = float32_format(self.payload.cycles)
        skew_ratio = int16_format(self.payload.skew_ratio)
        waveform = uint8_format(self.payload.waveform)
        set_hue = uint8_format(self.payload.set_hue)
        set_saturation = uint8_format(self.payload.set_saturation)
        set_brightness = uint8_format(self.payload.set_brightness)
        set_kelvin = uint8_format(self.payload.set_kelvin)

        return (
            reserved_8
            + transient
            + color
            + period
            + cycles
            + skew_ratio
            + waveform
            + set_hue
            + set_saturation
            + set_brightness
            + set_kelvin
        )


class LightStatePayload(BaseModel):
    color: list[int]
    reserved1: int
    power_level: int
    label: int
    reserved2: int


class LightState(Message):
    message_type: MessageType = MessageType.LightState
    payload: LightStatePayload

    def get_payload(self) -> bytes:
        color = b"".join(uint16_format(field) for field in self.payload.color)
        reserved1 = int16_format(self.payload.reserved1)
        power_level = uint16_format(self.payload.power_level)
        label = self.payload.label.ljust(32, b"\0")
        reserved2 = uint64_format(self.payload.reserved2)
        return color + reserved1 + power_level + label + reserved2


class LightGetPower(Message):
    message_type: MessageType = MessageType.LightGetPower


class SetPowerPayload(PowerPayload):
    duration: int


class LightSetPower(Message):
    message_type: MessageType = MessageType.LightSetPower
    payload: SetPowerPayload

    def get_payload(self) -> bytes:
        power_level = uint16_format(self.payload.power_level)
        duration = uint32_format(self.payload.duration)
        return power_level + duration


class LightStatePower(Message):
    message_type: MessageType = MessageType.LightStatePower
    payload: PowerPayload

    def get_payload(self) -> bytes:
        return uint16_format(self.payload.power_level)


##### INFRARED MESSAGES #####


class LightGetInfrared(Message):
    message_type: MessageType = MessageType.LightGetInfrared


class InfraredBrightnessPayload(BaseModel):
    infrared_brightness: int


class LightStateInfrared(Message):
    message_type: MessageType = MessageType.LightStateInfrared
    payload: InfraredBrightnessPayload

    def get_payload(self) -> bytes:
        return uint16_format(self.payload.infrared_brightness)


class LightSetInfrared(Message):
    message_type: MessageType = MessageType.LightSetInfrared
    payload: InfraredBrightnessPayload

    def get_payload(self) -> bytes:
        return uint16_format(self.payload.infrared_brightness)


##### HEV (LIFX Clean) MESSAGES #####
# https://lan.developer.lifx.com/docs/hev-light-control


class GetHevCycle(Message):
    message_type: MessageType = MessageType.GetHevCycle


class HevCyclePayload(BaseModel):
    enable: bool
    duration: int


class SetHevCycle(Message):
    message_type: MessageType = MessageType.SetHevCycle
    payload: HevCyclePayload

    def get_payload(self) -> bytes:
        enable = uint8_format(self.payload.enable)
        duration = uint32_format(self.payload.duration)
        return enable + duration


class StateHevCyclePayload(BaseModel):
    duration: int
    remaining: int
    last_power: int


class StateHevCycle(Message):
    message_type: MessageType = MessageType.StateHevCycle
    payload: StateHevCyclePayload

    def get_payload(self) -> bytes:
        duration = uint32_format(self.payload.duration)
        remaining = uint32_format(self.payload.remaining)
        last_power = uint8_format(self.payload.last_power)
        return duration + remaining + last_power


class GetHevCycleConfiguration(Message):
    message_type: MessageType = MessageType.GetHevCycleConfiguration


class HevCycleConfigurationPayload(BaseModel):
    indication: int
    duration: int


class SetHevCycleConfiguration(Message):
    message_type: MessageType = MessageType.SetHevCycleConfiguration
    payload: HevCycleConfigurationPayload

    def get_payload(self) -> bytes:
        indication = uint8_format(self.payload.indication)
        duration = uint32_format(self.payload.duration)
        return indication + duration


class StateHevCycleConfigurationPayload(Message):
    indication: int
    duration: int


class StateHevCycleConfiguration(Message):
    message_type: MessageType = MessageType.StateHevCycleConfiguration
    payload: StateHevCycleConfigurationPayload

    def get_payload(self) -> bytes:
        indication = uint8_format(self.payload.indication)
        duration = uint32_format(self.payload.duration)
        return indication + duration


class GetLastHevCycleResult(Message):
    message_type: MessageType = MessageType.GetLastHevCycleResult


class ResultPayload(BaseModel):
    result: int


class StateLastHevCycleResult(Message):
    message_type: MessageType = MessageType.StateLastHevCycleResult
    payload: ResultPayload

    def get_payload(self) -> bytes:
        return uint8_format(self.payload.result)

    @property
    def result_str(self) -> str:
        return LAST_HEV_CYCLE_RESULT.get(self.payload.result, "UNKNOWN")


##### MULTIZONE MESSAGES #####


class MultiZoneStateMultiZonePayload(BaseModel):
    count: int
    index: int
    color: list[list[int]]


class MultiZoneStateMultiZone(Message):
    message_type: MessageType = MessageType.MultiZoneStateMultiZone
    payload: MultiZoneStateMultiZonePayload

    def get_payload(self) -> bytes:
        count = uint8_format(self.payload.count)
        index = uint8_format(self.payload.index)
        payload = count + index
        for color in self.payload.color:
            payload += b"".join(uint16_format(field) for field in color)
        return payload


class MultiZoneStateZonePayload(BaseModel):
    count: int
    index: int
    color: list[int]


class MultiZoneStateZone(Message):  # 503
    message_type: MessageType = MessageType.MultiZoneStateZone
    payload: MultiZoneStateZonePayload

    def get_payload(self) -> bytes:
        count = uint8_format(self.payload.count)
        index = uint8_format(self.payload.index)
        color = b"".join(uint16_format(field) for field in self.payload.color)
        return count + index + color


class MultiZoneSetColorZonesPayload(BaseModel):
    start_index: int
    end_index: int
    color: list[int]
    duration: int
    apply: int


class MultiZoneSetColorZones(Message):
    message_type: MessageType = MessageType.MultiZoneSetColorZones
    payload: MultiZoneSetColorZonesPayload

    def get_payload(self) -> bytes:
        start_index = uint8_format(self.payload.start_index)
        end_index = uint8_format(self.payload.end_index)
        color = b"".join(uint16_format(field) for field in self.payload.color)
        duration = uint32_format(self.payload.duration)
        apply = uint8_format(self.payload.apply)
        return start_index + end_index + color + duration + apply


class MultiZoneGetColorZonesPayload(BaseModel):
    start_index: int
    end_index: int


class MultiZoneGetColorZones(Message):
    message_type: MessageType = MessageType.MultiZoneGetColorZones
    payload: MultiZoneGetColorZonesPayload

    def get_payload(self) -> bytes:
        start_index = uint8_format(self.payload.start_index)
        end_index = uint8_format(self.payload.end_index)
        return start_index + end_index


class MultiZoneGetMultiZoneEffect(Message):
    message_type: MessageType = MessageType.MultiZoneGetMultiZoneEffect


class MultiZoneSetMultiZoneEffectPayload(BaseModel):
    instanceid: int = randrange(1, 1 << 32)
    type: int
    speed: int
    duration: int
    direction: int


class MultiZoneSetMultiZoneEffect(Message):
    message_type: MessageType = MessageType.MultiZoneSetMultiZoneEffect
    payload: MultiZoneSetMultiZoneEffectPayload

    def get_payload(self) -> bytes:
        instanceid = uint32_format(self.payload.instanceid)
        type = uint8_format(self.payload.type)
        reserved6 = int16_format(2)
        speed = uint32_format(self.payload.speed)
        duration = uint64_format(self.payload.duration)
        reserved7 = int32_format(4)
        reserved8 = int32_format(4)
        parameter1 = uint32_format(4)
        direction = uint32_format(self.payload.direction)
        parameter3 = uint32_format(4)

        return (
            instanceid
            + type
            + reserved6
            + speed
            + duration
            + reserved7
            + reserved8
            + parameter1
            + direction
            + parameter3 * 6
        )


class MultiZoneSetMultiZoneEffectPayload(BaseModel):
    instanceid: int
    effect: MultiZoneEffectType
    speed: int
    duration: int
    direction: MultiZoneDirection


class MultiZoneStateMultiZoneEffect(Message):
    message_type: MessageType = MessageType.MultiZoneStateMultiZoneEffect
    payload: MultiZoneSetMultiZoneEffectPayload

    def get_payload(self) -> bytes:
        instanceid = uint32_format(self.payload.instanceid)
        effect = uint8_format(self.payload.effect.value)
        speed = uint32_format(self.payload.speed)
        duration = uint64_format(self.payload.duration)
        parameter1 = b"".join(uint8_format(8))
        direction = b"".join(uint8_format(c) for c in self.payload.direction)
        direction_padding = b"".join(
            uint8_format(0) for i in range(8 - len(self.payload.direction))
        )
        direction += direction_padding
        parameter3 = b"".join(uint8_format(8))
        parameter4 = b"".join(uint8_format(8))
        return (
            instanceid
            + effect
            + speed
            + duration
            + parameter1
            + direction
            + parameter3
            + parameter4
        )

    @property
    def effect_str(self) -> str:
        return self.payload.effect.name.upper()

    @property
    def direction_str(self) -> str:
        return self.payload.direction.name.lower()


class MultiZoneSetExtendedColorZonesPayload(BaseModel):
    duration: int
    apply: int
    zone_index: int
    colors_count: int
    colors: list[list[int]]


class MultiZoneSetExtendedColorZones(Message):
    message_type: MessageType = MessageType.MultiZoneSetExtendedColorZones
    payload: MultiZoneSetExtendedColorZonesPayload

    def get_payload(self) -> bytes:
        duration = uint32_format(self.payload.duration)
        apply = uint8_format(self.payload.apply)
        zone_index = uint16_format(self.payload.zone_index)
        colors_count = uint8_format(self.payload.colors_count)
        payload = duration + apply + zone_index + colors_count
        for color in self.payload.colors:
            payload += b"".join(uint16_format(field) for field in color)
        return payload


class MultiZoneGetExtendedColorZones(Message):
    message_type: MessageType = MessageType.MultiZoneGetExtendedColorZones


class MultiZoneStateExtendedColorZonesPayload(BaseModel):
    zones_count: int
    zone_index: int
    colors_count: int
    colors: list[list[int]]


class MultiZoneStateExtendedColorZones(Message):
    message_type: MessageType = MessageType.MultiZoneStateExtendedColorZones
    payload: MultiZoneStateExtendedColorZonesPayload

    def get_payload(self) -> bytes:
        zones_count = uint16_format(self.payload.zones_count)
        zone_index = uint16_format(self.payload.zone_index)
        colors_count = uint8_format(self.payload.colors_count)
        payload = zones_count + zone_index + colors_count
        for color in self.payload.colors:
            payload += b"".join(uint16_format(field) for field in color)
        return payload


class TileGetDeviceChain(Message):
    message_type: MessageType = MessageType.TileGetDeviceChain


class TileDevice(BaseModel):
    accel_meas_x: int
    accel_meas_y: int
    accel_meas_z: int
    user_x: float
    user_y: float
    width: int
    height: int
    device_version_vendor: int
    device_version_product: int
    firmware_build: int
    firmware_version_minor: int
    firmware_version_major: int


class TileStateDeviceChainPayload(BaseModel):
    start_index: int
    tile_devices: list[TileDevice]
    tile_devices_count: int


class TileStateDeviceChain(Message):
    message_type: MessageType = MessageType.TileStateDeviceChain
    payload: TileStateDeviceChainPayload

    def get_payload(self) -> bytes:
        start_index = uint8_format(self.payload.start_index)
        tile_devices = b""
        for tile_device in self.payload.tile_devices:
            tile_devices += b"".join(
                [
                    int16_format(tile_device.accel_meas_x),
                    int16_format(tile_device.accel_meas_y),
                    int16_format(tile_device.accel_meas_z),
                    float_format(tile_device.user_x),
                    float_format(tile_device.user_y),
                    uint8_format(tile_device.width),
                    uint8_format(tile_device.height),
                    uint32_format(tile_device.device_version_vendor),
                    uint32_format(tile_device.device_version_product),
                    uint64_format(tile_device.firmware_build),
                    uint16_format(tile_device.firmware_version_minor),
                    uint16_format(tile_device.firmware_version_major),
                ]
            )
        tile_devices_count = uint8_format(self.payload.tile_devices_count)
        return start_index + tile_devices + tile_devices_count


class TileGet64Payload(BaseModel):
    tile_index: int
    length: int
    x: int
    y: int
    width: int


class TileGet64(Message):
    message_type: MessageType = MessageType.TileGet64
    payload: TileGet64Payload

    def get_payload(self) -> bytes:
        tile_index = uint8_format(self.payload.tile_index)
        length = uint8_format(self.payload.length)
        reserved = uint8_format(0)
        x = uint8_format(self.payload.x)
        y = uint8_format(self.payload.y)
        width = uint8_format(self.payload.width)
        return tile_index + length + reserved + x + y + width


class TileSet64Payload(TileGet64Payload):
    duration: int
    colors: list[list[int]]


class TileSet64(Message):
    message_type: MessageType = MessageType.TileSet64
    payload: TileSet64Payload

    def get_payload(self) -> bytes:
        tile_index = uint8_format(self.payload.tile_index)
        length = uint8_format(self.payload.length)
        reserved = int8_format(0)
        x = uint8_format(self.payload.x)
        y = uint8_format(self.payload.y)
        width = uint8_format(self.payload.width)
        duration = uint32_format(self.payload.duration)
        payload = tile_index + length + reserved + x + y + width + duration
        for color in self.payload.colors:
            payload += b"".join(uint16_format(field) for field in color)
        return payload


class TileState64Payload(BaseModel):
    tile_index: int
    x: int
    y: int
    width: int
    colors: list[list[int]]


class TileState64(Message):
    message_type: MessageType = MessageType.TileState64
    payload: TileState64Payload

    def get_payload(self) -> bytes:
        tile_index = uint8_format(self.payload.tile_index)
        x = uint8_format(self.payload.x)
        y = uint8_format(self.payload.y)
        width = uint8_format(self.payload.width)
        payload = tile_index + x + y + width

        for color in self.payload.colors:
            payload += b"".join(uint16_format(field) for field in color)
        return payload


class TileGetTileEffect(Message):
    message_type: MessageType = MessageType.TileGetTileEffect


class TileSetTileEffectPayload(BaseModel):
    instanceid: int = randrange(1, 1 << 32)
    type: int
    speed: int
    duration: int
    sky_type: int
    cloud_saturation_min: int
    cloud_saturation_max: int
    palette_count: int
    palette: list[list[int]]


class TileSetTileEffect(Message):
    message_type: MessageType = MessageType.TileSetTileEffect
    payload: TileSetTileEffectPayload

    def get_payload(self) -> bytes:
        reserved = little_endian(bitstring.pack("int:8", 0))
        instanceid = uint32_format(self.payload.instanceid)
        type = uint8_format(self.payload.type)
        speed = uint32_format(self.payload.speed)
        duration = uint64_format(self.payload.duration)
        sky_type = uint8_format(self.payload.sky_type)
        cloud_saturation_min = uint8_format(self.payload.cloud_saturation_min)
        cloud_saturation_max = uint8_format(self.payload.cloud_saturation_max)
        palette_count = uint8_format(self.payload.palette_count)
        payload = (
            reserved * 2
            + instanceid
            + type
            + speed
            + duration
            + reserved * 8
            + sky_type
            + reserved * 3
            + cloud_saturation_min
            + reserved * 3
            + cloud_saturation_max
            + reserved * 23
            + palette_count
        )
        for color in self.payload.palette:
            payload += b"".join(uint16_format(field) for field in color)

        return payload


class TileStateTileEffectPayload(BaseModel):
    instanceid: int
    effect: int
    speed: int
    duration: int
    sky_type: int
    cloud_saturation_min: int
    cloud_saturation_max: int
    palette_count: int
    palette: list[list[int]]


class TileStateTileEffect(Message):
    message_type: MessageType = MessageType.TileStateTileEffect
    payload: TileStateTileEffectPayload

    def get_payload(self) -> bytes:
        instanceid = uint32_format(self.payload.instanceid)
        effect = uint8_format(self.payload.effect)
        speed = uint32_format(self.payload.speed)
        duration = uint64_format(self.payload.duration)
        sky_type = uint8_format(self.payload.sky_type)
        cloud_saturation_min = uint8_format(self.payload.cloud_saturation_min)
        cloud_saturation_max = uint8_format(self.payload.cloud_saturation_max)
        palette_count = uint8_format(self.payload.palette_count)
        payload = (
            instanceid
            + effect
            + speed
            + duration
            + sky_type
            + cloud_saturation_min
            + cloud_saturation_max
            + palette_count
        )
        for color in self.payload.palette:
            payload += b"".join(uint16_format(field) for field in color)

        return payload

    @property
    def effect_str(self):
        return TileEffectType(self.payload.effect).name.upper()

    @property
    def sky_type_str(self):
        if self.payload.effect == TileEffectType.SKY.value:
            return TileEffectSkyType(self.payload.sky_type).name.upper()
        return "NONE"


##### RELAY (SWITCH) MESSAGES #####
##### https://lan.developer.lifx.com/docs/the-lifx-switch #####


class RelayPowerPayload(BaseModel):
    relay_index: int


class GetRPower(Message):
    message_type: MessageType = MessageType.GetRPower
    payload: RelayPowerPayload

    def get_payload(self) -> bytes:
        return uint8_format(self.payload.relay_index)


class SetRelayPowerPayload(RelayPowerPayload):
    level: int


class SetRPower(Message):
    message_type: MessageType = MessageType.SetRPower
    payload: SetRelayPowerPayload

    def get_payload(self) -> bytes:
        relay_index = uint8_format(self.payload.relay_index)
        level = uint16_format(self.payload.level)
        return relay_index + level


class StateRelayPowerPayload(BaseModel):
    relay_index: int
    level: int


class StateRPower(Message):
    message_type: MessageType = MessageType.StateRPower
    payload: StateRelayPowerPayload

    def get_payload(self) -> bytes:
        relay_index = uint8_format(self.payload.relay_index)
        level = uint32_format(self.payload.level)
        return relay_index + level


##### SWITCH BUTTON MESSAGES #####
##### https://github.com/LIFX/public-protocol/blob/main/protocol.yml#L472-L541 #####


class GetButton(Message):
    message_type: MessageType = MessageType.GetButton


class SetButtonPayload(BaseModel): ...


class SetButton(Message):
    message_type: MessageType = MessageType.SetButton
    payload: SetButtonPayload

    def get_payload(self) -> bytes:
        msg = "Not implemented"
        raise Exception(msg)


class StateButtonPayload(BaseModel):
    count: int
    index: int
    buttons_count: int
    buttons: int


class StateButton(Message):
    message_type: MessageType = MessageType.StateButton
    payload: StateButtonPayload


class GetButtonConfig(Message):
    message_type: MessageType = MessageType.GetButtonConfig


class BacklightColor(BaseModel):
    hue: int
    saturation: int
    brightness: int
    kelvin: int


class SetButtonConfigPayload(BaseModel):
    haptic_duration_ms: int
    backlight_on_color: BacklightColor
    backlight_off_color: BacklightColor


class SetButtonConfig(Message):
    message_type: MessageType = MessageType.SetButtonConfig
    payload: SetButtonConfigPayload

    def get_payload(self) -> bytes:
        haptic_duration_ms = uint16_format(self.payload.haptic_duration_ms)
        backlight_on_color = (
            uint16_format(self.payload.backlight_on_color.hue)
            + uint16_format(self.payload.backlight_on_color.saturation)
            + uint16_format(self.payload.backlight_on_color.brightness)
            + uint16_format(self.payload.backlight_on_color.kelvin)
        )
        backlight_off_color = (
            uint16_format(self.payload.backlight_off_color.hue)
            + uint16_format(self.payload.backlight_off_color.saturation)
            + uint16_format(self.payload.backlight_off_color.brightness)
            + uint16_format(self.payload.backlight_off_color.kelvin)
        )
        return haptic_duration_ms + backlight_on_color + backlight_off_color


class StateButtonConfig(Message):
    message_type: MessageType = MessageType.StateButtonConfig


SERVICE_IDS = {1: "UDP", 2: "reserved", 3: "reserved", 4: "reserved"}

STR_MAP = {65535: "On", 0: "Off", None: "Unknown"}

ZONE_MAP = {0: "NO_APPLY", 1: "APPLY", 2: "APPLY_ONLY"}

LAST_HEV_CYCLE_RESULT = {
    0: "SUCCESS",
    1: "BUSY",
    2: "INTERRUPTED_BY_RESET",
    3: "INTERRUPTED_BY_HOMEKIT",
    4: "INTERRUPTED_BY_LAN",
    5: "INTERRUPTED_BY_CLOUD",
    255: "NONE",
}

TILE_EFFECT_SKY_PALETTE = {
    0: "SKY",
    1: "NIGHT_SKY",
    2: "DAWN_SKY",
    3: "DAWN_SUN",
    4: "FULL_SUN",
    5: "FINAL_SUN",
}


class Button:
    def __init__(self, data) -> None:
        self.actions = []
        self.actions_count = data[0]
        for i in range(self.actions_count):
            self.actions.append(ButtonAction(data[1 + i * 20 : 1 + (i + 1) * 20]))

    def get_payload(self) -> bytes:
        payload = uint8_format(self.actions_count)
        for action in self.actions:
            payload += action.get_payload()
        return payload


class ButtonAction:
    def __init__(self, data) -> None:
        self.gesture = ButtonGesture(data[0] + data[1] * 256)
        self.target_type = ButtonTargetType(data[2] + data[3] * 256)
        if self.target_type == ButtonTargetType.RELAYS:
            self.target = ButtonTargetRelays(data[4:])
        elif self.target_type == ButtonTargetType.DEVICE:
            self.target = ButtonTargetDevice(data[4:])
        elif self.target_type == ButtonTargetType.DEVICE_RELAYS:
            self.target = ButtonTargetDeviceRelays(data[4:])
        else:
            self.target = None

    def get_payload(self) -> bytes:
        payload = uint16_format(self.gesture.value)
        payload += uint16_format(self.target_type.value)
        if self.target_type == ButtonTargetType.RELAYS:
            payload += uint8_format(self.target.relays_count)
            for relay in self.target.relays:
                payload += uint8_format(relay)
        elif self.target_type == ButtonTargetType.DEVICE:
            payload += self.target.serial
            payload += self.target.reserved
        elif self.target_type == ButtonTargetType.DEVICE_RELAYS:
            payload += self.target.serial
            payload += uint8_format(self.target.relays_count)
            for relay in self.target.relays:
                payload += uint8_format(relay)
        return payload


MessageTypes = {
    MessageType.GetService: GetService,
    MessageType.StateService: StateService,
    MessageType.GetHostInfo: GetHostInfo,
    MessageType.StateHostInfo: StateHostInfo,
    MessageType.GetHostFirmware: GetHostFirmware,
    MessageType.StateHostFirmware: StateHostFirmware,
    MessageType.GetWifiInfo: GetWifiInfo,
    MessageType.StateWifiInfo: StateWifiInfo,
    MessageType.GetWifiFirmware: GetWifiFirmware,
    MessageType.StateWifiFirmware: StateWifiFirmware,
    MessageType.GetPower: GetPower,
    MessageType.SetPower: SetPower,
    MessageType.StatePower: StatePower,
    MessageType.GetLabel: GetLabel,
    MessageType.SetLabel: SetLabel,
    MessageType.StateLabel: StateLabel,
    MessageType.GetVersion: GetVersion,
    MessageType.StateVersion: StateVersion,
    MessageType.GetInfo: GetInfo,
    MessageType.StateInfo: StateInfo,
    MessageType.GetLocation: GetLocation,
    MessageType.StateLocation: StateLocation,
    MessageType.GetGroup: GetGroup,
    MessageType.StateGroup: StateGroup,
    MessageType.SetReboot: SetReboot,
    MessageType.Acknowledgement: Acknowledgement,
    MessageType.EchoRequest: EchoRequest,
    MessageType.EchoResponse: EchoResponse,
    MessageType.LightGet: LightGet,
    MessageType.LightSetColor: LightSetColor,
    MessageType.LightSetWaveform: LightSetWaveform,
    MessageType.LightSetWaveformOptional: LightSetWaveformOptional,
    MessageType.LightState: LightState,
    MessageType.LightGetPower: LightGetPower,
    MessageType.LightSetPower: LightSetPower,
    MessageType.LightStatePower: LightStatePower,
    MessageType.LightGetInfrared: LightGetInfrared,
    MessageType.LightStateInfrared: LightStateInfrared,
    MessageType.LightSetInfrared: LightSetInfrared,
    MessageType.GetHevCycle: GetHevCycle,
    MessageType.SetHevCycle: SetHevCycle,
    MessageType.StateHevCycle: StateHevCycle,
    MessageType.GetHevCycleConfiguration: GetHevCycleConfiguration,
    MessageType.SetHevCycleConfiguration: SetHevCycleConfiguration,
    MessageType.StateHevCycleConfiguration: StateHevCycleConfiguration,
    MessageType.GetLastHevCycleResult: GetLastHevCycleResult,
    MessageType.StateLastHevCycleResult: StateLastHevCycleResult,
    MessageType.MultiZoneStateMultiZone: MultiZoneStateMultiZone,
    MessageType.MultiZoneStateZone: MultiZoneStateZone,
    MessageType.MultiZoneSetColorZones: MultiZoneSetColorZones,
    MessageType.MultiZoneGetColorZones: MultiZoneGetColorZones,
    MessageType.MultiZoneGetMultiZoneEffect: MultiZoneGetMultiZoneEffect,
    MessageType.MultiZoneSetMultiZoneEffect: MultiZoneSetMultiZoneEffect,
    MessageType.MultiZoneStateMultiZoneEffect: MultiZoneStateMultiZoneEffect,
    MessageType.MultiZoneSetExtendedColorZones: MultiZoneSetExtendedColorZones,
    MessageType.MultiZoneGetExtendedColorZones: MultiZoneGetExtendedColorZones,
    MessageType.MultiZoneStateExtendedColorZones: MultiZoneStateExtendedColorZones,
    MessageType.TileGetDeviceChain: TileGetDeviceChain,
    MessageType.TileStateDeviceChain: TileStateDeviceChain,
    MessageType.TileGet64: TileGet64,
    MessageType.TileSet64: TileSet64,
    MessageType.TileState64: TileState64,
    MessageType.TileGetTileEffect: TileGetTileEffect,
    MessageType.TileSetTileEffect: TileSetTileEffect,
    MessageType.TileStateTileEffect: TileStateTileEffect,
    MessageType.GetRPower: GetRPower,
    MessageType.SetRPower: SetRPower,
    MessageType.StateRPower: StateRPower,
    MessageType.GetButton: GetButton,
    MessageType.SetButton: SetButton,
    MessageType.StateButton: StateButton,
    MessageType.GetButtonConfig: GetButtonConfig,
    MessageType.SetButtonConfig: SetButtonConfig,
    MessageType.StateButtonConfig: StateButtonConfig,
}
