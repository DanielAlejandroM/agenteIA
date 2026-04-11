import pandas as pd
import joblib
import seaborn as sns
import matplotlib.pyplot as plt
import os
import sys
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report

# --- CONFIGURACIÓN DE RUTAS ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.preprocesamiento import DataPreprocessor

class RFModelTrainer:
    def __init__(self, n_estimators=100, max_depth=None):
        self.model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_samples_split=8,
            min_samples_leaf=3,
            max_features='sqrt',
            random_state=42
        )

    def train_and_evaluate(self, X, y):
        # Stratify=y mantiene la proporción de personas que renuncian en el test set
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        self.model.fit(X_train, y_train)
        y_pred = self.model.predict(X_test)
        
        acc = accuracy_score(y_test, y_pred)
        cm = confusion_matrix(y_test, y_pred)
        report = classification_report(y_test, y_pred)
        
        self._plot_confusion_matrix(cm, acc)
        
        # Guardar el modelo entrenado (.pkl)
        joblib.dump(self.model, 'models/artifacts/random_forest.pkl')
        
        return acc, report

    def _plot_confusion_matrix(self, cm, acc):
        plt.figure(figsize=(6,5))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Greens', 
                    xticklabels=['No Renuncia', 'Renuncia'], 
                    yticklabels=['No Renuncia', 'Renuncia'])
        plt.title(f'Random Forest: Matriz de Confusión\nAccuracy: {acc:.2f}')
        plt.ylabel('Realidad')
        plt.xlabel('Predicción ')
        plt.tight_layout()
        plt.savefig('models/plots/confusion_rf.png')
        plt.close()

# --- EJECUCIÓN ---
if __name__ == "__main__":
    # 1. Cargar datos para prediccion
    df = pd.read_csv(r'data\empleados.csv')

    # 2. Preprocesamiento usando tu clase DataPreprocessor
    prep = DataPreprocessor()
    X_scaled, y, metadata = prep.prepare_data(df, training=True) 
    prep.save() # Guarda preprocessor.pkl en artifacts

    # 3. Entrenamiento de Random Forest
    rf_agent = RFModelTrainer(n_estimators=400, max_depth=5)
    accuracy, reporte = rf_agent.train_and_evaluate(X_scaled, y)

    print(f"--- ENTRENAMIENTO EXITOSO ---")
    print(f"Precisión General (Accuracy): {accuracy:.4f}")
    print("\nReporte de Clasificación Detallado:\n", reporte)
