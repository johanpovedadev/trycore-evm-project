# EVM (Earned Value Management) - Documentación

## Concepto General

Earned Value Management es una metodología de gestión de proyectos que integra alcance, cronograma y recursos para evaluar el desempeño del proyecto.

## Métricas Fundamentales

### BAC (Budget At Completion)
- **Definición:** Presupuesto total autorizado para el proyecto o actividad
- **Unidad:** Dinero (USD, EUR, etc.)
- **Notas:**
  - Es el presupuesto planeado total
  - Debe ser > 0
  - Se define al inicio del proyecto

### PV (Planned Value)
- **Definición:** Valor del trabajo que se esperaba completar en un momento dado
- **Fórmula:** `PV = planned_progress × BAC`
- **Unidad:** Dinero (misma que BAC)
- **Notas:**
  - Representa qué debería estar hecho según cronograma
  - Acumulativo a lo largo del tiempo

### EV (Earned Value)
- **Definición:** Valor del trabajo realmente completado
- **Fórmula:** `EV = actual_progress × BAC`
- **Unidad:** Dinero (misma que BAC)
- **Notas:**
  - Solo cuenta el trabajo realmente ejecutado
  - No puede ser mayor que PV en proyectos retrasados

### AC (Actual Cost)
- **Definición:** Costo real incurrido por el trabajo ejecutado
- **Unidad:** Dinero (misma que BAC)
- **Notas:**
  - No puede ser negativo
  - Puede ser mayor que EV si hay sobrecosto

---

## Indicadores Derivados

### CV (Cost Variance)
- **Fórmula:** `CV = EV − AC`
- **Rango:** (-∞, +∞)
- **Interpretación:**
  - `CV > 0` → Bajo presupuesto (favorable)
  - `CV = 0` → Exacto presupuesto
  - `CV < 0` → Sobre presupuesto (desfavorable)

### SV (Schedule Variance)
- **Fórmula:** `SV = EV − PV`
- **Rango:** (-∞, +∞)
- **Interpretación:**
  - `SV > 0` → Adelantado en cronograma (favorable)
  - `SV = 0` → Según cronograma
  - `SV < 0` → Retrasado en cronograma (desfavorable)

### CPI (Cost Performance Index)
- **Fórmula:** `CPI = EV / AC`
- **Rango:** (0, +∞)
- **Interpretación:**
  - `CPI > 1` → Eficiente en costos (favorable)
  - `CPI = 1` → Eficiente exacto
  - `CPI < 1` → Ineficiente en costos (desfavorable)
  - `CPI = 0` → Indefinido (cuando AC = 0)

### SPI (Schedule Performance Index)
- **Fórmula:** `SPI = EV / PV`
- **Rango:** (0, +∞)
- **Interpretación:**
  - `SPI > 1` → Adelantado (favorable)
  - `SPI = 1` → Según cronograma
  - `SPI < 1` → Retrasado (desfavorable)
  - `SPI = 0` → Indefinido (cuando PV = 0)

### EAC (Estimate At Completion)
- **Fórmula:** `EAC = BAC / CPI`
- **Rango:** (0, +∞)
- **Interpretación:**
  - Proyección de costo total al completar
  - Si `CPI < 1`, el EAC será mayor que BAC
  - Indefinido cuando `CPI = 0`

### VAC (Variance At Completion)
- **Fórmula:** `VAC = BAC − EAC`
- **Rango:** (-∞, +∞)
- **Interpretación:**
  - Ahorro o sobrecosto proyectado al final
  - `VAC > 0` → Se espera ahorro
  - `VAC < 0` → Se espera sobrecosto

---

## Consolidación de Indicadores por Proyecto

### Regla Crítica

**Los indicadores de proyecto NO se calculan promediando los indicadores de las actividades.**

Proceso correcto:

```
1. Sumar todos los BAC de actividades
   BAC_total = Σ BAC

2. Sumar todos los PV de actividades
   PV_total = Σ PV

3. Sumar todos los EV de actividades
   EV_total = Σ EV

4. Sumar todos los AC de actividades
   AC_total = Σ AC

5. Calcular indicadores sobre los totales
   CPI_proyecto = EV_total / AC_total
   SPI_proyecto = EV_total / PV_total
   EAC_proyecto = BAC_total / CPI_proyecto
   VAC_proyecto = BAC_total − EAC_proyecto
```

**Nunca:**
```
❌ CPI_proyecto = (CPI_act1 + CPI_act2 + ...) / N
❌ SPI_proyecto = Promedio(SPI)
```

---

## Manejo de Edge Cases

### Caso 1: AC = 0

**Contexto:** Actividad sin costo registrado aún

**Impacto:**
- CPI = EV / 0 → **Indefinido**
- EAC = BAC / CPI → **Indefinido**

**Decisión:**
- Retornar `null` para CPI cuando AC = 0
- Retornar `null` para EAC cuando CPI indefinido

### Caso 2: PV = 0

**Contexto:** No se ha iniciado actividad

**Impacto:**
- SPI = EV / 0 → **Indefinido**

**Decisión:**
- Retornar `null` para SPI cuando PV = 0

### Caso 3: EV = 0

**Contexto:** No hay progreso, pero hay costo

**Impacto:**
- CV = 0 - AC = -AC (negativo, desfavorable)
- CPI = 0 / AC = 0 (muy ineficiente)

**Decisión:**
- Permitir valores, son válidos
- CPI = 0 es un valor válido (no confundir con indefinido)

### Caso 4: BAC ≤ 0

**Contexto:** Presupuesto inválido

**Impacto:**
- Toda la lógica depende de BAC > 0

**Decisión:**
- Validar en entrada: BAC debe ser > 0
- Lanzar excepción si BAC ≤ 0

### Caso 5: AC < 0

**Contexto:** Costo negativo (reembolso, ajuste)

**Impacto:**
- Poco común pero posible en contabilidad
- CPI puede ser mayor que esperado

**Decisión:**
- Permitir AC < 0 (caso válido)
- Documentar en comentario de BD

### Caso 6: Progreso < 0% o > 100%

**Contexto:** Entrada de usuario inválida

**Impacto:**
- EV puede ser negativo o mayor que BAC

**Decisión:**
- Validar en entrada: progress ∈ [0.0, 1.0]
- Lanzar excepción si está fuera de rango

### Caso 7: Proyecto sin actividades

**Contexto:** Proyecto creado pero sin actividades

**Impacto:**
- BAC_total = 0 (suma vacía)
- PV_total, EV_total, AC_total = 0

**Decisión:**
- Retornar indicadores como `null` si no hay actividades
- O retornar estructura con valores 0 y ratios null

### Caso 8: Ratios indefinidos en consolidación

**Contexto:** AC_total = 0 o PV_total = 0

**Impacto:**
- CPI_proyecto indefinido
- SPI_proyecto indefinido

**Decisión:**
- Retornar `null` para ambos
- Nunca retornar Infinity o NaN en JSON

---

## Decisión sobre Representación de Indefinidos

### Opción elegida: `null`

**Razón:**
- JSON no soporta Infinity ni NaN
- `null` es explícito y claro
- Fácil de manejar en frontend

**Ejemplo de respuesta:**
```json
{
  "activity_id": 1,
  "bac": 1000.0,
  "pv": 500.0,
  "ev": 450.0,
  "ac": 400.0,
  "cv": 50.0,
  "sv": -50.0,
  "cpi": 1.125,
  "spi": 0.9,
  "eac": 888.89,
  "vac": 111.11
}
```

**Cuando AC = 0:**
```json
{
  "activity_id": 2,
  "bac": 1000.0,
  "pv": 500.0,
  "ev": 450.0,
  "ac": 0.0,
  "cv": 450.0,
  "sv": -50.0,
  "cpi": null,
  "spi": 0.9,
  "eac": null,
  "vac": null
}
```

---

## Fórmulas Resumen

| Métrica | Fórmula | Tipo |
|---------|---------|------|
| CV | EV - AC | Varianza |
| SV | EV - PV | Varianza |
| CPI | EV / AC | Ratio |
| SPI | EV / PV | Ratio |
| EAC | BAC / CPI | Proyección |
| VAC | BAC - EAC | Proyección |

---

## Implementación

**Ubicación:** `app/services/evm_service.py`

**Estructura aproximada:**
```python
class EVMIndicators:
    bac: float
    pv: float
    ev: float
    ac: float
    cv: float
    sv: float
    cpi: Optional[float]
    spi: Optional[float]
    eac: Optional[float]
    vac: Optional[float]

class EVMService:
    def calculate_activity_indicators(activity) -> EVMIndicators:
        # Implementar con reglas de edge cases
        pass
    
    def calculate_project_indicators(project) -> EVMIndicators:
        # Consolidar desde actividades
        pass
```

---

**Última actualización:** Foundation - Definiciones EVM
