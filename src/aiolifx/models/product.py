from pydantic import BaseModel


class Product(BaseModel):
    id: int
    name: str
    buttons: bool
    chain: bool
    color: bool
    extended_multizone: bool
    hev: bool
    infrared: bool
    matrix: bool
    multizone: bool
    relays: bool
    max_kelvin: int | None = None
    min_kelvin: int | None = None
    min_ext_mz_firmware: int | None = None
    min_ext_mz_firmware_components: list[int] | None = None
