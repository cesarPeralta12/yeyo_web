# yeyo_web

Sitio web de **Sergio "Yeyo" Vera** — consultor creativo estratégico, speaker y educador.
Concepto: *La verdad que mueve.*

![Verde Yeyo](https://img.shields.io/badge/%2395D200-verde%20maestro-95D200?style=flat-square&labelColor=000000)
![Sin dependencias](https://img.shields.io/badge/dependencias-0-000000?style=flat-square)
![Primera carga](https://img.shields.io/badge/primera%20carga-108%20KB-000000?style=flat-square)

HTML, CSS y JavaScript planos. Sin frameworks, sin npm, sin paso de compilación
más allá de un script de Python que genera las páginas desde una sola fuente de contenido.

Documentación del proyecto en [`docs/`](docs/):
[auditoría del material](docs/AUDITORIA-MATERIAL.md) ·
[análisis del boceto de referencia](docs/REFERENCIA-BOCETO.md)

---

Sitio estático de 5 páginas + 404. Sin frameworks, sin dependencias, sin build de node.
Primera carga de la home: **108 KB**. Peso total del sitio: **2,4 MB**.

## Cómo verlo

```bash
python -m http.server 8000
```

Y abrir <http://localhost:8000>.

## Cómo editarlo

Todo el contenido vive en **`build.py`**. Las páginas `.html` son generadas:
no las edites a mano, se sobrescriben.

```bash
python build.py
```

Dentro de `build.py`:

| Qué cambiar | Dónde |
|---|---|
| Dominio y correo | constantes `SITIO` y `CORREO`, arriba del todo |
| Redes sociales | diccionario `REDES` |
| Menú | lista `NAV` |
| Rutas del hero | lista `RUTAS` |
| Método V.E.R.A. | lista `VERA` |
| Cifras | lista `CIFRAS` |
| Servicios | lista `SERVICIOS` |
| Charlas | lista `CHARLAS` |
| Capítulos de Soy Yeyo | lista `CAPITULOS` |
| Artículos | lista `NOTAS` |
| Cabecera y pie | funciones `cabecera()` y `pie()` |

## Estructura

```
web/
├── build.py              generador — única fuente de verdad del contenido
├── index.html            home (9 secciones)
├── trabajo.html          consultoría · método · talleres · casos
├── conferencias.html     showreel · 3 charlas · formatos · contratación
├── ideas.html            destacado · filtros por categoría · boletín
├── soy-yeyo.html         historia en capítulos · recorrido · material
├── 404.html
├── robots.txt · sitemap.xml
└── assets/
    ├── css/style.css     sistema visual completo
    ├── js/main.js        menú, revelado, filtros, formularios
    └── img/
        ├── logo.svg      lockup vectorizado (símbolo verde + texto currentColor)
        ├── simbolo.svg   símbolo solo, 308 bytes, 4 chevrones simétricos
        ├── favicon.svg
        ├── avatar.webp   avatar 3D, usado solo en el 404
        ├── icono/        12 SVG del sistema de iconos YV
        └── foto/         10 fotos en B/N · 3 anchos WebP + JPG para OG
```

## Decisiones de marca aplicadas

- **Color**: solo #95D200, #000 y #FFF, como manda el manual. Los grises son de
  interfaz, declarados como variables aparte.
- **Tipografía**: `Archivo` variable de Google Fonts. Los titulares usan el eje de
  ancho real (`font-variation-settings:'wdth' 66`) para reproducir Nimbus Sans
  Narrow sin deformar la letra. Los textos van a `wdth 100`. Una sola familia,
  una sola petición.
- **Formas**: `border-radius: 0` y `box-shadow` en ninguna parte, según
  «bloques rectos · mucho aire · sin sombras».
- **Símbolo**: reconstruido como 4 chevrones rotados 90°, geométricamente exacto
  (IoU 0,974 contra el original) y en 308 bytes. Nunca rotado.
- **Fotografía**: las 10 fotos con el mismo tratamiento B/N para que lean como un
  sistema. A `qc21hd` se le recortó el 8% inferior donde tenía texto quemado.
- **Movimiento**: un solo gesto (revelar al entrar en pantalla), con
  `prefers-reduced-motion` respetado.

## Lo que falta antes de publicar

**Datos por confirmar** (marcados como PENDIENTE en `build.py`):

1. **Dominio y correo profesional** — hoy dice `yeyovera.com` / `hola@yeyovera.com`.
2. **Cifra de empresas** — el material dice 30+ en un sitio y 90+ en otro. Se publicó 90+.
3. **Años de experiencia** — se publicó 14+, pero con inicio laboral en 2009 serían 17.
4. **URLs reales de LinkedIn, Instagram, YouTube e ILUMINA** — hoy apuntan a la raíz.
5. Títulos de charlas, testimonios y casos autorizados.

**Contenido que no existe todavía:**

- Fotos de escenario, aula, trabajo y conversación (hoy solo hay retrato de estudio).
- 3 videocasos de 60-90 s con subtítulos y portada propia.
- Showreel de conferencias.
- Logos de 10-12 clientes en monocromo (hoy hay celdas con marcador de posición).
- Testimonios.
- Bio descargable y fotos oficiales para el speaker kit.
- Artículos reales (hoy hay 6 titulares de ejemplo marcados «Próximamente»).

**Formularios**: los tres formularios (contacto, contratación de conferencia y
boletín) validan en el navegador, llevan honeypot anti-spam y hoy abren el correo
del usuario con el mensaje ya redactado. Cuando exista un endpoint, sustituir el
bloque marcado en `assets/js/main.js` por un `fetch()` a ese endpoint.

## Accesibilidad

- Un solo `<h1>` por página, jerarquía de encabezados correcta.
- Todas las imágenes con `alt`; los SVG decorativos con `aria-hidden`.
- `:focus-visible` visible en verde sobre todos los interactivos.
- Menú móvil con `aria-expanded`, `aria-controls`, cierre con Escape y foco devuelto.
- Áreas táctiles del menú de 62 px de alto.
- `prefers-reduced-motion` desactiva todas las transiciones.
- Verificado: 0 imágenes rotas, 0 anclas muertas, 0 desbordes horizontales.
