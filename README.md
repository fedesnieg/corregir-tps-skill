# corregir-tps — Skill para Claude Code

Skill para corregir trabajos prácticos de programación de alumnos de secundaria.
Dado una carpeta con las entregas del campus virtual y la consigna del TP, genera
un archivo `correcciones.md` con el feedback de cada alumno y una nota sugerida.

---

## Requisitos

| Herramienta | Para qué |
|---|---|
| [Claude Code](https://claude.ai/code) | Ejecutar la skill desde la terminal |
| Suscripción Claude Pro o Max | Incluye uso de Claude Code |
| Node.js 18+ | Requerido por Claude Code |
| Python 3.10+ | Script de preparación de entregas |
| Git | Clonar repos de alumnos que entregaron URL de GitHub |

Verificar que tenés todo:
```bash
node --version    # debe ser 18 o superior
python3 --version # debe ser 3.10 o superior
git --version
```

---

## Instalación (una sola vez)

**1. Instalá Claude Code** (si no lo tenés)
```bash
npm install -g @anthropic/claude-code
claude login
```

**2. Cloná el repo e instalá la skill**
```bash
git clone https://github.com/fedesnieg/corregir-tps.git
mkdir -p ~/.claude/skills
cp -r corregir-tps ~/.claude/skills/
```

**3. Verificá que quedó bien**
```bash
ls ~/.claude/skills/corregir-tps/
# Debe mostrar: SKILL.md  scripts/  references/  ejemplos/
```

La skill queda disponible en todos tus proyectos automáticamente.

---

## Archivos incluidos

```
corregir-tps.skill                  ← skill para instalar en Claude Code
references/rubrica-ejemplo.md       ← plantilla para armar la rúbrica de cada TP
ejemplos/correcciones-ejemplo.md    ← ejemplo del output que genera la skill
scripts/preparar_entregas.py        ← script que normaliza las entregas (la skill lo corre sola)
```

---

## Uso

### 1. Descargá las entregas del campus

En el campus virtual, descargá los adjuntos de cada alumno a una carpeta `entregas/`.
Los alumnos pueden entregar:

- `Francisco.zip` — proyecto comprimido
- `Valentina.zip` — ZIP que contiene un `.txt` con URL de GitHub (lo maneja solo)
- `Matias.txt` — archivo con la URL de GitHub directamente

> Si un alumno pegó la URL en el campo de texto del campus (sin adjunto), creá vos
> un archivo `NombreAlumno.txt` con esa URL y poné lo en `entregas/`.

### 2. Armá la carpeta del TP

```
tp3-calculadora/
├── consigna.pdf        ← o consigna.txt / enunciado.pdf / rubrica.md
└── entregas/
    ├── Francisco.zip
    ├── Valentina.zip
    ├── Matias.txt
    └── Sofia.zip
```

El archivo de consigna puede llamarse `consigna`, `enunciado`, `rubrica`, `tp` o
`practica`, con extensión `.pdf`, `.txt` o `.md`. La skill lo encuentra automáticamente.

Si no tenés un archivo de consigna, podés dictarle la rúbrica directamente en el
mensaje (ver paso 4).

### 3. Abrí Claude Code en la carpeta del TP

```bash
cd tp3-calculadora
claude
```

### 4. Pedile que corrija

Dentro de Claude Code escribí:
```
Corregí los TPs de esta carpeta
```

Si no tenés archivo de consigna, podés incluir la rúbrica en el mensaje:
```
Corregí los TPs de esta carpeta. La rúbrica es: debe tener un formulario funcional,
usar let/const en vez de var, buena indentación, y el botón enviar debe validar
que los campos no estén vacíos.
```

### 5. Revisá el resultado

La skill genera `correcciones.md` en la carpeta del TP. Abrilo, revisá el feedback
de cada alumno, ajustá las notas que consideres, y listo.

---

## Qué hace la skill automáticamente

**Preparación de entregas**
- Descomprime los ZIPs de cada alumno
- Detecta si un ZIP contiene un `.txt` con URL de GitHub y clona el repo
- Clona repos directamente si el alumno entregó un `.txt` con la URL

**Corrección**
- Lee la consigna o rúbrica (archivo o texto)
- Analiza el código de cada alumno (HTML/CSS, JavaScript, React)
- Evalúa indentación, uso de `let`/`const`, HTML semántico, funcionalidades faltantes,
  y todos los criterios de la rúbrica
- Sugiere una nota del 1 al 10

**Detección de copias**
- Compara los TPs entre sí buscando similitudes estructurales
- Detecta copias aunque el alumno haya renombrado variables o reordenado bloques
- Marca en el feedback de cada alumno involucrado con una nota para que el profesor
  pueda verificar en clase

**Señales de uso excesivo de IA**
- Busca indicadores como comentarios exhaustivos, manejo de errores muy sofisticado,
  o un salto notable de nivel respecto a TPs anteriores
- Solo agrega un flag si hay múltiples señales simultáneas
- Es orientativo — la decisión final siempre es del profesor

---

## Formato del output

Cada alumno en `correcciones.md` tiene esta estructura:

```markdown
## Francisco: 9

El TP está muy bien hecho. La calculadora funciona correctamente para todas
las operaciones y el código está organizado en funciones claras.

**Correcciones:**
- Mejorá la indentación en `script.js` (líneas 12–28).
- En `script.js` línea 8, usás `var resultado` — cambialo a `let`.
- El `div` de la línea 15 en `index.html` no está cerrado.

**Puntos destacados:**
- La división por cero muestra "Error" en el display — muy buen detalle.

> ⚠️ Nota para el profesor: Este TP presenta similitudes con el de Valentina.
> Revisá en clase si Francisco puede explicar la función `calcularTotal()`.
```

Al final del archivo hay una tabla resumen con las notas sugeridas y el promedio
de la clase.

---

## Rúbrica

Podés definir los criterios de evaluación de tres formas:

**Opción A — Archivo en la carpeta del TP** (recomendada)
Copiá `references/rubrica-ejemplo.md`, renombralo (ej: `rubrica-tp3.md`) y editá
los criterios. La skill lo va a encontrar automáticamente.

**Opción B — Inline en el mensaje**
Dictale los criterios directamente al pedirle la corrección.

**Opción C — Sin rúbrica**
La skill aplica criterios universales de calidad de código y te pregunta si falta
algo antes de empezar.

---

## Estructura de carpetas recomendada

```
mis-tps/
├── tp1-html-basico/
│   ├── consigna.pdf
│   ├── entregas/
│   └── correcciones.md        ← generado por la skill
├── tp2-javascript/
│   ├── consigna.txt
│   ├── rubrica-tp2.md
│   ├── entregas/
│   └── correcciones.md
└── tp3-calculadora/
    ├── consigna.pdf
    └── entregas/
```

---

## Preguntas frecuentes

**¿Qué pasa si un alumno no entregó nada?**
No va a haber archivo en `entregas/` con su nombre. La skill solo corrige a los
alumnos que tienen entrega. Si querés que aparezca igual en `correcciones.md`,
creá un archivo vacío `NombreAlumno.txt` sin contenido — la skill lo va a marcar
como entrega faltante con nota 1.

**¿Puedo corregir un solo alumno?**
Sí. En Claude Code:
```
Corregí solo el TP de Valentina
```
El feedback aparece en la conversación, sin modificar `correcciones.md`.

**¿Qué pasa si el repo de GitHub es privado?**
El script no va a poder clonarlo. El alumno debe tener el repo público, o entregarlo
como ZIP.

**¿La skill ejecuta el código de los alumnos?**
No. Analiza el código leyéndolo, no ejecutándolo. Esto significa que no puede detectar
bugs que solo se manifiestan en runtime, pero es suficiente para los errores más
comunes en TPs de secundaria.

**¿Puedo ajustar las notas sugeridas?**
Sí, y se espera que lo hagas. Las notas son una sugerencia — el criterio final
siempre es tuyo.
