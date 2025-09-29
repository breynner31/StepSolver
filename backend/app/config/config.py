import os
import secrets

class Config:
    """Configuración base para la aplicación"""
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY') or secrets.token_hex(32)
    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
    
    # Configuración de WebSocket
    SOCKETIO_CORS_ALLOWED_ORIGINS = "*"
    
    # Configuración de archivos
    UPLOAD_FOLDER = 'static/audio'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    SOCKETIO_CORS_ALLOWED_ORIGINS = "http://localhost:3000"
    SOCKETIO_TRANSPORTS = ['polling']  # Solo polling para desarrollo

class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    SOCKETIO_CORS_ALLOWED_ORIGINS = os.environ.get('ALLOWED_ORIGINS', '').split(',')
    SOCKETIO_TRANSPORTS = ['polling', 'websocket']  # WebSockets habilitados en producción

# Configuración por defecto
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}