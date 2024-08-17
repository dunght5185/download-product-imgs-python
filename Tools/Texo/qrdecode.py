import cv2

def decodeQR(image_path):
    detector = cv2.QRCodeDetector()

    image = cv2.imread(image_path)

    data, bbox, straight_qrcode = detector.detectAndDecode(image)

    if bbox is not None:
        
        print(data)
        return data
    else:
        print("QR Code not detected")
        return None

decodeQR("/Users/dunghoang/Documents/FL/AllOfCheap/Tools/Images/Images/QRBuysim/78_qrcode.png")