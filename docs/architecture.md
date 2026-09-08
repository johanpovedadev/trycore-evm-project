# Arquitectura del Proyecto

## Visión General

El proyecto sigue una arquitectura de capas clara y separada, donde cada componente tiene una responsabilidad específica.

## Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────┐
│              REACT FRONTEND (TypeScript)                │
│         (Vite dev server on port 5173)                  │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP / JSON
                     ↓
┌─────────────────────────────────────────────────────────┐
│         FASTAPI APPLICATION (Python 3.12+)              │
│              (uvicorn on port 8000)                     │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │  ROUTERS (app/routers/)                         │   │
│  │  - HTTP endpoints                              │   │
│  │  - Request validation (Pydantic)              │   │
│  │  - Response formatting                        │   │
│  └────────────────┬────────────────────────────────┘   │
│                   │                                    │
│  ┌────────────────↓────────────────────────────────┐   │
│  │  SERVICES (app/services/)                       │   │
│  │  - Business logic                               │   │
│  │  - EVM calculations                             │   │
│  │  - Domain validations                           │   │
│  │  - Orchestration                                │   │
│  └────────────────┬────────────────────────────────┘   │
│                   │                                    │
│  ┌────────────────↓────────────────────────────────┐   │
│  │  REPOSITORIES (app/repositories/)               │   │
│  │  - Data access abstraction                      │   │
│  │  - CRUD operations                              │   │
│  │  - Query building                               │   │
│  └────────────────┬────────────────────────────────┘   │
│                   │                                    │
│  ┌────────────────↓────────────────────────────────┐   │
│  │  MODELS (app/models/)                           │   │
│  │  - SQLAlchemy ORM models                        │   │
│  │  - Database schema representation              │   │
│  └────────────────┬────────────────────────────────┘   │
└────────────────────┼────────────────────────────────────┘
                     │ SQL
                     ↓
┌─────────────────────────────────────────────────────────┐
│       POSTGRESQL DATABASE                               │
│  (Docker container: trycore_postgres)                   │
└─────────────────────────────────────────────────────────┘
```

## Componentes Principales

### Frontend (React + TypeScript + Vite)

**Ubicación:** `/frontend`

**Responsabilidades:**
- Interfaz de usuario
- Presentación de datos
- Interacción con usuario
- Llamadas a API backend

**Características:**
- TypeScript para type safety
- Vite para bundling rápido
- Port: 5173

### Backend (FastAPI)

**Ubicación:** `/backend/app`

**Puerto:** 8000

**Capas:**

#### Routers
- **Archivo:** `app/routers/`
- **Responsabilidad:** Manejar HTTP
- **Regla:** NO contiene lógica de negocio
- **Ejemplo:** Validación de estructura JSON, status codes

#### Services
- **Archivo:** `app/services/`
- **Responsabilidad:** Lógica de negocio
- **Incluye:** Cálculos EVM, validaciones de dominio
- **Orquesta:** Repositories y Models

#### Repositories
- **Archivo:** `app/repositories/`
- **Responsabilidad:** Acceso a datos
- **Operaciones:** CRUD, queries
- **Regla:** NO contiene lógica de negocio

#### Models
- **Archivo:** `app/models/`
- **Tipo:** SQLAlchemy ORM models
- **Representa:** Schema de base de datos

#### Schemas
- **Archivo:** `app/schemas/`
- **Tipo:** Pydantic models
- **Uso:** Validación y serialización de entrada/salida

### Base de Datos (PostgreSQL)

**Ubicación:** Docker container via `docker-compose.yml`

**Configuración:**
- Host: `localhost`
- Port: 5432
- User: `trycore_user`
- Password: `trycore_password`
- Database: `trycore_evm`

**Gestión de migraciones:** Alembic

## Flujo de una Solicitud HTTP

```
1. Frontend envía GET /api/projects

2. FastAPI Router recibe la solicitud
   - Valida estructura básica
   - Extrae parámetros

3. Router llama Service.get_projects()

4. Service ejecuta lógica:
   - Valida permisos/dominio
   - Prepara parámetros
   - Llama Repository

5. Repository ejecuta query:
   - Construye SQLAlchemy query
   - Ejecuta contra PostgreSQL
   - Retorna Models

6. Service procesa Models:
   - Calcula indicadores si necesario
   - Aplica transformaciones
   - Retorna datos procesados

7. Router convierte a JSON (Pydantic Schema)

8. Frontend recibe respuesta JSON
```

## Separación de Responsabilidades

### ✅ Debe estar en Routers
- Validación de estructura HTTP
- Manejo de status codes
- CORS headers
- Swagger documentation

### ❌ NO debe estar en Routers
- Lógica de negocio
- Cálculos EVM
- Validaciones complejas de dominio
- Acceso a base de datos

### ✅ Debe estar en Services
- Cálculos de indicadores EVM
- Validaciones de reglas de negocio
- Orquestación de múltiples repositories
- Transformaciones de datos

### ✅ Debe estar en Repositories
- Queries SQL
- CRUD operations
- Mapeo ORM

### ✅ Debe estar en Models
- Definición de tablas
- Relaciones
- Constraints de BD

### ✅ Debe estar en Schemas
- Validación de entrada
- Serialización de salida
- Documentación de API

## Consideraciones de Diseño

### La lógica EVM NO está en el frontend
- Todos los cálculos ocurren en backend
- Frontend solo presenta datos

### Backend es la fuente de verdad
- Las métricas se calculan una sola vez en backend
- Frontend consume resultados pre-calculados

### Type Safety
- Backend: Type hints en Python
- Frontend: TypeScript

### Testing Strategy
- Unit tests para Services
- Integration tests para endpoints
- Coverage ≥ 80%

---

**Última actualización:** Foundation - Arquitectura inicial
