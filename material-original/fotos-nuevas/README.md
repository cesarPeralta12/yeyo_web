# Fotos nuevas (septiembre 2026)

Las tres fotos que el cliente pidió por WhatsApp, con su destino:

| Archivo | Destino | Tratamiento |
|---|---|---|
| `1-header.webp` | Hero de la home | Ya venía recortado con transparencia. Se ajusta al sujeto y se le aplica el B/N del sistema conservando el alfa. |
| `2-home.webp` | Segunda foto de la home (sección Soy Yeyo) | **Se conserva a color.** Es la única foto a color del sitio. |
| `3-soy-yeyo.webp` | Página Soy Yeyo | B/N con menos contraste, porque el original ya viene muy contrastado. |

Regenerar los derivados:

```
python procesar.py
cd ../../ && python build.py
```

## Advertencia sobre la resolución

Estos tres archivos se recuperaron del historial de la conversación, donde
pasaron por una recompresión a WebP. Resoluciones actuales:

- `1-header` 1672x941 (sujeto útil 824x924)
- `2-home` 1086x1448
- `3-soy-yeyo` 1024x1536

Sirven bien para el sitio, pero **no son los originales**. Si el cliente pasa
los archivos originales, se reemplazan aquí con el mismo nombre y se vuelve a
correr `procesar.py`: el script ya no escala por encima del original, así que
aprovechará automáticamente la resolución extra.
