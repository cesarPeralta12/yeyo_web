# syntax=docker/dockerfile:1

# ---------------------------------------------------------------------------
# Etapa 1 — generar el sitio
#
# build.py sólo usa la biblioteca estándar, así que no hace falta pip install.
# Se regenera el HTML dentro de la imagen para que nunca quede desincronizado
# respecto al contenido de build.py.
# ---------------------------------------------------------------------------
FROM python:3.12-alpine AS constructor

WORKDIR /origen

# Primero lo que casi nunca cambia, para aprovechar la caché de capas.
COPY assets ./assets

# Después el generador y sus datos.
COPY build.py robots.txt sitemap.xml ./

RUN python build.py && \
    test -s index.html && \
    echo "Páginas generadas:" && ls -1 *.html


# ---------------------------------------------------------------------------
# Etapa 2 — servir
# ---------------------------------------------------------------------------
FROM nginx:1.27-alpine AS servidor

LABEL org.opencontainers.image.title="yeyo-web" \
      org.opencontainers.image.description="Sitio de Sergio Yeyo Vera. Estático, sin dependencias externas." \
      org.opencontainers.image.licenses="UNLICENSED"

RUN rm -rf /usr/share/nginx/html/*
COPY nginx.conf     /etc/nginx/conf.d/default.conf
COPY seguridad.conf /etc/nginx/seguridad.conf

COPY --from=constructor /origen/assets      /usr/share/nginx/html/assets
COPY --from=constructor /origen/*.html      /usr/share/nginx/html/
COPY --from=constructor /origen/robots.txt  /usr/share/nginx/html/
COPY --from=constructor /origen/sitemap.xml /usr/share/nginx/html/

# nginx:alpine ya corre los workers como el usuario nginx.
EXPOSE 80

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget -q -O /dev/null http://127.0.0.1/ || exit 1

STOPSIGNAL SIGQUIT
CMD ["nginx", "-g", "daemon off;"]
