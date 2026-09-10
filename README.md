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

## Desplegar con Docker

El sitio se sirve con nginx desde una imagen que se construye sola:

```bash
docker compose up -d --build
```

Queda en <http://localhost:8080>. Para parar: `docker compose down`.

Sin compose:

```bash
docker build -t yeyo-web .
docker run -d -p 8080:80 --name yeyo-web yeyo-web
```

La imagen es de dos etapas. La primera corre `build.py` sobre `python:3.12-alpine`
y **no instala nada**: el generador usa sólo la biblioteca estándar. La segunda
copia el resultado a `nginx:1.27-alpine`. Regenerar el HTML dentro de la imagen
evita que quede desincronizado respecto a `build.py`.

`material-original/` y `docs/` quedan fuera por `.dockerignore`: son 21 MB que
el sitio no sirve. A la imagen entran unos 3,2 MB de assets.

nginx sirve con gzip, cabeceras de seguridad, `Content-Security-Policy`, caché
de un año para `/assets/` (llevan huella en la URL, así que es seguro), sin
caché para el HTML, y URLs limpias: `/trabajo` funciona igual que
`/trabajo.html`.

Las cabeceras viven en `seguridad.conf` y se incluyen en cada `location`. No es
redundancia: en nginx un `add_header` dentro de un `location` descarta todos los
heredados del bloque `server`, así que declararlas una sola vez arriba las
perdería justo donde hacen falta.

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
├── Dockerfile · docker-compose.yml · .dockerignore
├── nginx.conf · seguridad.conf
└── assets/
    ├── css/style.css     sistema visual completo
    ├── fuente/           Archivo variable, auto-hospedada (SIL OFL 1.1)
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
- **Tipografía**: `Archivo` variable, **auto-hospedada** en `assets/fuente/`.
  Los titulares usan el eje de ancho real (`font-variation-settings:'wdth' 66`)
  para reproducir Nimbus Sans Narrow sin deformar la letra; los textos van a
  `wdth 100`. Una sola familia.
  Se sirve desde el propio dominio en vez de pedirla a `fonts.googleapis.com`:
  así no se filtra la IP de quien visita y la página no depende de que un
  tercero responda. Son 176 KB en dos subconjuntos (latin y latin-ext), y el
  navegador sólo descarga el que necesita.
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

**Formularios**: los cuatro (contacto en la home, contacto en Trabajo,
contratación de conferencia y boletín) envían por AJAX a **FormSubmit**, que
reenvía al correo configurado. No hace falta crear cuenta ni servidor, así que
funciona igual en GitHub Pages que en cualquier hosting estático.

Para activarlo, dos pasos:

1. Poner el correo real en la constante `CORREO` de `build.py` y correr
   `python build.py`. El endpoint se arma solo a partir de ese correo.
2. Hacer un envío de prueba desde el sitio. FormSubmit manda **una única vez**
   un correo de activación a esa dirección: hay que abrirlo y confirmar. A
   partir de ahí todos los envíos llegan directo.

Detalles de la implementación:

- Validación nativa del navegador antes de enviar; si algo falta, no sale nada.
- Honeypot `_honey`, que FormSubmit también entiende y filtra por su cuenta.
- Botón bloqueado y con rótulo «Enviando…» mientras dura la petición.
- Confirmación o error en línea, sin sacar al visitante de la página.
- **Respaldo**: si el endpoint falla o no responde, se abre el correo del
  visitante con el mensaje ya redactado. Nunca se pierde un contacto.
- Para cambiar de proveedor (Formspree, Basin, Netlify Forms) basta con tocar
  la constante `ENDPOINT` en `build.py`.

## Accesibilidad

- Un solo `<h1>` por página, jerarquía de encabezados correcta.
- Todas las imágenes con `alt`; los SVG decorativos con `aria-hidden`.
- `:focus-visible` visible en verde sobre todos los interactivos.
- Menú móvil con `aria-expanded`, `aria-controls`, cierre con Escape y foco devuelto.
- Áreas táctiles del menú de 62 px de alto.
- `prefers-reduced-motion` desactiva todas las transiciones.
- Verificado: 0 imágenes rotas, 0 anclas muertas, 0 desbordes horizontales.
