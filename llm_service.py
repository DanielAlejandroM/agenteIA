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
            - Máximo 5 recomendaciones
            - Y que cada recomendación sea de 2 líneas
            - Accesibles y accionables con mas de 5 palabras
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

    def generate_hr_email(self, employee_data, risk_score, risk_level):
        if not self.client:
            return {
                "subject": f"Alerta de riesgo laboral alto - {employee_data.get('Nombres', 'Empleado')}",
                "body": (
                    f"Se ha detectado un caso de riesgo {risk_level}.\n\n"
                    f"Empleado: {employee_data.get('Nombres', 'N/A')}\n"
                    f"ID: {employee_data.get('ID_empleados', 'N/A')}\n"
                    f"Risk score: {round(float(risk_score), 4)}\n"
                    f"Comentario: {employee_data.get('comentarios_empleado', '')}\n\n"
                    f"Se recomienda revisión inmediata por parte de Recursos Humanos."
                )
            }

        empleado_json = {
            "id_empleados": employee_data.get("id_empleados"),
            "employee_name": employee_data.get("employee_name"),
            "edad": employee_data.get("edad"),
            "salario": employee_data.get("salario"),
            "experiencia": employee_data.get("experiencia"),
            "antiguedad_empresa": employee_data.get("antiguedad_empresa"),
            "departamento": employee_data.get("departamento"),
            "tipo_contrato": employee_data.get("tipo_contrato"),
            "horas_trabajo": employee_data.get("horas_trabajo"),
            "satisfaccion_laboral": employee_data.get("satisfaccion_laboral"),
            "balance_trabajo_vida": employee_data.get("work_life_balance"),
            "promociones": employee_data.get("promociones"),
            "distancia_trabajo": employee_data.get("distancia_trabajo"),
            "comentarios_empleado": employee_data.get("comentarios_empleado", ""),
            "risk_score": round(float(risk_score), 4),
            "risk_level": risk_level
        }

        mensaje = f"""
    Eres un asistente experto en Recursos Humanos.

    Redacta un correo profesional para el departamento de RRHH notificando un caso de posible abandono laboral.
    El correo debe incluir:
    - asunto breve
    - resumen del caso
    - nivel de riesgo
    - risk score
    - comentario del empleado
    - recomendación de acción inmediata

    Datos del empleado:
    {empleado_json}

    Devuelve la respuesta en este formato exacto:
    ASUNTO: ...
    CUERPO:
    ...
    """

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=500,
                messages=[
                    {"role": "user", "content": mensaje}
                ]
            )

            text = response.content[0].text.strip()

            subject = "Alerta de riesgo laboral"
            body = text

            if "ASUNTO:" in text and "CUERPO:" in text:
                subject_part = text.split("CUERPO:")[0].replace("ASUNTO:", "").strip()
                body_part = text.split("CUERPO:")[1].strip()
                subject = subject_part
                body = body_part

            return {"subject": subject, "body": body}

        except Exception:
            return {
                "subject": f"Alerta de riesgo laboral alto - {employee_data.get('Nombres', 'Empleado')}",
                "body": (
                    f"Estimado equipo de Recursos Humanos,\n\n"
                    f"Se ha identificado un posible riesgo de rotación clasificado como '{risk_level}' "
                    f"para el colaborador {employee_data.get('employee_name', 'N/A')}, con un puntaje de "
                    f"{round(float(risk_score), 4)} según el análisis automatizado.\n\n"
                    f"Comentario registrado por el colaborador:\n"
                    f"{employee_data.get('comentarios_empleado', 'Sin comentarios registrados')}\n\n"
                    f"En función de estos resultados, se sugiere realizar una revisión oportuna del caso "
                    f"para evaluar posibles acciones preventivas.\n\n"
                    f"Atentamente,\n"
                    f"Sistema de Monitoreo de Talento"
)
            }
