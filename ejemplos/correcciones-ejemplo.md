# Correcciones — TP3: Calculadora interactiva

## Francisco: 9

El TP está muy bien hecho. La calculadora funciona correctamente para todas las
operaciones y el código está organizado en funciones claras. Algunas correcciones
menores para mejorar la calidad del código.

**Correcciones:**
- Mejorá la indentación en `script.js` (líneas 12–28) para que el código sea más
  fácil de leer. Los bloques `if/else` dentro de la función `operar()` no están
  alineados consistentemente.
- En `script.js` línea 8, usás `var resultado` — cambialo a `let` ya que el valor
  se reasigna dentro del loop.
- El `div` de la línea 15 en `index.html` no está cerrado correctamente.

**Puntos destacados:**
- Las cuatro operaciones funcionan perfecto, incluyendo la división por cero (que
  muestra "Error" en el display — muy buen detalle).

---

## Valentina: 7

El TP está bien encaminado. La interfaz se ve prolija y las operaciones básicas
funcionan. Hay algunas funcionalidades que necesitan revisión.

**Correcciones:**
- El botón "C" (Clear) no hace nada al clickearlo. La función `limpiar()` está
  definida en `script.js` pero no está conectada al evento `onclick` del botón
  en el HTML. Revisá la línea 22 de `index.html`.
- En `style.css`, los botones no tienen estilos para el estado `:hover`. Agregale
  un cambio de color o sombra para que se vea que son clickeables.
- Usás `var` en varias variables de `script.js` (líneas 3, 7 y 11). Reemplazalas
  por `let` o `const` según si el valor cambia o no.

---

## Matías: 4

El TP tiene la estructura básica pero la mayoría de las funcionalidades no están
implementadas o no funcionan. Hay que repasar la lógica de JavaScript.

**Correcciones:**
- La calculadora muestra el HTML pero no realiza ninguna operación. Las funciones
  `sumar()`, `restar()`, etc. están vacías en `script.js`.
- El display no se actualiza cuando se clickean los números. Falta conectar los
  eventos de los botones con la lógica de JavaScript.
- En `index.html` hay varios errores de sintaxis: los tags `<button>` no tienen
  el atributo `onclick`, y el `<div id="display">` no está cerrado (línea 18).
- Hay 4 `console.log()` de debug en `script.js` que no se limpiaron.

---

## Resumen de notas

| Alumno   | Nota sugerida |
|----------|---------------|
| Francisco | 9            |
| Valentina | 7            |
| Matías    | 4            |

**Promedio de la clase:** 6.7
