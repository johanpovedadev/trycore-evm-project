# CLAUDE.md - Instrucciones para Agentes de IA

Este archivo contiene instrucciones específicas para agentes de IA que trabajen en este repositorio.

## Lectura Inicial Obligatoria

Antes de hacer CUALQUIER cambio en el código:

1. Lee completamente **AGENTS.md**
2. Lee completamente **CLAUDE.md**
3. Inspecciona el código existente relacionado

## Restricciones Fundamentales

### Nunca:
- [ ] Crear commits automáticamente
- [ ] Hacer push automático
- [ ] Modificar la arquitectura sin justificación explícita
- [ ] Inventar requisitos o features
- [ ] Colocar lógica de negocio en routers
- [ ] Calcular EVM en el frontend
- [ ] Agregar complejidad innecesaria
- [ ] Afirmar que algo funciona sin ejecutarlo

## Reglas de Codificación

### Arquitectura

Cualquier nueva funcionalidad debe respetar:

```
HTTP Request
    ↓
Router (validación HTTP)
    ↓
Service (lógica de negocio)
    ↓
Repository (acceso a BD)
    ↓
Model (persistencia)
    ↓
PostgreSQL
```

### Separación de Responsabilidades

**Routers** (`app/routers/`):
- Manejar HTTP requests
- Validar estructura básica de entrada
- Retornar respuestas HTTP
- **NO contiene lógica de negocio**

**Services** (`app/services/`):
- Lógica de negocio pura
- Orquestación de repositories
- Cálculos EVM
- Validaciones de dominio

**Repositories** (`app/repositories/`):
- CRUD operations
- Queries SQL
- Mapeo de Models
- **NO contiene lógica de negocio**

### Type Hints

Todas las funciones deben tener type hints:

```python
def calculate_evm(bac: float, pv: float) -> EVMIndicators:
    pass
```

## Desarrollo de Features

### Paso 1: Planificación
- Lee AGEND.md para entender la fase
- Identifica qué necesita: Model, Schema, Service, Repository, Router
- No implementes más de lo necesario

### Paso 2: Implementación
- Comienza con Model (en `app/models/`)
- Luego Schema (en `app/schemas/`)
- Luego Repository (en `app/repositories/`)
- Luego Service (en `app/services/`)
- Por último Router (en `app/routers/`)

### Paso 3: Testing
- Crea tests unitarios para Services
- Crea tests de integración para endpoints
- Ejecuta: `pytest --cov=app`
- Verifica coverage ≥ 80%

### Paso 4: Linting
- Ejecuta: `ruff check app/`
- Corrige todos los errores
- NO fuerces --no-fix

### Paso 5: Validación
- Verifica que FastAPI arranque
- Prueba manualmente los endpoints
- Verifica que tests pasen

## Testing

### Ejecutar tests
```bash
cd backend
pytest
```

### Tests con coverage
```bash
cd backend
pytest --cov=app --cov-report=html
```

### Tests solo de un archivo
```bash
cd backend
pytest tests/test_health.py -v
```

### Crear tests

**Pattern para unit tests de Services:**
```python
def test_service_calculates_correctly():
    service = MyService()
    result = service.my_method(input)
    assert result.expected_field == expected_value
```

**Pattern para integration tests de routers:**
```python
def test_endpoint_returns_correct_status(client):
    response = client.get("/api/endpoint")
    assert response.status_code == 200
    data = response.json()
    assert "expected_field" in data
```

## Linting y Code Quality

### Ejecutar Ruff
```bash
cd backend
ruff check app/
```

### Ruff con auto-fix
```bash
cd backend
ruff check app/ --fix
```

### Nunca
- No hagas commits automáticos
- No ignores errores de Ruff
- No uses `# noqa` sin justificación

## Validación Después de Cambios

Después de cada cambio importante:

```bash
# 1. Tests
cd backend && pytest

# 2. Coverage
cd backend && pytest --cov=app

# 3. Lint
cd backend && ruff check app/

# 4. Servidor
cd backend && uvicorn app.main:app --reload

# 5. Verificar /health
curl http://localhost:8000/health
```

## AI_PROCESS.md

**IMPORTANTE:** Debes registrar EXACTAMENTE:

1. **Fecha** de la intervención
2. **Herramienta de IA** usada (Claude, etc.)
3. **Objetivo** de la tarea
4. **Prompt exacto** usado
5. **Respuesta/resultado** obtenida
6. **Qué se aceptó** del resultado
7. **Qué se rechazó** del resultado
8. **Validación realizada** (tests, ejecución, etc.)
9. **Decisión humana** final

**Nunca:**
- Inventes prompts posteriores
- Reconstruyas prompts de memoria
- Añadas prompts de otras sesiones

## Cambios y Commits

### Restricción Explícita
- Los agentes de IA **NO crean commits**
- Los agentes de IA **NO hacen push**
- El usuario hace git add, git commit, git push manualmente

### Cambios Pequeños
- Máximo 200 líneas por cambio
- Una funcionalidad por cambio
- Cambios revisables

## Comunicación

Después de cada intervención:

1. Reporta **qué cambiaste**
2. Reporta **qué tests corriste**
3. Reporta **resultado de lint**
4. Reporta **bloqueos o dudas**
5. **Nunca afirmes que algo funciona sin ejecutarlo**

## Referencia Rápida de Comandos

```bash
# Backend setup
cd backend
pip install -r requirements.txt

# Database (en otra terminal)
docker-compose up -d

# Servidor de desarrollo
cd backend
uvicorn app.main:app --reload

# Frontend setup
cd frontend
npm install

# Frontend dev
cd frontend
npm run dev

# Tests
cd backend
pytest

# Coverage
cd backend
pytest --cov=app --cov-report=html

# Lint
cd backend
ruff check app/

# Lint con fix
cd backend
ruff check app/ --fix
```

## Gitflow y Commits

### Estructura de Ramas

```
main (rama estable, lista para entrega)
  ↑
  release/* (candidatos a entrega)
  ↑
  develop (rama de integración)
  ↑
  feature/* (desarrollo de funcionalidades)
```

### Ciclo de Desarrollo de una Feature

```
1. git checkout -b feature/nombre-descriptivo (desde develop)
2. Implementar funcionalidad
3. Unit tests
4. Integration tests
5. Ejecutar: pytest --cov=app
6. Ejecutar: ruff check app/
7. Commits locales
8. git push origin feature/nombre-descriptivo
9. Pull Request a develop
10. Revisión
11. Merge a develop
```

### Reglas de Commits

Los commits deben ser:
- **Descriptivos**: mensaje claro sobre qué cambia
- **Pequeños**: relacionados con una sola intención
- **Imperativos**: "Add X", no "Added X" o "Adds X"
- **Atómicos**: compilables y testeable

**Ejemplos correctos:**
```
Initialize project foundation
Add EVM calculation service
Add EVM edge case tests for AC=0
Add project CRUD endpoints
Fix CPI calculation when AC equals zero
```

**Ejemplos incorrectos:**
```
✗ WIP - testing stuff
✗ Fixed things
✗ Updated files
✗ Changes to multiple features in one commit
```

### Antes del Commit

1. Verifica que tests pasen: `pytest`
2. Verifica coverage: `pytest --cov=app`
3. Verifica lint: `ruff check app/`
4. Verifica que .env NO esté staged: `git status`
5. Haz commit pequeno y descriptivo

### Flujo para Entrega

```
develop (contiene múltiples features)
  ↓
git checkout -b release/v0.1.0
  ↓
Validación final
  ↓
git merge a main (tag v0.1.0)
  ↓
git merge back a develop
```

---

**Última actualización:** Foundation inicial + Gitflow setup
