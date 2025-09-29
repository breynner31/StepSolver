# Configuración de StepSolver

## Variables de Entorno

Para configurar la aplicación correctamente, crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```bash
# Configuración de Flask
FLASK_SECRET_KEY=tu-clave-secreta-muy-segura-aqui
FLASK_ENV=development

# Configuración de Gemini AI (opcional)
GEMINI_API_KEY=tu-api-key-de-gemini-aqui
```

## Generación de Clave Secreta

Si no especificas `FLASK_SECRET_KEY`, la aplicación generará automáticamente una clave segura usando `secrets.token_hex(32)`.

## Seguridad

- **NUNCA** subas el archivo `.env` a GitHub
- El archivo `.env` está incluido en `.gitignore`
- Para producción, usa variables de entorno del servidor

## Configuración por Entorno

### Desarrollo
- `FLASK_ENV=development`
- CORS habilitado para `http://localhost:3000`
- Debug mode activado

### Producción
- `FLASK_ENV=production`
- CORS configurado via `ALLOWED_ORIGINS`
- Debug mode desactivado

## Ejemplo de .env

```bash
FLASK_SECRET_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6
FLASK_ENV=development
GEMINI_API_KEY=AIzaSyBxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
