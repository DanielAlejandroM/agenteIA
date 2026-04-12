import os

try:
    import anthropic
except Exception:
    anthropic = None


class ClaudeRecommendationService:
    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        self.client = anthropic.Anthropic(api_key=api_key) if (anthropic and api_key) else None

    def generate_recommendation(self, employee_data, risk_score, risk_level):
        if not self.client:
            return self._fallback_recommendation(risk_level)

        empleado_json = {
            "edad": employee_data.get("edad"),
            "salario": employee_data.get("salario"),
            "antiguedad_empresa": employee_data.get("antiguedad_empresa"),
            "departamento": employee_data.get("departamento"),
            "tipo_contrato": employee_data.get("tipo_contrato"),
            "satisfaccion_laboral": employee_data.get("satisfaccion_laboral"),
            "balance_trabajo_vida": employee_data.get("work_life_balance"),
            "risk_score": round(float(risk_score), 2),
            "risk_level": risk_level,
            "comentarios_empleado": employee_data.get("comentarios_empleado", "")
        }

        mensaje = f"""
Eres un experto en Recursos Humanos.

Analiza este empleado y genera recomendaciones para reducir su riesgo de abandono laboral.

Datos del empleado:
{empleado_json}

Reglas:
- Máximo 2 recomendaciones
- Y que cada recomendación sea de 1 sola línea
- Concretas y accionables
- Responde en español
- No expliques, solo da recomendaciones
"""

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=500,
                messages=[{"role": "user", "content": mensaje}],
            )
            return response.content[0].text.strip()
        except Exception:
            return self._fallback_recommendation(risk_level)

    def _fallback_recommendation(self, risk_level):
        fallback = {
            "Alto": "1. Reunión inmediata con RRHH\n2. Ajustar carga laboral\n3. Crear plan de retención",
            "Medio": "1. Seguimiento con líder\n2. Evaluar satisfacción laboral\n3. Ajustes menores en condiciones",
            "Bajo": "1. Mantener monitoreo\n2. Reforzar clima laboral\n3. Incentivar motivación"
        }
        return fallback.get(risk_level, "Sin recomendación disponible.")
