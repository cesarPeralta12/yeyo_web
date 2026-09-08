# Análisis del boceto — yeyo-vera.proshop-7746.chatgpt.site

## Sistema de diseño

Tokens:
  --green: #95d200   (acento único, "verde limón")
  --black: #000
  --white: #fff
  --line:  #d9d9d9
  --pad:   clamp(1.25rem, 5vw, 5rem)

- Tipografía: Arial/Helvetica (sistema, sin webfonts). Titulares UPPERCASE,
  line-height .92, letter-spacing -0.045em, font-size fluido con clamp().
  h1: clamp(3.4rem, 8.3vw, 9rem) — h2: clamp(2.7rem, 6.2vw, 6.5rem)
- Micro-texto (kicker/eyebrow/botones): 0.7–0.8rem, bold 700–800,
  uppercase, letter-spacing 0.08–0.16em.
- Cero border-radius. Cero sombras. Separación por líneas 1px.
- Fotos siempre en grayscale(100%) + object-fit: cover.
- Estilo: editorial suizo / brutalista-elegante, alto contraste.

## Ritmo de secciones (alterna fondo)

  header   negro, sticky, 94px, logo 150px + nav uppercase + CTA con borde verde
  01 hero        NEGRO   grid 1.7fr / 0.7fr, símbolo de marca al 12% opacidad
  02 rutas       BLANCO  3 columnas divididas por líneas verticales
  03 método      NEGRO   intro 1fr/2fr/1fr + 4 pasos (V.E.R.A.) con letra gigante verde
  04 proof       VERDE   #95d200 — h2 + 4 números grandes (14+, 90+, 200+, 9+)
  05 trabajo     BLANCO  foto 0.8fr / lista de servicios 1.2fr numerada
  06 conferencias NEGRO  2 columnas: copy + lista de charlas numeradas
  07 ideas       BLANCO  arte 4:3 negro + copy, chips de temas
  08 soy yeyo    #eee    foto 50% / texto 50%, chips "capítulos"
  09 contacto    NEGRO   copy + form de inputs underline (borde inferior gris → verde en focus)
  footer         negro, logo + copyright + link

## Patrones reutilizables

- `.section-head`: grid 1fr/3fr → kicker numerado ("01 / ELIGE TU PUNTO DE PARTIDA")
  a la izquierda, titular enorme a la derecha. Se repite en TODAS las secciones.
- Listas numeradas 01/02/03 con `border-top: 1px` en cada article.
- `.button`: sin radio, padding 1rem 1.4rem, uppercase 800; hover translateY(-2px).
- `.text-link`: uppercase + border-bottom, con flecha ↗ en verde.
- Chips: borde 1px negro, uppercase 0.65rem.
- Animación: una sola — `.reveal` (fade + translateY 24px, .8s).
- prefers-reduced-motion respetado.

## Responsive
- 900px: nav → menú hamburguesa; casi todos los grids colapsan a 1 columna;
  route-grid vertical con border-bottom; steps a 2 columnas.
- 560px: steps y numbers a 1 columna; actions en columna; h1 16vw.

## Assets del boceto
  assets/logo.png (1926x685), assets/symbol.png (mismo), 
  assets/yeyo-spotlight.jpg, yeyo-editorial.jpg, yeyo-portrait.jpg (todas verticales 2:3)

## Debilidades a mejorar en la versión final
- Arial pelado: subir a una tipografía real (grotesca tipo Archivo/Inter/Space Grotesk).
- Sin favicon, sin OG tags, sin schema.org.
- El form no envía a ningún lado.
- Sólo una animación; falta reveal on scroll (IntersectionObserver).
- Sin páginas internas (blog/ideas, casos), todo es one-page con anclas.
