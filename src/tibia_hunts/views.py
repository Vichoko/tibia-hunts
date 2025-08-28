from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    """Placeholder home page para TibiaHunts."""
    return HttpResponse("""
    <html>
    <head>
        <title>TibiaHunts - MVP</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #2c3e50; }
            .placeholder { background: #ecf0f1; padding: 20px; border-radius: 4px; margin: 20px 0; }
            .coming-soon { color: #7f8c8d; font-style: italic; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏹 TibiaHunts</h1>
            <p>Una plataforma comunitaria para registrar y compartir sesiones de caza en Tibia.</p>
            
            <div class="placeholder">
                <h3>🎯 Funcionalidades Planificadas (MVP)</h3>
                <ul>
                    <li>📝 Registrar hunts (sesiones de caza)</li>
                    <li>🗺️ Base de datos comunitaria de spots</li>
                    <li>📊 Métricas de XP/hr, Profit/hr, etc.</li>
                    <li>🔍 Buscar mejores spots por nivel/vocación</li>
                    <li>📋 Integración con Hunt Analyzer</li>
                </ul>
            </div>
            
            <div class="placeholder">
                <h3>🚧 Estado Actual</h3>
                <p class="coming-soon">Proyecto en desarrollo inicial - placeholder page</p>
                <p>Django 5.2.5 configurado y funcionando ✅</p>
                <p>Estructura del proyecto organizada en /src ✅</p>
                <p>Próximo: Modelos de datos según RFC v0.1</p>
            </div>
            
            <div class="placeholder">
                <h3>📖 Basado en RFC v0.1</h3>
                <p>Este proyecto sigue la especificación detallada en el RFC v0.1 que define:</p>
                <ul>
                    <li>Modelo de datos (Users, Characters, Spots, Hunts, etc.)</li>
                    <li>API REST para crear y consultar hunts</li>
                    <li>Parser para Hunt Analyzer output</li>
                    <li>Sistema de agregaciones y rankings</li>
                </ul>
            </div>
        </div>
    </body>
    </html>
    """)


def health(request):
    """Health check endpoint."""
    return HttpResponse("OK", content_type="text/plain")
