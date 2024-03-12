import asyncio
import inspect
import itertools

from bleak import BleakScanner
from parser import Parser

import processors
import output

decoders = {}
outputers = {}

async def scan(args):
    try:
        async with BleakScanner() as scanner:
            print("Scanning...")

            async for bd, ad in scanner.advertisement_data():
                if not bd.address in args.devices:
                    continue

                data = args.devices[bd.address]['decoder'](bd, ad)
                args.devices[bd.address]['outputer'](data)

    except KeyboardInterrupt:
        print("Shutting down...")
    except asyncio.exceptions.CancelledError:
        print("Shutting down...")

def main(args):
    devices = dict(reversed(item.split(":", 1)) for item in args.devices)
    devices = dict([addr, { 'decoder': decoders[dev].decode, 'outputer': outputers[dev].print }] for addr,dev in devices.items())
    args.devices = devices

    asyncio.run(scan(args))

def makedict(module):
    xxx = map(
                lambda m: (m[0], m[1][0][0], m[1][0][1]),
                map(
                    lambda m: (m[0], inspect.getmembers(m[1], inspect.isclass)),
                    map(
                        lambda moduleinfo: moduleinfo,
                        inspect.getmembers(module, inspect.ismodule)
                    )
                )
            )
    dict = { mi[0]:mi[2] for mi in xxx }
    return dict

if __name__ == "__main__":
    outputers = makedict(output)

    decoders = makedict(processors)

    args = Parser.parse()
    main(args)
