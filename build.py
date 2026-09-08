#!/usr/bin/env python3
"""
Generador estatico del sitio de Yeyo Vera.

Mantiene una sola fuente de verdad para cabecera, pie y metadatos, y escribe
los .html finales. Para regenerar el sitio:   python build.py
"""
import os
import re

AQUI = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(AQUI, "assets", "img")

SITIO = "https://yeyovera.com"          # PENDIENTE: confirmar dominio
CORREO = "hola@yeyovera.com"            # PENDIENTE: confirmar correo
REDES = {
    "LinkedIn": "https://www.linkedin.com/",
    "Instagram": "https://www.instagram.com/",
    "YouTube": "https://www.youtube.com/",
    "Podcast ILUMINA": "#",
}

NAV = [
    ("Trabajo", "trabajo.html"),
    ("Conferencias", "conferencias.html"),
    ("Ideas", "ideas.html"),
    ("Soy Yeyo", "soy-yeyo.html"),
]


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

def leer(nombre):
    with open(os.path.join(IMG, nombre), encoding="utf-8") as f:
        return f.read()


LOGO = leer("logo.svg")
SIMBOLO = leer("simbolo.svg")
_ICONOS = {}


def icono(nombre, clase="", etiqueta=None):
    """Inserta un icono del sistema YV en linea."""
    if nombre not in _ICONOS:
        _ICONOS[nombre] = leer(os.path.join("icono", nombre + ".svg"))
    svg = _ICONOS[nombre]
    attrs = ' aria-hidden="true"' if etiqueta is None else f' role="img" aria-label="{etiqueta}"'
    if clase:
        attrs += f' class="{clase}"'
    return svg.replace("<svg", "<svg" + attrs, 1)


def marca(clase="", etiqueta="Yeyo Vera"):
    return LOGO.replace("<svg", f'<svg class="{clase}"', 1) if clase else LOGO


def simbolo(clase=""):
    s = SIMBOLO.replace("<svg", '<svg aria-hidden="true"', 1)
    return s.replace("<svg", f'<svg class="{clase}"', 1) if clase else s


FLECHA = '<svg class="flecha" width="11" height="11" viewBox="0 0 11 11" fill="none" aria-hidden="true"><path d="M1 10L10 1M10 1H2.5M10 1v7.5" stroke="currentColor" stroke-width="1.6"/></svg>'
PLAY = '<svg width="17" height="19" viewBox="0 0 17 19" fill="currentColor" aria-hidden="true"><path d="M0 0l17 9.5L0 19z"/></svg>'


def enlace(texto, href, clase="enlace"):
    return f'<a class="{clase}" href="{href}"><span>{texto}</span>{FLECHA}</a>'


def foto(nombre, alt, sizes, clase="", pos=None, eager=False):
    """<img> con srcset webp y respaldo jpg."""
    src = f"assets/img/foto/{nombre}-v-1000.webp"
    srcset = ", ".join(
        f"assets/img/foto/{nombre}-v-{w}.webp {w}w" for w in (640, 1000, 1500)
    )
    estilo = f' style="object-position:{pos}"' if pos else ""
    carga = ' loading="eager" fetchpriority="high"' if eager else ' loading="lazy"'
    cl = f' class="{clase}"' if clase else ""
    return (f'<img{cl} src="{src}" srcset="{srcset}" sizes="{sizes}" '
            f'alt="{alt}" width="1000" height="1500" decoding="async"{carga}{estilo}>')


# --------------------------------------------------------------------------
# cascarón
# --------------------------------------------------------------------------

def cabecera(activa):
    items = []
    for texto, href in NAV:
        actual = ' aria-current="page"' if href == activa else ""
        items.append(f'<a href="{href}"{actual}>{texto}</a>')
    items.append('<a class="menu__cta" href="index.html#conversemos">Conversemos</a>')
    return f"""<header class="cabecera">
  <a class="marca" href="index.html" aria-label="Yeyo Vera, ir al inicio">{marca()}</a>
  <nav id="menu-principal" class="menu" aria-label="Navegación principal">
    {''.join(items)}
  </nav>
  <button class="hamburguesa" type="button" aria-label="Abrir menú" aria-expanded="false" aria-controls="menu-principal">
    <span></span><span></span><span></span>
  </button>
</header>"""


def pie():
    redes = "".join(f'<li><a href="{u}" rel="noopener">{n}</a></li>' for n, u in REDES.items())
    nav = "".join(f'<li><a href="{h}">{t}</a></li>' for t, h in NAV)
    return f"""<footer class="pie">
  <div class="pie__top">
    <div class="pie__marca">
      {marca()}
      <p>Acompaño a marcas, equipos y personas a convertir propósito en estrategia, creatividad y acción.</p>
    </div>
    <div>
      <h4>Navegar</h4>
      <ul>{nav}<li><a href="index.html#conversemos">Conversemos</a></li></ul>
    </div>
    <div>
      <h4>Encontrarme</h4>
      <ul>{redes}</ul>
    </div>
    <div>
      <h4>Escribir</h4>
      <ul>
        <li><a href="mailto:{CORREO}">{CORREO}</a></li>
        <li><a href="conferencias.html#invitar">Invitar a una conferencia</a></li>
        <li><a href="ideas.html#boletin">Recibir nuevas ideas</a></li>
      </ul>
    </div>
  </div>
  <div class="pie__bajo">
    <p>&copy; <span data-anio>2026</span> Sergio &ldquo;Yeyo&rdquo; Vera &middot; Country Manager Bolivia, Atomik Pro</p>
    <p>La verdad que mueve</p>
  </div>
</footer>"""


JSON_LD = """{
 "@context":"https://schema.org",
 "@type":"Person",
 "name":"Sergio \u201cYeyo\u201d Vera",
 "alternateName":"Yeyo Vera",
 "jobTitle":"Consultor creativo estrat\u00e9gico, speaker y educador",
 "description":"Acompa\u00f1a a marcas, equipos y personas a convertir prop\u00f3sito en estrategia, creatividad y acci\u00f3n.",
 "url":"%(sitio)s",
 "image":"%(sitio)s/assets/img/foto/retrato-frontal.jpg",
 "email":"mailto:%(correo)s",
 "worksFor":{"@type":"Organization","name":"Atomik Pro"},
 "knowsAbout":["Estrategia de marca","Creatividad","Marketing","Liderazgo","Prop\u00f3sito"],
 "knowsLanguage":"es",
 "sameAs":[%(redes)s]
}"""


def página(archivo, titulo, descripcion, cuerpo, activa="", clase_body=""):
    canon = f"{SITIO}/{archivo}"
    json_ld = JSON_LD % {
        "sitio": SITIO,
        "correo": CORREO,
        "redes": ",".join(f'"{u}"' for u in REDES.values() if u.startswith("http")),
    }
    body_attr = f' class="{clase_body}"' if clase_body else ""
    html = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo}</title>
<meta name="description" content="{descripcion}">
<link rel="canonical" href="{canon}">
<meta name="theme-color" content="#000000">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_BO">
<meta property="og:site_name" content="Yeyo Vera">
<meta property="og:title" content="{titulo}">
<meta property="og:description" content="{descripcion}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{SITIO}/assets/img/foto/retrato-frontal.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&display=swap">
<link rel="stylesheet" href="assets/css/style.css">
<script type="application/ld+json">{json_ld}</script>
</head>
<body{body_attr}>
{cabecera(activa)}
<main id="contenido">
{cuerpo}
</main>
{pie()}
<script src="assets/js/main.js" defer></script>
</body>
</html>
"""
    ruta = os.path.join(AQUI, archivo)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(html)
    return len(html)


def encabezado(n, kicker, titulo, texto="", extra=""):
    cuerpo = f"<h2>{titulo}</h2>"
    if texto:
        cuerpo += f'<p class="texto">{texto}</p>'
    if extra:
        cuerpo += extra
    return f"""<div class="encabezado revelar">
  <p class="kicker"><span class="n">{n}</span>{kicker}</p>
  <div>{cuerpo}</div>
</div>"""


def portada(miga, kicker, titulo, lead, acciones=""):
    return f"""<section class="portada">
  {simbolo('portada__marca')}
  <p class="miga revelar"><a href="index.html">Inicio</a> <span>/</span> <span>{miga}</span></p>
  <div class="portada__grid">
    <div class="revelar">
      <p class="kicker kicker--tenue" style="margin-top:2rem">{kicker}</p>
      <h1>{titulo}</h1>
    </div>
    <div class="revelar revelar--d1">
      <p class="lead">{lead}</p>
      {acciones}
    </div>
  </div>
</section>"""


# --------------------------------------------------------------------------
# datos de contenido
# --------------------------------------------------------------------------

RUTAS = [
    ("01", "marketing", "Una marca",
     "Tengo una marca, un producto o una idea que necesita dirección.",
     "Explorar consultoría", "trabajo.html"),
    ("02", "workshops", "Un equipo",
     "Necesito cambiar la forma en que mi equipo piensa, crea o actúa.",
     "Ver talleres", "trabajo.html#talleres"),
    ("03", "conversacion", "Una audiencia",
     "Busco una conferencia que deje algo más que aplausos.",
     "Ver conferencias", "conferencias.html"),
]

VERA = [
    ("V", "verdad", "Verdad", "Negocio, personas y cultura."),
    ("E", "enfoque", "Enfoque", "Qué importa y qué resolver."),
    ("R", "ruta", "Ruta", "Posicionamiento y narrativa."),
    ("A", "activacion", "Activación", "Experiencias y resultados."),
]

CIFRAS = [("14+", "Años"), ("90+", "Empresas"), ("200+", "Emprendimientos"), ("9+", "Países")]

SERVICIOS = [
    ("01", "Estrategia de marca",
     "Posicionamiento, propuesta de valor, narrativa, tono y arquitectura de comunicación."),
    ("02", "Plataforma creativa",
     "Concepto rector, territorio, mensajes, dirección visual y ejemplos de bajada."),
    ("03", "Crecimiento y lanzamiento",
     "Fases, contenidos, canales, experiencias, responsables, KPIs y desarrollo comercial."),
]

CHARLAS = [
    ("01", "La verdad antes de la idea",
     "Por qué las mejores ideas no nacen de una lluvia de ideas, sino de entender qué es cierto antes de decidir qué decir.",
     "Marcas, equipos creativos y liderazgo"),
    ("02", "Crecer sin perderte",
     "Cómo sostener el crecimiento de un negocio o una carrera sin dejar por el camino lo que le daba sentido.",
     "Emprendedores, equipos comerciales y universidades"),
    ("03", "Marcas humanas en un mundo automático",
     "Qué sigue siendo insustituible cuando todo se puede automatizar, y cómo construir desde ahi.",
     "Congresos, gremios y organizaciones"),
]

FASES = [
    ("01", "Desafio", "Qué debía cambiar."),
    ("02", "Verdad", "Qué entendimos."),
    ("03", "Construccion", "Qué hicimos."),
    ("04", "Cambio", "Qué resultado dejó."),
]

CAPITULOS = [
    ("crecimiento", "Crear",
     "Empecé haciendo. Piezas, campañas, marcas pequeñas y encargos que enseñaron más que cualquier manual."),
    ("ruta", "Liderar",
     "Dirigir equipos me obligó a cambiar la pregunta: de qué idea es mejor a qué necesita esta gente para dar lo mejor."),
    ("workshops", "Enseñar",
     "El aula me devolvió el oficio. Explicar algo bien es la prueba más honesta de haberlo entendido."),
    ("marketing", "Emprender",
     "Levantar cosas propias enseña el costo real de una decisión, y por qué la estrategia sin ejecucion es un deseo."),
    ("gospel", "Vivir con propósito",
     "Mi fe en Jesus es la raiz desde la que entiendo el propósito: no como una frase bonita, sino como una manera de servir, decidir y construir."),
]

CATEGORIAS = [("marketing", "Marketing"), ("proposito", "Creatividad"),
              ("gospel", "Propósito"), ("ruta", "Liderazgo")]

NOTAS = [
    ("marketing", "Marketing", "Artículo",
     "Tu marca no tiene un problema de comunicación",
     "Casi siempre lo que falta no es una campaña, es una decisión que nadie quiso tomar."),
    ("proposito", "Creatividad", "Video",
     "Las buenas ideas no aparecen, se construyen",
     "Un recorrido corto por el sistema que uso para decidir qué merece existir."),
    ("gospel", "Propósito", "Podcast ILUMINA",
     "Servir también es una estrategia",
     "Conversación sobre trabajo, fe y las decisiones que no se miden en resultados inmediatos."),
    ("ruta", "Liderazgo", "Artículo",
     "El equipo no necesita más motivación, necesita dirección",
     "Sobre la diferencia entre animar a la gente y darle un criterio para decidir."),
    ("marketing", "Marketing", "Videocaso",
     "Cómo se ordena una marca con demasiadas ideas",
     "Un caso real contado en cuatro movimientos: desafio, verdad, construccion y cambio."),
    ("proposito", "Creatividad", "Recurso",
     "Cinco preguntas antes de escribir un brief",
     "Una guia breve para llegar a la reunion con el problema bien planteado."),
]


# --------------------------------------------------------------------------
# páginas
# --------------------------------------------------------------------------

def home():
    rutas = "".join(f"""<article class="ruta revelar revelar--d{i}">
      <p class="kicker kicker--tenue">{n}</p>
      <div class="ruta__icono">{icono(ic)}</div>
      <h3>{tit}</h3>
      <p class="texto">{txt}</p>
      {enlace(cta, href)}
    </article>""" for i, (n, ic, tit, txt, cta, href) in enumerate(RUTAS))

    pasos = "".join(f"""<article class="paso revelar revelar--d{i}">
      <span class="paso__letra">{letra}</span>
      <h3>{tit}</h3>
      <p class="texto">{txt}</p>
      <div class="paso__icono">{icono(ic)}</div>
    </article>""" for i, (letra, ic, tit, txt) in enumerate(VERA))

    cifras = "".join(f"""<div class="cifra revelar revelar--d{i}">
      <span class="dato">{v}</span><span>{k}</span>
    </div>""" for i, (v, k) in enumerate(CIFRAS))

    clientes = "".join(f"<li>Cliente {i:02d}</li>" for i in range(1, 11))

    casos = "".join(f"""<article class="caso revelar revelar--d{i}">
      <a class="caso__media" href="trabajo.html#casos" aria-label="Videocaso {n}: próximamente">
        {foto(f, "Fotograma del videocaso " + n, "(max-width:900px) 92vw, 30vw")}
        <span class="caso__play">{PLAY}</span>
        <span class="caso__etiqueta">Videocaso {n}</span>
      </a>
      <h3>{tit}</h3>
      <p class="texto">{txt}</p>
    </article>""" for i, (n, f, tit, txt) in enumerate([
        ("01", "estudio-a", "Título del caso", "Video de 60 a 90 segundos. Pendiente de publicación."),
        ("02", "estudio-c", "Título del caso", "Video de 60 a 90 segundos. Pendiente de publicación."),
        ("03", "retrato-gesto", "Título del caso", "Video de 60 a 90 segundos. Pendiente de publicación."),
    ]))

    fases = "".join(f"""<div class="fase revelar revelar--d{i}">
      <p class="kicker kicker--tenue">{n}</p><h4>{t}</h4><p>{d}</p>
    </div>""" for i, (n, t, d) in enumerate(FASES))

    charlas = "".join(f"""<li class="revelar revelar--d{i}">
      <span class="lista__n">{n}</span>
      <div><h3>{t}</h3><p class="texto texto--claro">{d}</p></div>
    </li>""" for i, (n, t, d, _a) in enumerate(CHARLAS))

    servicios = "".join(f"""<li class="revelar revelar--d{i}">
      <span class="lista__n">{n}</span>
      <div><h3>{t}</h3><p class="texto">{d}</p></div>
    </li>""" for i, (n, t, d) in enumerate(SERVICIOS))

    chips = "".join(f'<a class="chip" href="ideas.html">{icono(ic)}<span>{t}</span></a>'
                    for ic, t in CATEGORIAS)

    capitulos = "".join(f'<span class="chip">{t}</span>' for _ic, t, _d in CAPITULOS)

    cuerpo = f"""
<section class="hero" id="inicio">
  {simbolo('hero__marca')}
  <div class="hero__copy">
    <p class="kicker kicker--tenue revelar">Sergio &ldquo;Yeyo&rdquo; Vera &middot; Country Manager Bolivia, Atomik Pro</p>
    <h1 class="revelar revelar--d1">Todo lo que crece de verdad<br>empieza con una <span class="verde">verdad</span>.</h1>
    <p class="lead revelar revelar--d2">Acompaño a marcas, equipos y personas a convertir propósito en estrategia, creatividad y acción.</p>
    <div class="hero__acciones revelar revelar--d3">
      <a class="btn btn--verde" href="#rutas"><span>Encontrar una ruta</span></a>
      {enlace('Ver mi trabajo', 'trabajo.html')}
    </div>
  </div>
  <figure class="hero__figura revelar revelar--d2" style="margin:0">
    {foto('retrato-frontal', 'Retrato de Sergio Yeyo Vera', '(max-width:900px) 86vw, 30vw', pos='center 20%', eager=True)}
    <figcaption class="hero__pie"><span>La verdad que mueve</span><span>Santa Cruz, Bolivia</span></figcaption>
  </figure>
</section>

<section class="seccion envoltura" id="rutas">
  {encabezado('01', 'Elige tu punto de partida', '&iquest;Qué estás tratando de mover?')}
  <div class="rutas">{rutas}</div>
</section>

<section class="seccion envoltura oscuro" id="metodo">
  <div class="metodo__intro">
    <p class="kicker revelar"><span class="n">02</span>Método V.E.R.A.</p>
    <div class="revelar revelar--d1">
      <h2>Las buenas ideas no aparecen.<br>Se construyen.</h2>
    </div>
    <p class="texto texto--claro revelar revelar--d2">No entrego una coleccion de ideas. Construyo un sistema que ayuda a decidir qué merece existir y como llevarlo a la realidad.</p>
  </div>
  <div class="pasos">{pasos}</div>
</section>

<section class="seccion envoltura acento" id="prueba">
  <div class="prueba">
    <div class="revelar">
      <p class="kicker">03 &middot; Experiencia sin exhibicionismo</p>
      <h2 style="margin-top:1.6rem">He aprendido haciendo.<br>Y haciendo con otros.</h2>
    </div>
    <div class="cifras">{cifras}</div>
  </div>
  <div style="margin-top:clamp(3rem,6vw,5rem)" class="revelar">
    <p class="kicker" style="margin-bottom:1.4rem">Marcas y organizaciones con las que he trabajado</p>
    <ul class="clientes">{clientes}</ul>
  </div>
</section>

<section class="seccion envoltura" id="trabajo">
  {encabezado('04', 'Trabajo que se puede ver',
              'Cuando hay muchas ideas,<br>pero todavía no hay dirección.',
              'Los casos no cuentan todo. Muestran como pienso.')}
  <div class="casos">{casos}</div>
  <div class="fases">{fases}</div>
  <ul class="lista" style="margin-top:clamp(3rem,6vw,5rem)">{servicios}</ul>
  <div style="margin-top:2.6rem" class="revelar">
    <a class="btn btn--negro" href="trabajo.html"><span>Conversemos sobre el desafio</span></a>
  </div>
</section>

<section class="seccion envoltura oscuro" id="conferencias">
  <div class="encabezado revelar">
    <p class="kicker"><span class="n">05</span>Conferencias</p>
    <div>
      <h2>Ideas para llevarse.<br>No solo para escuchar.</h2>
      <p class="texto texto--claro">Charlas que ayudan a mirar distinto, encontrar una verdad útil y convertirla en movimiento.</p>
      <div style="margin-top:2rem"><a class="btn btn--verde" href="conferencias.html#invitar"><span>Invitar a Yeyo</span></a></div>
    </div>
  </div>
  <ul class="lista">{charlas}</ul>
  <p class="kicker kicker--tenue" style="margin-top:2rem">Keynote &middot; Taller &middot; Conversación</p>
</section>

<section class="seccion envoltura" id="ideas">
  {encabezado('06', 'Ideas', 'Contenido para mover<br>lo que importa.')}
  <div class="idea-destacada">
    <div class="idea-arte revelar">
      {simbolo('idea-arte__simbolo')}
      <span class="idea-arte__nombre">ILUMINA</span>
    </div>
    <div class="revelar revelar--d1">
      <p class="kicker kicker--tenue">Una idea con propósito</p>
      <h3 style="margin:1.2rem 0 1.4rem;font-size:clamp(1.9rem,3.6vw,3.4rem)">Sin fórmulas mágicas.<br>Sin ruido innecesario.</h3>
      <p class="texto">Reflexiones sobre marcas, crecimiento, creatividad y vida. Ideas breves para leer, escuchar y poner en práctica.</p>
      <div class="chips">{chips}</div>
      {enlace('Quiero recibir nuevas ideas', 'ideas.html#boletin')}
    </div>
  </div>
</section>

<section class="sobre" id="soy-yeyo">
  <div class="sobre__foto revelar">
    {foto('retrato-pecho', 'Sergio Yeyo Vera', '(max-width:900px) 100vw, 50vw', pos='center 15%')}
  </div>
  <div class="sobre__copy revelar revelar--d1">
    <p class="kicker kicker--tenue"><span class="n">07</span>Soy Yeyo</p>
    <h2>Trabajo con estrategia.<br>Vivo desde el propósito.</h2>
    <p class="texto">Soy Sergio Vera, aunque casi todos me dicen Yeyo. Durante más de 14 años he trabajado entre marcas, agencias, negocios, aulas y escenarios.</p>
    <p class="texto">Hoy soy Country Manager Bolivia de Atomik Pro y continuo acompañando a organizaciones, equipos y profesionales que necesitan convertir ideas en dirección.</p>
    <p class="texto">Mi fe en Jesus es la raiz desde la que entiendo el propósito: no como una frase bonita, sino como una manera de servir, decidir y construir.</p>
    <div class="capitulos">{capitulos}</div>
    <div style="margin-top:2.4rem">{enlace('Conocer mi historia', 'soy-yeyo.html')}</div>
  </div>
</section>

<section class="seccion envoltura oscuro" id="conversemos">
  <div class="contacto">
    <div class="revelar">
      <p class="kicker"><span class="n">08</span>Conversemos</p>
      <h2 style="margin-top:1.6rem">&iquest;Qué estás tratando<br>de mover?</h2>
      <p class="texto texto--claro" style="margin-top:2rem">Una marca, un equipo, una audiencia o quizás algo que todavía necesita nombre. Cuentame el desafio y te respondo con una primera lectura.</p>
      <p class="texto texto--claro" style="margin-top:2rem">También puedes escribir directo a <a href="mailto:{CORREO}" style="color:var(--verde)">{CORREO}</a>.</p>
    </div>
    <form class="formulario revelar revelar--d1" data-form="contacto" data-destino="{CORREO}" novalidate>
      <div class="campo--doble">
        <div class="campo">
          <label for="c-nombre">Nombre</label>
          <input id="c-nombre" name="Nombre" type="text" autocomplete="name" required>
        </div>
        <div class="campo">
          <label for="c-empresa">Empresa u organización</label>
          <input id="c-empresa" name="Empresa" type="text" autocomplete="organization">
        </div>
      </div>
      <div class="campo">
        <label for="c-contacto">Correo o WhatsApp</label>
        <input id="c-contacto" name="Contacto" type="text" autocomplete="email" required>
      </div>
      <div class="campo">
        <label id="lbl-mover">&iquest;Qué necesitas mover?</label>
        <div class="opciones" role="group" aria-labelledby="lbl-mover">
          <label class="opcion"><input type="radio" name="Necesidad" value="Una marca" checked><span>Una marca</span></label>
          <label class="opcion"><input type="radio" name="Necesidad" value="Un equipo"><span>Un equipo</span></label>
          <label class="opcion"><input type="radio" name="Necesidad" value="Una audiencia"><span>Una audiencia</span></label>
          <label class="opcion"><input type="radio" name="Necesidad" value="Todavía no lo se"><span>Todavía no lo se</span></label>
        </div>
      </div>
      <div class="campo">
        <label for="c-desafio">Breve desafio</label>
        <textarea id="c-desafio" name="Desafio" rows="3" required></textarea>
      </div>
      <p class="miel" aria-hidden="true"><label>No llenar<input type="text" name="website" tabindex="-1" autocomplete="off"></label></p>
      <button class="btn btn--verde" type="submit"><span>Iniciar conversación</span></button>
      <p class="respuesta" role="status" hidden></p>
    </form>
  </div>
</section>
"""
    return página("index.html", "Yeyo Vera — La verdad que mueve",
                  "Sergio Yeyo Vera acompana a marcas, equipos y personas a convertir propósito en estrategia, creatividad y acción. Consultoría, conferencias e ideas.",
                  cuerpo, activa="")


def trabajo():
    servicios = "".join(f"""<li class="revelar revelar--d{i}">
      <span class="lista__n">{n}</span>
      <div><h3>{t}</h3><p class="texto">{d}</p></div>
    </li>""" for i, (n, t, d) in enumerate(SERVICIOS))

    pasos = "".join(f"""<article class="paso revelar revelar--d{i}">
      <span class="paso__letra">{l}</span><h3>{t}</h3><p class="texto">{d}</p>
      <div class="paso__icono">{icono(ic)}</div>
    </article>""" for i, (l, ic, t, d) in enumerate(VERA))

    fases = "".join(f"""<div class="fase revelar revelar--d{i}">
      <p class="kicker kicker--tenue">{n}</p><h4>{t}</h4><p>{d}</p></div>"""
                    for i, (n, t, d) in enumerate(FASES))

    cuerpo = f"""
{portada('Trabajo', 'Consultoría estratégica y creativa',
         'Muchas ideas.<br>Ninguna dirección.',
         'Cuando una marca tiene muchas ideas, pero todavía no tiene una dirección. Trabajo con equipos que ya intentaron de todo y necesitan decidir qué sostener, qué soltar y por dónde empezar.',
         '<div style="margin-top:2.2rem"><a class="btn btn--verde" href="#hablemos"><span>Conversemos sobre el desafio</span></a></div>')}

<section class="banda">
  {simbolo('banda__simbolo')}
  <p class="kicker">Problema &middot; Método &middot; Entregable &middot; Casos &middot; Conversemos</p>
</section>

<section class="seccion envoltura">
  {encabezado('01', 'El problema real',
              'El problema casi nunca<br>es la falta de ideas.',
              'Es la falta de un criterio compartido para elegir entre ellas. Sin ese criterio, cada decisión se discute de cero y el equipo se agota antes de ejecutar.')}
  <div class="con-foto">
    <figure class="con-foto__foto revelar" style="margin:0">
      {foto('retrato-brazos', 'Yeyo Vera en sesión de trabajo', '(max-width:900px) 92vw, 34vw', pos='center 16%')}
      <figcaption class="con-foto__pie">Qué entrego</figcaption>
    </figure>
    <ul class="lista revelar revelar--d1" style="margin:0">{servicios}</ul>
  </div>
</section>

<section class="seccion envoltura oscuro" id="metodo">
  <div class="metodo__intro">
    <p class="kicker revelar"><span class="n">02</span>Método V.E.R.A.</p>
    <div class="revelar revelar--d1"><h2>Un sistema para decidir<br>que merece existir.</h2></div>
    <p class="texto texto--claro revelar revelar--d2">Cuatro movimientos que se aplican igual a una marca, a un equipo o a un lanzamiento. Cambia la profundidad, no la lógica.</p>
  </div>
  <div class="pasos">{pasos}</div>
</section>

<section class="seccion envoltura" id="talleres">
  {encabezado('03', 'Talleres para equipos',
              'Cambiar como piensa<br>un equipo, no solo que hace.',
              'Sesiones de trabajo donde el equipo aplica el método sobre su propio negocio. Se sale con decisiones tomadas, no con apuntes.')}
  <ul class="lista">
    <li class="revelar"><span class="lista__n">01</span><div><h3>Diagnóstico de verdad</h3><p class="texto">Medio día. Entender el negocio, las personas y la cultura antes de proponer nada.</p></div></li>
    <li class="revelar revelar--d1"><span class="lista__n">02</span><div><h3>Taller de enfoque</h3><p class="texto">Un día. Definir qué importa ahora y qué problema se resuelve primero.</p></div></li>
    <li class="revelar revelar--d2"><span class="lista__n">03</span><div><h3>Ruta y activación</h3><p class="texto">Acompanamiento por fases. Narrativa, plan y responsables.</p></div></li>
  </ul>
</section>

<section class="seccion envoltura tenue" id="casos">
  {encabezado('04', 'Casos', 'Como se ve el método<br>cuando aterriza.',
              'Cada caso se cuenta en cuatro movimientos. Los videos estan en producción.')}
  <div class="fases">{fases}</div>
  <p class="texto revelar" style="margin-top:2.5rem">Los videocasos se publicarán aquí en formato de 60 a 90 segundos, con subtitulos y portada propia.</p>
</section>

<section class="seccion envoltura oscuro" id="hablemos">
  <div class="contacto">
    <div class="revelar">
      <p class="kicker"><span class="n">05</span>Conversemos</p>
      <h2 style="margin-top:1.6rem">Cuentame el desafio.</h2>
      <p class="texto texto--claro" style="margin-top:2rem">La conversación define el alcance. No trabajo con paquetes cerrados ni publico precios: cada proyecto se propone después de entender el problema.</p>
    </div>
    <form class="formulario revelar revelar--d1" data-form="contacto" data-destino="{CORREO}" novalidate>
      <div class="campo--doble">
        <div class="campo"><label for="t-nombre">Nombre</label><input id="t-nombre" name="Nombre" type="text" required autocomplete="name"></div>
        <div class="campo"><label for="t-org">Organización</label><input id="t-org" name="Organización" type="text" autocomplete="organization"></div>
      </div>
      <div class="campo"><label for="t-contacto">Correo o WhatsApp</label><input id="t-contacto" name="Contacto" type="text" required></div>
      <div class="campo"><label for="t-desafio">Qué necesitas mover</label><textarea id="t-desafio" name="Desafio" rows="4" required></textarea></div>
      <p class="miel" aria-hidden="true"><label>No llenar<input type="text" name="website" tabindex="-1" autocomplete="off"></label></p>
      <button class="btn btn--verde" type="submit"><span>Iniciar conversación</span></button>
      <p class="respuesta" role="status" hidden></p>
    </form>
  </div>
</section>
"""
    return página("trabajo.html", "Trabajo — Yeyo Vera",
                  "Consultoría de estrategia de marca, plataforma creativa y crecimiento. Método V.E.R.A. para marcas y equipos que necesitan dirección.",
                  cuerpo, activa="trabajo.html")


def conferencias():
    charlas = "".join(f"""<li class="revelar revelar--d{i}">
      <span class="lista__n">{n}</span>
      <div><h3>{t}</h3><p class="texto texto--claro">{d}</p>
      <p class="kicker kicker--tenue" style="margin-top:1rem">Para: {a}</p></div>
    </li>""" for i, (n, t, d, a) in enumerate(CHARLAS))

    formatos = "".join(f"""<div class="fase revelar revelar--d{i}">
      <p class="kicker kicker--tenue">{n}</p><h4>{t}</h4><p>{d}</p></div>"""
                       for i, (n, t, d) in enumerate([
                           ("01", "Keynote", "45 a 60 minutos. Para congresos y eventos de marca."),
                           ("02", "Taller", "3 horas a un día. El grupo trabaja sobre su propio caso."),
                           ("03", "Conversación", "Formato entrevista o panel, con preguntas del publico."),
                       ]))

    cuerpo = f"""
{portada('Conferencias', 'Keynote &middot; Taller &middot; Conversación',
         'Ideas para llevarse.<br>No solo para escuchar.',
         'Charlas que ayudan a mirar distinto, encontrar una verdad útil y convertirla en movimiento.',
         '<div style="margin-top:2.2rem"><a class="btn btn--verde" href="#invitar"><span>Invitar a Yeyo</span></a></div>')}

<section class="seccion envoltura">
  {encabezado('01', 'Showreel', 'Cómo se ve en escenario.')}
  <div class="caso__media revelar" style="aspect-ratio:16/9">
    {foto('traje-oscuro', 'Yeyo Vera en escenario', '92vw', pos='center 12%')}
    <span class="caso__play">{PLAY}</span>
    <span class="caso__etiqueta">Showreel &middot; 60-90 s &middot; próximamente</span>
  </div>
</section>

<section class="seccion envoltura oscuro">
  {encabezado('02', 'Tres charlas', 'Cada charla tiene<br>una promesa concreta.')}
  <ul class="lista">{charlas}</ul>
</section>

<section class="seccion envoltura">
  {encabezado('03', 'Formatos', 'Se adapta el formato,<br>no el fondo.')}
  <div class="fases">{formatos}</div>
  <div class="chips revelar" style="margin-top:3rem">
    <span class="chip">Congresos</span><span class="chip">Universidades</span>
    <span class="chip">Equipos internos</span><span class="chip">Gremios</span>
    <span class="chip">Iglesias</span><span class="chip">Eventos de marca</span>
  </div>
</section>

<section class="seccion envoltura tenue">
  {encabezado('04', 'Speaker kit', 'Todo lo que el equipo<br>organizador necesita.',
              'Bio corta y larga, fotografías oficiales en alta, requerimientos técnicos y títulos de charlas.')}
  <div class="chips revelar">
    <a class="chip" href="#invitar">{icono('contenido')}<span>Bio descargable &middot; pendiente</span></a>
    <a class="chip" href="#invitar">{icono('marketing')}<span>Fotos oficiales &middot; pendiente</span></a>
  </div>
</section>

<section class="seccion envoltura oscuro" id="invitar">
  <div class="contacto">
    <div class="revelar">
      <p class="kicker"><span class="n">05</span>Invitar a Yeyo</p>
      <h2 style="margin-top:1.6rem">Cuentame del evento.</h2>
      <p class="texto texto--claro" style="margin-top:2rem">Con estos datos puedo responder con disponibilidad, formato sugerido y propuesta en pocos días.</p>
    </div>
    <form class="formulario revelar revelar--d1" data-form="conferencia" data-destino="{CORREO}" novalidate>
      <div class="campo--doble">
        <div class="campo"><label for="f-fecha">Fecha</label><input id="f-fecha" name="Fecha" type="date" required></div>
        <div class="campo"><label for="f-ciudad">Ciudad o virtual</label><input id="f-ciudad" name="Ciudad" type="text" required></div>
      </div>
      <div class="campo--doble">
        <div class="campo"><label for="f-org">Organización</label><input id="f-org" name="Organización" type="text" required autocomplete="organization"></div>
        <div class="campo"><label for="f-audiencia">Tipo de audiencia</label><input id="f-audiencia" name="Audiencia" type="text"></div>
      </div>
      <div class="campo--doble">
        <div class="campo"><label for="f-asistentes">Asistentes</label><input id="f-asistentes" name="Asistentes" type="number" min="1" inputmode="numeric"></div>
        <div class="campo"><label for="f-formato">Formato</label>
          <select id="f-formato" name="Formato">
            <option>Keynote</option><option>Taller</option><option>Conversación</option><option>Por definir</option>
          </select>
        </div>
      </div>
      <div class="campo"><label for="f-presupuesto">Presupuesto estimado</label><input id="f-presupuesto" name="Presupuesto" type="text"></div>
      <div class="campo"><label for="f-contacto">Contacto</label><input id="f-contacto" name="Contacto" type="text" required></div>
      <p class="miel" aria-hidden="true"><label>No llenar<input type="text" name="website" tabindex="-1" autocomplete="off"></label></p>
      <button class="btn btn--verde" type="submit"><span>Enviar invitacion</span></button>
      <p class="respuesta" role="status" hidden></p>
    </form>
  </div>
</section>
"""
    return página("conferencias.html", "Conferencias — Yeyo Vera",
                  "Tres conferencias sobre verdad, crecimiento y marcas humanas. Keynote, taller o conversación. Formulario de contratación.",
                  cuerpo, activa="conferencias.html")


def ideas():
    filtros = '<button class="chip chip--activo" type="button" data-filtro="todo" aria-pressed="true"><span>Todo</span></button>'
    filtros += "".join(
        f'<button class="chip" type="button" data-filtro="{ic}" aria-pressed="false">{icono(ic)}<span>{t}</span></button>'
        for ic, t in CATEGORIAS)

    notas = "".join(f"""<article class="nota revelar" data-categoria="{cat}">
      <p class="kicker">{c} &middot; {f}</p>
      <h3>{t}</h3>
      <p class="texto" style="font-size:.92rem">{d}</p>
      <p class="meta">Próximamente</p>
    </article>""" for cat, c, f, t, d in NOTAS)

    cuerpo = f"""
{portada('Ideas', 'Artículos &middot; Videos &middot; Videocasos &middot; Podcast ILUMINA',
         'El contenido no es relleno.<br>Es parte de la propuesta.',
         'Reflexiones sobre marcas, crecimiento, creatividad y vida. Ideas breves para leer, escuchar y poner en práctica.')}

<section class="seccion envoltura">
  <div class="idea-destacada">
    <div class="idea-arte revelar">
      {simbolo('idea-arte__simbolo')}
      <span class="idea-arte__nombre">ILUMINA</span>
    </div>
    <div class="revelar revelar--d1">
      <p class="kicker kicker--tenue">Podcast &middot; Una idea con propósito</p>
      <h2 style="margin:1.2rem 0 1.4rem;font-size:clamp(2rem,4vw,3.6rem)">Sin fórmulas mágicas.<br>Sin ruido innecesario.</h2>
      <p class="texto">Conversaciones sobre trabajo, fe, creatividad y las decisiones que no se miden en resultados inmediatos.</p>
      <div style="margin-top:2rem">{enlace('Escuchar ILUMINA', '#boletin')}</div>
    </div>
  </div>
</section>

<section class="seccion envoltura tenue">
  {encabezado('01', 'Explorar', 'Una idea destacada<br>por formato.')}
  <div class="chips revelar" style="margin-bottom:2.5rem">{filtros}</div>
  <div class="notas">{notas}</div>
</section>

<section class="seccion envoltura oscuro" id="boletin">
  <div class="boletin">
    <div class="revelar">
      <p class="kicker"><span class="n">02</span>Boletin</p>
      <h2 style="margin-top:1.6rem">Una idea<br>con propósito.</h2>
      <p class="texto texto--claro" style="margin-top:2rem">Breve, útil y con una frecuencia sostenible. Sin spam y con baja en un clic.</p>
    </div>
    <form class="formulario revelar revelar--d1" data-form="boletin" data-destino="{CORREO}" novalidate>
      <div class="boletin__form">
        <div class="campo">
          <label for="b-correo">Tu correo</label>
          <input id="b-correo" name="Correo" type="email" required autocomplete="email" placeholder="nombre@correo.com">
        </div>
        <button class="btn btn--verde" type="submit"><span>Suscribirme</span></button>
      </div>
      <p class="miel" aria-hidden="true"><label>No llenar<input type="text" name="website" tabindex="-1" autocomplete="off"></label></p>
      <p class="respuesta" role="status" hidden></p>
    </form>
  </div>
</section>
"""
    return página("ideas.html", "Ideas — Yeyo Vera",
                  "Artículos, videos, videocasos y el podcast ILUMINA. Marketing, creatividad, propósito y liderazgo. Boletin Una idea con propósito.",
                  cuerpo, activa="ideas.html")


def soy_yeyo():
    caps = "".join(f"""<article class="capitulo revelar">
      <div>
        <div class="capitulo__icono">{icono(ic)}</div>
        <h3>{t}</h3>
      </div>
      <p class="texto">{d}</p>
    </article>""" for ic, t, d in CAPITULOS)

    cuerpo = f"""
{portada('Soy Yeyo', 'Sergio &ldquo;Yeyo&rdquo; Vera',
         'Una historia en capitulos.<br>No un CV cronológico.',
         'Trabajo con estrategia. Vivo desde el propósito. Más de 14 años entre marcas, agencias, negocios, aulas y escenarios.')}

<section class="sobre">
  <div class="sobre__foto revelar">
    {foto('traje-claro', 'Sergio Yeyo Vera, retrato', '(max-width:900px) 100vw, 50vw', pos='center 12%')}
  </div>
  <div class="sobre__copy revelar revelar--d1">
    <p class="kicker kicker--tenue">Quien soy</p>
    <h2>Trabajo con estrategia.<br>Vivo desde el propósito.</h2>
    <p class="texto">Soy Sergio Vera, aunque casi todos me dicen Yeyo. Durante más de 14 años he trabajado entre marcas, agencias, negocios, aulas y escenarios.</p>
    <p class="texto">Hoy soy Country Manager Bolivia de Atomik Pro y continuo acompañando a organizaciones, equipos y profesionales que necesitan convertir ideas en dirección.</p>
    <p class="texto">Mi fe en Jesus es la raiz desde la que entiendo el propósito: no como una frase bonita, sino como una manera de servir, decidir y construir.</p>
    <div style="margin-top:2.4rem">{enlace('Conversemos', 'index.html#conversemos')}</div>
  </div>
</section>

<section class="seccion envoltura">
  {encabezado('01', 'Capitulos', 'Cinco maneras<br>de haber aprendido.')}
  {caps}
</section>

<section class="seccion envoltura acento">
  <div class="prueba">
    <div class="revelar">
      <p class="kicker">02 &middot; Recorrido</p>
      <h2 style="margin-top:1.6rem">He aprendido haciendo.<br>Y haciendo con otros.</h2>
    </div>
    <div class="cifras">{''.join(f'<div class="cifra revelar"><span class="dato">{v}</span><span>{k}</span></div>' for v, k in CIFRAS)}</div>
  </div>
</section>

<section class="seccion envoltura oscuro">
  {encabezado('03', 'Material', 'Para prensa<br>y organizadores.',
              'Bio corta, bio larga, fotografías oficiales en alta resolución y títulos de charlas.')}
  <div class="chips revelar">
    <a class="chip" href="index.html#conversemos">{icono('contenido')}<span>Bio descargable &middot; pendiente</span></a>
    <a class="chip" href="conferencias.html#invitar">{icono('conversacion')}<span>Invitar a una conferencia</span></a>
  </div>
</section>
"""
    return página("soy-yeyo.html", "Soy Yeyo — Sergio Vera",
                  "La historia de Sergio Yeyo Vera en capitulos: crear, liderar, enseñar, emprender y vivir con propósito.",
                  cuerpo, activa="soy-yeyo.html")


def error404():
    cuerpo = f"""
<section class="seccion envoltura oscuro" style="min-height:calc(100svh - var(--header-h));display:grid;align-content:center">
  <div class="contacto" style="align-items:center">
    <div class="revelar">
      <p class="kicker"><span class="n">404</span>Página no encontrada</p>
      <h1 style="margin:1.6rem 0 1.8rem;font-size:clamp(2.6rem,6vw,6rem)">Esta ruta<br>todavía no existe.</h1>
      <p class="texto texto--claro">Puede que el enlace haya cambiado. Volvamos a un punto de partida.</p>
      <div class="hero__acciones">
        <a class="btn btn--verde" href="index.html"><span>Ir al inicio</span></a>
        {enlace('Encontrar una ruta', 'index.html#rutas')}
      </div>
    </div>
    <div class="revelar revelar--d1" style="text-align:center">
      <img src="assets/img/avatar.webp" alt="" width="444" height="700" loading="lazy" style="margin-inline:auto;max-height:56vh;width:auto">
    </div>
  </div>
</section>
"""
    return página("404.html", "Página no encontrada — Yeyo Vera",
                  "La página que buscas no existe. Vuelve al inicio de yeyovera.com.",
                  cuerpo)


# --------------------------------------------------------------------------

if __name__ == "__main__":
    total = 0
    for fn in (home, trabajo, conferencias, ideas, soy_yeyo, error404):
        n = fn()
        total += n
        print(f"  {fn.__name__:14s} {n:7,} B")
    print(f"  {'total':14s} {total:7,} B")
