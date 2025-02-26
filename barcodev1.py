import cv2
import sqlite3
import datetime
import time
from pyzbar.pyzbar import decode

DB_FILE = "attendance.db"
SCAN_DELAY = 5  # Delay in seconds to prevent continuous scanning

# Create table if it doesn't exist
def create_table():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS attendance_log (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        barcode TEXT UNIQUE,
                        time_in TEXT,
                        time_out TEXT)''')
    conn.commit()
    conn.close()

# Insert or update scan record
def log_scan(barcode_data):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT time_in, time_out FROM attendance_log WHERE barcode = ?", (barcode_data,))
    record = cursor.fetchone()

    current_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    if record:
        if record[1] is None:  # If time_out is empty, update it
            cursor.execute("UPDATE attendance_log SET time_out = ? WHERE barcode = ?", (current_time, barcode_data))
    else:
        cursor.execute("INSERT INTO attendance_log (barcode, time_in) VALUES (?, ?)", (barcode_data, current_time))

    conn.commit()
    conn.close()

last_scanned = None
last_scan_time = 0

def scan_barcode():
    global last_scanned, last_scan_time
    cap = cv2.VideoCapture("http://192.168.50.102:4747/video") 
    cap.set(3, 1920)  
    cap.set(4, 1080)
    while True:
        success, frame = cap.read()
        if not success:
            continue

        for barcode in decode(frame):
            barcode_data = barcode.data.decode("utf-8")
            current_time = time.time()

            if barcode_data == last_scanned and (current_time - last_scan_time) < SCAN_DELAY:
                continue  # Skip scanning the same barcode within the delay period

            log_scan(barcode_data)  # Save scan to database
            last_scanned = barcode_data
            last_scan_time = current_time
            print(f"Scanned Successfully: {barcode_data}")

            # Display message for 3 seconds
            cv2.putText(frame, "Scanned Successfully!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow("Scanner", frame)
            cv2.waitKey(3000)  # Pause for 3 seconds

        cv2.imshow("Scanner", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    create_table()
    scan_barcode()



