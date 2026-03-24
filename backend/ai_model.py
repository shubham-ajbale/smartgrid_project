import pandas as pd
import psycopg2
import os
from sklearn.linear_model import LinearRegression
import numpy as np

DATABASE_URL = os.getenv("DATABASE_URL")


def predict_power():
    try:
        conn = psycopg2.connect(DATABASE_URL)

        df = pd.read_sql_query(
            "SELECT power FROM energy ORDER BY timestamp ASC",
            conn
        )

        conn.close()

        if len(df) < 5:
            return 0

        df["index"] = range(len(df))

        model = LinearRegression()
        model.fit(df[["index"]], df["power"])

        pred = model.predict(np.array([[len(df) + 1]]))

        return float(pred[0])

    except Exception as e:
        print("AI Error:", e)
        return 0