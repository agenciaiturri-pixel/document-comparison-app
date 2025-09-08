@echo off
echo ========================================
echo    DESPLIEGUE EN LINEA - AUTOMATIZADO
echo ========================================
echo.

echo [1/5] Verificando repositorio Git...
if not exist ".git" (
    echo ERROR: No se encontro repositorio Git
    echo Ejecuta: git init
    pause
    exit /b 1
)

echo [2/5] Agregando cambios recientes...
git add .
git commit -m "Preparando para despliegue en linea" 2>nul

echo [3/5] Creando archivo de configuracion para Railway...
echo PORT=8000 > backend\.env.production
echo DATABASE_URL=postgresql://user:pass@host:5432/db >> backend\.env.production
echo SECRET_KEY=change-this-in-production >> backend\.env.production
echo ALLOWED_ORIGINS=https://your-app.vercel.app >> backend\.env.production

echo [4/5] Preparando frontend para Vercel...
cd frontend
if not exist "vercel.json" (
    echo ERROR: vercel.json no encontrado
    cd ..
    pause
    exit /b 1
)

echo [5/5] Instrucciones de despliegue:
echo.
echo ========================================
echo           PASOS A SEGUIR
echo ========================================
echo.
echo 1. CREAR REPOSITORIO EN GITHUB:
echo    - Ve a https://github.com/new
echo    - Nombre: document-comparison-app
echo    - Publico o Privado
echo    - NO inicializar con archivos
echo.
echo 2. SUBIR CODIGO A GITHUB:
echo    git remote add origin https://github.com/TU-USUARIO/document-comparison-app.git
echo    git push -u origin main
echo.
echo 3. DESPLEGAR FRONTEND EN VERCEL:
echo    - Ve a https://vercel.com
echo    - Login con GitHub
echo    - New Project ^> Import tu repositorio
echo    - Root Directory: frontend
echo    - Deploy
echo.
echo 4. DESPLEGAR BACKEND EN RAILWAY:
echo    - Ve a https://railway.app
echo    - Login con GitHub
echo    - New Project ^> Deploy from GitHub
echo    - Selecciona tu repositorio
echo    - Agrega PostgreSQL database
echo    - Configura variables de entorno
echo.
echo 5. CONFIGURAR VARIABLES DE ENTORNO:
echo    Ver archivo DEPLOYMENT_GUIDE.md para detalles
echo.
echo ========================================
echo Tu app estara en linea en minutos!
echo ========================================
echo.
pause