
# qr_exporter.py

import qrcode
from PIL import Image
from io import BytesIO
import base64

def generate_qr_code(data):
    qr = qrcode.QRCode()
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    return img

def decode_qr_code(uploaded_file):
    from pyzbar.pyzbar import decode
    img = Image.open(uploaded_file)
    result = decode(img)
    if result:
        return result[0].data.decode()
    else:
        return ""
