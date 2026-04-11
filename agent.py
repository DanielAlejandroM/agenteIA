import os
import json
import joblib
from db_service import PredictionRepository
from llm_service import ClaudeRecommendationService
from models.preprocesamiento import DataPreprocessor
import pandas as pd


class IAAgent:
    def __init__(self, model_path="models/artifacts/random_forest.pkl",
                 preprocessor_path="models/artifacts/preprocesador.pkl",
                 reference_data_path="data/empleados.csv"):
        self.model = joblib.load(model_path)
        self.preprocessor = self.load_preprocessor(preprocessor_path, reference_data_path)
        self.repo = PredictionRepository()
        self.llm = ClaudeRecommendationService()

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
        df = df.copy()
        df.columns = [c.strip() for c in df.columns]
        for col in df.columns:
            if df[col].dtype == "object":
                df[col] = df[col].fillna("unknown")
            else:
                df[col] = df[col].fillna(df[col].median())
        if "employee_id" not in df.columns:
            df["employee_id"] = [f"EMP{idx + 1:04d}" for idx in range(len(df))]
        return df

    def predict_employee(self, df):
        df = self.clean_data(df)
        x_scaled, _, _ = self.preprocessor.prepare_data(df, training=False)
        results = df.copy()
        results["risk_score"] = self.model.predict_proba(x_scaled)[:, 1]
        results["risk_level"] = results["risk_score"].apply(self.classify_risk)
        results["recommendation"] = results.apply(
            lambda row: self.generate_recommendation(row.to_dict()), axis=1
        )
        return results

    def classify_risk(self, risk_score):
        if risk_score >= 0.75:
            return "Alto"
        if risk_score >= 0.40:
            return "Medio"
        return "Bajo"

    def generate_recommendation(self, employee_payload):
        return self.llm.generate_recommendation(employee_payload)

    def save_prediction_sqlite(self, results_df):
        self.repo.save_predictions(results_df)

    def generate_report_csv(self, results_df, output_path="reports/reporte_riesgo_empleados.csv"):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        results_df.to_csv(output_path, index=False, encoding="utf-8")
        return output_path

    def generar_recomendaciones_y_chat(self, data_json, output_json="models/results/resultados_agente_ia.json"):
        enriched = []
        for item in data_json:
            payload = {
                "employee_id": item.get("employee_id", "N/A"),
                "risk_score": item.get("riesgo_ml", 0),
                "risk_level": self.classify_risk(item.get("riesgo_ml", 0)),
                "comentarios_empleado": item.get("comentarios_empleado", ""),
                "departamento": item.get("contexto", "N/A"),
            }
            payload["recommendation"] = self.generate_recommendation(payload)
            enriched.append(payload)
        with open(output_json, "w", encoding="utf-8") as f:
            json.dump(enriched, f, indent=4, ensure_ascii=False)
        return enriched
