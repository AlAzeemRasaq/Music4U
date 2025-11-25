import board
import busio
from adafruit_pn532.i2c import PN532_I2C

i2c = busio.I2C(board.SCL, board.SDA)
pn532 = PN532_I2C(i2c, debug=False)
pn532.SAM_configuration()

print("Waiting for an RFID/NFC card...")
print("Press Ctrl+C to stop.")

try:
    while True:
        uid = pn532.read_passive_target(timeout=0.5)
        
        if uid is None:
            continue
        card_id = "".join([hex(i).replace("0x", "").upper().zfill(2) for i in uid])
        
        print(f"Card Detected! UID: {card_id}")

except KeyboardInterrupt:
    print("\n\nProgram stopped by user. Goodbye! 👋")