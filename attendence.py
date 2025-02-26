from flask import Flask, render_template, request
import sqlite3
import pandas as pd

app = Flask(__name__)

def get_attendance_data():
    """Fetch attendance records from the database."""
    conn = sqlite3.connect("attendance.db")
    df = pd.read_sql_query("SELECT * FROM attendance_log", conn)
    conn.close()
    return df

@app.route('/')
def dashboard():
    data = get_attendance_data()
    return render_template("dashboard.html", records=data.to_dict(orient='records'))

@app.route('/export')
def export():
    data = get_attendance_data()
    data.to_csv("attendance_records.csv", index=False)
    return "CSV Exported Successfully!"

if __name__ == '__main__':
    app.run(debug=True)