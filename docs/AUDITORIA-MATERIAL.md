# AUDITORÍA COMPLETA DEL MATERIAL — YEYO VERA

Fecha de análisis: 6 sep 2026
Fuentes: manual de marca, blueprint (16 pp), 13 archivos de logo/elementos, 10 fotos, boceto web online.

---

## A. SISTEMA DE MARCA (Manual de Marca — autoridad final)

### Color: exactamente 3, sin excepciones

| Rol | HEX | RGB | CMYK | Nota |
|---|---|---|---|---|
| Verde Yeyo (maestro) | **#95D200** | 149/210/0 | 29/0/100/18 | Pantone 375 C aprox. |
| Negro | #000000 | 0/0/0 | K100 | estructura |
| Blanco | #FFFFFF | 255/255/255 | 0/0/0/0 | estructura |

Regla textual: *"No crear tonos alternativos."* Verificado en píxeles del logo: el verde es **#95D200 exacto**.

Implicación web: no hay grises de marca. Los grises de UI (#111, #555, #d9d9d9) son decisión de implementación, no de marca — usar los mínimos posibles.

### Tipografía

- Titulares: **Nimbus Sans Narrow Bold** — altas, tracking compacto.
- Textos: **Nimbus Sans Regular**.
- Nimbus Sans = clon URW de Helvetica. Es **libre** (URW base35, AFPL/GPL+exception): `github.com/ArtifexSoftware/urw-base35-fonts` → auto-hospedar en WOFF2 = 100% fiel a marca.
- Plan B (Google Fonts): `Archivo Narrow` (títulos) + `Archivo` (texto). Nunca Arial.
- ⚠️ El boceto online usa **Arial pelado**. Es su mayor debilidad visual.

### Logotipo: 3 versiones autorizadas

- **A / Positiva**: símbolo verde + "YEYO VERA" negro (fondo claro)
- **B / Negativa**: símbolo verde + "YEYO VERA" blanco (fondo oscuro)
- **C / Símbolo solo**: el asterisco de 6 brazos
- Tamaño mínimo: firma **140 px** · símbolo **32 px**
- Área de respeto: **1X** alrededor (X = grosor de un brazo)

### Símbolo: "NODO EXPANSIVO"

Asterisco de 6 brazos. Funciona como **firma, acento, máscara, transición o trama ampliada**. Nunca rotar. Nunca deformar.

### Lenguaje de formas

**Bloques rectos · mucho aire · sin sombras.**

⚠️ Los mockups del blueprint dibujan tarjetas con esquinas redondeadas. **El manual manda: esquinas rectas, radius 0, sin box-shadow.** El boceto online acertó en esto.

### Prohibido

× Rotar · × Efectos · × Bajo contraste

---

## B. BLUEPRINT WEB (16 páginas — el brief real del proyecto)

### 01 · Decisión estratégica

> "La web no debe parecer un CV. Debe mostrar qué puedes mover en los demás."

- **Riesgo declarado:** presentar cargos/estudios/premios antes de explicar el valor.
- **Posicionamiento paraguas:** Marcas + equipos + personas / Estrategia + creatividad + propósito.

### 02 · Benchmark

Simon Sinek · Seth Godin · Ann Handley · Jay Shetty · Vilma Núñez · Oso Trava.

> Aprendizaje: **la autoridad aparece DESPUÉS de la propuesta de valor.**

### 03 · Concepto rector

**LA VERDAD QUE MUEVE.**

- H1: *TODO LO QUE CRECE DE VERDAD EMPIEZA CON UNA VERDAD.*
- Promesa: *Acompaño a marcas, equipos y personas a convertir propósito en estrategia, creatividad y acción.*
- Firma: Country Manager Bolivia de Atomik Pro · Consultor creativo estratégico · Speaker y educador.
- Nota: *"El cargo aporta actualidad, pero no reemplaza el posicionamiento personal."*

### 04 · Arquitectura — 5 ítems de menú, SIN "Inicio"

`TRABAJO · CONFERENCIAS · IDEAS · SOY YEYO · CONVERSEMOS` (el logo es el acceso al inicio)

### 05-09 · Homepage (5 bloques)

1. Hero + **selector de necesidades** (Una marca / Un equipo / Una audiencia)
2. **Método V.E.R.A.** (Verdad · Enfoque · Ruta · Activación) + prueba (14+ / 90+ / 200+ / 9+) + **muro de 10-12 logos monocromos**
3. **Trabajo**: 3 videocasos con estructura `Desafío → Verdad → Construcción → Cambio`
4. Conferencias (3 charlas) + Ideas (4 categorías, newsletter *"Una idea con propósito"*, podcast **ILUMINA**)
5. Sobre Yeyo (incluye su fe en Jesús como raíz del propósito) + formulario de contacto

### 10-13 · Páginas internas — 4 páginas que el boceto NO tiene

- **TRABAJO / CONSULTORÍA** — flujo: Problema → Método V.E.R.A. → Entregable → Casos → Conversemos. *Sin precios. No convertirlo en dossier técnico.*
- **CONFERENCIAS** — showreel 60-90s, 3 charlas + promesa, audiencias, formatos (keynote/taller/conversación), marcas y testimonios, **speaker kit descargable**, y formulario de contratación de 8 campos: `Fecha · Ciudad/virtual · Organización · Tipo de audiencia · Asistentes · Formato · Presupuesto · Contacto`
- **IDEAS** — categorías (marketing, creatividad, propósito, crecimiento, educación) × formatos (artículos, videos, videocasos, podcast ILUMINA, recursos). *"Una idea destacada por formato. Sin grillas interminables."*
- **SOY YEYO** — historia en **capítulos**, no CV cronológico: `CREAR · LIDERAR · ENSEÑAR · EMPRENDER · VIVIR CON PROPÓSITO` + bio descargable.

### 14 · Dirección creativa

- Fotografía: **momentos reales en blanco y negro** — trabajo, aula, escenario, conversación.
- Forma: el símbolo YV como nodo, firma, **máscara**, **transición** y recurso de expansión.
- Movimiento: *"Breve y funcional. Revelar, conectar y dirigir; nunca decorar sin propósito."*
- Sensación: **editorial + estratega + speaker.**

### 15 · Tono — reglas de microcopy

| ✅ SÍ DECIR | ❌ EVITAR |
|---|---|
| "He tenido la oportunidad de trabajar con..." | "Soy uno de los mejores..." |
| "Esto es lo que he aprendido..." | "La fórmula definitiva..." |
| "Conversemos sobre el desafío." | "Contrátame ahora." |
| "Ideas para llevarse." | Un muro de cargos y premios. |

### 16 · Handoff — checklist técnico exigido

- **CMS**: casos, ideas, charlas, testimonios y logos administrables.
- **Experiencia**: mobile first · subtítulos en todos los videos · animaciones breves + reduce-motion · carga rápida.
- **Medición**: eventos `contacto / speaking / caso / suscripción` · SEO por intención · formularios con confirmación + anti-spam · enlaces a LinkedIn, Instagram, YouTube e ILUMINA.

**⚠️ VALIDAR ANTES DE PUBLICAR (lo dice el propio blueprint):**

1. Unificar la cifra de empresas — **el material dice 30+ en un lado y 90+ en otro**.
2. Revisar los años de experiencia frente al inicio laboral registrado en **2009** (2009→2026 = 17 años, no 14+).
3. Definir **dominio y correo profesional**.
4. Confirmar títulos de charlas, testimonios y casos autorizados.
5. Usar Atomik Pro como cargo actual; **evitar co-branding sin autorización**.

---

## C. INVENTARIO DE ASSETS

### Logos (todos PNG raster — NO hay SVG)

| Archivo | Tamaño | Contenido | Uso web |
|---|---|---|---|
| `LOGO YV.png` | 2000² (recorte útil 1926×685) | Positiva, transparente | ★ principal fondo claro |
| `LOGO YV.jpg` | 2000² | Positiva sobre blanco | fallback / redes |
| `LOGO YV 2 cont1.png` | 2000² | Texto blanco + marco negro | fondo oscuro |
| `LOGO YV 2 cont2.png` | 2000² | Texto negro + marco negro | fondo claro con marco |
| `LOGO YV 2 cont3.png` | 2000² | Texto blanco + marco blanco | sobre foto |
| `LOGO YV 2 contenedor.png` | 2000² | Bloque negro + texto blanco | ★ badge / base de favicon |

**FALTA: el símbolo suelto como archivo.** Hay que extraerlo (está limpio en el PSD, x 1609-1787 / y 241-430) y **vectorizarlo a SVG**.

### Elementos gráficos

- `LINEA ICONOCIA DE YEYO VERA.psd` (1920×1080) — **el asset más valioso e infrautilizado**: un sistema de **11 iconos geométricos** con el mismo ADN que el símbolo, mapeados a `MARKETING · CLASSES · COACHING · WORKSHOPS · TRIPS · CONTENT · GOSPEL · MUSIC · GYM · FOOD` + el símbolo maestro. Todos son formas planas de 2 colores → **vectorizables a SVG sin pérdida**. Grid confirmado: 4 filas × 3 columnas, separables por bounding box.
- `titulos.png` (1440×2560) — plantilla de banda: bloque negro con el símbolo sangrando por el borde izquierdo. **Excelente motivo reutilizable para encabezados de sección web.**
- `Wallpaper.jpg`, `instagram.jpg` (1440×2560) — fondos verticales negros con símbolo verde.
- `foto portada FB.jpg` (851×315) — cover Facebook.

### Avatar 3D (3 PNG, ~9 poses) — ⚠️ DECISIÓN PENDIENTE

Personaje 3D estilo Pixar de Yeyo generado con Gemini: señalando, saludando, encogiéndose de hombros, arrodillado, pulgar arriba, etc.

**Choca frontalmente con la dirección "editorial, blanco y negro, sin exhibicionismo".** No cabe en la home. Sí podría vivir en: estados vacíos, 404, onboarding del newsletter, o material de redes/aula. Requiere decisión explícita.

### Fotografía: 4 reales + 6 generadas por IA

**REALES** (Nikon Z8 · Viltrox AF 50mm f/1.4 · 17 ago 2026 · f/4 · ISO 400 · 3333×5000):
`0J0_1598 · 0J0_1602 · 0J0_1608 · 0J0_1621`

Las 4 son de la **misma sesión, mismo setup, con 75 segundos de diferencia entre la primera y la última**: aro de luz blanco tras él, negro sobre negro, plano entero vertical.

**GENERADAS CON IA (Gemini)** — 6 archivos:

- `2h11zx`, `ykloy7`, `dtyc44`, `qc21hd` → variantes del mismo setup de aro de luz
- `6e6byj` → traje sobre fondo beige · `hapqqn` → traje sobre fondo oscuro (retrato ejecutivo)
- ⚠️ `qc21hd` tiene texto quemado en la imagen: *"PREMIUM MAGAZINE COVER PORTRAIT / EDITORIAL FINISH"* → **inutilizable sin recortar**.

---

## D. BRECHAS CRÍTICAS (lo que hoy impide que quede profesional)

**1. Fotografía — el problema #1.** Hay 4 fotos reales de UN solo setup. El blueprint pide "trabajo, aula, escenario y conversación". **No existe ni una foto de escenario, aula, trabajo o conversación.** Una web de speaker sin fotos de escenario carece de su prueba principal.

**2. Coherencia IA vs. concepto.** El concepto es *"La verdad que mueve"*. Publicar retratos de sí mismo generados por IA en esa web es un riesgo de coherencia que un ojo entrenado detecta. Recomendación: usar **solo las 4 reales**, tratadas a B/N, y programar una sesión que cubra escenario + aula + trabajo.

**3. Cero video.** El blueprint exige 3 videocasos (60-90s, subtítulos, portada propia) + showreel de conferencias. No hay ninguno.

**4. Cero prueba social.** Faltan los 10-12 logos de clientes monocromos y todos los testimonios.

**5. Cero contenido de casos.** No hay ni un caso escrito con la estructura Desafío/Verdad/Construcción/Cambio.

**6. Cero copy de páginas internas.** Solo existe copy de homepage.

**7. Sin vectores.** Todo raster. Un sitio profesional necesita logo y símbolo en SVG (nítidos en retina, animables, ligeros).

**8. Contradicción numérica sin resolver.** 30+ vs 90+ empresas; 14+ años vs inicio en 2009.

**9. Sin dominio ni correo** definidos.

**10. Peso de imágenes.** Los originales pesan ~1,1 MB cada uno a 3333×5000. Requiere pipeline: AVIF/WebP + `srcset` responsive.

---

## E. QUÉ APORTA CADA FUENTE

- **Manual de marca** → la ley visual (color, tipo, logo, formas). Innegociable.
- **Blueprint** → la arquitectura, el copy, el tono y el checklist de handoff. Es el brief.
- **Boceto online** → una maqueta HTML de **solo la homepage**, en Arial, sin iconos, sin videocasos, sin logos de clientes, sin newsletter y sin las 4 páginas internas. Sirve como referencia de ritmo y layout, no como base final.
- **Assets** → logo sólido, sistema de iconos excelente (sin usar), fotografía insuficiente.

---

## F. DECISIONES CERRADAS (6 sep 2026)

### (a) Fotografía: se usan las 10
Todas pasan por el mismo tratamiento B/N + alto contraste, para que lean como un solo sistema.
Reparto por rol:
- **4 reales** (0J0_1598 / 1602 / 1608 / 1621) en los puntos de identidad: hero, Soy Yeyo, bio, OG image.
- **IA de aro de luz** (2h11zx, ykloy7, dtyc44) como apoyo en secciones internas.
- **IA de traje** (6e6byj, hapqqn) para el registro ejecutivo: speaker kit, consultoría.
- **qc21hd**: recortar el 8% inferior para eliminar el texto quemado "PREMIUM MAGAZINE COVER PORTRAIT / EDITORIAL FINISH".

### (b) Avatar 3D: existe, pero fuera de la home
Los 3 archivos estan en LOGO Y ELEMENTOS (hmer06, i7uycq, tw9co1), ~9 poses.
Se reservan para superficies donde no compiten con la direccion editorial:
404, estados vacios, confirmacion de formulario, y material de redes/aula.
Nunca en home, consultoria ni conferencias.

### (c) Cifras: pendientes, se usan las del blueprint
Se publica 14+ / 90+ / 200+ / 9+ (las que aparecen en el mockup de homepage).
Quedan marcadas como PENDIENTE DE VALIDAR hasta que llegue el dato definitivo:
- 30+ vs 90+ empresas
- 14+ anos vs inicio laboral 2009 (serian 17)
- dominio y correo profesional
- titulos de charlas, testimonios y casos autorizados

### Pendiente de material (no bloquea el diseno, bloquea el lanzamiento)
Fotos de escenario/aula/trabajo · 3 videocasos · showreel · logos de clientes ·
testimonios · copy de las 4 paginas internas.
Se construye con placeholders estructurados para que entren sin rehacer nada.
