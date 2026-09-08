# AGENTS.md - Contrato Técnico del Proyecto

## Objetivo del Proyecto

Implementar un backend EVM (Earned Value Management) con API REST profesional, integrado con una interfaz React moderna.

**Stack definido:**
- Backend: Python 3.12+ / FastAPI / SQLAlchemy / Alembic / PostgreSQL
- Frontend: React 18 / TypeScript / Vite
- Base de datos: PostgreSQL
- Testing: pytest / pytest-cov
- Linting: Ruff

## Arquitectura

```
React (Frontend)
        ↓
    FastAPI Routers (HTTP)
        ↓
    Services (Lógica de Negocio)
        ↓
    Repositories (Acceso a Datos)
        ↓
    SQLAlchemy Models
        ↓
    PostgreSQL
```

### Separación de Responsabilidades

- **Routers**: Manejan solicitudes HTTP, validan entrada básica
- **Services**: Contienen toda la lógica de negocio, incluyendo cálculos EVM
- **Repositories**: Abstracción de acceso a datos, operaciones CRUD
- **Models**: Representan la persistencia (tablas de BD)
- **Schemas**: Contratos de entrada/salida (Pydantic)

### Reglas de Arquitectura

1. Los routers **nunca** contienen lógica de negocio.
2. La lógica EVM está **aislada** en una capa de servicios específica.
3. El **backend es la fuente de verdad** para todos los cálculos.
4. El frontend **nunca** calcula indicadores EVM (CPI, SPI, etc.).
5. Los indicadores de proyecto se calculan a partir de **totales consolidados**, no promedios.

## Reglas de Calidad

1. **80% mínimo de coverage** en la capa de negocio
2. **Sin deuda técnica**: no agregar features innecesarias
3. **Código limpio**: nombres claros, sin comentarios obvios
4. **Type hints** obligatorios en todas las funciones
5. **Validación en límites**: solo en entrada de usuario/APIs

## Reglas de Testing

### Unit Tests
- Lógica EVM: casos normales + edge cases
- Services: toda la lógica de negocio
- Repositories: operaciones de BD (cuando sea crítico)

### Integration Tests
- Cada endpoint debe validar:
  - Status code correcto
  - Estructura de respuesta
  - Contrato JSON esperado

### Cobertura
```bash
pytest --cov=app --cov-report=html
```

Mínimo 80% en `app/services` y lógica EVM.

## Reglas de Gitflow

```
main (producción)
  ↑
  release/* (preparación para entrega)
  ↑
  develop (integración)
  ↑
  feature/* (desarrollo de features)
```

### Flujo de una feature

1. Crear rama `feature/mi-feature` desde `develop`
2. Trabajar localmente
3. Crear Pull Request a `develop`
4. Ejecutar tests, lint, cobertura
5. Merge en `develop`
6. Después: `develop` → `release/*` → `main`

### Restricción: No commits automáticos
- Los agentes de IA **no crean commits automáticamente**
- Los agentes de IA **no hacen push automático**
- El usuario confirma manualmente

## Reglas para Uso de IA

1. **Leer AGENTS.md y CLAUDE.md** antes de modificar código
2. **Inspeccionar código existente** antes de hacer cambios
3. **No inventar requisitos** ni agregar features innecesarias
4. **Respetar la arquitectura**: Router → Service → Repository
5. **Crear tests con cada funcionalidad**
6. **Ejecutar tests después de cambios**
7. **Ejecutar Ruff antes de hacer commit**
8. **No afirmar funcionamiento** sin ejecución real
9. **Mantener cambios pequeños y revisables**
10. **Priorizar simplicidad** sobre abstracción prematura
11. **Registrar en AI_PROCESS.md** prompts exactos y decisiones

## Restricciones de Alcance

**NO agregar inicialmente:**
- Redis, Celery, Kafka, RabbitMQ
- Kubernetes, Docker para cada servicio
- JWT, OAuth (solo si requisito explícito)
- WebSockets
- Microservicios
- CI/CD pipeline
- Cloud infrastructure

## Manejo de Errores

1. **Validación en límites**: routers validan entrada
2. **Excepciones específicas**: crear excepciones de dominio
3. **Logging**: usar logging estándar (no print)
4. **Respuestas JSON**: siempre estructura uniforme

### Respuestas de Error

```json
{
  "error": "error_code",
  "message": "Descripción legible",
  "details": {}
}
```

## Regla de No Complejidad Innecesaria

- 3 líneas duplicadas es mejor que 1 abstracción innecesaria
- No diseñar para futuros que no existen
- No colocar feature flags para casos que no suceden
- Eliminar código muerto completamente
- No agregar "just in case" features

## Estado del Proyecto

- [x] Foundation inicial
- [ ] EVM Domain
- [ ] Backend Completo
- [ ] Integration Testing
- [ ] Frontend
- [ ] Quality & Refactoring
- [ ] Documentation
- [ ] Gitflow Setup
- [ ] Final Validation

---

**Última actualización:** Foundation inicial - Preparado para Fase 1
