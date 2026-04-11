import os

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


class OpenAIRecommendationService:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key) if OpenAI and api_key else None

    def generate_recommendation(self, payload):
        risk_level = payload.get("risk_level", "Bajo")
        if not self.client:
            return self._fallback(risk_level)

        prompt = f"""
Eres un asistente de RRHH experto en retención de talento.
Genera una recomendación breve, accionable y personalizada en español.
Máximo 4 líneas.

Datos del empleado:
- ID: {payload.get('employee_id', 'N/A')}
- Risk score: {payload.get('risk_score', 0):.2f}
- Nivel de riesgo: {risk_level}
- Departamento: {payload.get('departamento', 'N/A')}
- Tipo de contrato: {payload.get('tipo_contrato', 'N/A')}
- Antigüedad empresa: {payload.get('antiguedad_empresa', 'N/A')}
- Satisfacción laboral: {payload.get('satisfaccion_laboral', 'N/A')}
- Work-life balance: {payload.get('work_life_balance', 'N/A')}
- Comentario del empleado: \"{payload.get('comentarios_empleado', 'Sin comentario')}\"
"""
        try:
            response = self.client.responses.create(model="gpt-5.4", input=prompt)
            return response.output_text.strip()
        except Exception:
            return self._fallback(risk_level)

    def _fallback(self, risk_level):
        rules = {
            "Alto": "Intervenir de inmediato con RRHH, revisar carga laboral, salario y plan de retención.",
            "Medio": "Hacer seguimiento con jefatura y revisar satisfacción, desarrollo y balance trabajo-vida.",
            "Bajo": "Mantener monitoreo periódico y reforzar acciones de bienestar y reconocimiento."
        }
        return rules.get(risk_level, "Sin recomendación disponible.")
