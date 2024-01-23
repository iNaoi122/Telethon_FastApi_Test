import datetime
import time

import qrcode


class QR:
    def __init__(self, data: str):
        self.img = qrcode.make(data)

    def save(self):
        try:
            self.img.save(f"static/qr.png")
        except FileNotFoundError:
            self.img.save("qr.png")


if __name__ == '__main__':
    pass
