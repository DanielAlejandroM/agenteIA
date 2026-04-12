import os
import joblib
import pandas as pd
from pandas.core.dtypes.common import is_numeric_dtype

from db_service import PredictionRepository
from llm_service import ClaudeRecommendationService
from models.preprocesamiento import DataPreprocessor


class IAAgent:
    def __init__(
        self,
        model_path="models/artifacts/random_forest.pkl",
        preprocessor_path="models/artifacts/preprocesador.pkl",
        reference_data_path="data/empleados.csv",
        db_path="data/predictions_history.db",
    ):
        self.model = joblib.load(model_path)
        self.preprocessor = self.load_preprocessor(preprocessor_path, reference_data_path)
        self.repo = PredictionRepository(db_path)
        self.llm = ClaudeRecommendationService()
        self.expected_features = [
            "id_empleados",
            "employee_name",
            "edad",
            "salario",
            "experiencia",
            "antiguedad_empresa",
            "departamento",
            "tipo_contrato",
            "horas_trabajo",
            "satisfaccion_laboral",
            "balance_trabajo_vida",
            "promociones",
            "distancia_trabajo",
            "comentarios_empleado",
        ]

    def load_model(self):
        return self.model

    def load_preprocessor(self, preprocessor_path, reference_data_path):
        try:
            return joblib.load(preprocessor_path)
        except Exception:
            df_ref = pd.read_csv(reference_data_path)
            fallback = DataPreprocessor()
            fallback.prepare_data(df_ref, training=True)
            return fallback

    def clean_data(self, df):
        cleaned = df.copy()
        cleaned.columns = [col.strip().lower() for col in cleaned.columns]

        for col in cleaned.columns:
            if is_numeric_dtype(cleaned[col]):
                cleaned[col] = cleaned[col].fillna(cleaned[col].median())
            else:
                cleaned[col] = cleaned[col].fillna("unknown")

        return cleaned

    def classify_risk(self, risk_score):
        if risk_score >= 0.75:
            return "Alto"
        if risk_score >= 0.40:
            return "Medio"
        return "Bajo"

    def generate_basic_recommendation(self, risk_level):
        base = {
            "Alto": "1. Reunión inmediata con RRHH\n2. Revisar salario y clima laboral",
            "Medio": "1. Seguimiento con liderazgo\n2. Revisar satisfacción laboral",
            "Bajo": "1. Mantener monitoreo\n2. Reforzar motivación y reconocimiento",
        }
        return base.get(risk_level, "Sin recomendación disponible.")

    def generate_recommendation(self, employee_payload):
        risk_level = employee_payload.get("risk_level", "Bajo")
        risk_score = float(employee_payload.get("risk_score", 0.0))
        if risk_level == "Alto":
            return self.llm.generate_recommendation(employee_payload, risk_score, risk_level)
        return self.generate_basic_recommendation(risk_level)

    def predict_employee(self, df):
        original_df = df.copy()
        clean_df = self.clean_data(df)
        x_scaled, _, _ = self.preprocessor.prepare_data(clean_df, training=False)

        results = original_df.copy()
        results["employee_id"] = results.get("ID_empleados", results.index.astype(str))
        results["employee_name"] = results.get("Nombres", "N/A")
        results["risk_score"] = self.model.predict_proba(x_scaled)[:, 1]
        results["risk_level"] = results["risk_score"].apply(self.classify_risk)
        results["recommendation"] = results.apply(
            lambda row: self.generate_recommendation(row.to_dict()), axis=1
        )
        return results

    def analyze_employee_json(self, employee_json: dict):
        original_df = pd.DataFrame([employee_json])
        clean_df = self.clean_data(original_df)

        missing = [c for c in self.expected_features if c not in clean_df.columns]
        if missing:
            raise ValueError(f"Faltan columnas requeridas: {missing}")

        x_scaled, _, _ = self.preprocessor.prepare_data(clean_df, training=False)
        probability = float(self.model.predict_proba(x_scaled)[0][1])
        risk_level = self.classify_risk(probability)

        result = employee_json.copy()
        result["employee_id"] = str(employee_json.get("ID_empleados", "SIN_ID"))
        result["employee_name"] = str(employee_json.get("Nombres", "SIN_NOMBRE"))
        result["risk_score"] = round(probability, 4)
        result["risk_level"] = risk_level
        result["recommendation"] = self.generate_recommendation(result)

        self.save_prediction_sqlite(pd.DataFrame([result]))
        return result

    def save_prediction_sqlite(self, results_df):
        self.repo.save_predictions(results_df)

    def generate_report_csv(self, results_df, output_path="reports/reporte_riesgo_empleados.csv"):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        results_df.to_csv(output_path, index=False, encoding="utf-8")
        return output_path
