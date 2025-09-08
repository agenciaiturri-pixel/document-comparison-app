# 🚀 Despliegue Rápido - 5 Minutos

## ✅ Estado Actual
- ✅ Código listo para producción
- ✅ Archivos de configuración creados
- ✅ Repositorio Git inicializado
- ✅ Scripts de despliegue preparados

## 🎯 Próximos Pasos (5 minutos)

### 1. GitHub (1 minuto)
```bash
# Crear repositorio en https://github.com/new
# Nombre: document-comparison-app
# Luego ejecutar:
git remote add origin https://github.com/TU-USUARIO/document-comparison-app.git
git push -u origin main
```

### 2. Vercel - Frontend (2 minutos)
1. Ve a [vercel.com](https://vercel.com)
2. Login con GitHub
3. "New Project" → Selecciona tu repo
4. **Root Directory**: `frontend`
5. Deploy

### 3. Railway - Backend (2 minutos)
1. Ve a [railway.app](https://railway.app)
2. Login con GitHub
3. "New Project" → "Deploy from GitHub"
4. Selecciona tu repositorio
5. Agrega PostgreSQL database
6. Variables de entorno:
   ```
   SECRET_KEY=tu-clave-secreta
   ALLOWED_ORIGINS=https://tu-app.vercel.app
   DATABASE_URL=${{Postgres.DATABASE_URL}}
   ```

## 🌐 URLs Finales
- **App**: `https://tu-proyecto.vercel.app`
- **API**: `https://tu-backend.railway.app`
- **Docs**: `https://tu-backend.railway.app/docs`

## 💡 Tips
- Vercel detecta automáticamente Next.js
- Railway detecta automáticamente el Dockerfile
- Los despliegues son automáticos desde Git
- Ambos servicios tienen planes gratuitos

## 🆘 Ayuda
Si tienes problemas, revisa:
- `DEPLOYMENT_GUIDE.md` - Guía completa
- `README.md` - Documentación general
- Logs en Vercel/Railway dashboards

---
**¡Tu aplicación estará en línea en menos de 5 minutos!** 🎉