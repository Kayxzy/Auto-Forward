from Kymang.config import ADMINS
from Kymang.modules.data import *


async def plernya():
    if 1225177634 not in await cek_seller():
        await add_seller(1225177634)
    if 1715129921 not in await cek_seller():
        await add_seller(1715129921)