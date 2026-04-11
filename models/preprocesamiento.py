import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler

class DataPreprocessor:
    def __init__(self):
        self.scaler = StandardScaler()
        self.columnas_finales = None

    def prepare_data(self, df, training=True):
        # 1. Copia de seguridad y separación de data no numérica
        X = df.copy()
        
        # Guardamos comentarios y IDs (índices) para el JSON de entrega
        comentarios = X['comentarios_empleado'].copy()
        
        # target
        y = X['renuncia'] if 'renuncia' in X.columns else None
        
        # 2. Eliminamos lo que el modelo NO debe procesar
        X = X.drop(['renuncia', 'comentarios_empleado'], axis=1, errors='ignore')

        # 3. Convertir categorías a números (One-Hot Encoding)
        # Esto procesará 'departamento' y 'tipo_contrato'
        X = pd.get_dummies(X)

        if training:
            # Guardamos el orden de las columnas para que la inferencia no falle
            self.columnas_finales = X.columns
            # 4. Ajustar y transformar escalador
            X_scaled = self.scaler.fit_transform(X)
        else:
            # En inferencia (para el JSON), nos aseguramos de tener las mismas columnas
            X = X.reindex(columns=self.columnas_finales, fill_value=0)
            X_scaled = self.scaler.transform(X)

        # Retornamos la data lista para el modelo y los comentarios originales
        return X_scaled, y, comentarios

    def save(self, path='models/artifacts/preprocesador.pkl'):
        joblib.dump(self, path)
