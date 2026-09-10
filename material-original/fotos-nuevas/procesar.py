#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Procesa las fotos que mandó el cliente y las deja en web/assets/img/foto/.

Uso:   python procesar.py

Entradas esperadas en esta carpeta (cualquier extensión de imagen):
  1-header      recorte con transparencia, B/N   -> hero de la home
  2-home        color naranja/turquesa sobre negro -> segunda foto de la home
  3-soy-yeyo    B/N de perfil sobre negro        -> página Soy Yeyo
"""
import glob
import os
import sys

import numpy as np
from PIL import Image, ImageEnhance, ImageOps

AQUI = os.path.dirname(os.path.abspath(__file__))
DESTINO = os.path.join(AQUI, "..", "web", "assets", "img", "foto")


def buscar(base):
    for p in sorted(glob.glob(os.path.join(AQUI, base + ".*"))):
        if p.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
            return p
    return None


def blanco_y_negro(im, contraste=1.16, punto_negro=0.03):
    """El mismo tratamiento editorial que usan las otras fotos del sitio."""
    a = np.asarray(ImageOps.grayscale(im)).astype(np.float32) / 255.0
    a = np.clip((a - punto_negro) / (1 - punto_negro - 0.03), 0, 1) ** 1.06
    a = np.clip(0.5 + (a - 0.5) * contraste, 0, 1)
    out = Image.fromarray((a * 255).astype(np.uint8), "L").convert("RGB")
    return ImageEnhance.Sharpness(out).enhance(1.15)


def recortar(im, ratio, sesgo_y=0.16, sesgo_x=0.5):
    w, h = im.size
    tw, th = (w, int(w / ratio)) if w / h < ratio else (int(h * ratio), h)
    izq = int((w - tw) * sesgo_x)
    arr = int((h - th) * sesgo_y)
    return im.crop((izq, arr, izq + tw, arr + th))


def exportar(im, nombre, anchos, ratio=None, alfa=False, calidad=80):
    c = recortar(im, ratio) if ratio else im
    # nunca escalar por encima del original: ablanda la imagen y pesa de más
    utiles = sorted({w for w in anchos if w < c.size[0]} | {c.size[0]})
    if utiles != sorted(anchos):
        print(f"    (origen {c.size[0]}px: se exportan {utiles} en vez de {list(anchos)})")
    for wd in utiles:
        alto = round(wd * c.size[1] / c.size[0])
        r = c.resize((wd, alto), Image.LANCZOS)
        ruta = os.path.join(DESTINO, f"{nombre}-v-{wd}.webp")
        if alfa:
            r.save(ruta, "WEBP", quality=88, method=6, exact=True)
        else:
            r.convert("RGB").save(ruta, "WEBP", quality=calidad, method=6)
    print(f"    -> {nombre}-v-{{{','.join(map(str, utiles))}}}.webp  desde {c.size[0]}x{c.size[1]}")


def jpg_social(im, nombre, w=1200):
    base = im.convert("RGB")
    base.resize((w, round(w * base.size[1] / base.size[0])), Image.LANCZOS).save(
        os.path.join(DESTINO, f"{nombre}.jpg"), "JPEG",
        quality=82, optimize=True, progressive=True)


def main():
    os.makedirs(DESTINO, exist_ok=True)
    faltan = []

    # ---- 1. hero: recorte con transparencia, se conserva el alfa ----------
    f = buscar("1-header")
    if f:
        im = Image.open(f)
        print("1-header <-", os.path.basename(f), im.size, im.mode)
        if im.mode != "RGBA":
            print("    AVISO: no trae canal alfa, se usará tal cual sobre el fondo negro")
            im = im.convert("RGBA")
        # recorte ajustado al sujeto, con un respiro del 2%
        al = np.asarray(im.split()[3])
        ys, xs = np.where(al > 8)
        pad = int(0.02 * max(xs.max() - xs.min(), ys.max() - ys.min()))
        caja = (max(0, xs.min() - pad), max(0, ys.min() - pad),
                min(im.size[0], xs.max() + 1 + pad), min(im.size[1], ys.max() + 1 + pad))
        rec = im.crop(caja)
        # B/N conservando el alfa
        alfa = rec.split()[3]
        out = blanco_y_negro(rec.convert("RGB")).convert("RGBA")
        out.putalpha(alfa)
        exportar(out, "hero-yeyo", (640, 900, 1200), alfa=True)
        print(f"    sujeto {rec.size[0]}x{rec.size[1]}, ratio {rec.size[0]/rec.size[1]:.2f}")
    else:
        faltan.append("1-header")

    # ---- 2. segunda foto de la home: se respeta el color ------------------
    f = buscar("2-home")
    if f:
        im = Image.open(f).convert("RGB")
        print("2-home <-", os.path.basename(f), im.size)
        exportar(im, "home-color", (640, 1000, 1400), ratio=3 / 4, calidad=82)
        jpg_social(im, "home-color")
    else:
        faltan.append("2-home")

    # ---- 3. Soy Yeyo: ya viene en B/N sobre negro -------------------------
    f = buscar("3-soy-yeyo")
    if f:
        im = Image.open(f).convert("RGB")
        print("3-soy-yeyo <-", os.path.basename(f), im.size)
        exportar(blanco_y_negro(im, contraste=1.08), "soy-yeyo", (640, 1000, 1400), ratio=2 / 3)
        jpg_social(im, "soy-yeyo")
    else:
        faltan.append("3-soy-yeyo")

    print()
    if faltan:
        print("Faltan:", ", ".join(faltan))
        return 1
    print("Listo. Ahora:  cd ../web && python build.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
