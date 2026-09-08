# Testing Strategy

## Objetivo

Garantizar que el código sea correcto, mantenible y que los indicadores EVM se calculen de forma precisa.

**Target:** Coverage ≥ 80% en lógica de negocio

---

## Niveles de Testing

### 1. Unit Tests

**Objetivo:** Validar lógica aislada

**Scope:**
- Funciones de Services
- Funciones de Repositories (cuando crítico)
- Utilidades y helpers

**Framework:** pytest

**Ubicación:** `backend/tests/test_*.py`

**Ejemplo de estructura:**
```
tests/
├── test_health.py
├── test_evm_service.py
├── test_project_service.py
├── test_activity_service.py
└── ...
```

#### Unit Tests para EVM

Casos a cubrir:

```python
def test_cv_normal():
    # CV = EV - AC
    # Caso: EV > AC (favorable)
    pass

def test_sv_normal():
    # SV = EV - PV
    # Caso: EV < PV (retrasado)
    pass

def test_cpi_normal():
    # CPI = EV / AC
    # Caso: CPI > 1 (eficiente)
    pass

def test_cpi_undefined():
    # AC = 0
    # Retorna null
    pass

def test_spi_undefined():
    # PV = 0
    # Retorna null
    pass

def test_eac_undefined():
    # CPI = 0 (EV < AC)
    # Retorna null
    pass

def test_progress_validation():
    # Progress fuera de [0, 1]
    # Lanza excepción
    pass

def test_bac_validation():
    # BAC <= 0
    # Lanza excepción
    pass

def test_project_consolidation():
    # Múltiples actividades
    # Consolidación correcta
    pass

def test_project_no_activities():
    # Proyecto sin actividades
    # Manejo correcto
    pass
```

### 2. Integration Tests

**Objetivo:** Validar endpoints y flujos

**Scope:**
- Endpoints HTTP
- Flujos completos (crear → leer → actualizar)
- Contratos de API

**Framework:** pytest + TestClient de FastAPI

**Ubicación:** `backend/tests/test_*.py` con fixture `client`

**Ejemplo de estructura:**
```python
def test_get_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()

def test_create_project(client):
    payload = {"name": "Test", "bac": 1000}
    response = client.post("/projects", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test"
    assert "id" in data
```

#### Integration Tests Mínimos

Cada endpoint debe tener:

- ✅ Test de creación (201)
- ✅ Test de lectura (200)
- ✅ Test de actualización (200)
- ✅ Test de eliminación (204)
- ✅ Test de no encontrado (404)
- ✅ Test de validación (422)

---

## Estructura de Tests

### Conftest (Fixtures)

**Archivo:** `backend/tests/conftest.py`

**Propósito:** Fixtures reutilizables

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def sample_project():
    return {
        "name": "Test Project",
        "description": "Test Description",
        "bac": 10000.0,
    }

@pytest.fixture
def sample_activity():
    return {
        "name": "Test Activity",
        "project_id": 1,
        "bac": 5000.0,
        "planned_progress": 0.5,
        "actual_progress": 0.3,
        "actual_cost": 2000.0,
    }
```

### Test File Pattern

```python
# tests/test_project_service.py
import pytest
from app.services.project_service import ProjectService

class TestProjectService:
    def test_create_project(self):
        service = ProjectService()
        result = service.create({"name": "Test"})
        assert result.name == "Test"
    
    def test_get_project(self):
        service = ProjectService()
        # Setup
        project = service.create({"name": "Test"})
        # Test
        retrieved = service.get(project.id)
        assert retrieved.id == project.id

# tests/test_project_endpoints.py
def test_list_projects(client):
    response = client.get("/projects")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_project(client):
    payload = {"name": "New", "bac": 1000}
    response = client.post("/projects", json=payload)
    assert response.status_code == 201
```

---

## Coverage

### Ejecutar coverage

```bash
cd backend
pytest --cov=app --cov-report=html --cov-report=term
```

### Verificar coverage

```bash
# Solo mostrar resumen
pytest --cov=app --cov-report=term-missing

# Generar HTML
pytest --cov=app --cov-report=html
# Abrir backend/htmlcov/index.html en navegador
```

### Target

- **Lógica de negocio (Services):** ≥ 80%
- **Repositories:** ≥ 70%
- **Routers:** ≥ 60% (menos crítico)
- **Models:** ≥ 60% (menos crítico)

---

## Running Tests

### Todos los tests
```bash
cd backend
pytest
```

### Con verbosidad
```bash
cd backend
pytest -v
```

### Con output detallado
```bash
cd backend
pytest -vv
```

### Solo un archivo
```bash
cd backend
pytest tests/test_evm_service.py -v
```

### Solo una función
```bash
cd backend
pytest tests/test_evm_service.py::test_cpi_normal -v
```

### Con markers
```bash
cd backend
pytest -m evm  # Solo tests con @pytest.mark.evm
```

### Failfast (parar en primer error)
```bash
cd backend
pytest -x
```

### Último fallo
```bash
cd backend
pytest --lf
```

---

## Edge Cases a Testear

### Para EVM

- [x] AC = 0 → CPI indefinido
- [x] PV = 0 → SPI indefinido
- [x] EV = 0 → CV = -AC (válido)
- [x] CPI = 0 → EAC indefinido
- [x] Progress = 0% → EV = 0
- [x] Progress = 100% → EV = BAC
- [x] Progress < 0% → Error
- [x] Progress > 100% → Error
- [x] BAC = 0 → Error
- [x] BAC < 0 → Error
- [x] AC < 0 → Válido
- [x] Proyecto sin actividades → Manejo correcto

### Para CRUD

- [x] Crear con datos válidos → 201
- [x] Crear con datos inválidos → 422
- [x] Leer existente → 200
- [x] Leer inexistente → 404
- [x] Actualizar → 200
- [x] Actualizar inexistente → 404
- [x] Eliminar → 204
- [x] Eliminar inexistente → 404

---

## Pytest Configuration

**Archivo:** `backend/pytest.ini`

```ini
[pytest]
pythonpath = .
testpaths = tests
addopts = --tb=short -v
```

---

## CI/CD Integration

Estos tests serán ejecutados por CI/CD antes de merge.

**Comando típico:**
```bash
cd backend && pytest --cov=app --cov-fail-under=80
```

---

## Herramientas

| Herramienta | Versión | Propósito |
|-------------|---------|----------|
| pytest | 7.4.3+ | Test runner |
| pytest-cov | 4.1.0+ | Coverage |
| pytest-asyncio | 0.21.1+ | Async support |
| httpx | 0.25.2+ | HTTP client (TestClient) |

---

**Última actualización:** Foundation - Testing strategy
