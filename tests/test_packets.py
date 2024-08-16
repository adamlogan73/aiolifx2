from aiolifx.unpack import unpack_lifx_message
from tests.data import packets


def test_messages() -> None:
    print(len(packets))
    for i, packet in enumerate(packets):
        print(i)
        # print(packet)
        message = unpack_lifx_message(packet)
        print(message)
