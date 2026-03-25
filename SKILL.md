---
name: corregir-tps
description: >
  Skill para corregir trabajos prácticos de programación de estudiantes secundarios.
  Usar cuando el usuario quiera revisar código de alumnos (HTML/CSS, JavaScript, React),
  asignar una nota sugerida y generar feedback formateado. Se activa cuando el usuario
  menciona "corregir TPs", "revisar trabajos", "corrección de alumnos", "nota sugerida",
  o cuando provee repos de GitHub o archivos ZIP de estudiantes para evaluar.
  También usar cuando el usuario pide procesar una lista de alumnos o generar un archivo
  de correcciones. SIEMPRE usar esta skill cuando haya código de alumnos para revisar.
---

# Skill: Corrección de TPs de Programación

Ayuda al profesor a corregir trabajos prácticos de alumnos de forma rápida y consistente.
El flujo genera un archivo `correcciones.md` con el feedback de todos los alumnos, listo
para que el profesor revise, ajuste notas si quiere, y comparta.

---

## Paso 0 — Normalizar las entregas del campus

Las entregas de los alumnos llegan mezcladas en una carpeta. Antes de corregir,
ejecutar el script `scripts/preparar_entregas.py` para normalizarlas todas a
`alumnos/<nombre>/` independientemente del formato.

### Formatos que maneja automáticamente

| Archivo del alumno | Contenido | Qué hace el script |
|---|---|---|
| `Francisco.zip` | Proyecto web | Descomprime → `alumnos/Francisco/` |
| `Valentina.zip` | Un `.txt` con URL de GitHub | Descomprime → detecta URL → clona |
| `Matias.txt` | URL de GitHub directa | Clona → `alumnos/Matias/` |
| `Sofia.zip` | Proyecto + un `.txt` con URL | Descomprime → detecta URL → clona |

El script también maneja el caso en que el alumno zipee el `.txt` por error.

### Cómo ejecutarlo

```bash
# Estructura esperada antes de correr:
# entregas/
#   Francisco.zip
#   Valentina.zip
#   Matias.txt
#   Sofia.zip

python scripts/preparar_entregas.py --entregas ./entregas --salida ./alumnos
```

Si la carpeta se llama `entregas` y está en el directorio actual, alcanza con:
```bash
python scripts/preparar_entregas.py
```

### Output del script

Muestra el estado de cada alumno y un resumen al final:
```
👤 Francisco (.zip)
  ✓ ZIP descomprimido

👤 Valentina (.zip)
  → ZIP contiene .txt con URL: https://github.com/vale/tp3.git
  ✓ repo clonado (desde ZIP)

👤 Matias (.txt)
  → Clonando https://github.com/mati/tp3.git ...
  ✓ repo clonado
```

Si algún alumno aparece con `⚠ .txt sin URL válida` o `✗ error`, revisarlo
manualmente antes de continuar con la corrección.

### Prerequisitos
- `git` instalado y en el PATH
- Python 3.10 o superior (usa `str | None` syntax)
- Conexión a internet para clonar repos

---

## Paso 1 — Obtener la consigna y/o rúbrica del TP

Antes de corregir, buscar la consigna del TP en este orden de prioridad:

### 1a. Buscar archivo de consigna en el directorio de trabajo

Buscar automáticamente archivos con nombres como:
`consigna`, `enunciado`, `rubrica`, `tp`, `practica` (con cualquier extensión)

```bash
find . -maxdepth 2 \( -name "consigna*" -o -name "enunciado*" \
  -o -name "rubrica*" -o -name "tp*" -o -name "practica*" \) \
  \( -iname "*.txt" -o -iname "*.pdf" -o -iname "*.md" \) \
  ! -path "*/alumnos/*" ! -path "*/node_modules/*" \
  | head -10
```

- Si encuentra un `.txt` o `.md` → leerlo directamente con `cat`
- Si encuentra un `.pdf` → leerlo con `python3 -c "import pdfplumber; ..."`  
  o con `pdftotext consigna.pdf -` si está disponible
- Si encuentra más de un archivo → preguntar al profesor cuál usar

### 1b. Rúbrica provista inline en el prompt

Si el profesor escribió los criterios directamente en su mensaje, usarlos.
Ejemplo: *"La rúbrica es: formulario funcional, usar let/const, buena indentación."*

### 1c. Ninguna consigna encontrada

Si no hay archivo ni rúbrica en el prompt, preguntar antes de continuar:
> "No encontré un archivo de consigna en la carpeta. ¿Podés compartirme la rúbrica
> del TP o dejarme un archivo `consigna.txt` / `consigna.pdf` en el directorio?
> Si querés, usá el formato de ejemplo en `references/rubrica-ejemplo.md`."

### Qué extraer de la consigna

Al leer la consigna (sea archivo o texto), identificar:
- **Funcionalidades requeridas** (qué debe hacer el proyecto)
- **Restricciones técnicas** (usar/no usar ciertas tecnologías o patrones)
- **Criterios de evaluación** si los hay explícitos
- **Nivel esperado** (¿es el primer TP o ya saben bastante?)

---

## Paso 2 — Verificar que alumnos/ esté lista

Después del Paso 0, la carpeta `alumnos/` debe tener una subcarpeta por alumno.
Verificar con:

```bash
ls alumnos/
# Francisco/   Valentina/   Matias/   Sofia/
```

Si el usuario saltó el Paso 0 y tiene:
- **Carpeta `alumnos/` ya armada**: continuar directamente al Paso 3.
- **ZIPs sin procesar**: ejecutar el script del Paso 0.
- **URLs sueltas en el prompt**: clonar manualmente:
  ```bash
  git clone https://github.com/usuario/repo.git alumnos/NombreAlumno
  ```

El nombre del alumno para el feedback se toma **del nombre de la subcarpeta**.

---

## Paso 3 — Analizar el código de cada alumno

Para cada alumno, leer los archivos relevantes según la tecnología del TP:

### HTML/CSS
- Leer todos los `.html` y `.css`
- Buscar: `index.html`, `style.css`, `main.css`

### JavaScript Vanilla
- Leer todos los `.js` (excluir `node_modules/`)
- Prestar atención a: `app.js`, `main.js`, `script.js`

### React
- Leer `src/` completo (`.jsx`, `.tsx`, `.js`)
- Leer `package.json` para verificar dependencias
- Excluir: `node_modules/`, `dist/`, `build/`, `.git/`

### Comandos útiles para explorar el proyecto
```bash
# Ver estructura general (sin node_modules)
find alumnos/<nombre> -type f \
  ! -path "*/node_modules/*" \
  ! -path "*/.git/*" \
  ! -path "*/dist/*" \
  | head -50

# Leer un archivo
cat alumnos/<nombre>/src/App.jsx
```

**Leer el código completo** antes de evaluar. No hacer suposiciones sobre lo que
el alumno hizo o no hizo sin haber leído el archivo.

---

## Paso 4 — Evaluar según la rúbrica

Para cada criterio de la rúbrica, determinar:
- ✅ Cumplido correctamente
- ⚠️ Cumplido parcialmente o con errores menores
- ❌ No cumplido o con errores graves

### Criterios universales a revisar SIEMPRE (aunque no estén en la rúbrica)

| Categoría | Qué revisar |
|-----------|-------------|
| **Indentación** | ¿El código tiene indentación consistente y legible? |
| **Nomenclatura** | ¿Variables y funciones tienen nombres descriptivos en español o inglés consistente? |
| **`var` vs `let/const`** | ¿Usa `let`/`const` en vez de `var`? |
| **HTML semántico** | ¿Usa tags semánticos (`header`, `main`, `section`, etc.) donde corresponde? |
| **Tags sin cerrar** | ¿Todos los tags HTML están correctamente cerrados? |
| **Console.log olvidados** | ¿Hay `console.log` de debug que no se limpiaron? |
| **Funcionalidades faltantes** | ¿El enunciado pedía algo que no está implementado? |
| **Errores de sintaxis obvios** | ¿Hay errores que impedirían que el código corra? |

Para React, agregar:
| **Categoría** | **Qué revisar** |
|---------------|-----------------|
| **Keys en listas** | ¿Usa `key` prop en elementos renderizados con `.map()`? |
| **Estado correcto** | ¿Usa `useState` apropiadamente? ¿Modifica el estado directamente? |
| **Props** | ¿Los componentes reciben y usan props correctamente? |
| **Efectos** | ¿`useEffect` tiene las dependencias correctas? |

---

## Paso 4b — Detectar copias y uso abusivo de IA

Este paso se ejecuta **después de leer el código de todos los alumnos** y antes
de generar el feedback individual. Los resultados se incorporan luego en el
feedback de cada alumno afectado (Paso 6).

---

### Detección de copias entre alumnos

Comparar los TPs de todos los alumnos entre sí buscando similitudes estructurales.
**No alcanza con que el código sea visualmente distinto** — hay que comparar la lógica.

#### Qué comparar

| Señal | Cómo detectarla |
|-------|-----------------|
| **Misma estructura de funciones** | ¿Los mismos nombres de función, en el mismo orden, con la misma lógica interna? |
| **Variables renombradas** | ¿`contador` en uno y `count` en otro, pero el resto igual? |
| **Strings y comentarios cambiados** | ¿Mismo código pero con textos o comentarios distintos? |
| **Reordenamiento superficial** | ¿Mismos bloques de código en distinto orden pero idénticos internamente? |
| **HTML idéntico con CSS distinto** | ¿La estructura HTML es copia pero los estilos fueron cambiados? |
| **Mismos bugs** | ¿Dos alumnos tienen exactamente el mismo error en el mismo lugar? Señal muy fuerte. |

#### Niveles de sospecha

- 🔴 **Alta**: Misma lógica, mismos nombres o muy similares, mismos bugs. Casi certeza de copia.
- 🟡 **Media**: Estructura muy similar pero con diferencias que podrían ser coincidencia
  (el TP era guiado y todos siguieron los mismos pasos).
- ⚪ **Baja / ignorar**: Similar solo en la parte que el enunciado obligaba a hacer igual.

Solo reportar nivel **media** o **alta**. Las similitudes esperadas por el enunciado no son copia.

#### Cómo incorporarlo en el feedback

En el feedback de **cada alumno involucrado** en una sospecha media o alta, agregar
al final del feedback individual (después de las correcciones técnicas):

```markdown
> ⚠️ **Nota para el profesor:** Este TP presenta similitudes importantes con el de
> [Nombre del otro alumno]. Revisá en clase si [Nombre] puede explicar el código,
> especialmente [señalar la parte más sospechosa, ej: "la función `calcularTotal()`"].
```

No acusar directamente al alumno — este texto es una nota interna para el profesor.

---

### Detección de uso excesivo de IA

**Importante:** Esta detección es orientativa. Un alumno prolijo puede activar
estas señales sin haber usado IA. Nunca usar esto para sancionar directamente —
solo para decidir si vale la pena preguntar en clase.

#### Señales a buscar

| Señal | Descripción |
|-------|-------------|
| **Comentarios exhaustivos** | Cada línea o bloque tiene un comentario explicativo detallado, inusual para el nivel del curso |
| **Manejo de errores sofisticado** | `try/catch` con mensajes descriptivos, validaciones de edge cases que van muy más allá del enunciado |
| **Nomenclatura perfectamente consistente** | Todos los nombres en inglés, en camelCase sin excepción, descriptivos al máximo — contrasta con el nivel del alumno en TPs anteriores |
| **Estructura de carpetas profesional** | Separación de concerns, organización en módulos que nadie en el curso haría espontáneamente |
| **Funcionalidades no pedidas** | El TP tiene features extras bien implementadas que el enunciado no pedía |
| **Contraste con el nivel previo** | El alumno entregó TPs anteriores muy básicos y este es notablemente más sofisticado |
| **Código sin errores de principiante** | Cero `var`, indentación perfecta, sin `console.log` olvidados — cuando el resto de la clase sí los tiene |

#### Cuántas señales activan el flag

- **1 señal sola**: No es suficiente. No marcar.
- **2–3 señales juntas**: Flag sutil en el feedback.
- **4 o más señales**: Flag con mención de cuáles señales se observaron.

#### Cómo incorporarlo en el feedback

Agregar al final del feedback individual, **después** de las correcciones técnicas
y después de cualquier nota de copia si la hubiera:

```markdown
> 💡 **Nota para el profesor:** Este TP muestra algunas características inusuales
> para el nivel del curso (comentarios muy detallados, manejo de errores sofisticado,
> estructura profesional). Podría valer la pena pedirle a [Nombre] que explique
> alguna parte del código en clase para confirmar que lo comprende.
```

Si hay pocas señales o la explicación más probable es que el alumno simplemente
es bueno, **no agregar el flag**. Ante la duda, omitir.

---

## Paso 5 — Calcular la nota sugerida

La nota va de 1 a 10. Usar la siguiente lógica base, ajustada según los pesos
de la rúbrica si el profesor los definió:

| Situación | Nota base |
|-----------|-----------|
| Todo cumplido, código prolijo | 9–10 |
| Mayoría cumplido, errores menores | 7–8 |
| Funcionalidades principales OK, varios problemas de calidad | 5–6 |
| Funcionalidades principales incompletas | 3–4 |
| Poco o nada implementado correctamente | 1–2 |

Si el profesor definió pesos en la rúbrica, calcular la nota proporcionalmente.

**Regla importante**: Si una funcionalidad requerida por el enunciado está completamente
ausente (no implementada), bajar al menos 1.5 puntos por funcionalidad faltante.

---

## Paso 6 — Generar el archivo de correcciones

Crear el archivo `correcciones.md` en el directorio de trabajo con el siguiente formato
**exacto** para cada alumno:

```markdown
## <Nombre del Alumno>: <Nota sugerida>

<Un párrafo introductorio: ¿el TP está bien hecho en general? Tono constructivo.>

**Correcciones:**
- <Corrección 1: específica, con referencia al archivo/línea si es posible>
- <Corrección 2>
- <Corrección N>

**Puntos destacados:** *(solo si hay algo genuinamente bueno para resaltar)*
- <Punto positivo>

> ⚠️ **Nota para el profesor:** [Solo si hay sospecha de copia — ver Paso 4b]

> 💡 **Nota para el profesor:** [Solo si hay señales de uso excesivo de IA — ver Paso 4b]

---
```

Las notas `⚠️` y `💡` son opcionales — solo aparecen si el Paso 4b las activó.
Nunca inventar sospechas. Si no hay señales claras, omitir completamente esas líneas.

### Reglas de redacción del feedback

- **Tutear al alumno** (ej: "No te olvides de...", "Hiciste bien...")
- **Ser específico**: mencionar el archivo y número de línea cuando sea posible
  (ej: "En `script.js` línea 23, la variable `x` debería llamarse `contador`")
- **Tono constructivo**: señalar el error y sugerir cómo corregirlo
- **No ser repetitivo**: si hay muchos errores del mismo tipo (ej: indentación en
  todo el archivo), mencionarlo una sola vez
- **Español neutro**: sin regionalismos, comprensible para alumnos argentinos
- **Longitud del feedback**: entre 3 y 7 bullets por alumno. Si hay más de 7 problemas,
  priorizar los más importantes.

---

## Paso 7 — Resumen final

Al final del archivo `correcciones.md`, agregar una tabla resumen:

```markdown
---

## Resumen de notas

| Alumno | Nota sugerida |
|--------|---------------|
| Francisco | 9 |
| Valentina | 7 |
| ...    | ...           |

**Promedio de la clase:** X.X
```

---

## Notas adicionales

### Si el repo está vacío o el ZIP no tiene código
Escribir en el feedback:
> "No se encontró código para revisar. Si subiste el archivo incorrecto o el repo
> está vacío, contactá al profesor."
> Nota sugerida: 1

### Si el código no corre (errores de sintaxis graves)
Mencionarlo como primer bullet: "El código tiene errores de sintaxis que impedirían
que funcione. Revisá [archivo] en la línea [N]."

### Si el profesor quiere revisar un solo alumno
Generar el feedback de ese alumno en la conversación, sin crear archivo.

### Archivos a ignorar siempre
`.git/`, `node_modules/`, `dist/`, `build/`, `.DS_Store`, `*.lock`, `*.map`

---

## Referencia rápida de comandos

```bash
# Clonar un repo
git clone https://github.com/usuario/repo.git alumnos/nombre_alumno

# Ver estructura del proyecto
find alumnos/nombre -type f ! -path "*/node_modules/*" ! -path "*/.git/*"

# Descomprimir todos los ZIPs en una carpeta
for zip in *.zip; do unzip -q "$zip" -d "alumnos/${zip%.zip}"; done

# Ver todos los archivos JS de un alumno
find alumnos/nombre -name "*.js" ! -path "*/node_modules/*"
```

Para más detalles sobre el formato de rúbrica, leer `references/rubrica-ejemplo.md`.
