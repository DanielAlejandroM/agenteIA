import os
import sqlite3
from datetime import datetime
import pandas as pd


class PredictionRepository:
    def __init__(self, db_path="data/predictions_history.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_database()

    def _init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS predictions_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id TEXT,
                employee_name TEXT,
                risk_score REAL,
                risk_level TEXT,
                employee_comment TEXT,
                recommendation TEXT,
                prediction_date TEXT
            )
        """)
        conn.commit()
        conn.close()

    def save_predictions(self, results_df):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        for _, row in results_df.iterrows():
            cursor.execute("""
                INSERT INTO predictions_history (
                    employee_id, employee_name, risk_score, risk_level, employee_comment,
                    recommendation, prediction_date
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                str(row.get("employee_id", "N/A")),
                str(row.get("employee_name", "N/A")),
                float(row.get("risk_score", 0.0)),
                row.get("risk_level", "N/A"),
                row.get("comentarios_empleado", ""),
                row.get("recommendation", ""),
                now,
            ))
        conn.commit()
        conn.close()

    def load_history(self):
        conn = sqlite3.connect(self.db_path)
        try:
            return pd.read_sql_query(
                "SELECT employee_id AS Empleado, risk_level AS Riesgo, "
                "ROUND(risk_score * 100, 2) AS Score, recommendation AS Recomendación, "
                "prediction_date AS Fecha FROM predictions_history ORDER BY prediction_date DESC",
                conn,
            )
        finally:
            conn.close()
