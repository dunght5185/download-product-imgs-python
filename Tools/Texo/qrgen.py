# wide_border_qrcode.py

import segno
import random


def generate_au_phone_number():
    # Start with the '09' prefix for AU mobile numbers
    number = '09'
    # Generate the next eight digits randomly
    for _ in range(8):
        number += str(random.randint(0, 9))
    # Format the number as '09XX XXX XXX'
    formatted_number = number[:4] + ' ' + number[4:7] + ' ' + number[7:]
    return formatted_number

for i in range(10):
    qrcode = segno.make_qr(generate_au_phone_number())
    qrcode.save(
        "Images/QrBuysim/{}_qrcode.png".format(i+1),  # Use `str.format()` to include [`i`](command:_github.copilot.openSymbolFromReferences?%5B%7B%22%24mid%22%3A1%2C%22path%22%3A%22%2FUsers%2Fdunghoang%2FDocuments%2FFL%2FAllOfCheap%2FTools%2FImages%2Fqrgen.py%22%2C%22scheme%22%3A%22file%22%7D%2C%7B%22line%22%3A16%2C%22character%22%3A4%7D%5D "qrgen.py")
        scale=50,
        border=1,
    )
