import os
import sqlite3
from datetime import datetime
import pandas as pd


class PredictionRepository:
    def __init__(self, db_path="data/predictions_history.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_database()

    def _get_conn(self):
        return sqlite3.connect(self.db_path)

    def _init_database(self):
        conn = self._get_conn()
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
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                employee_id TEXT PRIMARY KEY,
                employee_name TEXT,
                edad INTEGER,
                salario REAL,
                experiencia INTEGER,
                antiguedad_empresa INTEGER,
                departamento TEXT,
                tipo_contrato TEXT,
                horas_trabajo INTEGER,
                satisfaccion_laboral INTEGER,
                work_life_balance INTEGER,
                promociones INTEGER,
                distancia_trabajo REAL,
                comentarios_empleado TEXT,
                updated_at TEXT
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_pred_employee_id ON predictions_history(employee_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_pred_risk_level ON predictions_history(risk_level)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_pred_date ON predictions_history(prediction_date)")
        conn.commit()
        conn.close()

    def save_predictions(self, results_df):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = self._get_conn()
        cursor = conn.cursor()
        for _, row in results_df.iterrows():
            employee_id = str(row.get("employee_id", row.get("ID_empleados", "N/A")))
            employee_name = str(row.get("employee_name", row.get("Nombres", "N/A")))
            cursor.execute(
                """
                INSERT INTO employees (
                    employee_id, employee_name, edad, salario, experiencia,
                    antiguedad_empresa, departamento, tipo_contrato, horas_trabajo,
                    satisfaccion_laboral, work_life_balance, promociones,
                    distancia_trabajo, comentarios_empleado, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(employee_id) DO UPDATE SET
                    employee_name=excluded.employee_name,
                    edad=excluded.edad,
                    salario=excluded.salario,
                    experiencia=excluded.experiencia,
                    antiguedad_empresa=excluded.antiguedad_empresa,
                    departamento=excluded.departamento,
                    tipo_contrato=excluded.tipo_contrato,
                    horas_trabajo=excluded.horas_trabajo,
                    satisfaccion_laboral=excluded.satisfaccion_laboral,
                    work_life_balance=excluded.work_life_balance,
                    promociones=excluded.promociones,
                    distancia_trabajo=excluded.distancia_trabajo,
                    comentarios_empleado=excluded.comentarios_empleado,
                    updated_at=excluded.updated_at
                """,
                (
                    employee_id,
                    employee_name,
                    row.get("edad"),
                    row.get("salario"),
                    row.get("experiencia"),
                    row.get("antiguedad_empresa"),
                    row.get("departamento"),
                    row.get("tipo_contrato"),
                    row.get("horas_trabajo"),
                    row.get("satisfaccion_laboral"),
                    row.get("work_life_balance"),
                    row.get("promociones"),
                    row.get("distancia_trabajo"),
                    row.get("comentarios_empleado", ""),
                    now,
                ),
            )
            cursor.execute(
                """
                INSERT INTO predictions_history (
                    employee_id, employee_name, risk_score, risk_level, employee_comment,
                    recommendation, prediction_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
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
        conn = self._get_conn()
        try:
            return pd.read_sql_query(
                "SELECT employee_id AS Empleado, employee_name AS Nombre, risk_level AS Riesgo, "
                "ROUND(risk_score * 100, 2) AS Score, recommendation AS Recomendación, "
                "prediction_date AS Fecha FROM predictions_history ORDER BY prediction_date DESC",
                conn,
            )
        finally:
            conn.close()
