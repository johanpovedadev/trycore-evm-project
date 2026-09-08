# Architectural Decision Records (ADRs)

## ADR-001: Framework Backend - FastAPI

**Fecha:** 2026-09-07

**Status:** Aceptada

**Context:**
- Necesitamos un framework REST API moderno para Python
- Requisitos: type hints, performance, documentación automática, validación

**Decisión:**
Usar FastAPI como framework principal del backend.

**Razones:**
- ✅ Type hints nativo (Pydantic)
- ✅ Performance comparable a Node.js
- ✅ OpenAPI/Swagger automático
- ✅ Validación built-in
- ✅ Async/await soportado
- ✅ Comunidad grande
- ✅ Documentación excelente

**Alternativas Rechazadas:**
- Django REST: Demasiado heavyweight para este scope
- Flask: Falta features out-of-the-box
- Starlette: Nivel demasiado bajo

---

## ADR-002: Arquitectura en Capas - Router → Service → Repository

**Fecha:** 2026-09-07

**Status:** Aceptada

**Context:**
- Necesitamos separación clara de responsabilidades
- Backend tendrá lógica EVM compleja
- Debe ser mantenible y testeable

**Decisión:**
Implementar arquitectura de capas estricta:

```
HTTP Routers
    ↓
Services (Lógica de Negocio)
    ↓
Repositories (Acceso a Datos)
    ↓
SQLAlchemy Models
    ↓
PostgreSQL
```

**Razones:**
- ✅ Separación de responsabilidades clara
- ✅ Fácil de testear
- ✅ Code reusable
- ✅ Mantenibilidad
- ✅ Escalable

**Reglas Asociadas:**
1. Routers NUNCA contienen lógica de negocio
2. Services orquestan la lógica
3. Repositories son abstracciones de acceso a datos
4. Models representan el schema de BD

---

## ADR-003: Base de Datos - PostgreSQL

**Fecha:** 2026-09-07

**Status:** Aceptada

**Context:**
- Necesitamos RDBMS confiable
- EVM requiere integridad referencial
- Transacciones ACID son críticas

**Decisión:**
Usar PostgreSQL como base de datos principal.

**Razones:**
- ✅ RDBMS maduro y confiable
- ✅ Excelente para consultas complejas
- ✅ ACID compliance
- ✅ Triggers y stored procedures si necesario
- ✅ Free y open source
- ✅ Docker simplifica local development

**Configuración:**
- Host: `localhost:5432`
- User: `trycore_user`
- DB: `trycore_evm`
- Gestión de migraciones: Alembic

---

## ADR-004: Lógica EVM - Aislada en Services

**Fecha:** 2026-09-07

**Status:** Aceptada

**Context:**
- EVM es el core del proyecto
- Cálculos complejos con múltiples edge cases
- Deben ser testeable e independiente de HTTP/BD

**Decisión:**
La lógica EVM vive exclusivamente en `app/services/evm_service.py`.

**Reglas:**
1. Lógica EVM es **independiente de HTTP**
2. Lógica EVM es **independiente de persistencia**
3. Services reciben datos y retornan indicadores
4. Frontend **NUNCA** calcula EVM
5. Backend es la **fuente de verdad**

**Beneficios:**
- ✅ Fácil de testear
- ✅ Reutilizable
- ✅ No duplicación de lógica

**Ejemplo:**
```python
# ✅ Correcto
def calculate_cpi(ev: float, ac: float) -> Optional[float]:
    if ac == 0:
        return None
    return ev / ac

# ❌ Incorrecto
@router.get("/indicators")
def get_indicators(activity_id: int):
    # No poner lógica aquí
    cpi = ev / ac  # ❌
```

---

## ADR-005: Consolidación de Indicadores por Proyecto

**Fecha:** 2026-09-07

**Status:** Aceptada

**Context:**
- Un proyecto tiene múltiples actividades
- Necesitamos indicadores consolidados del proyecto
- Hay dos formas de calcularlos: suma de totales vs promedio de ratios

**Decisión:**
Los indicadores de proyecto se calculan **consolidando primero** (sumando todos los BAC, PV, EV, AC) **y luego calculando ratios**.

**Fórmula Correcta:**
```
BAC_proyecto = Σ BAC_actividades
PV_proyecto = Σ PV_actividades
EV_proyecto = Σ EV_actividades
AC_proyecto = Σ AC_actividades

CPI_proyecto = EV_proyecto / AC_proyecto
SPI_proyecto = EV_proyecto / PV_proyecto
```

**Fórmula Incorrecta:**
```
❌ CPI_proyecto = Promedio(CPI_actividades)
❌ SPI_proyecto = Promedio(SPI_actividades)
```

**Razón:**
- Los promedios ponderados distorsionan la realidad
- La consolidación refleja el estado real del proyecto

**Referencia:**
PMI Project Management Institute - Practice Standard

---

## ADR-006: Representación de Valores Indefinidos

**Fecha:** 2026-09-07

**Status:** Aceptada

**Context:**
- Algunos ratios son matemáticamente indefinidos
  - CPI cuando AC = 0
  - SPI cuando PV = 0
  - EAC cuando CPI es indefinido
- JSON no soporta Infinity ni NaN
- Necesitamos representación clara y consistente

**Decisión:**
Representar valores indefinidos como **`null`** en JSON.

**Reglas:**
- CPI = null cuando AC = 0
- SPI = null cuando PV = 0
- EAC = null cuando CPI es indefinido
- VAC = null cuando EAC es indefinido
- CPI = 0 cuando EV/AC y ambos >= 0 y AC != 0 (caso válido, no indefinido)

**Ejemplo:**
```json
{
  "cpi": 1.25,        // Válido
  "spi": 0.95,        // Válido
  "eac": 800.0,       // Válido
  "vac": 200.0        // Válido
}

// Cuando AC = 0
{
  "cpi": null,        // Indefinido
  "eac": null,        // Indefinido
  "vac": null         // Indefinido
  "spi": 0.95         // Válido, PV puede ser > 0
}
```

**Beneficios:**
- ✅ Explícito y claro
- ✅ JSON-compatible
- ✅ Fácil de manejar en frontend
- ✅ No hay ambigüedad

---

## ADR-007: Frontend Type Safety - TypeScript

**Fecha:** 2026-09-07

**Status:** Aceptada

**Context:**
- Frontend tiene lógica de presentación compleja
- Integración con API backend
- Necesidad de mantenibilidad

**Decisión:**
Usar TypeScript en todo el frontend.

**Razones:**
- ✅ Type safety
- ✅ IntelliSense
- ✅ Prevención de bugs
- ✅ Documentación implícita

---

## ADR-008: Testing - Coverage Mínimo 80%

**Fecha:** 2026-09-07

**Status:** Aceptada

**Context:**
- EVM requiere exactitud
- Bugs en cálculos afectan decisiones del proyecto
- Necesitamos confianza en el código

**Decisión:**
Mantener mínimo 80% de coverage en lógica de negocio (Services).

**Target:**
- Services: ≥ 80%
- Repositories: ≥ 70%
- Routers: ≥ 60%

**Método:**
```bash
pytest --cov=app --cov-report=html
```

**Enforced:**
CI/CD rechazará merges que reduzcan coverage.

---

## ADR-009: Linting - Ruff para Python

**Fecha:** 2026-09-07

**Status:** Aceptada

**Context:**
- Necesitamos estándares de código consistente
- Python permite mucho "magic"
- Queremos evitar deuda técnica

**Decisión:**
Usar Ruff como linter principal.

**Configuración:**
- `backend/pyproject.toml`
- Reglas: E, W, F, I, N
- Line length: 120

**Enforced:**
Todos los commits deben pasar lint.

---

## ADR-010: Versionado de API

**Fecha:** 2026-09-07

**Status:** Pendiente (Fase 2)

**Context:**
- API evolucionará
- Necesitaremos compatibilidad backward
- Clientes pueden estar en diferentes versiones

**Decisión Tentativa:**
Versionado en URL: `/api/v1/projects`

**Revisión:** Se tomará en Fase 2 cuando se cree el primer endpoint de negocio.

---

## ADR-011: Autenticación y Autorización

**Fecha:** 2026-09-07

**Status:** Rechazada (Por ahora)

**Context:**
- El proyecto inicial no requiere autenticación
- Agregar JWT aumentaría complejidad
- Requisitos no lo especifican

**Decisión:**
NO implementar autenticación en Foundation.

**Revisión:**
Si en fases posteriores aparece requisito explícito, se reconsiderará.

---

## ADR-012: Infraestructura - Docker Compose solo para DB

**Fecha:** 2026-09-07

**Status:** Aceptada

**Context:**
- Desarrollo local debe ser simple
- Backend y frontend arrancan directo en máquina
- Solo DB merece ser containerizada

**Decisión:**
- PostgreSQL: Docker container via `docker-compose.yml`
- Backend: uvicorn local (`uvicorn app.main:app`)
- Frontend: Vite local (`npm run dev`)

**Razón:**
- ✅ Desarrollo más rápido
- ✅ Debugging más fácil
- ✅ Sin overhead de orchestración
- ✅ Escalable si necesario después

---

## Decisiones Futuras

Las siguientes decisiones se tomarán cuando sea necesario:

- [ ] ADR-013: Validación de entrada (Pydantic vs custom)
- [ ] ADR-014: Manejo de errores (Exception hierarchy)
- [ ] ADR-015: Logging (nivel, formato, rotación)
- [ ] ADR-016: Caching (Redis vs en memoria)
- [ ] ADR-017: Asincronía (async/await scope)

---

**Última actualización:** Foundation - Decisiones iniciales

