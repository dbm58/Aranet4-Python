import asyncio

from bleak import BleakScanner
from parser import Parser

import processors
import output

processors = {
    'aranet4': processors.Aranet4.decode
}

async def scan(args):
    try:
        async with BleakScanner() as scanner:
            print("Scanning...")

            async for bd, ad in scanner.advertisement_data():
                if not bd.address in args.devices:
                    continue

                data = args.devices[bd.address](bd, ad)

                #  todo:  accumulate data into a processing list, and then output later
                output.Aranet4.print(data)

    except KeyboardInterrupt:
        print("Shutting down...")
    except asyncio.exceptions.CancelledError:
        print("Shutting down...")

def main(args):
    devices = dict(reversed(item.split(":", 1)) for item in args.devices)
    devices = dict([item, processors[dev]] for item,dev in devices.items())
    args.devices = devices

    asyncio.run(scan(args))

if __name__ == "__main__":
    args = Parser.parse()
    main(args)
