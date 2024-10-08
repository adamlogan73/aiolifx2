import binascii
import struct
from collections.abc import Callable

from aiolifx.models.message import Message
from aiolifx.models.message_types import ButtonGesture
from aiolifx.models.message_types import ButtonTargetType
from aiolifx.models.message_types import MessageType
from aiolifx.models.message_types import MessageTypes
from aiolifx.resources.const import HEADER_SIZE_BYTES


def add_state_service_payload(data: dict) -> None:
    service = struct.unpack("B", data["payload_str"][0:1])[0]
    port = struct.unpack("I", data["payload_str"][1:5])[0]
    data["payload"] = {"service": service, "port": port}


def add_state_host_info_payload(data: dict) -> None:
    signal = struct.unpack("f", data["payload_str"][0:4])[0]
    tx = struct.unpack("I", data["payload_str"][4:8])[0]
    rx = struct.unpack("I", data["payload_str"][8:12])[0]
    reserved1 = struct.unpack("h", data["payload_str"][12:14])[0]
    data["payload"] = {"signal": signal, "tx": tx, "rx": rx, "reserved1": reserved1}


def add_state_host_firmware_payload(data: dict) -> None:
    build = struct.unpack("Q", data["payload_str"][0:8])[0]
    reserved1 = struct.unpack("Q", data["payload_str"][8:16])[0]
    version = struct.unpack("I", data["payload_str"][16:20])[0]
    data["payload"] = {"build": build, "reserved1": reserved1, "version": version}


def add_state_wifi_info_payload(data: dict) -> None:
    signal = struct.unpack("f", data["payload_str"][0:4])[0]
    tx = struct.unpack("I", data["payload_str"][4:8])[0]
    rx = struct.unpack("I", data["payload_str"][8:12])[0]
    reserved1 = struct.unpack("h", data["payload_str"][12:14])[0]
    data["payload"] = {"signal": signal, "tx": tx, "rx": rx, "reserved1": reserved1}


def add_state_wifi_firmware_payload(data: dict) -> None:
    build = struct.unpack("Q", data["payload_str"][0:8])[0]
    reserved1 = struct.unpack("Q", data["payload_str"][8:16])[0]
    version = struct.unpack("I", data["payload_str"][16:20])[0]
    data["payload"] = {"build": build, "reserved1": reserved1, "version": version}


def add_state_button_payload(data: dict) -> None:
    count = struct.unpack("B", data["payload_str"][:1])[0]
    index = struct.unpack("B", data["payload_str"][1:2])[0]
    buttons_count = struct.unpack("B", data["payload_str"][2:3])[0]

    # always an array of 8 buttons
    buttons = []
    for i in range(8):
        # each button is 101 bytes
        button_bytes = data["payload_str"][3 + (i * 101) : 104 + (i * 101)]
        actions_count = struct.unpack("B", button_bytes[:1])[0]
        # each button has 5 actions, size 100 bytes each
        button_actions = []
        for j in range(5):
            button_action_bytes = button_bytes[1 + (j * 20) : 21 + (j * 20)]

            button_gesture = struct.unpack("H", button_action_bytes[:2])[0]
            button_gesture_enum = ButtonGesture(button_gesture)

            button_target_type = struct.unpack("H", button_action_bytes[2:4])[0]
            button_target_type_enum = ButtonTargetType(button_target_type)

            button_target = button_action_bytes[4:]
            button_target_properties = {"type": button_target_type_enum}
            if button_target_type_enum == ButtonTargetType.RELAYS:
                button_target_properties["relays_count"] = struct.unpack(
                    "B", button_target[:1]
                )[0]
                button_target_properties["relays"] = struct.unpack(
                    "B" * 15, button_target[1:]
                )
            elif button_target_type_enum == ButtonTargetType.DEVICE:
                button_target_properties["serial"] = struct.unpack(
                    "B" * 6, button_target[:6]
                )
                button_target_properties["reserved"] = struct.unpack(
                    "B" * 10, button_target[6:]
                )
            elif button_target_type_enum == ButtonTargetType.LOCATION:
                button_target_properties["location_id"] = struct.unpack(
                    "B" * 16, button_target[:16]
                )
            elif button_target_type_enum == ButtonTargetType.GROUP:
                button_target_properties["group_id"] = struct.unpack(
                    "B" * 16, button_target[:16]
                )
            elif button_target_type_enum == ButtonTargetType.SCENE:
                button_target_properties["scene_id"] = struct.unpack(
                    "B" * 16, button_target[:16]
                )
            elif button_target_type_enum == ButtonTargetType.DEVICE_RELAYS:
                button_target_properties["serial"] = struct.unpack(
                    "B" * 6, button_target[:6]
                )
                button_target_properties["relays_count"] = struct.unpack(
                    "B", button_target[6:7]
                )[0]
                button_target_properties["relays"] = struct.unpack(
                    "B" * 9, button_target[7:]
                )
            button_action = {
                "button_gesture": button_gesture_enum,
                "button_target_type": button_target_type_enum,
                "button_target": button_target_properties,
            }
            button_actions.append(button_action)
        button = {"actions_count": actions_count, "button_actions": button_actions}
        buttons.append(button)

    data["payload"] = {
        "count": count,
        "index": index,
        "buttons_count": buttons_count,
        "buttons": buttons,
    }


def add_set_power_payload(data: dict) -> None:
    power_level = struct.unpack("H", data["payload_str"][0:2])[0]
    data["payload"] = {"power_level": power_level}


def add_state_label_payload(data: dict) -> None:
    label = binascii.unhexlify(
        "".join(
            [
                "%2.2x" % (b & 0x000000FF)
                for b in struct.unpack("b" * 32, data["payload_str"][0:32])
            ]
        )
    )
    data["payload"] = {"label": label}


def add_state_location_payload(data: dict) -> None:
    location = list(struct.unpack("B" * 16, data["payload_str"][0:16]))
    label = binascii.unhexlify(
        "".join(
            [
                "%2.2x" % (b & 0x000000FF)
                for b in struct.unpack("b" * 32, data["payload_str"][16:48])
            ]
        )
    )
    updated_at = struct.unpack("Q", data["payload_str"][48:56])[0]
    data["payload"] = {"location": location, "label": label, "updated_at": updated_at}


def add_state_group_payload(data: dict) -> None:
    group = list(struct.unpack("B" * 16, data["payload_str"][0:16]))
    label = binascii.unhexlify(
        "".join(
            [
                "%2.2x" % (b & 0x000000FF)
                for b in struct.unpack("b" * 32, data["payload_str"][16:48])
            ]
        )
    )
    updated_at = struct.unpack("Q", data["payload_str"][48:56])[0]
    data["payload"] = {"group": group, "label": label, "updated_at": updated_at}


def add_state_version_payload(data: dict) -> None:
    vendor = struct.unpack("I", data["payload_str"][0:4])[0]
    product = struct.unpack("I", data["payload_str"][4:8])[0]
    version = struct.unpack("I", data["payload_str"][8:12])[0]
    data["payload"] = {"vendor": vendor, "product": product, "version": version}


def add_state_info_payload(data: dict) -> None:
    time = struct.unpack("Q", data["payload_str"][0:8])[0]
    uptime = struct.unpack("Q", data["payload_str"][8:16])[0]
    downtime = struct.unpack("Q", data["payload_str"][16:24])[0]
    data["payload"] = {"time": time, "uptime": uptime, "downtime": downtime}


def add_echo_request_payload(data: dict) -> None:
    byte_array_len = len(data["payload_str"])
    byte_array = list(
        struct.unpack("B" * byte_array_len, data["payload_str"][0:byte_array_len])
    )
    data["payload"] = {"byte_array": byte_array}


def add_light_set_color_payload(data: dict) -> None:
    color = struct.unpack("H" * 4, data["payload_str"][0:8])
    duration = struct.unpack("I", data["payload_str"][8:12])[0]
    data["payload"] = {"color": color, "duration": duration}


def add_light_state_payload(data: dict) -> None:
    color = struct.unpack("H" * 4, data["payload_str"][0:8])
    reserved1 = struct.unpack("H", data["payload_str"][8:10])[0]
    power_level = struct.unpack("H", data["payload_str"][10:12])[0]
    label = binascii.unhexlify(
        "".join(
            [
                "%2.2x" % (b & 0x000000FF)
                for b in struct.unpack("b" * 32, data["payload_str"][12:44])
            ]
        )
    )
    reserved2 = struct.unpack("Q", data["payload_str"][44:52])[0]
    data["payload"] = {
        "color": color,
        "reserved1": reserved1,
        "power_level": power_level,
        "label": label,
        "reserved2": reserved2,
    }


def add_light_set_power_payload(data: dict) -> None:
    power_level = struct.unpack("H", data["payload_str"][0:2])[0]
    duration = struct.unpack("I", data["payload_str"][2:6])[0]
    data["payload"] = {"power_level": power_level, "duration": duration}


def add_light_state_power_payload(data: dict) -> None:
    power_level = struct.unpack("H", data["payload_str"][0:2])[0]
    data["payload"] = {"power_level": power_level}


def add_light_state_infrared_payload(data: dict) -> None:
    infrared_brightness = struct.unpack("H", data["payload_str"][0:2])[0]
    data["payload"] = {"infrared_brightness": infrared_brightness}


def add_set_hev_cycle_payload(data: dict) -> None:
    enable, duration = struct.unpack("<BI", data["payload_str"][:5])
    data["payload"] = {"enable": enable == 1, "duration": duration}


def add_state_hev_cycle_payload(data: dict) -> None:
    duration, remaining, last_power = struct.unpack("<IIB", data["payload_str"][:9])
    data["payload"] = {
        "duration": duration,
        "remaining": remaining,
        "last_power": last_power == 1,
    }


def add_set_hev_cycle_configuration_payload(data: dict) -> None:
    indication, duration = struct.unpack("<BI", data["payload_str"][:5])
    data["payload"] = {"indication": indication == 1, "duration": duration}


def add_state_last_hev_cycle_result(data: dict) -> None:
    (result,) = struct.unpack("<B", data["payload_str"][:1])
    data["payload"] = {"result": result}


def add_multi_zone_state_zone_payload(data: dict) -> None:
    count = struct.unpack("c", data["payload_str"][0:1])[0]
    count = ord(count)  # 8 bit
    index = struct.unpack("c", data["payload_str"][1:2])[0]
    index = ord(index)  # 8 bit
    color = struct.unpack("H" * 4, data["payload_str"][2:10])
    data["payload"] = {"count": count, "index": index, "color": color}


def add_multi_zone_state_multi_zone_payload(data: dict) -> None:
    count = struct.unpack("c", data["payload_str"][0:1])[0]
    count = ord(count)  # 8 bit
    index = struct.unpack("c", data["payload_str"][1:2])[0]
    index = ord(index)  # 8 bit
    colors = []
    for i in range(8):
        color = struct.unpack("H" * 4, data["payload_str"][2 + (i * 8) : 10 + (i * 8)])
        colors.append(color)
    data["payload"] = {"count": count, "index": index, "color": colors}


def add_multi_zone_get_multi_zone_effect_payload(data: dict) -> None:
    _, effect, _, speed, duration, _, _, _, direction, _, _ = struct.unpack(
        "<IBHIQIIBBBB", data["payload_str"][:31]
    )
    data["payload"] = {
        "effect": effect,
        "speed": speed,
        "duration": duration,
        "direction": direction,
    }


def add_multi_zone_state_multi_zone_effect_payload(data: dict) -> None:
    (instanceid, effect, _, speed, duration, _, _) = struct.unpack(
        "<IBHIQII", data["payload_str"][:27]
    )
    direction = struct.unpack("I", data["payload_str"][31:35])[0]
    data["payload"] = {
        "instanceid": instanceid,
        "effect": effect,
        "speed": speed,
        "duration": duration,
        "direction": direction,
    }


def add_multi_zone_state_extended_color_zones_payload(data: dict) -> None:
    zones_count = struct.unpack("H", data["payload_str"][0:2])[0]
    zone_index = struct.unpack("H", data["payload_str"][2:4])[0]
    colors_count = struct.unpack("B", data["payload_str"][4:5])[0]
    colors = []
    for i in range(82):
        color = struct.unpack("H" * 4, data["payload_str"][5 + (i * 8) : 13 + (i * 8)])
        colors.append(color)

    data["payload"] = {
        "zones_count": zones_count,
        "zone_index": zone_index,
        "colors_count": colors_count,
        "colors": colors,
    }


def add_tile_state_device_chain_payload(data: dict) -> None:
    start_index = struct.unpack("B", data["payload_str"][0:1])[0]
    tile_devices_count = struct.unpack(
        "B", data["payload_str"][len(data["payload_str"]) - 1 : len(data["payload_str"])]
    )[0]

    tile_devices = []
    for i in range(tile_devices_count):
        tile_devices.append(getTile(data["payload_str"][1 + (i * 55) : 55 + (i * 55)]))

    data["payload"] = {
        "start_index": start_index,
        "tile_devices": tile_devices,
        "tile_devices_count": tile_devices_count,
    }


def add_tile_get_64_payload(data: dict) -> None:
    tile_index = struct.unpack("B", data["payload_str"][0:1])[0]
    length = struct.unpack("B", data["payload_str"][1:2])[0]
    x = struct.unpack("B", data["payload_str"][3:4])[0]
    y = struct.unpack("B", data["payload_str"][4:5])[0]
    width = struct.unpack("B", data["payload_str"][5:6])[0]
    data["payload"] = {
        "tile_index": tile_index,
        "length": length,
        "x": x,
        "y": y,
        "width": width,
    }


def add_tile_state_64_payload(data: dict) -> None:
    tile_index = struct.unpack("B", data["payload_str"][0:1])[0]
    x = struct.unpack("B", data["payload_str"][2:3])[0]
    y = struct.unpack("B", data["payload_str"][3:4])[0]
    width = struct.unpack("B", data["payload_str"][4:5])[0]
    colors = []
    for i in range(64):
        color = struct.unpack("H" * 4, data["payload_str"][5 + (i * 8) : 13 + (i * 8)])
        colors.append(color)

    data["payload"] = {
        "tile_index": tile_index,
        "x": x,
        "y": y,
        "width": width,
        "colors": colors,
    }


def add_tile_set_64_payload(data: dict) -> None:
    tile_index = struct.unpack("B", data["payload_str"][0:1])[0]
    length = struct.unpack("B", data["payload_str"][1:2])[0]
    x = struct.unpack("B", data["payload_str"][3:4])[0]
    y = struct.unpack("B", data["payload_str"][4:5])[0]
    width = struct.unpack("B", data["payload_str"][5:6])[0]
    duration = struct.unpack("I", data["payload_str"][6:10])[0]
    colors = []
    for i in range(64):
        color = struct.unpack("H" * 4, data["payload_str"][10 + (i * 8) : 18 + (i * 8)])
        colors.append(color)
    data["payload"] = {
        "tile_index": tile_index,
        "length": length,
        "x": x,
        "y": y,
        "width": width,
        "duration": duration,
        "colors": colors,
    }


def add_tile_state_tile_effect_payload(data: dict) -> None:
    instanceid = struct.unpack("I", data["payload_str"][1:5])[0]
    effect = struct.unpack("B", data["payload_str"][5:6])[0]
    speed = struct.unpack("I", data["payload_str"][6:10])[0]
    duration = struct.unpack("Q", data["payload_str"][10:18])[0]
    sky_type = struct.unpack("B", data["payload_str"][26:27])[0]
    cloud_saturation_min = struct.unpack("B", data["payload_str"][30:31])[0]
    cloud_saturation_max = struct.unpack("B", data["payload_str"][34:35])[0]
    palette_count = struct.unpack("B", data["payload_str"][58:59])[0]
    palette = []
    for i in range(16):
        color = struct.unpack("H" * 4, data["payload_str"][59 + (i * 8) : 67 + (i * 8)])
        palette.append(color)

    data["payload"] = {
        "instanceid": instanceid,
        "effect": effect,
        "speed": speed,
        "duration": duration,
        "sky_type": sky_type,
        "cloud_saturation_min": cloud_saturation_min,
        "cloud_saturation_max": cloud_saturation_max,
        "palette_count": palette_count,
        "palette": palette,
    }


def add_state_relay_power_payload(data: dict) -> None:
    relay_index = struct.unpack("B", data["payload_str"][:1])[0]
    level = struct.unpack(">H", data["payload_str"][1:])[0]
    data["payload"] = {"relay_index": relay_index, "level": level}


def add_state_button_config_payload(data: dict) -> None:
    haptic_duration_ms = struct.unpack("B", data["payload_str"][:1])[0]

    backlight_on_color_values = data["payload_str"][1:9]
    backlight_on_color = getBacklightColor(backlight_on_color_values)

    backlight_off_color_values = data["payload_str"][9:17]
    backlight_off_color = getBacklightColor(backlight_off_color_values)

    data["payload"] = {
        "haptic_duration_ms": haptic_duration_ms,
        "backlight_on_color": backlight_on_color,
        "backlight_off_color": backlight_off_color,
    }


payload_function_map: dict[MessageType, Callable[[dict], None]] = {
    MessageType.StateService: add_state_service_payload,
    MessageType.StateHostInfo: add_state_host_info_payload,
    MessageType.StateHostFirmware: add_state_host_firmware_payload,
    MessageType.StateWifiInfo: add_state_wifi_info_payload,
    MessageType.StateWifiFirmware: add_state_wifi_firmware_payload,
    MessageType.SetPower: add_set_power_payload,
    MessageType.StatePower: add_set_power_payload,
    MessageType.SetLabel: add_state_label_payload,
    MessageType.StateLabel: add_state_label_payload,
    MessageType.StateLocation: add_state_location_payload,
    MessageType.StateGroup: add_state_group_payload,
    MessageType.StateVersion: add_state_version_payload,
    MessageType.StateInfo: add_state_info_payload,
    MessageType.EchoRequest: add_echo_request_payload,
    MessageType.EchoResponse: add_echo_request_payload,
    MessageType.LightSetColor: add_light_set_color_payload,
    MessageType.LightState: add_light_state_payload,
    MessageType.LightSetPower: add_light_set_power_payload,
    MessageType.LightStatePower: add_light_state_power_payload,
    MessageType.LightStateInfrared: add_light_state_infrared_payload,
    MessageType.LightSetInfrared: add_light_state_infrared_payload,
    MessageType.SetHevCycle: add_set_hev_cycle_payload,
    MessageType.StateHevCycle: add_state_hev_cycle_payload,
    MessageType.SetHevCycleConfiguration: add_set_hev_cycle_configuration_payload,
    MessageType.StateHevCycleConfiguration: add_set_hev_cycle_configuration_payload,
    MessageType.StateLastHevCycleResult: add_state_last_hev_cycle_result,
    MessageType.MultiZoneStateZone: add_multi_zone_state_zone_payload,
    MessageType.MultiZoneStateMultiZone: add_multi_zone_state_multi_zone_payload,
    MessageType.MultiZoneGetMultiZoneEffect: add_multi_zone_get_multi_zone_effect_payload,
    MessageType.MultiZoneSetMultiZoneEffect: add_multi_zone_get_multi_zone_effect_payload,
    MessageType.MultiZoneStateMultiZoneEffect: add_multi_zone_state_multi_zone_effect_payload,  # noqa: E501
    MessageType.MultiZoneStateExtendedColorZones: add_multi_zone_state_extended_color_zones_payload,  # noqa: E501
    MessageType.TileStateDeviceChain: add_tile_state_device_chain_payload,
    MessageType.TileGet64: add_tile_get_64_payload,
    MessageType.TileState64: add_tile_state_64_payload,
    MessageType.TileSet64: add_tile_set_64_payload,
    MessageType.TileStateTileEffect: add_tile_state_tile_effect_payload,
    MessageType.StateRPower: add_state_relay_power_payload,
    MessageType.StateButton: add_state_button_payload,
    MessageType.StateButtonConfig: add_state_button_config_payload,
}


def unpack_lifx_message(packed_message: bytes) -> Message:
    header_str = packed_message[0:HEADER_SIZE_BYTES]
    payload_str = packed_message[HEADER_SIZE_BYTES:]
    message_type = MessageType(struct.unpack("H", header_str[32:34])[0])
    flags = struct.unpack("H", header_str[2:4])[0]
    response_flags = struct.unpack("B", header_str[22:23])[0]
    data = {
        "header_str": header_str,
        "payload_str": payload_str,
        "size": struct.unpack("H", header_str[0:2])[0],
        "flags": flags,
        "origin": (flags >> 14) & 3,
        "tagged": (flags >> 13) & 1,
        "addressable": (flags >> 12) & 1,
        "protocol": flags & 4095,
        "source_id": struct.unpack("I", header_str[4:8])[0],
        "target_addr": ":".join(
            [(f"{b:02x}") for b in struct.unpack("B" * 6, header_str[8:14])]
        ),
        "ack_requested": response_flags & 2,
        "response_requested": response_flags & 1,
        "seq_num": struct.unpack("B", header_str[23:24])[0],
        "message_type": struct.unpack("H", header_str[32:34])[0],
        "response_flags": response_flags,
    }
    add_payload = payload_function_map.get(message_type)
    if add_payload is not None:
        add_payload(data=data)
    message_class = MessageTypes[message_type]
    return message_class.model_validate(data)
