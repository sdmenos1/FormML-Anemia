from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import TaskForms
from .serializer import TaskSerializer
import pickle
import pandas as pd
import numpy as np
import os
from django.conf import settings
import resend

class TaskViewSet(viewsets.ModelViewSet):
    queryset = TaskForms.objects.all()
    serializer_class = TaskSerializer
    
    _model = None
    _le_distrito = None
    _feature_names = None
    
    @classmethod
    def get_modelo(cls):
        if cls._model is None:
            try:
                model_path = os.path.join(settings.BASE_DIR, '..', 'trainModelRandomForest')
                # Normalizar la ruta
                model_path = os.path.normpath(model_path)
                
                modelo_file = os.path.join(model_path, 'random_forest_anemia_model.pkl')
                encoder_file = os.path.join(model_path, 'distrito_label_encoder.pkl')
                features_file = os.path.join(model_path, 'feature_names.pkl')
                
                if not os.path.exists(modelo_file):
                    raise FileNotFoundError(f"No se encontró: {modelo_file}")
                if not os.path.exists(encoder_file):
                    raise FileNotFoundError(f"No se encontró: {encoder_file}")
                if not os.path.exists(features_file):
                    raise FileNotFoundError(f"No se encontró: {features_file}")
                
                with open(modelo_file, 'rb') as f:
                    cls._model = pickle.load(f)
                
                with open(encoder_file, 'rb') as f:
                    cls._le_distrito = pickle.load(f)
                
                with open(features_file, 'rb') as f:
                    cls._feature_names = pickle.load(f)
                
                print("✓ Modelo cargado exitosamente desde ../trainModelRandomForest/")
                print(f"  - Modelo: {modelo_file}")
                print(f"  - Encoder: {encoder_file}")
                print(f"  - Features: {features_file}")
            except Exception as e:
                print(f"✗ Error al cargar modelo: {str(e)}")
                print(f"  BASE_DIR: {settings.BASE_DIR}")
                print(f"  Buscando en: {os.path.normpath(os.path.join(settings.BASE_DIR, '..', 'trainModelRandomForest'))}")
                cls._model = None
        
        return cls._model, cls._le_distrito, cls._feature_names
    
    def _enviar_email_resultados(self, email_destino, nombre, prediccion_data):
        """Envía email con los resultados de la predicción usando Resend"""
        try:
            resend.api_key = settings.RESEND_API_KEY
            
            if prediccion_data.get('tiene_anemia'):
                color_resultado = "#ef4444"  
                emoji_resultado = "⚠️"
                titulo_resultado = "Resultado: Se detectó anemia"
            else:
                color_resultado = "#10b981"  
                emoji_resultado = "✅"
                titulo_resultado = "Resultado: Sin anemia detectada"
            
            resultado_texto = prediccion_data.get('resultado', 'No disponible')
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    body {{
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                        line-height: 1.6;
                        color: #333;
                        margin: 0;
                        padding: 0;
                        background-color: #f3f4f6;
                    }}
                    .container {{
                        max-width: 600px;
                        margin: 40px auto;
                        background: white;
                        border-radius: 12px;
                        overflow: hidden;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    }}
                    .header {{
                        background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
                        padding: 30px;
                        text-align: center;
                        color: white;
                    }}
                    .header h1 {{
                        margin: 0;
                        font-size: 24px;
                        font-weight: 600;
                    }}
                    .header p {{
                        margin: 10px 0 0 0;
                        opacity: 0.9;
                        font-size: 14px;
                    }}
                    .content {{
                        padding: 30px;
                    }}
                    .greeting {{
                        font-size: 18px;
                        margin-bottom: 20px;
                        color: #1f2937;
                    }}
                    .resultado-box {{
                        background: {color_resultado};
                        color: white;
                        padding: 20px;
                        border-radius: 8px;
                        text-align: center;
                        margin: 20px 0;
                    }}
                    .resultado-box h2 {{
                        margin: 0 0 10px 0;
                        font-size: 22px;
                    }}
                    .resultado-box p {{
                        margin: 0;
                        font-size: 16px;
                        opacity: 0.95;
                    }}
                    .info-section {{
                        background: #f9fafb;
                        padding: 20px;
                        border-radius: 8px;
                        margin: 20px 0;
                    }}
                    .info-section h3 {{
                        margin: 0 0 15px 0;
                        color: #1f2937;
                        font-size: 16px;
                    }}
                    .info-item {{
                        display: flex;
                        justify-content: space-between;
                        padding: 8px 0;
                        border-bottom: 1px solid #e5e7eb;
                    }}
                    .info-item:last-child {{
                        border-bottom: none;
                    }}
                    .info-label {{
                        font-weight: 500;
                        color: #6b7280;
                    }}
                    .info-value {{
                        color: #1f2937;
                        font-weight: 600;
                    }}
                    .recomendaciones {{
                        background: #fef3c7;
                        border-left: 4px solid #f59e0b;
                        padding: 15px;
                        margin: 20px 0;
                        border-radius: 4px;
                    }}
                    .recomendaciones h3 {{
                        margin: 0 0 10px 0;
                        color: #92400e;
                        font-size: 16px;
                    }}
                    .recomendaciones p {{
                        margin: 5px 0;
                        color: #78350f;
                        font-size: 14px;
                    }}
                    .footer {{
                        background: #f9fafb;
                        padding: 20px;
                        text-align: center;
                        color: #6b7280;
                        font-size: 12px;
                    }}
                    .footer a {{
                        color: #2563eb;
                        text-decoration: none;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🩺 Sistema de Detección de Anemia</h1>
                        <p>Resultados de Evaluación Clínica</p>
                    </div>
                    
                    <div class="content">
                        <p class="greeting">Hola <strong>{nombre}</strong>,</p>
                        
                        <p>Hemos procesado tu evaluación clínica. A continuación encontrarás los resultados:</p>
                        
                        <div class="resultado-box">
                            <h2>{emoji_resultado} {titulo_resultado}</h2>
                            <p>{resultado_texto}</p>
                        </div>
                        
                        <div class="recomendaciones">
                            <h3>💡 Recomendaciones Importantes</h3>
                            <p>• Este resultado es una evaluación preliminar basada en inteligencia artificial.</p>
                            <p>• Se recomienda consultar con un profesional de la salud para un diagnóstico definitivo.</p>
                            <p>• Mantén una alimentación balanceada rica en hierro.</p>
                            {f'<p>• Es importante realizar seguimiento médico y considerar suplementación.</p>' if prediccion_data.get('tiene_anemia') else ''}
                        </div>
                        
                        <p style="margin-top: 30px; color: #6b7280; font-size: 14px;">
                            Si tienes alguna pregunta o necesitas más información, no dudes en contactarnos.
                        </p>
                    </div>
                    
                    <div class="footer">
                        <p>Este es un correo automático, por favor no responder.</p>
                        <p>Sistema de Detección Temprana de Anemia © 2024</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            # Enviar email
            params = {
                "from": settings.RESEND_FROM_EMAIL,
                "to": [email_destino],
                "subject": f"Resultados de tu Evaluación de Anemia - {resultado_texto}",
                "html": html_content,
            }
            
            email_result = resend.Emails.send(params)
            print(f"✓ Email enviado exitosamente a {email_destino}")
            return True
            
        except Exception as e:
            print(f"✗ Error al enviar email: {str(e)}")
            return False
    
    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        instance = serializer.instance
        
        modelo, le_distrito, feature_names = self.get_modelo()
        
        response_data = serializer.data
        
        if modelo is not None:
            try:
                prediccion_result = self._realizar_prediccion(
                    instance, modelo, le_distrito, feature_names
                )
                response_data['prediccion'] = prediccion_result
                
                email_enviado = self._enviar_email_resultados(
                    email_destino=instance.email,
                    nombre=instance.name,
                    prediccion_data=prediccion_result
                )
                
                response_data['email_enviado'] = email_enviado
                
            except Exception as e:
                response_data['prediccion'] = {
                    'error': f'No se pudo realizar predicción: {str(e)}'
                }
                response_data['email_enviado'] = False
        
        headers = self.get_success_headers(serializer.data)
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)
    
    def _realizar_prediccion(self, instance, modelo, le_distrito, feature_names):
        try:
        
            genero = str(instance.genero).upper()
            if genero in ['MASCULINO', 'M', 'MALE']:
                sexo_encoded = 1
            elif genero in ['FEMENINO', 'F', 'FEMALE']:
                sexo_encoded = 0
            else:
                sexo_encoded = 0  # Por defecto F
            
            edad_meses = float(instance.age) * 12
            
            cred = int(instance.cred)
            suplementacion = int(instance.suplementacion)
            altura_ren = getattr(instance, 'altura_ren', 0)  # Este puede quedar por defecto
            
            datos = {
                'Sexo': sexo_encoded,
                'Peso': float(instance.peso),
                'Talla': float(instance.talla),
                'Cred': cred,
                'Suplementacion': suplementacion,
                'DistritoREN': 0,
                'AlturaREN': float(altura_ren),
                'Edad': edad_meses,
                'IMC': float(instance.peso) / ((float(instance.talla)/100) ** 2),
                'Peso_Talla_Ratio': float(instance.peso) / float(instance.talla),
                'EdadMeses': edad_meses,
                'EdadAnios': float(instance.age)
            }
            
            entrada = pd.DataFrame([datos])
            entrada = entrada[feature_names]
            
            try:
                distrito_str = str(instance.distrito).upper()
                entrada.loc[0, 'DistritoREN'] = le_distrito.transform([distrito_str])[0]
            except:
                entrada.loc[0, 'DistritoREN'] = 0
            
            prediccion = modelo.predict(entrada)[0]
            
            tiene_anemia = prediccion != 0
            
            interpretaciones = {
                0: "Sin anemia",
                1: "Anemia leve",
                2: "Anemia moderada",
                3: "Anemia severa"
            }
            
            return {
                "tiene_anemia": tiene_anemia,
                "resultado": interpretaciones.get(prediccion, "Desconocido")
            }
        except Exception as e:
            import traceback
            return {
                "error": f"Error en predicción: {str(e)}",
                "detalles": traceback.format_exc()
            }
    
    @action(detail=False, methods=['post'])
    def predecir_anemia(self, request):
        modelo, le_distrito, feature_names = self.get_modelo()
        
        if modelo is None:
            return Response(
                {"error": "Modelo no disponible"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        try:
            sexo = request.data.get('sexo', '').upper()
            edad_meses = float(request.data.get('edad_meses', 0))
            peso = float(request.data.get('peso', 0))
            talla = float(request.data.get('talla', 0))
            cred = int(request.data.get('cred', 0))
            suplementacion = int(request.data.get('suplementacion', 0))
            distrito = request.data.get('distrito', '').upper()
            altura_ren = float(request.data.get('altura_ren', 0))
            
            # Validaciones
            if sexo not in ['F', 'M']:
                return Response(
                    {"error": "Sexo debe ser 'F' o 'M'"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if any(v <= 0 for v in [edad_meses, peso, talla]):
                return Response(
                    {"error": "Edad, peso y talla deben ser positivos"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            datos = {
                'Sexo': 0 if sexo == 'F' else 1,
                'Peso': peso,
                'Talla': talla,
                'Cred': cred,
                'Suplementacion': suplementacion,
                'DistritoREN': 0,
                'AlturaREN': altura_ren,
                'Edad': edad_meses,
                'IMC': peso / ((talla/100) ** 2),
                'Peso_Talla_Ratio': peso / talla,
                'EdadMeses': edad_meses,
                'EdadAnios': edad_meses / 12
            }
            
            entrada = pd.DataFrame([datos])
            entrada = entrada[feature_names]
            
            distrito_warning = None
            try:
                entrada.loc[0, 'DistritoREN'] = le_distrito.transform([distrito])[0]
            except:
                entrada.loc[0, 'DistritoREN'] = 0
                distrito_warning = f"Distrito '{distrito}' no encontrado"
            
            # Predecir
            prediccion = modelo.predict(entrada)[0]
            
            # Determinar si tiene anemia
            tiene_anemia = prediccion != 0
            
            interpretaciones = {
                0: "Sin anemia",
                1: "Anemia leve",
                2: "Anemia moderada",
                3: "Anemia severa"
            }
            
            respuesta = {
                "tiene_anemia": tiene_anemia,
                "resultado": interpretaciones.get(prediccion, "Desconocido")
            }
            
            if distrito_warning:
                respuesta["advertencias"] = [distrito_warning]
            
            return Response(respuesta, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {"error": f"Error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def predecir_desde_registro(self, request, pk=None):

        modelo, le_distrito, feature_names = self.get_modelo()
        
        if modelo is None:
            return Response(
                {"error": "Modelo no disponible"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        try:
            instance = self.get_object()
            resultado = self._realizar_prediccion(instance, modelo, le_distrito, feature_names)
            return Response(resultado, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"Error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def info_modelo(self, request):

        modelo, le_distrito, feature_names = self.get_modelo()
        
        if modelo is None:
            return Response(
                {"error": "Modelo no disponible"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        return Response({
            "modelo_cargado": True,
            "tipo": type(modelo).__name__,
            "numero_caracteristicas": len(feature_names),
            "caracteristicas": feature_names,
            "clases": [int(c) for c in modelo.classes_],
            "interpretaciones": {
                "0": "Sin anemia",
                "1": "Anemia leve",
                "2": "Anemia moderada",
                "3": "Anemia severa"
            }
        }, status=status.HTTP_200_OK)
    
    def _realizar_prediccion(self, instance, modelo, le_distrito, feature_names):
        """Método interno para realizar predicción"""
        try:

            genero = str(instance.genero).upper()
            if genero in ['MASCULINO', 'M', 'MALE']:
                sexo_encoded = 1
            elif genero in ['FEMENINO', 'F', 'FEMALE']:
                sexo_encoded = 0
            else:
                sexo_encoded = 0  # Por defecto F
            
            edad_meses = float(instance.age) * 12
            
            cred = int(instance.cred)
            suplementacion = int(instance.suplementacion)
            altura_ren = getattr(instance, 'altura_ren', 0)  # Este puede quedar por defecto
            
            datos = {
                'Sexo': sexo_encoded,
                'Peso': float(instance.peso),
                'Talla': float(instance.talla),
                'Cred': cred,
                'Suplementacion': suplementacion,
                'DistritoREN': 0,
                'AlturaREN': float(altura_ren),
                'Edad': edad_meses,
                'IMC': float(instance.peso) / ((float(instance.talla)/100) ** 2),
                'Peso_Talla_Ratio': float(instance.peso) / float(instance.talla),
                'EdadMeses': edad_meses,
                'EdadAnios': float(instance.age)
            }
            
            entrada = pd.DataFrame([datos])
            entrada = entrada[feature_names]
            
            # Transformar distrito
            try:
                distrito_str = str(instance.distrito).upper()
                entrada.loc[0, 'DistritoREN'] = le_distrito.transform([distrito_str])[0]
            except:
                entrada.loc[0, 'DistritoREN'] = 0
            
            # Predecir
            prediccion = modelo.predict(entrada)[0]
            
            # Determinar si tiene anemia (cualquier clase diferente de 0)
            tiene_anemia = prediccion != 0
            
            interpretaciones = {
                0: "Sin anemia",
                1: "Anemia leve",
                2: "Anemia moderada",
                3: "Anemia severa"
            }
            
            return {
                "tiene_anemia": tiene_anemia,
                "resultado": interpretaciones.get(prediccion, "Desconocido")
            }
        except Exception as e:
            import traceback
            return {
                "error": f"Error en predicción: {str(e)}",
                "detalles": traceback.format_exc()
            }