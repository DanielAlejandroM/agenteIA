import json
import joblib
import pandas as pd
from datetime import datetime
import os
import sys

# --- CONFIGURACIÓN DE RUTAS ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class ChurnInference:
    def __init__(self, model_path, preprocessor_path):
        self.model = joblib.load(model_path)
        self.preprocessor = joblib.load(preprocessor_path)

    def process_and_export(self, csv_path, output_json='models/results/resultados_ML.json'):
        df_nuevo = pd.read_csv(csv_path)
        
        # Preprocesar usando el escalador cargado
        X_scaled, _, _ = self.preprocessor.prepare_data(df_nuevo, training=False)
        
        # Obtener probabilidades
        probs = self.model.predict_proba(X_scaled)[:, 1]
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        json_completo = []

        for i, riesgo in enumerate(probs):
            registro = {
                "fecha_evaluacion": fecha_actual,
                "riesgo_ml": round(float(riesgo), 4),
                "comentarios_empleado": df_nuevo.iloc[i]['comentarios_empleado'],
                "contexto": f"Departamento: {df_nuevo.iloc[i]['departamento']} | Antigüedad: {df_nuevo.iloc[i]['antiguedad_empresa']} años"
            }
            json_completo.append(registro)

        # Guardar el JSON localmente
        os.makedirs(os.path.dirname(output_json), exist_ok=True)
        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump(json_completo, f, indent=4, ensure_ascii=False)
            
        # --- LLAMADA AL FLUJO AUTOMÁTICO ---
        if len(json_completo) > 0:
            self._enviar_a_agente_ia(json_completo)
            
        return json_completo

    def _enviar_a_agente_ia(self, data_json):
        """
        Llama al método en agent.py para simular el envío a la API
        """
        try:
            from agent import IAAgent
            
            # Instanciar y llamar al método
            agente_ia = IAAgent()
            agente_ia.generar_recomendaciones_y_chat(data_json)
            
        except ImportError:
            print("\n[ERROR] No se pudo encontrar 'agent.py'. Asegúrate de que esté en la raíz del proyecto.")
        except Exception as e:
            print(f"\n[ERROR] Ocurrió un problema en la integración: {e}")

# --- Ejecución ---
if __name__ == "__main__":
    predictor = ChurnInference('models/artifacts/random_forest.pkl', 'models/artifacts/preprocesador.pkl')
    predictor.process_and_export('data/empleados10.csv')
