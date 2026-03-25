#!/usr/bin/env python3
"""
preparar_entregas.py
--------------------
Normaliza las entregas del campus virtual a una carpeta alumnos/ lista para corregir.

Formatos soportados:
  - Francisco.zip          → proyecto directo         → descomprimir
  - Valentina.zip          → contiene un .txt con URL → descomprimir → clonar
  - Matias.txt             → URL de GitHub directa    → clonar
  - Sofia.zip              → proyecto + txt zipeado   → descomprimir → clonar

Uso:
  python preparar_entregas.py --entregas ./entregas --salida ./alumnos
  python preparar_entregas.py  (usa ./entregas y ./alumnos por defecto)
"""

import os
import re
import sys
import shutil
import zipfile
import argparse
import subprocess
import tempfile
from pathlib import Path


# ── Helpers ──────────────────────────────────────────────────────────────────

GITHUB_PATTERN = re.compile(
    r"https?://(?:www\.)?github\.com/[\w\-]+/[\w\-\.]+(?:\.git)?",
    re.IGNORECASE,
)


def encontrar_url_github(texto: str) -> str | None:
    """Extrae la primera URL de GitHub que encuentre en un texto."""
    match = GITHUB_PATTERN.search(texto)
    if match:
        url = match.group(0)
        if not url.endswith(".git"):
            url += ".git"
        return url
    return None


def leer_txt(path: Path) -> str:
    """Lee un archivo .txt con distintas encodings."""
    for enc in ("utf-8", "latin-1", "utf-8-sig"):
        try:
            return path.read_text(encoding=enc).strip()
        except UnicodeDecodeError:
            continue
    return ""


def clonar_repo(url: str, destino: Path) -> bool:
    """Clona un repo de GitHub. Devuelve True si tuvo éxito."""
    print(f"  → Clonando {url} ...")
    result = subprocess.run(
        ["git", "clone", "--depth=1", url, str(destino)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"  ✗ Error al clonar: {result.stderr.strip()}")
        return False
    return True


def nombre_alumno(archivo: Path) -> str:
    """Extrae el nombre del alumno del nombre del archivo (sin extensión)."""
    return archivo.stem


# ── Procesadores por tipo ─────────────────────────────────────────────────────

def procesar_txt(archivo: Path, destino: Path) -> str:
    """
    .txt con URL de GitHub → clonar directamente.
    Devuelve estado: 'clonado' | 'sin_url' | 'error'
    """
    contenido = leer_txt(archivo)
    url = encontrar_url_github(contenido)

    if not url:
        print(f"  ✗ No se encontró una URL de GitHub válida en {archivo.name}")
        # Guardamos el .txt igual para que el corrector lo vea
        destino.mkdir(parents=True, exist_ok=True)
        shutil.copy2(archivo, destino / archivo.name)
        return "sin_url"

    if clonar_repo(url, destino):
        return "clonado"
    return "error"


def procesar_zip(archivo: Path, destino: Path) -> str:
    """
    ZIP → descomprimir → buscar si hay .txt con URL adentro.
    Si hay URL, clonar y descartar el ZIP descomprimido.
    Devuelve estado: 'descomprimido' | 'clonado_desde_zip' | 'error'
    """
    try:
        with zipfile.ZipFile(archivo, "r") as zf:
            # Extraer a carpeta temporal primero
            with tempfile.TemporaryDirectory() as tmp:
                zf.extractall(tmp)
                tmp_path = Path(tmp)

                # Buscar .txt con URL de GitHub (en cualquier nivel)
                txts = list(tmp_path.rglob("*.txt"))
                url_encontrada = None

                for txt in txts:
                    contenido = leer_txt(txt)
                    url = encontrar_url_github(contenido)
                    if url:
                        url_encontrada = url
                        break

                if url_encontrada:
                    print(f"  → ZIP contiene .txt con URL: {url_encontrada}")
                    if clonar_repo(url_encontrada, destino):
                        return "clonado_desde_zip"
                    return "error"
                else:
                    # Es un proyecto normal, mover el contenido descomprimido
                    # Si hay una sola carpeta raíz adentro, aplanar un nivel
                    hijos = [p for p in tmp_path.iterdir()]
                    if len(hijos) == 1 and hijos[0].is_dir():
                        shutil.copytree(hijos[0], destino)
                    else:
                        shutil.copytree(tmp_path, destino)
                    return "descomprimido"

    except zipfile.BadZipFile:
        print(f"  ✗ {archivo.name} no es un ZIP válido")
        return "error"


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Prepara entregas para corrección")
    parser.add_argument(
        "--entregas",
        default="./entregas",
        help="Carpeta con los archivos del campus (default: ./entregas)",
    )
    parser.add_argument(
        "--salida",
        default="./alumnos",
        help="Carpeta destino normalizada (default: ./alumnos)",
    )
    args = parser.parse_args()

    carpeta_entregas = Path(args.entregas)
    carpeta_salida = Path(args.salida)

    if not carpeta_entregas.exists():
        print(f"✗ No existe la carpeta de entregas: {carpeta_entregas}")
        sys.exit(1)

    carpeta_salida.mkdir(parents=True, exist_ok=True)

    # Recolectar archivos a procesar (.zip y .txt en el nivel raíz)
    archivos = sorted(
        [
            f
            for f in carpeta_entregas.iterdir()
            if f.is_file() and f.suffix.lower() in (".zip", ".txt")
        ]
    )

    if not archivos:
        print(f"✗ No se encontraron archivos .zip o .txt en {carpeta_entregas}")
        sys.exit(1)

    print(f"\n📂 Procesando {len(archivos)} entregas en '{carpeta_entregas}'\n")

    resumen = []

    for archivo in archivos:
        alumno = nombre_alumno(archivo)
        destino = carpeta_salida / alumno

        if destino.exists():
            print(f"⚠  {alumno}: ya existe en alumnos/, saltando.")
            resumen.append((alumno, "ya existía"))
            continue

        print(f"👤 {alumno} ({archivo.suffix})")

        if archivo.suffix.lower() == ".txt":
            estado = procesar_txt(archivo, destino)
        else:
            estado = procesar_zip(archivo, destino)

        iconos = {
            "clonado": "✓ repo clonado",
            "clonado_desde_zip": "✓ repo clonado (desde ZIP)",
            "descomprimido": "✓ ZIP descomprimido",
            "sin_url": "⚠ .txt sin URL válida",
            "error": "✗ error",
            "ya existía": "– saltado",
        }
        print(f"  {iconos.get(estado, estado)}\n")
        resumen.append((alumno, estado))

    # Resumen final
    print("─" * 40)
    print(f"{'Alumno':<25} {'Estado'}")
    print("─" * 40)
    for alumno, estado in resumen:
        print(f"  {alumno:<23} {estado}")
    print("─" * 40)

    errores = [a for a, e in resumen if e in ("error", "sin_url")]
    if errores:
        print(f"\n⚠  Revisá manualmente: {', '.join(errores)}")
    else:
        print(f"\n✓ Listo. Carpeta alumnos/ lista en '{carpeta_salida}'")


if __name__ == "__main__":
    main()
