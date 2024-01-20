import qrcode

class QR:
    def __init__(self, data:str):
        self.img = qrcode.make(data)

    def save(self):
        self.img.save("qr.png")



if __name__ == '__main__':
    pass