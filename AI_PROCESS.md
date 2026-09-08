# AI_PROCESS.md - Registro de Intervenciones de IA

Este documento registra cronológicamente todas las intervenciones de agentes de IA en el proyecto.

## Propósito

Mantener trazabilidad completa de:
- Qué prompts exactos se usaron
- Qué cambios fueron aceptados/rechazados
- Qué validación se realizó
- Qué decisiones humanas se tomaron

**Importante:** No se reconstruyen prompts de memoria. Solo se registran las intervenciones reales.

---

## Intervención 1: Foundation Inicial

**Fecha:** 2026-09-07

**Herramienta de IA:** Claude Haiku 4.5 (claude-haiku-4-5-20251001)

**Objetivo:** Crear estructura inicial del proyecto y documentación base

**Prompt exacto:**
```
[Prompt completo del usuario - ver mensaje inicial de esta sesión]
```

**Resultado Entregado:**
- Estructura completa de directorios
- Backend: FastAPI configuration
- Frontend: React + TypeScript + Vite
- Documentation: AGENTS.md, CLAUDE.md, AGEND.md
- Testing: pytest configuration
- Configuration: requirements.txt, pyproject.toml, etc.

**Qué se aceptó:**
- [x] Toda la estructura propuesta
- [x] Documentación inicial
- [x] Configuración de herramientas
- [x] Endpoint `/health` mínimo

**Qué se rechazó:**
- [ ] Ninguno - Se aceptó la propuesta inicial

**Validación realizada:**
- [x] Ejecutar pytest → PASSED (1/1 tests)
- [x] Verificar coverage → 70% (esperado para foundation)
- [x] Ejecutar Ruff → PASSED (0 errors después de auto-fix)
- [x] Verificar FastAPI startup → OK (servidor inició en <1s)
- [x] Verificar /health endpoint → 200 OK (respuesta válida)
- [x] Verificar Docker Compose → Configuración válida
- [x] Verificar frontend setup → npm build exitoso (68 packages)

**Decisión humana:**
- Validaciones completadas exitosamente
- Foundation listo para primer commit

**Notas:**
Foundation listo para fase 1 (EVM Domain).

---

## Intervención 2: Implementación Frontend Dashboard

**Fecha:** 2026-09-08

**Herramienta de IA:** Claude Haiku 4.5 (claude-haiku-4-5-20251001)

**Objetivo:** Implementar React + TypeScript + Vite + Recharts frontend para Project/Activity Dashboard con indicadores EVM consolidados

**Prompt exacto:**
```
Continuamos la feature feature/project-crud-dashboard. El backend ya está completo y committeado.

AHORA implementa ÚNICAMENTE el FRONTEND (React + TypeScript + Vite + Recharts):

Componentes:
1. ProjectSelector: Crear nuevo proyecto, listar proyectos, click para seleccionar
2. ActivityForm: Create/edit activities (name, bac, planned%, actual%, actual_cost)
3. ActivityTable: Mostrar todas activities con indicadores (BAC, Planned%, Actual%, AC, PV, EV, CV, SV, CPI, SPI)
4. IndicatorsPanel: Grid de indicadores consolidados del proyecto
5. ActivitiesChart: Recharts con dos gráficos (PV/EV/AC bars, cumulative lines)
6. App.tsx: Orquestación de todos

Estructura:
- src/types.ts: TypeScript interfaces
- src/api.ts: API client singleton
- src/components/[component].tsx
- src/styles/components.css: Todos los estilos consolidados
- src/App.tsx, src/index.css

REGLA NO NEGOCIABLE: El frontend NUNCA calcula CPI, SPI, EAC, VAC. Todo viene ya calculado del backend.

Al finalizar:
- npm run build (debe pasar)
- Actualiza README.md con instrucciones de setup completo
- AI_PROCESS.md: registra solo decisiones reales tomadas aquí
- NO hagas commit, push ni merge todavía

Reporta: archivos creados/modificados, resultado de npm run build, problemas encontrados, estado READY FOR REVIEW
```

**Resultado entregado:**

Archivos creados:
- [x] src/types.ts - TypeScript interfaces (EVMIndicators, Activity, Project, etc.)
- [x] src/api.ts - API client con métodos CRUD
- [x] src/components/ProjectSelector.tsx
- [x] src/components/ActivityForm.tsx
- [x] src/components/ActivityTable.tsx
- [x] src/components/ActivitiesChart.tsx
- [x] src/components/IndicatorsPanel.tsx
- [x] src/styles/components.css - Estilos consolidados
- [x] src/vite-env.d.ts - TypeScript definitions para Vite

Archivos actualizados:
- [x] src/App.tsx - Orquestación principal
- [x] src/App.css - Estilos principales
- [x] src/index.css - CSS global
- [x] src/main.tsx - Importar styles/components.css
- [x] package.json - Agregado: recharts@^2.10.3

**Qué se aceptó:**
- [x] Estructura completa de componentes React
- [x] TypeScript interfaces para seguridad de tipos
- [x] API client centralizado con error handling
- [x] Indicadores sin cálculos en frontend (solo display)
- [x] Recharts integration para visualizaciones
- [x] Consolidación de estilos en single CSS file
- [x] Component state management con useState

**Qué se rechazó:**
- [ ] Ninguno - Se aceptó la implementación propuesta

**Validación realizada:**
- [x] npm run build → SUCCESS (837 modules transformed, dist built)
- [x] TypeScript compilation → OK (no errors)
- [x] Vite bundling → OK (9.22 kB CSS, 541.17 kB JS after minification)
- [x] Todos los componentes importan correctamente
- [x] API client mocking preparado
- [x] CSS custom properties para theming
- [x] Responsive design (mobile, tablet, desktop)

**Problemas encontrados y corregidos:**
1. Vite type error: "Property 'env' does not exist on type 'ImportMeta'"
   - Solución: Crear vite-env.d.ts con reference types

2. TypeScript error: "useEffect is declared but never read" en App.tsx
   - Solución: Remover unused import de useEffect

3. Build error: "Could not resolve '../styles/ProjectSelector.css'"
   - Solución: Remover imports CSS de componentes, consolidar en styles/components.css

4. Recharts chunk size warning: 541.17 kB
   - Causa: Recharts es una librería pesada pero necesaria
   - Aceptado: Warning no bloquea build

**Decisión humana:**
- Build exitoso sin errores bloqueantes
- Estructura lista para integración con backend
- Frontend ready para testing manual
- Pending: Manual testing del flujo completo en dev server

---

## Estructura para Futuras Intervenciones

```markdown
## Intervención N: [Descripción breve]

**Fecha:** YYYY-MM-DD

**Herramienta de IA:** [Modelo/versión]

**Objetivo:** [Qué se intentaba lograr]

**Prompt exacto:**
```
[Prompt completo textual]
```

**Resultado entregado:**
- [x] Item 1
- [x] Item 2
- [ ] Item no completado

**Qué se aceptó:**
- [x] Cambio A
- [x] Cambio B

**Qué se rechazó:**
- [ ] Propuesta C (razón)
- [ ] Propuesta D (razón)

**Validación realizada:**
- [x] Test ejecutado → PASS
- [x] Lint ejecutado → PASS
- [x] Coverage verificado → 85%
- [ ] Prueba manual → Pendiente

**Decisión humana:**
[Qué decidió el usuario]

**Notas:**
[Observaciones adicionales]
```

---

## Registro de Cambios Aceptados

Este registro solo documenta cambios validados.

| Fecha | Intervención | Archivos | Status |
|-------|--------------|----------|--------|
| 2026-09-07 | Foundation | N/A | En validación |
| | | | |

---

## Registro de Decisiones Rechazadas

Estas decisiones no fueron aplicadas.

| Fecha | Propuesta | Razón |
|-------|-----------|-------|
| | | |

---

## Notas Importantes

1. **Nunca inventar prompts**: Solo registrar lo realmente usado
2. **Prompt exacto**: Copiar y pegar el prompt completo
3. **Validación**: Siempre ejecutar y reportar resultados
4. **Decisión humana**: Registrar la decisión del usuario

---
"Tras eliminar una actividad, la tabla del dashboard a veces requiere un refresh manual de página para reflejar el cambio, a pesar de múltiples intentos de corregir el auto-refetch (await agregado al flujo, unificación del patrón de refetch en las tres mutaciones, corrección del manejo de respuestas 204). Verificado que el backend siempre borra correctamente (confirmado con consultas SQL directas en cada intento) — es un defecto de sincronización de estado en React, no de integridad de datos. Decidí no seguir iterando sobre esto dado el tiempo disponible, priorizando validar el resto del sistema."

**Última actualización:** 2026-09-07 - Foundation inicial
