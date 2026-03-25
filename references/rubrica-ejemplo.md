# Rúbrica de ejemplo — TP: Calculadora interactiva

> Copiá este archivo, renombralo con el nombre del TP (ej: `rubrica-tp3.md`)
> y modificalo según los criterios de tu trabajo práctico.

---

## Descripción del TP

Crear una calculadora web que permita realizar las 4 operaciones básicas.
Debe tener una interfaz con botones y mostrar el resultado en pantalla.

## Criterios de evaluación

| # | Criterio | Peso | Descripción |
|---|----------|------|-------------|
| 1 | Estructura HTML correcta | 15% | El HTML tiene estructura semántica (header, main, etc.), tags cerrados, indentación |
| 2 | Estilos CSS | 10% | La calculadora se ve ordenada, botones estilizados, responsive básico |
| 3 | Operaciones funcionan | 30% | Suma, resta, multiplicación y división funcionan correctamente |
| 4 | Manejo del display | 15% | El display muestra los números ingresados y el resultado |
| 5 | Botón "C" / Clear | 10% | El botón limpiar resetea el estado de la calculadora |
| 6 | Calidad del código JS | 20% | Usa let/const, nombres de variables descriptivos, funciones bien organizadas |

## Penalizaciones automáticas

- Uso de `var` en lugar de `let`/`const`: -0.5 puntos por variable
- `console.log` de debug sin limpiar: -0.3 puntos
- Funcionalidad completamente ausente: -1.5 puntos por funcionalidad

## Ejemplos de feedback esperado

**Bien hecho:**
> "La calculadora funciona correctamente para todas las operaciones. El código está
> bien organizado y usa let/const consistentemente."

**Error típico:**
> "En `script.js` línea 34, usás `var resultado` — cambialo a `const resultado`
> ya que el valor se asigna una sola vez."

## Nota mínima para aprobar

6 (sobre 10)

---

> **Tip para el profesor**: Podés definir los pesos como porcentajes (como arriba)
> o simplemente listar los criterios sin pesos y dejar que la IA evalúe cualitativamente.
> Ambos formatos funcionan.
