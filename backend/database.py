import psycopg2
import os
import time

DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection(retries=3):
    for i in range(retries):
        try:
            conn = psycopg2.connect(DATABASE_URL, connect_timeout=5)
            return conn
        except Exception as e:
            print(f"❌ DB Error (attempt {i+1}):", e)
            time.sleep(2)
    return None


def insert_data(voltage, current, power, energy):
    conn = get_connection()
    if conn is None:
        return

    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO energy(voltage,current,power,energy) VALUES(%s,%s,%s,%s)",
            (voltage, current, power, energy)
        )
        conn.commit()
        cur.close()
        conn.close()
        print("✅ Data inserted")

    except Exception as e:
        print("❌ Insert Error:", e)


def get_latest():
    conn = get_connection()
    if conn is None:
        return None

    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT voltage,current,power,energy FROM energy ORDER BY id DESC LIMIT 1"
        )
        row = cur.fetchone()
        cur.close()
        conn.close()
        return row

    except Exception as e:
        print("❌ Fetch Error:", e)
        return None