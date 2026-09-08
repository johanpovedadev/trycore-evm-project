# Trycore EVM - Proyecto Backend

EVM (Earned Value Management) Backend API con React Frontend. Reto técnico Trycore Colombia - Ingeniero de Desarrollo.

## 📋 Descripción

Sistema de gestión de proyectos con indicadores de Earned Value Management (EVM). Permite crear proyectos, registrar actividades y calcular indicadores de desempeño integrados (CPI, SPI, EAC, VAC).

## 🎯 Objetivo

Implementar un backend profesional que:
- Calcula correctamente métricas EVM
- Maneja edge cases y validaciones
- Proporciona API REST consistente
- Integra con frontend React

## 🛠️ Stack Técnico

### Backend
- **Python 3.12+**
- **FastAPI** - Framework web
- **SQLAlchemy** - ORM
- **Alembic** - Migraciones de BD
- **PostgreSQL** - Base de datos
- **Pydantic** - Validación
- **pytest** - Testing
- **Ruff** - Linting

### Frontend
- **React 18** - UI Framework
- **TypeScript** - Type Safety
- **Vite** - Build tool

### Infraestructura
- **Docker Compose** - Orchestración local (PostgreSQL en puerto 5434)

## 🚀 Quick Start

```bash
# Terminal 1: Base de datos
docker-compose up -d

# Terminal 2: Backend (crear venv si es primera vez)
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Terminal 3: Frontend
cd frontend
npm install
npm run dev

# Abrir en navegador: http://localhost:5180
```

## 📁 Estructura del Proyecto

```
trycore-evm-project/
├── backend/
│   ├── app/
│   │   ├── core/           # Configuración, DB
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── repositories/   # Acceso a datos
│   │   ├── services/       # Lógica de negocio
│   │   ├── routers/        # Endpoints HTTP
│   │   └── main.py         # FastAPI app
│   ├── tests/              # Test suite
│   ├── alembic/            # Migraciones
│   ├── requirements.txt
│   ├── pytest.ini
│   └── pyproject.toml
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
│
├── docs/
│   ├── architecture.md      # Descripción arquitectura
│   ├── evm.md              # Documentación EVM
│   ├── testing.md          # Estrategia de testing
│   └── decisions.md        # Decisiones arquitectónicas
│
├── AGENTS.md               # Contrato técnico
├── CLAUDE.md              # Instrucciones IA
├── AGEND.md               # Roadmap
├── AI_PROCESS.md          # Log de intervenciones IA
├── docker-compose.yml
├── .env.example
└── .gitignore
```

## 🚀 Requisitos Previos

- **Python 3.12+** instalado
- **Node.js 18+** instalado
- **Docker y Docker Compose** (para PostgreSQL local)
- **Git**

## 📦 Instalación

### Backend

```bash
# Entrar al directorio backend
cd backend

# Crear virtual environment
python -m venv venv

# Activar virtual environment
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### Frontend

```bash
# Entrar al directorio frontend
cd frontend

# Instalar dependencias
npm install

# Configurar variable de entorno (opcional)
# Por defecto: http://localhost:8000
# Crear archivo .env.local si necesitas cambiar:
echo "VITE_API_URL=http://localhost:8000" > .env.local
```

### Base de Datos

```bash
# En la raíz del proyecto
docker-compose up -d

# Verificar que PostgreSQL está corriendo
docker-compose ps
```

## 🔧 Configuración

### Variables de Entorno

Crear archivo `.env` en la raíz de `backend/`:

```bash
# Copiar del template
cp .env.example .env

# Ajustar si es necesario (por defecto funciona con Docker)
```

**Valores por defecto (.env):**
- `DATABASE_URL`: `postgresql://trycore_user:trycore_password@localhost:5434/trycore_evm`
  - ⚠️ **IMPORTANTE:** Puerto 5434 (mapeado por docker-compose desde container 5432)
- `FASTAPI_ENV`: `development`
- `PORT`: `8000`
- `FRONTEND_URL`: `http://localhost:5173`

## ▶️ Ejecución

### Backend

```bash
cd backend

# Con virtual environment activado
uvicorn app.main:app --reload

# Servidor disponible en: http://localhost:8000
# Docs en: http://localhost:8000/docs
```

### Frontend

```bash
cd frontend

# Desarrollo con Vite
npm run dev

# Disponible en: http://localhost:5173
```

#### Build para Producción

```bash
cd frontend

# Compilar TypeScript y bundlear con Vite
npm run build

# Salida: ./dist/

# Verificar localmente la build
npm run preview
```

### Base de Datos

```bash
# Iniciar PostgreSQL (en otra terminal)
docker-compose up

# Detener PostgreSQL
docker-compose down

# Ver logs
docker-compose logs postgres
```

## ✅ Testing

### Ejecutar todos los tests

```bash
cd backend

pytest
```

### Ejecutar con coverage

```bash
cd backend

pytest --cov=app --cov-report=html

# Abrir reporte en: htmlcov/index.html
```

### Ejecutar tests específicos

```bash
cd backend

# Solo archivo
pytest tests/test_health.py -v

# Solo función
pytest tests/test_health.py::test_health_check -v
```

## 🧹 Linting

### Verificar código

```bash
cd backend

ruff check app/
```

### Auto-fix

```bash
cd backend

ruff check app/ --fix
```

## 📖 Documentación

### Leer primero:
1. **[AGENTS.md](./AGENTS.md)** - Contrato técnico del proyecto
2. **[docs/architecture.md](./docs/architecture.md)** - Arquitectura

### Documentación técnica:
- **[docs/evm.md](./docs/evm.md)** - EVM fórmulas y conceptos
- **[docs/testing.md](./docs/testing.md)** - Estrategia de testing
- **[docs/decisions.md](./docs/decisions.md)** - Decisiones arquitectónicas
- **[AGEND.md](./AGEND.md)** - Roadmap por fases

### Para agentes de IA:
- **[CLAUDE.md](./CLAUDE.md)** - Instrucciones para IA
- **[AI_PROCESS.md](./AI_PROCESS.md)** - Log de intervenciones

## 🔍 Endpoints Actuales

### Health Check
```
GET /health
```

**Response:**
```json
{
  "status": "ok",
  "message": "Service is running"
}
```

## 📊 API Docs

Cuando el backend está corriendo:

```
http://localhost:8000/docs        # Swagger UI
http://localhost:8000/redoc       # ReDoc
```

## 🌳 Gitflow

```
main (producción)
  ↑
  release/*
  ↑
  develop
  ↑
  feature/*
```

**Workflow:**
1. Crear rama `feature/mi-feature` desde `develop`
2. Trabajar y hacer commits locales
3. Crear Pull Request a `develop`
4. Después de review y tests: merge
5. Antes de entregar: `develop` → `release/v*` → `main`

## 🗂️ Estado del Proyecto

### ✅ Completado
- [x] Foundation (Fase 0)
  - [x] Estructura de directorios
  - [x] FastAPI setup
  - [x] PostgreSQL con Docker
  - [x] pytest y pytest-cov
  - [x] Ruff configuration
  - [x] React + TypeScript + Vite
  - [x] Documentación inicial
  - [x] Endpoint `/health`

- [x] Fase 1: EVM Domain
  - [x] Modelos de dominio (Project, Activity)
  - [x] Cálculos EVM (CPI, SPI, EAC, VAC, CV, SV)
  - [x] Validaciones edge cases

- [x] Fase 2: Backend CRUD
  - [x] CRUD Projects
  - [x] CRUD Activities
  - [x] Validaciones de negocio

- [x] Fase 3: EVM Integration
  - [x] Cálculo automático de indicadores

- [x] Fase 4: Integration Testing
  - [x] Tests unitarios (Services)
  - [x] Tests de integración (Endpoints)

- [x] Fase 5: Frontend Dashboard
  - [x] Project Selector con Create
  - [x] Activity Table con CRUD inline
  - [x] Indicators Panel consolidados
  - [x] Charts (PV/EV/AC)
  - [x] API client con error handling

### ⏳ Pendiente
- [ ] Fase 6: Frontend Refinement (si se requiere)
- [ ] Fase 7: E2E Testing
- [ ] Fase 8: Quality & Refactoring
- [ ] Fase 9: Documentación Completa
- [ ] Fase 10: Gitflow & Release
- [ ] Fase 11: Final Validation

Ver [AGEND.md](./AGEND.md) para detalles de cada fase.

## 🔐 Restricciones de Scope

**NO implementado (por ahora):**
- ❌ Autenticación / JWT
- ❌ OAuth
- ❌ Microservicios
- ❌ Kubernetes
- ❌ Redis / Celery
- ❌ CI/CD pipeline
- ❌ Cloud infrastructure
- ❌ WebSockets

Se agregarán **solo si hay requisito explícito**.

## 📝 Committing

**El proyecto usa Gitflow. Cambios se hacen en branches feature y se mergean a `develop`.**

No commits automáticos.

## 🤖 Uso de IA

Este proyecto fue desarrollado con asistencia de IA (Claude).

- Leer [CLAUDE.md](./CLAUDE.md) para instrucciones
- Revisar [AI_PROCESS.md](./AI_PROCESS.md) para historial

## 🐛 Troubleshooting

### PostgreSQL no conecta
```bash
# Verificar que Docker está corriendo
docker-compose ps

# Ver logs
docker-compose logs postgres

# Reiniciar
docker-compose restart postgres
```

### Port ya en uso
```bash
# Backend (8000)
lsof -i :8000  # Ver proceso
kill -9 <PID>  # Matar proceso

# Frontend (5173)
lsof -i :5173
```

### Tests fallan
```bash
# Verificar que virtual environment está activado
source venv/bin/activate

# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall

# Correr tests con debug
pytest -vv
```

## 📚 Referencias

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Pydantic Docs](https://docs.pydantic.dev/)
- [pytest Docs](https://docs.pytest.org/)
- [Alembic Docs](https://alembic.sqlalchemy.org/)
- [React Docs](https://react.dev/)
- [TypeScript Docs](https://www.typescriptlang.org/)
- [Vite Docs](https://vitejs.dev/)

## 📄 Licencia

Proyecto educativo - Trycore Colombia

## 👤 Autor

Desarrollo: Claude Haiku 4.5 (Asistencia IA) + Desarrollador Humano

**Última actualización:** 2026-09-07

---

**Próximo paso:** Ver [AGEND.md](./AGEND.md) - Fase 1: EVM Domain

