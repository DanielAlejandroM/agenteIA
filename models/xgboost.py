import pandas as pd
import joblib
import seaborn as sns
import matplotlib.pyplot as plt
import os
import sys
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report

# --- CONFIGURACIÓN DE RUTAS ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.preprocesamiento import DataPreprocessor


class XGBModelTrainer:
    def __init__(self, n_estimators=200, learning_rate=0.05, max_depth=6):
    
        self.model = XGBClassifier(
            n_estimators=n_estimators,
            learning_rate=learning_rate,
            max_depth=max_depth,
            random_state=42,
            eval_metric='logloss',
        )

    def train_and_evaluate(self, X, y):
        # 1. División de datos (80% entrenamiento, 20% prueba)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # 2. Entrenamiento
        self.model.fit(X_train, y_train)
        
        # 3. Predicción
        y_pred = self.model.predict(X_test)
        
        # 4. Métricas
        acc = accuracy_score(y_test, y_pred)
        cm = confusion_matrix(y_test, y_pred)
        report = classification_report(y_test, y_pred)
        
        # 5. Generar Matriz de Confusión
        self._plot_confusion_matrix(cm, acc)
        
        # 6. Guardar el modelo entrenado
        joblib.dump(self.model, 'models/artifacts/xgboost_model.pkl')
        
        return acc, report

    def _plot_confusion_matrix(self, cm, acc):
        plt.figure(figsize=(6,5))
        # Color Naranja para diferenciarlo visualmente del Random Forest (Verde)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Oranges', 
                    xticklabels=['No Renuncia', 'Renuncia'], 
                    yticklabels=['No Renuncia', 'Renuncia'])
        plt.title(f'XGBoost: Matriz de Confusión\nAccuracy: {acc:.2f}')
        plt.ylabel('Realidad')
        plt.xlabel('Predicción del Agente')
        plt.tight_layout()
        plt.savefig('models/plots/confusion_xgb.png')
        plt.close()

# ---EJECUCIÓN ---
if __name__ == "__main__":
    # 1. Cargar datos
    df = pd.read_csv(r'data\empleados.csv')

    # 2. Preprocesamiento
    prep = DataPreprocessor()
    X_scaled, y, metadata = prep.prepare_data(df, training=True) 
    prep.save() # Guarda preprocessor.pkl en artifacts

    # 3. Entrenamiento de XGBoost
    xgb_agent = XGBModelTrainer(n_estimators=200, learning_rate=0.05)
    accuracy, reporte = xgb_agent.train_and_evaluate(X_scaled, y)

    print(f"--- ENTRENAMIENTO XGBOOST EXITOSO ---")
    print(f"Precisión General (Accuracy): {accuracy:.4f}")
    print("\nReporte de Clasificación Detallado:\n", reporte)
    print("Modelo guardado en: models/artifacts/xgboost_model.pkl")
    print("Gráfica guardada en: models/plots/confusion_xgb.png")
