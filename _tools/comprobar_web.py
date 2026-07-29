#!/usr/bin/env python3
"""
TrainLab · comprobar_web.py — la red de seguridad de la web de la marca.

La web es HTML estático sin sistema de build, así que su modo de romperse no
es "no compila": es un enlace interno roto, una imagen que ya no existe o una
página que referencia un recurso borrado. Nada de eso avisa — el visitante se
lo encuentra. Esto lo caza antes de publicar (auditoría transversal, punto 13:
de los seis repositorios, este era el ÚNICO sin integración continua, y es la
web pública de la marca).

Sin dependencias: solo la librería estándar. Sale con código 1 si algo falla.
"""
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
fallos = []

paginas = sorted(RAIZ.glob("*.html"))
if not paginas:
    print("✗ No hay ni un .html en la raíz: ¿se ha movido la web?")
    sys.exit(1)

# 1) Cada href/src local apunta a un archivo que EXISTE.
ATTR = re.compile(r'(?:href|src)="([^"#?]+)[^"]*"')
for pag in paginas:
    texto = pag.read_text(encoding="utf-8")
    for ref in ATTR.findall(texto):
        if ref.startswith(("http://", "https://", "mailto:", "tel:", "//", "data:")):
            continue
        destino = (RAIZ / ref.lstrip("/")).resolve()
        if not destino.exists():
            fallos.append(f"{pag.name}: referencia rota → {ref}")

# 2) Lo mínimo que toda página pública debe llevar.
for pag in paginas:
    if pag.name == "404.html":
        continue
    texto = pag.read_text(encoding="utf-8")
    if '<html lang="es"' not in texto:
        fallos.append(f'{pag.name}: falta <html lang="es"> (el lector de pantalla leería español con fonética inglesa)')
    if "<title>" not in texto:
        fallos.append(f"{pag.name}: no tiene <title>")

# 3) El sitemap no promete páginas que no existen.
from urllib.parse import urlparse
sitemap = RAIZ / "sitemap.xml"
if sitemap.exists():
    for loc in re.findall(r"<loc>([^<]+)</loc>", sitemap.read_text(encoding="utf-8")):
        ruta = urlparse(loc.strip()).path.strip("/")   # "" = la portada
        nombre = ruta or "index.html"
        if not (RAIZ / nombre).exists():
            fallos.append(f"sitemap.xml: promete {loc} y {nombre} no existe")

if fallos:
    print(f"✗ {len(fallos)} problema(s):")
    for f in fallos:
        print(f"  · {f}")
    sys.exit(1)

print(f"✓ Web en orden: {len(paginas)} páginas, todos los enlaces internos existen, lang y title presentes, sitemap honesto.")
