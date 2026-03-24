import psycopg2
import os
import time

# ✅ Use Render ENV variable
DATABASE_URL = os.getenv("DATABASE_URL")


# ---------------- CONNECT DATABASE ----------------
def get_connection(retries=3):
    for i in range(retries):
        try:
            print(f"🔌 Connecting to DB (attempt {i+1})...")
            conn = psycopg2.connect(DATABASE_URL, connect_timeout=5)
            print("✅ DB Connected")
            return conn

        except Exception as e:
            print(f"❌ DB Error {i+1}:", e)
            time.sleep(2)

    print("❌ DB connection failed after retries")
    return None


# ---------------- INSERT DATA ----------------
def insert_data(voltage, current, power, energy):
    conn = get_connection()

    if conn is None:
        print("❌ Cannot insert, DB unavailable")
        return

    try:
        cur = conn.cursor()

        print(f"📥 Inserting → V:{voltage} I:{current} P:{power} E:{energy}")

        cur.execute(
            "INSERT INTO energy(voltage, current, power, energy) VALUES (%s, %s, %s, %s)",
            (voltage, current, power, energy)
        )

        conn.commit()

        print("✅ Data inserted successfully")

        cur.close()
        conn.close()

    except Exception as e:
        print("❌ Insert Error:", e)


# ---------------- GET LATEST ----------------
def get_latest():
    conn = get_connection()

    if conn is None:
        print("❌ Cannot fetch, DB unavailable")
        return None

    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT voltage, current, power, energy
            FROM energy
            ORDER BY id DESC
            LIMIT 1
        """)

        row = cur.fetchone()

        cur.close()
        conn.close()

        print("📤 Latest row:", row)

        return row

    except Exception as e:
        print("❌ Fetch Error:", e)
        return None


# ---------------- GET HISTORY ----------------
def get_history(limit=100):
    conn = get_connection()

    if conn is None:
        return []

    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT voltage, current, power, energy, timestamp
            FROM energy
            ORDER BY id DESC
            LIMIT %s
        """, (limit,))

        rows = cur.fetchall()

        cur.close()
        conn.close()

        rows.reverse()

        return rows

    except Exception as e:
        print("❌ History Error:", e)
        return []