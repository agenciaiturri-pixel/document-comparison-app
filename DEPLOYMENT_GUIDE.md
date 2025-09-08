# 🚀 Guía de Despliegue en Línea

## Paso 1: Crear Repositorio en GitHub

1. Ve a [GitHub](https://github.com) y crea una cuenta si no tienes una
2. Crea un nuevo repositorio:
   - Nombre: `document-comparison-app`
   - Descripción: `Aplicación de comparación de documentos con Next.js y FastAPI`
   - Público o Privado (tu elección)
   - **NO** inicialices con README, .gitignore o licencia

3. Una vez creado, copia la URL del repositorio (ejemplo: `https://github.com/tu-usuario/document-comparison-app.git`)

4. En tu terminal, ejecuta:
```bash
git remote add origin https://github.com/tu-usuario/document-comparison-app.git
git push -u origin main
```

## Paso 2: Desplegar Frontend en Vercel

### Opción A: Desde GitHub (Recomendado)
1. Ve a [Vercel](https://vercel.com)
2. Regístrate con tu cuenta de GitHub
3. Haz clic en "New Project"
4. Selecciona tu repositorio `document-comparison-app`
5. Configura el proyecto:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`

6. Variables de entorno:
   ```
   NEXT_PUBLIC_API_URL=https://tu-backend-url.railway.app
   ```
   (La URL del backend la obtendrás en el siguiente paso)

7. Haz clic en "Deploy"

### Opción B: Desde CLI
1. Instala Vercel CLI: `npm i -g vercel`
2. En la carpeta `frontend`: `vercel`
3. Sigue las instrucciones

## Paso 3: Desplegar Backend en Railway

1. Ve a [Railway](https://railway.app)
2. Regístrate con tu cuenta de GitHub
3. Haz clic en "New Project"
4. Selecciona "Deploy from GitHub repo"
5. Elige tu repositorio `document-comparison-app`

### Configurar el Servicio Backend
1. Railway detectará automáticamente el `Dockerfile` en la carpeta `backend`
2. Configura las variables de entorno:
   ```
   DATABASE_URL=postgresql://usuario:password@host:puerto/database
   SECRET_KEY=tu-clave-secreta-muy-segura
   ALLOWED_ORIGINS=https://tu-frontend.vercel.app
   ```

### Configurar Base de Datos PostgreSQL
1. En Railway, haz clic en "+ New"
2. Selecciona "Database" → "PostgreSQL"
3. Copia la `DATABASE_URL` generada
4. Pégala en las variables de entorno del backend

## Paso 4: Actualizar Variables de Entorno

### En Vercel (Frontend)
1. Ve a tu proyecto en Vercel
2. Settings → Environment Variables
3. Agrega:
   ```
   NEXT_PUBLIC_API_URL=https://tu-backend.railway.app
   ```

### En Railway (Backend)
1. Ve a tu servicio backend
2. Variables → Add Variable
3. Agrega todas las variables necesarias

## Paso 5: Verificar Despliegue

1. **Frontend**: Tu app estará disponible en `https://tu-proyecto.vercel.app`
2. **Backend**: API disponible en `https://tu-backend.railway.app`
3. **Documentación API**: `https://tu-backend.railway.app/docs`

## 🔧 Comandos Útiles

### Actualizar Despliegue
```bash
# Hacer cambios en el código
git add .
git commit -m "Descripción de cambios"
git push origin main
```

### Ver Logs
- **Vercel**: Dashboard → Functions → View Function Logs
- **Railway**: Dashboard → Deployments → View Logs

## 🌐 URLs de Ejemplo

- **Frontend**: https://document-comparison-app.vercel.app
- **Backend API**: https://document-comparison-app-production.up.railway.app
- **API Docs**: https://document-comparison-app-production.up.railway.app/docs

## 🚨 Solución de Problemas

### Error de CORS
- Verifica que `ALLOWED_ORIGINS` en Railway incluya tu dominio de Vercel

### Error de Base de Datos
- Verifica que `DATABASE_URL` esté correctamente configurada
- Asegúrate de que la base de datos PostgreSQL esté ejecutándose

### Error de Build
- Revisa los logs en Vercel/Railway
- Verifica que todas las dependencias estén en `package.json`/`requirements.txt`

## 💰 Costos

- **Vercel**: Gratis para proyectos personales
- **Railway**: $5/mes después de los créditos gratuitos
- **Total**: ~$5/mes para una aplicación completa

## 🎉 ¡Listo!

Tu aplicación estará disponible en línea 24/7 con:
- ✅ HTTPS automático
- ✅ CDN global
- ✅ Escalado automático
- ✅ Monitoreo incluido
- ✅ Despliegues automáticos desde Git