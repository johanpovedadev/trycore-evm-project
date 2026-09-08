# AI_PROCESS.md - Registro de Intervenciones de IA

Este documento registra cronológicamente el uso de IA durante el desarrollo
del reto técnico Trycore EVM. No se han reconstruido ni inventado prompts:
todos los que aparecen aquí fueron efectivamente enviados a Claude Code
durante la sesión de desarrollo.

---

## 1. Herramientas de IA utilizadas

- **Claude (claude.ai)** — usado para planificación, arquitectura,
  diseño de prompts para Claude Code, revisión de resultados, y debugging
  colaborativo cuando aparecían errores que requerían diagnóstico (CORS,
  UnicodeDecodeError, conflictos de puertos, bugs de estado en React).
- **Claude Code** — usado como agente de implementación: ejecutó los
  prompts detallados abajo, escribió código, corrió tests, y reportó
  resultados que luego fueron verificados manualmente.
- **Gemini y ChatGPT** — usados de forma exploratoria y conversacional
  para entender los conceptos de EVM antes de empezar a implementar
  (ver sección 2).

Elegí este flujo (Claude para pensar/planificar, Claude Code para
ejecutar) para mantener una separación clara entre las decisiones de
arquitectura y dominio (mías) y la implementación mecánica (asistida
por IA), tal como pide AGENTS.md del propio proyecto.

---

## 2. Cómo aprendí EVM

El aprendizaje de los conceptos de Earned Value Management (PV, EV, AC,
CV, SV, CPI, SPI, EAC, VAC y su interpretación) lo hice consultando
Gemini y ChatGPT de forma exploratoria, sin un prompt único o
estructurado — fueron preguntas sueltas y conversacionales mientras
leía el documento del reto, buscando entender qué significaba cada
sigla y por qué la fórmula de consolidación debía sumar totales antes
de calcular razones, en vez de promediar los índices individuales.

No hubo un prompt de aprendizaje dirigido a Claude Code ni a Claude
(claude.ai) — para cuando empecé a escribir los primeros prompts de
implementación (sección 3.1 en adelante), ya tenía el concepto
suficientemente claro como para especificar las fórmulas y los edge
cases exactos que quería que el sistema implementara.

La validación real de que entendí las fórmulas correctamente no
ocurrió durante esa fase exploratoria de estudio, sino **durante el
desarrollo**: verifiqué a mano, con calculadora, cada resultado que el
sistema producía contra el cálculo manual de las fórmulas oficiales,
en múltiples ocasiones documentadas en la sección 4 — incluyendo un
caso donde esa verificación manual reveló un error real de precisión
numérica en la implementación (sección 4.1).

---

## 3. Registro cronológico de prompts (textuales)

### 3.1 — Foundation: primer commit del proyecto

```text
Estamos en el proyecto trycore-evm-project.

El Gitflow Foundation ya fue configurado y auditado.

ESTADO ACTUAL:
- Git inicializado
- main creada
- develop creada y activa
- No existen commits todavía
- .gitignore verificado
- .env ignorado
- .env.example seguro
- Foundation validada
- pytest pasa
- Ruff pasa
- frontend build pasa
- docker compose config pasa
- No existe todavía implementación de EVM, CRUD ni dashboard

OBJETIVO DE ESTA TAREA:
Crear el PRIMER COMMIT de la foundation.

ANTES DE HACER EL COMMIT:
1. Ejecuta:
   git status
   git branch
   git diff --stat
2. Revisa todos los archivos staged/untracked.
3. Verifica que NO entren:
   .env
   .venv
   node_modules
   __pycache__
   .pytest_cache
   .coverage
   dist
   htmlcov
   secretos o credenciales reales.
4. Verifica que AI_PROCESS.md no contenga prompts inventados.
5. Verifica que INFORME_FOUNDATION.md sea documentación válida y no contenga información sensible.
6. Ejecuta nuevamente:
   pytest
   pytest --cov=app --cov-report=term-missing
   ruff check .
   docker compose config
   frontend build
7. Si alguna validación falla, NO hagas commit. Corrige únicamente el problema necesario y vuelve a validar.

SI TODO ESTÁ CORRECTO:
- git add .
- git status
- crea el commit en develop con exactamente:

chore: initialize Trycore EVM project foundation

NO hagas push.
NO crees ramas feature.
NO modifiques funcionalidades de aplicación.
NO implementes EVM todavía.

AL FINAL REPORTA:
- commit hash
- branch actual
- archivos incluidos
- validaciones ejecutadas
- resultado de cada validación
- coverage
- cualquier warning
- siguiente paso recomendado.

No inventes resultados.
```

**Resultado:** commit `8964ffe` — "chore: initialize Trycore EVM project
foundation", 45 archivos, pytest 1/1 pass, coverage 70%, ruff pass.

---

### 3.2 — Feature: EVM domain + API

```text
Implementa ahora la primera feature real del proyecto:

BRANCH:
feature/evm-domain

OBJETIVO:
Implementar el dominio EVM y su API REST asociada en una única feature.

IMPORTANTE:
Esta feature NO debe implementar todavía:

* Project CRUD
* Activity CRUD
* persistencia de proyectos
* persistencia de actividades
* dashboard React
* autenticación
* funcionalidades no requeridas por el challenge.

==================================================
1. CONTRATO DE DATOS DEL DOMINIO
==================================================

El dominio EVM debe ser independiente de SQLAlchemy y de la persistencia.

NO crees una entidad Project ni una entidad Activity dentro del dominio EVM.

El cálculo debe recibir un contrato de entrada simple, por ejemplo:

EVMInput(
  bac,
  planned_percentage,
  actual_percentage,
  actual_cost
)

Puede implementarse como Pydantic model, dataclass o value object simple según la arquitectura existente. Usa Pydantic v2 (ConfigDict, no class-based Config).

El cálculo debe depender únicamente de los valores necesarios para EVM.

NO debe depender de:

* SQLAlchemy
* sesiones de DB
* repositories
* FastAPI Request
* HTTP
* React.

La función principal debe ser fácilmente testeable de forma aislada.

==================================================
2. CÁLCULOS
==================================================

Implementa:

PV = planned_percentage × BAC
EV = actual_percentage × BAC
CV = EV − AC
SV = EV − PV
CPI = EV / AC
SPI = EV / PV
EAC = BAC / CPI
VAC = BAC − EAC

Utiliza Decimal para cálculos monetarios cuando corresponda.

No utilizar floats para dinero si puede evitarse.

==================================================
3. EDGE CASES OBLIGATORIOS
==================================================

AC = 0:
CPI = null.

PV = 0:
SPI = null.

EV = 0 y AC > 0:
CPI = 0.

EV = 0 y PV > 0:
SPI = 0.

CPI = 0:
EAC = null.
VAC = null.

Sin actividades:
los indicadores consolidados deben ser null y el estado debe representar NO_DATA.

Validar:

BAC > 0
0 <= planned_percentage <= 100
0 <= actual_percentage <= 100
AC >= 0

No ocultar errores mediante valores artificiales como Infinity, NaN o división por uno.

==================================================
4. CONSOLIDACIÓN
==================================================

Para múltiples actividades:

BAC_total = SUM(BAC)
PV_total = SUM(PV)
EV_total = SUM(EV)
AC_total = SUM(AC)

Después calcular:

CV = EV_total - AC_total
SV = EV_total - PV_total
CPI = EV_total / AC_total
SPI = EV_total / PV_total
EAC = BAC_total / CPI
VAC = BAC_total - EAC

PROHIBIDO:

NO calcular el CPI consolidado como promedio de CPI individuales.

NO calcular el SPI consolidado como promedio de SPI individuales.

Los indicadores consolidados siempre deben calcularse a partir de los totales.

==================================================
5. INTERPRETACIÓN
==================================================

CPI:
> 1 = favorable / eficiencia de costos
= 1 = en línea
< 1 = desfavorable / sobrecosto

SPI:
> 1 = adelantado
= 1 = según plan
< 1 = retrasado

VAC:
> 0 = favorable
= 0 = en presupuesto
< 0 = sobrecosto proyectado

Implementa estados de forma clara y mantenible (enum, no strings mágicos).

Evita magic strings y magic numbers.

==================================================
6. TESTS UNITARIOS
==================================================

Antes de terminar la feature, crea tests exhaustivos para el servicio EVM.

Como mínimo:

1. cálculo normal
2. AC = 0
3. PV = 0
4. EV = 0 con AC > 0
5. EV = 0 con PV > 0
6. CPI = 0
7. proyecto sin actividades
8. múltiples actividades
9. consolidación correcta
10. demostrar que NO se promedian CPI/SPI
11. BAC inválido
12. AC negativo
13. planned_percentage inválido
14. actual_percentage inválido
15. VAC negativo válido

Utiliza valores numéricos conocidos y aserciones precisas.

==================================================
7. API
==================================================

Expón solamente los endpoints necesarios para consultar/calcular EVM.

La API debe recibir datos mediante schemas Pydantic y delegar la lógica al servicio.

NO coloques cálculos EVM dentro del router.

El router solamente debe encargarse de:

HTTP
validación de entrada
llamada al servicio
serialización
status codes
errores HTTP.

La lógica debe permanecer en services.

Documenta automáticamente los endpoints mediante OpenAPI.

==================================================
8. INTEGRATION TESTS
==================================================

Cada endpoint implementado debe tener al menos un integration test.

Validar:

* respuesta exitosa
* contrato de respuesta
* entrada inválida
* casos de división por cero cuando corresponda.

==================================================
9. CALIDAD
==================================================

Ejecuta:

pytest
pytest --cov
ruff check .

El business layer debe alcanzar mínimo 80% de coverage.

No aumentes coverage artificialmente.

Corrige:

* imports sin usar
* funciones excesivamente grandes
* duplicación
* magic numbers
* magic strings
* código muerto
* comentarios innecesarios
* excepciones genéricas
* lógica de negocio en routers.

==================================================
10. DOCUMENTACIÓN
==================================================

Actualiza únicamente documentación que realmente corresponda.

AI_PROCESS.md:
NO inventes prompts.
Si necesitas registrar una decisión, describe solamente la decisión realmente tomada durante esta implementación.

docs/evm.md debe permanecer consistente con la implementación.

==================================================
11. VALIDACIÓN FINAL DE LA FEATURE
==================================================

Antes de finalizar ejecuta:

pytest
pytest --cov=app --cov-report=term-missing
ruff check .
docker compose config

Si frontend no fue modificado, no gastes tiempo reconstruyéndolo innecesariamente.

==================================================
12. GIT
==================================================

NO hagas commit todavía.
NO hagas push.
NO hagas merge.
NO crees otra feature.

Al finalizar reporta:

* archivos creados/modificados
* arquitectura utilizada
* contrato EVM
* endpoints
* cantidad de tests
* tests pass/fail
* coverage
* Ruff
* edge cases cubiertos
* problemas encontrados
* problemas pendientes
* estado READY FOR REVIEW o NOT READY FOR REVIEW.

Si existe un problema funcional conocido, NO declares READY FOR REVIEW.
```

**Resultado:** 29 tests (18 unit + 11 integration), 90% coverage
(EVM service 100%), Ruff pass. Ver sección 4.1 para el bug de precisión
encontrado y corregido en esta feature.

---

### 3.3 — Fix de precisión: EAC/VAC calculados con CPI/SPI redondeado

```text
Encontré un problema de precisión en EVMService.

Verificación manual:
bac=1000, planned=50, actual=45, actual_cost=400

CPI real (sin redondear) = 450/400 = 1.125
EAC correcto = BAC / CPI_real = 1000 / 1.125 = 888.888... → 888.89

El sistema actual está devolviendo EAC = 884.96, lo que indica que
EAC se está calculando usando CPI ya redondeado a 2 decimales
(1000 / 1.13) en vez del valor de precisión completa.

CORRECCIÓN REQUERIDA:

Todos los cálculos intermedios (CPI, SPI, EAC, VAC) deben realizarse
con la precisión completa de Decimal, SIN redondear valores intermedios.

El redondeo a 2 decimales debe aplicarse ÚNICAMENTE en el punto de
serialización de salida (en el schema de respuesta / al construir
EVMIndicators), nunca dentro de fórmulas que dependan de otro resultado
ya calculado.

Es decir:
- CPI se calcula con precisión completa.
- EAC se calcula usando el CPI de precisión completa (no el CPI mostrado).
- VAC se calcula usando el EAC de precisión completa.
- El redondeo a 2 decimales ocurre solo al momento de mostrar/serializar
  el resultado final.

TAREAS:
1. Revisa EVMService y corrige el orden de redondeo/cálculo descrito arriba.
2. Recalcula manualmente el ejemplo (bac=1000, planned=50, actual=45, ac=400)
   y confirma que EAC = 888.89 y VAC = 111.11 (aprox, según redondeo final).
3. Revisa TODOS los tests unitarios y de integración que dependan de EAC/VAC
   y corrige los valores esperados con el cálculo correcto, mostrando el
   cálculo manual de cada uno en tu reporte (no solo "ajusté el valor").
4. Vuelve a ejecutar:
   pytest
   pytest --cov=app --cov-report=term-missing
   ruff check .
5. Reporta el diff exacto de EVMService, los valores antes/después del
   ejemplo de referencia, y el resultado de tests/coverage/lint.

NO toques la estructura de EVMInput, EVMIndicators, el router, ni agregues
funcionalidad nueva. Este es un fix quirúrgico de precisión numérica.

NO hagas commit todavía.
```

**Resultado:** corrección aplicada — cálculos intermedios sin redondeo,
redondeo solo en la serialización de salida. EAC recalculado: `1000/1.125
= 888.89` (antes daba `884.96`, incorrecto). 29/29 tests pass tras
actualizar valores esperados. Ver sección 4.1 para el análisis completo
de este bug.

---

### 3.4 — Feature: Project/Activity CRUD + Dashboard React

```text
Implementa ahora la siguiente feature del proyecto:

BRANCH:
feature/project-crud-dashboard

CONTEXTO:
Ya existe el dominio EVM implementado y probado en:
- backend/app/services/evm_service.py
- backend/app/schemas/evm.py

Esta feature debe REUTILIZAR ese servicio, NUNCA reimplementar
lógica EVM en otro lugar.

OBJETIVO:
Implementar persistencia de Project/Activity (backend) y el
dashboard funcional (frontend) en una sola feature coherente.

==================================================
PARTE 1 — BACKEND: MODELOS Y PERSISTENCIA
==================================================

Crea:

backend/app/models/project.py
backend/app/models/activity.py

Project:
- id
- name
- created_at
- activities (relación uno a muchos)

Activity:
- id
- project_id (FK)
- name
- bac (Budget at Completion)
- planned_percentage
- actual_percentage
- actual_cost
- created_at
- updated_at

IMPORTANTE:
Estos son modelos SQLAlchemy de PERSISTENCIA. NO son el mismo objeto
que EVMInput. Debe existir una función de conversión explícita:

Activity (ORM) → EVMInput (dominio)

Ejemplo conceptual:
def activity_to_evm_input(activity: Activity) -> EVMInput: ...

Configura Alembic y genera la migración inicial.

==================================================
PARTE 2 — SCHEMAS
==================================================

backend/app/schemas/project.py
backend/app/schemas/activity.py

Define:
- ProjectCreate, ProjectUpdate, ProjectResponse
- ActivityCreate, ActivityUpdate, ActivityResponse
- ActivityResponse debe incluir sus indicadores EVM calculados
  (reutilizando EVMService, no recalculando manualmente)
- ProjectResponse debe incluir los indicadores consolidados del proyecto
  (reutilizando EVMService.consolidate_indicators, NO promediando)

Validaciones deben coincidir con las reglas EVM ya definidas
(BAC > 0, percentages 0-100, AC >= 0).

==================================================
PARTE 3 — REPOSITORIES
==================================================

backend/app/repositories/project_repository.py
backend/app/repositories/activity_repository.py

Solo acceso a datos. Sin lógica de negocio.

==================================================
PARTE 4 — SERVICES
==================================================

backend/app/services/project_service.py
backend/app/services/activity_service.py

Responsables de:
- orquestar repository + EVMService
- convertir Activity ORM → EVMInput
- construir las respuestas con indicadores calculados
- manejar reglas de negocio (proyecto no encontrado, etc.)

NO dupliques cálculos EVM aquí. Delega siempre a EVMService.

==================================================
PARTE 5 — ROUTERS
==================================================

POST   /projects
GET    /projects
GET    /projects/{id}          (incluye EVM consolidado + actividades)
PUT    /projects/{id}
DELETE /projects/{id}

POST   /projects/{id}/activities
GET    /projects/{id}/activities
GET    /activities/{id}
PUT    /activities/{id}
DELETE /activities/{id}

Códigos de estado correctos: 200, 201, 204, 404, 422.

Documentación OpenAPI completa (descripciones, ejemplos, errores).

==================================================
PARTE 6 — SEED DE DATOS
==================================================

Crea backend/scripts/seed.py (comando manual, NO automático):

Proyecto "Proyecto Demo" con actividades:
- Diseño: bac=10000, planned=60, actual=40, ac=5000
- Desarrollo: bac=20000, planned=50, actual=45, ac=8000
- Pruebas: bac=5000, planned=30, actual=20, ac=2000

==================================================
PARTE 7 — TESTS BACKEND
==================================================

Integration tests para cada endpoint:
- creación exitosa
- listado
- detalle (verifica que incluya indicadores correctos)
- actualización
- eliminación
- 404 en recurso inexistente
- 422 en datos inválidos
- verificar que proyecto con múltiples actividades consolida
  correctamente (NO promedio de CPI/SPI — usa un caso con 2+ actividades
  y verifica el resultado contra el cálculo manual)

==================================================
PARTE 8 — FRONTEND (React + TypeScript + Vite + Recharts)
==================================================

Páginas/componentes:
- Selector/listado de proyectos
- Formulario crear/editar actividad
- Tabla de actividades con columnas: nombre, BAC, %planeado, %real,
  AC, y sus indicadores (PV, EV, CV, SV, CPI, SPI)
- Panel de indicadores consolidados del proyecto (CPI, SPI, EAC, VAC)
  con indicación visual clara (color/badge) de estado
- Gráfico de barras/líneas comparando PV, EV, AC por actividad (Recharts)
- Botón eliminar actividad con confirmación
- Estados de loading y error en las llamadas a la API

REGLA NO NEGOCIABLE:
El frontend NUNCA calcula CPI, SPI, EAC, VAC ni ningún indicador.
Todo indicador viene ya calculado desde el backend. React solo
muestra lo que la API retorna.

Después de crear/editar/eliminar una actividad, refresca los
indicadores del proyecto llamando de nuevo al endpoint correspondiente.

==================================================
PARTE 9 — CALIDAD
==================================================

Ejecuta:
pytest
pytest --cov=app --cov-report=term-missing
ruff check .
docker compose config
(frontend) npm run build

Business layer debe mantenerse >= 80% de coverage global.

Corrige: imports sin usar, magic numbers/strings, lógica de negocio
en routers o en React, código muerto, funciones grandes, duplicación.

==================================================
PARTE 10 — DOCUMENTACIÓN
==================================================

Actualiza README.md con:
- instrucciones de setup completo (docker compose up, migraciones, seed)
- cómo correr backend y frontend localmente

AI_PROCESS.md: NO inventes prompts. Registra únicamente decisiones
realmente tomadas en esta implementación (ej. la función de conversión
Activity→EVMInput si fue una decisión relevante).

==================================================
PARTE 11 — GIT
==================================================

NO hagas commit todavía.
NO hagas push.
NO hagas merge.

Al finalizar reporta:
- archivos creados/modificados (backend y frontend por separado)
- endpoints implementados
- cantidad de tests y resultado
- coverage
- Ruff
- resultado de npm run build
- captura textual de un caso de consolidación con 2+ actividades
  (valores de entrada y el JSON de respuesta) para que yo lo verifique
  manualmente
- problemas encontrados
- problemas pendientes
- estado READY FOR REVIEW o NOT READY FOR REVIEW

Si existe un problema funcional conocido, NO declares READY FOR REVIEW.
```

**Resultado (backend):** 49 tests, 93% coverage global (services 100%,
schemas 100%, repositories 63%). Bloqueado inicialmente por un bug de
configuración de tests (ver sección 4.2). Consolidación verificada con
2 actividades: entrada BAC=1000/5000, salida CPI consolidado=1.60,
distinto del promedio simple (1.40) — confirmado correcto.

**Resultado (frontend):** generado en una sesión posterior por corte de
contexto (ver 3.5). Componentes: ProjectSelector, ActivityForm,
ActivityTable, IndicatorsPanel, ActivitiesChart. Build exitoso, 837
módulos.

---

### 3.5 — Fix: configuración de tests con SQLite (StaticPool)

```text
El problema en conftest.py es un patrón conocido: SQLite en memoria
(:memory:) crea una conexión nueva por cada operación por defecto, y
cada conexión nueva pierde las tablas creadas anteriormente. Además,
si el override de get_db no se aplica ANTES de que la app cree su
propio engine, los tests usan el engine de producción en vez del de test.

CORRECCIÓN REQUERIDA EN conftest.py:

1. Crea el engine de test usando StaticPool para que todas las
   conexiones compartan la misma conexión SQLite en memoria:

   from sqlalchemy.pool import StaticPool

   engine = create_engine(
       "sqlite:///:memory:",
       connect_args={"check_same_thread": False},
       poolclass=StaticPool,
   )

2. Crea las tablas explícitamente en un fixture con scope apropiado
   (function o session, decide cuál evita fugas de datos entre tests):

   Base.metadata.create_all(bind=engine)

   (asegúrate de que TODOS los modelos —Project, Activity— ya estén
   importados antes de esta línea, o create_all no los verá)

3. Sobrescribe la dependencia get_db de la app ANTES de instanciar
   el TestClient:

   app.dependency_overrides[get_db] = override_get_db

4. Si usas un fixture de sesión por test, haz rollback o recreate
   de las tablas entre tests para evitar contaminación de datos.

TAREAS:
1. Reescribe conftest.py aplicando este patrón completo.
2. Ejecuta pytest y confirma que "no such table" desaparece.
3. Ejecuta pytest --cov=app --cov-report=term-missing
4. Ejecuta ruff check .
5. Reporta el resultado completo (no resumido) de tests y coverage.

NO toques la lógica de negocio, routers, services ni repositories.
Este es un fix aislado a la configuración de test de conftest.py.

NO hagas commit todavía.
```

**Resultado:** 49/49 tests pasando tras el fix. Ver sección 4.2 para
el análisis del bug.

---

### 3.6 — Fix: CORS para nuevos puertos de frontend

```text
El frontend (http://localhost:5174, puerto Vite dinámico) recibe error CORS
al llamar al backend (http://localhost:8000):

"blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present"

Revisa backend/app/main.py y agrega el middleware CORS de FastAPI.

Requisitos:
- Debe permitir origen(es) de desarrollo local (localhost:5173, localhost:5174,
  y en general cualquier puerto de localhost usado por Vite en dev, ya que
  Vite puede cambiar de puerto si el anterior está ocupado)
- Permitir métodos: GET, POST, PUT, DELETE, OPTIONS
- Permitir headers necesarios (Content-Type, Authorization si aplica)
- NO uses allow_origins=["*"] junto con allow_credentials=True (FastAPI/Starlette
  lo rechaza); si necesitas credentials, lista los orígenes explícitamente o
  usa una lista de orígenes permitidos vía variable de entorno.

Después de agregarlo:
1. Reinicia el servidor backend (o confirma que --reload lo recargó).
2. Reporta el diff exacto aplicado a main.py.
3. NO toques nada más (routers, services, modelos).
4. NO hagas commit todavía.
```

**Resultado:** middleware CORS agregado con `allow_origins` explícito.
Repetido dos veces más (secciones 3.7 y sesión del día siguiente) al
cambiar el frontend de puerto varias veces por conflictos locales.

---

### 3.7 — Fix: puerto fijo del frontend (5180) + actualización de CORS

```text
Agrega "http://localhost:5180" a la lista allow_origins del middleware CORS
en backend/app/main.py, manteniendo los orígenes existentes. No toques nada más.
```

---

### 3.8 — Diagnóstico y fix: conflicto de puerto Postgres (5432)

*(Contexto: no fue un único prompt sino un proceso de diagnóstico
colaborativo con Claude en claude.ai, ejecutando comandos de
verificación uno por uno directamente en PowerShell — no vía Claude
Code. Ver sección 4.3 para el relato completo. El fix final aplicado
al proyecto vía edición manual fue:)*

```text
docker-compose.yml: cambio de "5432:5432" a "5434:5432" en el mapeo
de puertos del servicio postgres, para evitar conflicto con un
PostgreSQL nativo de Windows preexistente que ya ocupaba el puerto
5432 en la máquina de desarrollo.
```

---

### 3.9 — Fix: badges de estado SPI usando etiquetas de CPI

```text
En el frontend, los badges de estado para SPI están usando las etiquetas
de CPI ("Over Budget" / "Good" / "At Risk", que son términos de costos).

SPI mide cronograma, no costos. Las etiquetas correctas para SPI son:
- SPI > 1 → "Ahead of Schedule"
- SPI = 1 → "On Schedule"
- SPI < 1 → "Behind Schedule"

CPI mantiene sus etiquetas actuales (Over Budget / Good / etc., son correctas
para costos).

Revisa el componente que renderiza los badges (probablemente ActivityTable.tsx
e IndicatorsPanel.tsx) y corrige el mapeo de estado para que SPI use sus
propias etiquetas, no las de CPI.

NO toques los cálculos numéricos, solo el texto/lógica de los badges visuales.

Reporta el diff y confirma con npm run build.
```

---

### 3.10 — Fix: formulario no acepta AC=0

```text
En el formulario de crear/editar actividad (ActivityForm.tsx), el campo
"Actual Cost" no permite ingresar el valor 0 — probablemente tiene un
atributo min="1" o una validación que rechaza 0 como valor inválido.

El backend permite AC=0 explícitamente y ya está confirmado funcionando
(cuando AC=0, CPI/EAC/VAC se devuelven como null). El formulario debe
reflejar esto: AC=0 es un valor válido y debe poder enviarse al backend.

Revisa el <input> de actual_cost en ActivityForm.tsx y cualquier
validación asociada (min, required con truthy check en vez de
null/undefined check, etc.) y corrígelo para que:
- El mínimo permitido del input sea 0 (no 1)
- 0 sea tratado como valor válido, no como "vacío" o "faltante"
  (cuidado con validaciones tipo `if (!value)` que tratan 0 como falsy)

Mismo chequeo defensivo para planned_percentage y actual_percentage
(0 debe ser válido ahí también). BAC sí debe seguir siendo > 0 (mínimo 1
o algo mayor a 0), no lo cambies.

Reporta el diff y confirma con npm run build.
```

---

### 3.11 — Fix: indicadores null mostrados como "0" en vez de "N/A"

```text
BUG CONFIRMADO: en ActivityTable.tsx (y posiblemente IndicatorsPanel.tsx),
cuando el backend devuelve un indicador como null (por ejemplo cpi: null
cuando AC=0), el frontend lo está mostrando como "0" en vez de "N/A".

Verificado con datos reales: actividad "Prueba AC Cero" (id=4) tiene
AC=0, y el backend devuelve correctamente cpi: null, eac: null, vac: null
en la respuesta del API. Pero la tabla muestra "0" en la columna CPI en
vez de "N/A".

CAUSA PROBABLE: alguna expresión tipo `value || 0` o `value ?? 0` que
trata null como "usar el default 0" en vez de "mostrar N/A explícitamente".

TAREAS:
1. Busca en ActivityTable.tsx, IndicatorsPanel.tsx, y cualquier otro
   componente que renderice cpi, spi, eac, o vac, todas las expresiones
   que puedan estar convirtiendo null en 0 (revisa especialmente
   operadores ||, ??, parseFloat sobre null, o valores por defecto en
   destructuring).
2. Corrige para que null se muestre siempre como "N/A" en la interfaz,
   distinguible claramente de un 0 real.
3. Verifica también spi y sv/cv (que si tienen valores reales como 0
   deben mostrar 0, no N/A — la corrección es solo para valores null).
4. Recarga el dashboard y confirma visualmente que la actividad
   "Prueba AC Cero" (id=4) ahora muestra CPI = "N/A", EAC = "N/A",
   VAC = "N/A", mientras que SPI sigue mostrando su valor numérico real
   (0.60), ya que SPI no depende de AC.

Reporta el diff y confirma con npm run build.
```

*(Nota honesta: el primer intento de fix, aplicado a PV/EV/CV/SV, no
cubrió la celda de CPI. Fue necesario un segundo prompt puntual
señalando específicamente que la celda de CPI seguía sin corregirse,
confirmado visualmente en el navegador antes de aceptar el fix.)*

---

### 3.12 — Fix definitivo: inputs numéricos (texto pegado / bloqueo de 0)

```text
SOLUCIÓN DEFINITIVA — usa un estado de texto separado por campo:

En vez de que el input esté controlado directamente por el número
(formData.bac), usa un estado de tipo STRING para lo que se muestra
en pantalla, y solo conviertes a número al validar/enviar.

Ejemplo del patrón correcto para el campo Actual Cost:

const [actualCostText, setActualCostText] = useState(
  initialData?.actual_cost !== undefined ? String(initialData.actual_cost) : ''
);

<input
  type="number"
  min="0"
  step="0.01"
  value={actualCostText}
  onChange={(e) => setActualCostText(e.target.value)}
  placeholder="0.00"
  disabled={loading}
/>

Y en el submit, conviertes:
const actualCost = actualCostText === '' ? 0 : parseFloat(actualCostText);
(valida que actualCost sea un número válido y >= 0 antes de enviar)

APLICA ESTE MISMO PATRÓN a los 4 campos numéricos: bac, planned_percentage,
actual_percentage, actual_cost. Cada uno con su propio estado de texto
independiente (bacText, plannedText, actualPercentageText, actualCostText).

Requisitos que DEBEN cumplirse simultáneamente después de este fix:
1. El campo puede estar completamente vacío mientras el usuario escribe
   (sin forzar un 0 ni bloquear el borrado).
2. El usuario puede escribir exactamente "0" y que se quede así en pantalla.
3. El usuario puede escribir "50" sin que se pegue ningún cero previo.
4. Al enviar el formulario, un campo vacío para actual_cost se trata como
   0 (comportamiento por defecto razonable), pero un campo con "0"
   explícito también se envía como 0 — ambos casos válidos.
5. BAC sigue validándose como > 0 al enviar (rechaza 0 o vacío para ese
   campo específico, ya que BAC=0 no tiene sentido de negocio).

Reporta el diff completo y confirma con npm run build.
```

*(Nota honesta: este fue el tercer intento sobre el mismo problema.
Los dos primeros —quitar el `|| ''`, luego un check `=== 0 ? '' :`—
cada uno resolvió un síntoma pero introdujo el síntoma contrario. El
patrón de estado-texto-separado fue la solución correcta y definitiva.)*

---

### 3.13 — Fix: respuesta 204 rompe el cliente API

```text
Bug confirmado: al eliminar una actividad, aparece en pantalla el error
"Failed to execute 'json' on 'Response': Unexpected end of JSON input".

Causa probable: el endpoint DELETE /activities/{id} devuelve 204 No
Content (sin body), que es el comportamiento HTTP correcto, pero el
cliente API en frontend/src/api.ts intenta llamar .json() sobre la
respuesta de cualquier método sin verificar si hay contenido, lo cual
falla en una respuesta vacía.

Revisa la función deleteActivity() (y cualquier otra función que llame
a un endpoint DELETE) en api.ts. Corrige para que, en respuestas 204 o
sin Content-Length, no intente parsear JSON — simplemente resuelva sin
valor (void), en vez de llamar response.json() incondicionalmente.

Reporta el diff y confirma con npm run build.
```

---

### 3.14 — Fix: tabla no se refresca tras eliminar (intentos 1-3)

```text
Bug confirmado: después de eliminar una actividad (Delete + confirmar),
la tabla de actividades no se actualiza automáticamente en pantalla —
la actividad eliminada sigue apareciendo hasta que el usuario recarga
la página manualmente. El backend sí borra correctamente (verificado
en base de datos), es solo el estado de React el que no se refresca.

Revisa el handler de delete en el componente que maneja las actividades
(probablemente App.tsx o ActivityTable.tsx) y confirma que después de
una eliminación exitosa se vuelve a pedir los datos del proyecto
(refetch) o se actualiza el estado local removiendo esa actividad,
igual que ya se hace correctamente después de crear o editar una
actividad (esos casos sí refrescan bien).

Reporta el diff y confirma con npm run build.
```

*(Segundo intento, tras confirmar en base de datos que el borrado sí
ocurría pero la UI no se actualizaba:)*

```text
En vez de seguir depurando por qué el estado de React no se refresca
tras eliminar una actividad, simplifica el enfoque: después de CUALQUIER
mutación (crear, editar, eliminar actividad), vuelve a pedir los datos
completos del proyecto seleccionado directamente del backend
(GET /projects/{id}), y reemplaza el estado del proyecto con la
respuesta fresca completa.

Esto debe aplicar de forma consistente a los tres flujos:
- Crear actividad → después de POST exitoso, refetch del proyecto
- Editar actividad → después de PUT exitoso, refetch del proyecto
- Eliminar actividad → después de DELETE exitoso, refetch del proyecto

Reporta el diff completo y confirma con npm run build.
```

*(Resultado final documentado en sección 6 — este bug quedó parcialmente
sin resolver, documentado como known issue.)*

---

### 3.15 — Auditoría final (timebox 45 min)

```text
AUDITORÍA FINAL TIMEBOX — TRYCORE EVM

TIEMPO MÁXIMO:
45 minutos.

NO realices una auditoría exploratoria completa desde cero.
El proyecto ya fue validado incrementalmente por feature.

OBJETIVO:
Encontrar únicamente defectos que puedan comprometer la entrega.

PRIORIDAD 1 — EVM
- validar manualmente los cálculos con un caso nuevo no probado antes
- confirmar que CPI/SPI consolidados NO se promedian
- validar AC=0, PV=0, proyecto sin actividades

PRIORIDAD 2 — API SMOKE TEST
pytest
pytest --cov=app --cov-report=term-missing

PRIORIDAD 3 — CALIDAD
ruff check .
docker compose config
(frontend) npm run build

PRIORIDAD 4 — SEGURIDAD
Buscar en el repo secretos, .env versionado, archivos sensibles.

PRIORIDAD 5 — DOCUMENTACIÓN
Verificar README.md actualizado (puerto Postgres, migraciones, seed).

PRIORIDAD 6 — OPENAPI
Confirmar /docs funciona y documenta todos los endpoints.

VERDICT:
READY FOR RELEASE o NOT READY FOR RELEASE.

NO hagas commit. NO hagas push.
```

**Resultado:** READY FOR RELEASE. 49/49 tests, 93% coverage, ruff
limpio, sin secretos en el historial (verificado independientemente,
ver sección 4.3), README corregido.

---

## 4. Decisiones donde NO seguí lo que la IA propuso

### 4.1 — Precisión numérica: redondeo intermedio vs. redondeo final

**Qué propuso Claude Code inicialmente:** la primera implementación del
`EVMService` calculaba CPI, SPI, EAC y VAC redondeando cada resultado
intermedio a 2 decimales *antes* de usarlo en la siguiente fórmula
(ej. `EAC = BAC / CPI_redondeado`).

**Por qué no lo acepté:** verifiqué manualmente el ejemplo de referencia
(BAC=1000, planned=50%, actual=45%, AC=400) con calculadora:
```
CPI real = 450/400 = 1.125
EAC correcto = 1000/1.125 = 888.89
```
El sistema devolvía `EAC=884.96`, que solo se explica si usó
`1000/1.13` (CPI ya redondeado) en vez de `1000/1.125`. La diferencia
es pequeña en este caso pero se agrava con presupuestos grandes o
consolidaciones de muchas actividades — es un error de acumulación de
redondeo, no un error de fórmula.

**Cómo verifiqué la corrección:** pedí el fix explícito (prompt 3.3),
y volví a calcular a mano dos casos distintos (el original y un segundo
caso con EV=600/AC=700, CPI=0.857142...) confirmando que EAC y VAC
coincidían con el cálculo manual de precisión completa en ambos, antes
de aceptar el commit.

### 4.2 — Configuración de tests: SQLite en memoria sin StaticPool

**Qué propuso Claude Code inicialmente:** al implementar los tests de
integración para el CRUD de Project/Activity, la configuración inicial
de `conftest.py` usaba SQLite en memoria (`sqlite:///:memory:`) con la
configuración por defecto de SQLAlchemy, sin `StaticPool`.

**Por qué no lo acepté:** los tests fallaban con `"no such table:
projects"` de forma intermitente. En vez de aceptar workarounds
sugeridos (como usar Postgres real en tests, que habría sido más lento
y dependiente de Docker en cada corrida), reconocí el patrón como un
problema conocido de SQLite en memoria: cada conexión nueva del pool
pierde las tablas creadas por conexiones anteriores si no se fuerza
una única conexión compartida.

**Cómo verifiqué la corrección:** pedí explícitamente el patrón
`StaticPool` (prompt 3.5) explicando la causa raíz, en vez de dejar que
Claude Code iterara por ensayo y error. Confirmé el fix viendo pasar
los 49 tests de forma consistente en corridas repetidas.

### 4.3 — Diagnóstico manual del UnicodeDecodeError (fuera de Claude Code)

Este caso no fue una decisión de "rechazar una sugerencia de Claude
Code", sino un proceso completo de diagnóstico que hice manualmente,
con apoyo de Claude (claude.ai) para guiar los siguientes pasos, sin
delegarlo a Claude Code:

Al intentar conectar el backend a PostgreSQL, aparecía un
`UnicodeDecodeError: 'utf-8' codec can't decode byte 0xf3` dentro de
psycopg2. Antes de aceptar cualquier solución superficial, verifiqué
metódicamente: el contenido real del `.env`, la ausencia de un
`.pgpass`, la ausencia de variables de entorno `PG*` del sistema, y
finalmente aislé psycopg2 de SQLAlchemy conectando directamente con
`psycopg2.connect()`. Cambié temporalmente a un driver 100% Python
(`pg8000`) para obtener un mensaje de error legible, que reveló la
causa real: un PostgreSQL nativo de Windows (EnterpriseDB) competía
por el puerto 5432 con mi contenedor Docker, y ese servidor nativo
devolvía sus mensajes de error en español (con tildes), lo cual rompía
la decodificación UTF-8 de psycopg2 al reportar el fallo de
autenticación. La solución fue mover el puerto publicado de Docker a
5434, sin tocar el servidor nativo.

---

## 5. Decisión de arquitectura tomada de forma independiente

**Separación de datos de dominio EVM y modelos de persistencia.**

Antes de implementar la feature de CRUD, decidí explícitamente (no fue
sugerencia inicial de Claude Code, sino una instrucción mía en el
prompt 3.4) que el servicio `EVMService` nunca debía recibir ni conocer
los modelos SQLAlchemy `Project`/`Activity` directamente. En su lugar,
exigí una función de conversión explícita `activity_to_evm_input()`
que traduce el modelo ORM al contrato de dominio `EVMInput` (un objeto
Pydantic sin dependencias de SQLAlchemy, HTTP o React).

La razón: quería poder testear la lógica financiera de forma
completamente aislada de la base de datos (que ya se había probado en
`feature/evm-domain` sin persistencia), y evitar que un cambio futuro
en el esquema de la base de datos rompiera silenciosamente los cálculos
EVM. Esto también evitó el riesgo de tener dos representaciones
distintas de "actividad" divergiendo con el tiempo.

---

## 6. Reflexión honesta: qué haría diferente

Si repitiera este ejercicio, invertiría más tiempo al principio en
**configurar el entorno de desarrollo de forma reproducible antes de
escribir código** — específicamente:

1. Habría verificado desde el inicio si había conflictos de puertos
   locales (Postgres nativo de Windows en 5432, otro proyecto propio en
   el puerto 8000) antes de empezar a levantar servicios, en vez de
   descubrirlo a mitad de la noche mediante un `UnicodeDecodeError`
   difícil de diagnosticar que en realidad era Postgres devolviendo un
   mensaje de error en español desde un servidor completamente
   distinto al que creía estar usando.

2. Habría usado un entorno virtual de Python (`venv`) desde el primer
   commit, en vez de instalar dependencias globalmente — esto habría
   evitado la sorpresa de descubrir a mitad de la noche que `alembic`
   nunca se había instalado realmente hasta que intenté correr la
   primera migración.

3. Habría fijado el "Default branch" del repositorio en GitHub a `main`
   desde que esa rama se creó, no al final — durante la verificación
   final descubrí que el default branch seguía apuntando a una rama
   vieja (`feature/evm-domain`), lo que habría hecho que cualquier
   evaluador que clonara el repo sin especificar rama viera una versión
   incompleta del proyecto, sin el CRUD ni el frontend.

4. En el frontend, habría implementado desde el principio el patrón de
   "estado de texto separado del estado numérico" para los inputs de
   formulario, en vez de llegar a él por tres iteraciones de prueba y
   error (bloqueo de escritura de 0, luego ceros pegados al escribir,
   luego bloqueo de 0 otra vez) — es un patrón conocido de React con
   inputs numéricos controlados que debí anticipar.

**Known issues no resueltos, documentados honestamente:**

Tras eliminar una actividad, la tabla del dashboard a veces requiere un
refresh manual de página para reflejar el cambio, a pesar de múltiples
intentos de corregir el auto-refetch (await agregado al flujo,
unificación del patrón de refetch en las tres mutaciones, corrección
del manejo de respuestas 204). Verificado que el backend siempre borra
correctamente (confirmado con consultas SQL directas en cada intento)
— es un defecto de sincronización de estado en React, no de integridad
de datos. Decidí no seguir iterando sobre esto dado el tiempo
disponible, priorizando validar el resto del sistema.

Adicionalmente, quedan sin resolver por falta de tiempo: reordenamiento
visual de filas de actividades tras editar/eliminar, diseño no
completamente responsive (los botones de acción pueden quedar ocultos
en pantallas pequeñas), e inconsistencia de idioma (mezcla de español
e inglés) en la interfaz. Ninguno afecta la corrección de los cálculos
EVM ni la integridad de los datos.
