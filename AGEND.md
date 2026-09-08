# AGEND.md - Plan de Desarrollo por Fases

## Visión General

Este documento describe el roadmap de desarrollo del proyecto en fases secuenciales.

---

## FASE 0: Foundation ✅

**Estado:** Completada

**Objetivos:**
- [x] Repositorio inicializado
- [x] Estructura de directorios creada
- [x] Configuración de Backend (FastAPI, SQLAlchemy, Alembic)
- [x] Configuración de Frontend (React, TypeScript, Vite)
- [x] Configuración de Testing (pytest, pytest-cov)
- [x] Configuración de Linting (Ruff)
- [x] Docker Compose para PostgreSQL
- [x] Documentación inicial (AGENTS.md, CLAUDE.md, AGEND.md)
- [x] Endpoint mínimo `/health`
- [x] Test mínimo para `/health`
- [x] Git inicializado (main, develop)
- [x] Gitflow documentado y listo

**Artefactos:**
- `.gitignore`
- `.env.example`
- `docker-compose.yml`
- `requirements.txt`
- `pyproject.toml`
- `pytest.ini`
- FastAPI application structure
- React + TypeScript + Vite setup

**Pendiente:** Iniciar Fase 1

---

## FASE 1: EVM Domain

**Estado:** ⏳ Pendiente

**Objetivo:**
Definir y documentar el dominio de EVM. Crear estructuras de datos y fórmulas.

**Tareas:**
- [ ] Definir modelo conceptual de EVM
- [ ] Documentar fórmulas:
  - [ ] PV = planned_progress × BAC
  - [ ] EV = actual_progress × BAC
  - [ ] CV = EV − AC
  - [ ] SV = EV − PV
  - [ ] CPI = EV / AC
  - [ ] SPI = EV / PV
  - [ ] EAC = BAC / CPI
  - [ ] VAC = BAC − EAC
- [ ] Documentar interpretaciones (CPI > 1, etc.)
- [ ] Documentar edge cases y decisiones
- [ ] Crear `app/models/evm.py` (modelos iniciales)
- [ ] Crear `app/services/evm_service.py` (cálculos)
- [ ] Crear tests unitarios para cálculos EVM
- [ ] Validar coverage ≥ 80%

**Artefactos:**
- `docs/evm.md` (actualizado)
- `app/models/evm.py`
- `app/services/evm_service.py`
- `tests/test_evm_service.py`

**Criterio de Aceptación:**
- Todas las fórmulas documentadas
- Edge cases identificados y documentados
- Tests unitarios para casos normales + edge cases
- Coverage ≥ 80% en lógica EVM
- Sin código ejecutable aún

---

## FASE 2: Backend - Modelos y CRUD

**Estado:** ⏳ Pendiente

**Objetivo:**
Crear la persistencia y operaciones CRUD básicas.

**Tareas:**
- [ ] Crear modelos SQLAlchemy:
  - [ ] `Project`
  - [ ] `Activity`
  - [ ] Relaciones
- [ ] Crear Alembic migrations
- [ ] Crear Pydantic schemas para entrada/salida
- [ ] Crear repositories:
  - [ ] `ProjectRepository`
  - [ ] `ActivityRepository`
- [ ] Crear services:
  - [ ] `ProjectService`
  - [ ] `ActivityService`
- [ ] Crear routers:
  - [ ] `/projects` (POST, GET, GET by ID, PUT, DELETE)
  - [ ] `/activities` (POST, GET, GET by ID, PUT, DELETE)
- [ ] Tests de integración para endpoints

**Artefactos:**
- `app/models/project.py`
- `app/models/activity.py`
- `app/schemas/project.py`
- `app/schemas/activity.py`
- `app/repositories/project_repository.py`
- `app/repositories/activity_repository.py`
- `app/services/project_service.py`
- `app/services/activity_service.py`
- `app/routers/projects.py`
- `app/routers/activities.py`
- Alembic migrations
- Tests de integración

**Criterio de Aceptación:**
- CRUD completo funcionando
- Tests de integración para todos los endpoints
- Coverage ≥ 80%
- Lint pass

---

## FASE 3: Backend - EVM Integration

**Estado:** ⏳ Pendiente

**Objetivo:**
Integrar cálculos EVM con datos persistidos.

**Tareas:**
- [ ] Extender `Activity` con campos EVM:
  - [ ] BAC
  - [ ] Planned Value
  - [ ] Actual Cost
  - [ ] Actual Progress
- [ ] Extender `Project` con consolidación de EVM
- [ ] Crear endpoints para obtener indicadores:
  - [ ] `/projects/{id}/indicators`
  - [ ] `/activities/{id}/indicators`
- [ ] Validaciones de dominio:
  - [ ] AC ≠ negativo
  - [ ] Progress dentro de [0, 1]
  - [ ] BAC > 0
- [ ] Tests de cálculos con datos persistidos

**Artefactos:**
- Modelos actualizados
- `app/services/indicator_service.py`
- `app/routers/indicators.py` (si aplica)
- Migrations Alembic
- Tests

**Criterio de Aceptación:**
- Cálculos EVM funcionando con datos de BD
- Consolidación de proyecto funcionando
- Validaciones de dominio en su lugar
- Coverage ≥ 80%

---

## FASE 4: Integration Testing

**Estado:** ⏳ Pendiente

**Objetivo:**
Validar contratos de API y flujos completos.

**Tareas:**
- [ ] Tests de flujos end-to-end:
  - [ ] Crear proyecto
  - [ ] Agregar actividades
  - [ ] Actualizar progreso
  - [ ] Obtener indicadores
- [ ] Validar estructura de respuestas
- [ ] Validar códigos de estado HTTP
- [ ] Validar errores y validaciones
- [ ] Tests de casos límite

**Artefactos:**
- `tests/test_integration_*.py`
- Documentación de contratos API

**Criterio de Aceptación:**
- Coverage ≥ 80%
- Todos los endpoints tienen tests de integración
- Flujos críticos cubiertos

---

## FASE 5: Frontend - Dashboard

**Estado:** ⏳ Pendiente

**Objetivo:**
Crear interfaz para visualizar proyectos e indicadores.

**Tareas:**
- [ ] Componente `ProjectList`
- [ ] Componente `ProjectDetail`
- [ ] Componente `IndicatorDisplay` (KPI cards)
- [ ] Tabla de actividades
- [ ] Conexión a API backend (`/projects`)
- [ ] State management (Context API o similar)
- [ ] Error handling
- [ ] Loading states

**Artefactos:**
- `frontend/src/components/ProjectList.tsx`
- `frontend/src/components/ProjectDetail.tsx`
- `frontend/src/components/IndicatorDisplay.tsx`
- `frontend/src/pages/DashboardPage.tsx`
- `frontend/src/api/` (cliente HTTP)

**Criterio de Aceptación:**
- Proyecto carga en navegador
- Lista de proyectos visible
- Indicadores se muestran
- Manejo de errores funciona

---

## FASE 6: Frontend - Formularios y CRUD

**Estado:** ⏳ Pendiente

**Objetivo:**
Crear formularios para crear/editar proyectos y actividades.

**Tareas:**
- [ ] Formulario de creación de proyecto
- [ ] Formulario de creación de actividad
- [ ] Validaciones frontend
- [ ] Confirmación de eliminación
- [ ] Feedback de usuario (toast, spinner)
- [ ] Manejo de errores de API

**Artefactos:**
- Componentes de formularios
- Validaciones
- Manejo de estados

**Criterio de Aceptación:**
- CRUD completo desde UI
- Validaciones funcionales
- UX aceptable

---

## FASE 7: Frontend - Visualizaciones

**Estado:** ⏳ Pendiente

**Objetivo:**
Agregar gráficos y visualizaciones EVM.

**Tareas:**
- [ ] Gráfico de líneas: PV vs EV vs AC
- [ ] Gráfico de barras: CPI por actividad
- [ ] Gráfico de indicadores: SPI, CPI de proyecto
- [ ] Tabla de actividades con indicadores
- [ ] Exportación de datos

**Artefactos:**
- Componentes de gráficos (Chart.js, Recharts, etc.)
- `frontend/src/components/Charts/`

**Criterio de Aceptación:**
- Gráficos se renderizan correctamente
- Datos se actualizan en tiempo real
- Responsive design

---

## FASE 8: Quality & Refactoring

**Estado:** ⏳ Pendiente

**Objetivo:**
Asegurar calidad, cobertura y mantenibilidad.

**Tareas:**
- [ ] Revisar coverage global (target ≥ 80%)
- [ ] Refactoring de código duplicado
- [ ] Optimización de queries
- [ ] Revisar edge cases
- [ ] Performance testing
- [ ] Security review

**Criterio de Aceptación:**
- Coverage ≥ 80%
- Lint pass
- Performance acceptable

---

## FASE 9: Documentation

**Estado:** ⏳ Pendiente

**Objetivo:**
Documentar completamente el proyecto.

**Tareas:**
- [ ] Actualizar `README.md`
- [ ] Completar `docs/architecture.md`
- [ ] Completar `docs/evm.md`
- [ ] Actualizar `docs/testing.md`
- [ ] Actualizar `docs/decisions.md`
- [ ] Crear `docs/api.md` (Endpoints)
- [ ] Crear `docs/deployment.md` (Producción)
- [ ] Actualizar `AI_PROCESS.md`

**Criterio de Aceptación:**
- Toda la documentación es clara y actualizada
- Nuevos desarrolladores pueden comenzar

---

## FASE 10: Gitflow & Release

**Estado:** ⏳ Pendiente

**Objetivo:**
Configurar Gitflow y preparar primera entrega.

**Tareas:**
- [ ] Configurar branches:
  - [ ] `main` (producción)
  - [ ] `develop` (integración)
  - [ ] `release/v0.1.0` (preparación)
- [ ] Merge de `develop` → `release/v0.1.0`
- [ ] Merge de `release/v0.1.0` → `main`
- [ ] Tag `v0.1.0`

**Criterio de Aceptación:**
- Gitflow configurado
- Primera versión etiquetada
- Listo para entrega

---

## FASE 11: Final Validation

**Estado:** ⏳ Pendiente

**Objetivo:**
Validación final antes de entrega.

**Tareas:**
- [ ] Ejecutar todos los tests
- [ ] Verificar coverage ≥ 80%
- [ ] Ejecutar lint completo
- [ ] Verificar que Docker Compose funciona
- [ ] Verificar que frontend se inicia
- [ ] Prueba manual completa
- [ ] Revisar documentación
- [ ] Preparar video/presentación
- [ ] Validación final del requisito

**Criterio de Aceptación:**
- Todo funciona
- Requisitos cumplidos
- Documentación completa
- Listo para entrega

---

## Definition of Done

Una tarea se considera completa cuando:

1. **Código escrito** y funcional
2. **Tests escritos** y pasen
3. **Coverage ≥ 80%** en la lógica de negocio
4. **Lint pass** (Ruff clean)
5. **Documentación actualizada** (docstrings, markdown)
6. **Revisado manualmente** sin issues
7. **Registrado en AI_PROCESS.md** (si usó IA)
8. **Cambios pequeños y revisables** (no monolíticos)

---

## Notas

- Cada fase depende de la anterior
- No saltar fases
- Validar incrementalmente
- Mantener la arquitectura limpia

---

**Última actualización:** Foundation inicial - Fase 0 completada
