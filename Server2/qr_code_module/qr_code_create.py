import qrcode
import os

class QRCodeGenerator:
    def __init__(self, version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4):
        self.qr = qrcode.QRCode(
            version=version,
            error_correction=error_correction,
            box_size=box_size,
            border=border,
        )

    def generate_url_qr(self, url, filename="django_qr_code.png"):
        self.qr.clear()
        self.qr.add_data(url)
        self.qr.make(fit=True)

        img = self.qr.make_image(fill_color="black", back_color="#f5f5f5")
        img.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), filename))

    def generate_wifi_qr(self, ssid, password, wifi_type='WPA', filename="wifi_qr_code.png"):
        wifi_data = f'WIFI:T:{wifi_type};S:{ssid};P:{password};;'
        self.qr.clear()
        self.qr.add_data(wifi_data)
        self.qr.make(fit=True)

        img = self.qr.make_image(fill_color="black", back_color="white")
        img.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), filename))


if __name__ == "__main__":
    qr_generator = QRCodeGenerator()

    url = 'http://192.168.1.108:8000'
    qr_generator.generate_url_qr(url)

    ssid = 'Keenetic-6348'
    password = 'UfPFYaTH'
    wifi_type = 'WPA'
    qr_generator.generate_wifi_qr(ssid, password, wifi_type)