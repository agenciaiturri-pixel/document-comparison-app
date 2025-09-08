# Sistema de Comparación de Documentos

Aplicación web para comparar Facturas Comerciales con Bills of Lading, detectando discrepancias y generando reportes de riesgo.

## 🚀 Despliegue en Producción

### Opción 1: Docker Compose (Recomendado)

1. **Clonar el repositorio**
```bash
git clone <tu-repositorio>
cd docs
```

2. **Configurar variables de entorno**
```bash
cp backend/.env.example backend/.env
# Editar backend/.env con tus configuraciones
```

3. **Ejecutar con Docker Compose**
```bash
docker-compose up -d
```

La aplicación estará disponible en:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Base de datos: localhost:5432

### Opción 2: Despliegue Separado

#### Frontend en Vercel

1. **Conectar repositorio a Vercel**
   - Ir a [vercel.com](https://vercel.com)
   - Importar proyecto desde Git
   - Seleccionar carpeta `frontend`

2. **Configurar variables de entorno en Vercel**
   - `NEXT_PUBLIC_API_URL`: URL de tu backend (ej: https://tu-backend.railway.app)

3. **Deploy automático**
   - Vercel detectará Next.js automáticamente
   - El deploy se ejecutará en cada push

#### Backend en Railway

1. **Conectar repositorio a Railway**
   - Ir a [railway.app](https://railway.app)
   - Crear nuevo proyecto desde GitHub
   - Seleccionar carpeta `backend`

2. **Configurar variables de entorno**
```
PORT=8000
ENVIRONMENT=production
ALLOWED_ORIGINS=https://tu-frontend.vercel.app
DATABASE_URL=postgresql://...
```

3. **Agregar base de datos PostgreSQL**
   - En Railway, agregar servicio PostgreSQL
   - Copiar DATABASE_URL a las variables de entorno

#### Backend en Render

1. **Crear Web Service en Render**
   - Ir a [render.com](https://render.com)
   - Crear nuevo Web Service
   - Conectar repositorio

2. **Configuración del servicio**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Environment: Python 3.11

3. **Variables de entorno**
```
PORT=10000
ENVIRONMENT=production
ALLOWED_ORIGINS=https://tu-frontend.vercel.app
```

### Opción 3: VPS/Servidor Propio

1. **Instalar Docker y Docker Compose**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install docker.io docker-compose
```

2. **Clonar y configurar**
```bash
git clone <tu-repositorio>
cd docs
cp backend/.env.example backend/.env
# Editar configuraciones
```

3. **Ejecutar**
```bash
docker-compose up -d
```

4. **Configurar proxy reverso (Nginx)**
```nginx
server {
    listen 80;
    server_name tu-dominio.com;
    
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🛠️ Desarrollo Local

### Prerrequisitos
- Node.js 18+
- Python 3.11+
- Tesseract OCR

### Backend
```bash
cd backend
pip install -r requirements.txt
python main.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 📋 Variables de Entorno

### Backend (.env)
```
PORT=8000
HOST=0.0.0.0
ENVIRONMENT=development
UPLOAD_DIR=./uploads
REPORTS_DIR=./reports
ALLOWED_ORIGINS=http://localhost:3000
DATABASE_URL=postgresql://user:pass@localhost:5432/db
SECRET_KEY=your-secret-key
TESSERACT_CMD=/usr/bin/tesseract
```

### Frontend
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🔧 Características

- ✅ Subida de documentos (PDF, JPG, PNG)
- ✅ Interfaz multilenguaje (ES/EN)
- ✅ Comparación automática de documentos
- ✅ Sistema de semáforo de riesgo
- ✅ Reportes detallados
- 🚧 OCR con Tesseract
- 🚧 Base de datos PostgreSQL
- 🚧 Sistema de autenticación
- 🚧 Exportación de reportes

## 📞 Soporte

Para problemas de despliegue o configuración, revisar los logs:

```bash
# Docker Compose
docker-compose logs -f

# Servicios individuales
docker-compose logs backend
docker-compose logs frontend
```

## 🔧 Stack Tecnológico

### Frontend
- **Framework**: Next.js 14 con App Router
- **Styling**: Tailwind CSS
- **UI Components**: Headless UI / Radix UI
- **State Management**: Zustand
- **Forms**: React Hook Form + Zod
- **Internacionalización**: next-intl

### Backend
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **File Storage**: AWS S3 / Azure Blob
- **OCR**: Tesseract.js / Azure Document Intelligence
- **Queue**: Redis + BullMQ
- **Authentication**: JWT + bcrypt

### DevOps
- **Containerización**: Docker + Docker Compose
- **Orquestación**: Kubernetes (opcional)
- **CI/CD**: GitHub Actions
- **Monitoring**: Prometheus + Grafana

## 📁 Estructura del Proyecto

```
document-comparison-system/
├── frontend/                 # Aplicación Next.js
│   ├── src/
│   │   ├── app/             # App Router pages
│   │   ├── components/      # Componentes reutilizables
│   │   ├── lib/            # Utilidades y configuración
│   │   └── types/          # Definiciones TypeScript
│   ├── public/             # Archivos estáticos
│   └── package.json
├── backend/                 # API FastAPI
│   ├── app/
│   │   ├── api/            # Endpoints
│   │   ├── core/           # Configuración y seguridad
│   │   ├── models/         # Modelos de base de datos
│   │   ├── services/       # Lógica de negocio
│   │   └── utils/          # Utilidades
│   ├── requirements.txt
│   └── Dockerfile
├── docker-compose.yml       # Configuración de desarrollo
├── docs/                   # Documentación
└── README.md
```

## 🔒 Seguridad

- Roles (Analista/Supervisor)
- Límite 25MB por archivo
- Antivirus integrado
- TLS/HTTPS obligatorio
- Logs de auditoría y hashes SHA-256
- Opción "Modo efímero" (no guardar archivos)

## 📊 Criterios de Aceptación

- ✅ Procesar en <60s con progreso visible
- ✅ Detección correcta ≥90% de campos comunes
- ✅ 0 falsos positivos en IDs
- ✅ Reportes exportables con evidencia y trazabilidad

## 🧪 Casos de Prueba

- Caso todo coincide
- Diferencia en bultos
- Incoterm distinto
- Descripción similar (umbral)
- Faltan HS codes
- Contenedor inválido
- OCR baja confianza (<60%) → reintento

## 🚀 Instalación y Desarrollo

### Prerrequisitos
- Node.js 18+
- Python 3.11+
- Docker y Docker Compose
- PostgreSQL 15+

### Desarrollo Local

```bash
# Clonar repositorio
git clone <repository-url>
cd document-comparison-system

# Iniciar servicios con Docker
docker-compose up -d

# Frontend
cd frontend
npm install
npm run dev

# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 📝 API Endpoints

- `POST /api/upload` → Recibe archivos
- `POST /api/compare/:job_id` → Devuelve JSON comparativo
- `GET /api/result/:job_id.json` → Resultado crudo
- `GET /api/report/:job_id.pdf` → Reporte PDF

## 🔮 Roadmap Futuro

- Firma digital en PDF
- Webhook a ERP/forwarder
- Validación automática con catálogos UN/LOCODE y SUNAT
- Machine Learning para mejorar precisión OCR
- API GraphQL
- Mobile app

## 📄 Licencia

MIT License - ver archivo LICENSE para detalles.

## 🤝 Contribución

Ver CONTRIBUTING.md para guías de contribución.