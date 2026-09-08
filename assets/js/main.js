/* YEYO VERA — comportamiento. Breve y funcional: revelar, conectar y dirigir. */
(function () {
  'use strict';

  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- menú móvil ---------- */
  var boton = document.querySelector('.hamburguesa');
  var menu = document.getElementById('menu-principal');

  if (boton && menu) {
    var cerrar = function () {
      menu.classList.remove('abierto');
      boton.setAttribute('aria-expanded', 'false');
      document.body.style.removeProperty('overflow');
    };

    boton.addEventListener('click', function () {
      var abierto = menu.classList.toggle('abierto');
      boton.setAttribute('aria-expanded', String(abierto));
      boton.setAttribute('aria-label', abierto ? 'Cerrar menú' : 'Abrir menú');
      document.body.style.overflow = abierto ? 'hidden' : '';
    });

    menu.addEventListener('click', function (e) {
      if (e.target.closest('a')) cerrar();
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && menu.classList.contains('abierto')) {
        cerrar();
        boton.focus();
      }
    });

    window.addEventListener('resize', function () {
      if (window.innerWidth > 900) cerrar();
    });
  }

  /* ---------- revelar al entrar en pantalla ---------- */
  var objetivos = document.querySelectorAll('.revelar');

  if (reduce || !('IntersectionObserver' in window)) {
    objetivos.forEach(function (el) { el.classList.add('visible'); });
  } else {
    var obs = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (en) {
        if (en.isIntersecting) {
          en.target.classList.add('visible');
          obs.unobserve(en.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    objetivos.forEach(function (el) { obs.observe(el); });
  }

  /* ---------- filtros de la página Ideas ---------- */
  var filtros = document.querySelectorAll('[data-filtro]');
  var notas = document.querySelectorAll('[data-categoria]');

  filtros.forEach(function (f) {
    f.addEventListener('click', function () {
      var cat = f.dataset.filtro;
      filtros.forEach(function (o) {
        var activo = o === f;
        o.classList.toggle('chip--activo', activo);
        o.setAttribute('aria-pressed', String(activo));
      });
      notas.forEach(function (n) {
        n.hidden = !(cat === 'todo' || n.dataset.categoria === cat);
      });
    });
  });

  /* ---------- formularios ---------- */
  document.querySelectorAll('form[data-form]').forEach(function (form) {
    var salida = form.querySelector('.respuesta');
    var envio = form.querySelector('[type="submit"]');
    var trampa = form.querySelector('.miel input');

    form.addEventListener('submit', function (e) {
      e.preventDefault();

      // anti-spam: si el campo oculto viene lleno, es un bot
      if (trampa && trampa.value) return;

      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }

      var texto = envio ? envio.querySelector('span').textContent : '';
      if (envio) {
        envio.disabled = true;
        envio.querySelector('span').textContent = 'Enviando…';
      }

      // Sin backend todavía: se abre el correo con el mensaje ya redactado.
      // Cuando exista endpoint, sustituir este bloque por un fetch().
      var datos = new FormData(form);
      var lineas = [];
      datos.forEach(function (v, k) {
        if (k !== 'website' && String(v).trim()) lineas.push(k + ': ' + v);
      });

      var asunto = form.dataset.form === 'conferencia'
        ? 'Invitación a conferencia'
        : 'Nueva conversación desde la web';

      window.location.href = 'mailto:' + (form.dataset.destino || 'hola@yeyovera.com') +
        '?subject=' + encodeURIComponent(asunto) +
        '&body=' + encodeURIComponent(lineas.join('\n'));

      if (salida) {
        salida.hidden = false;
        salida.textContent = 'Gracias. Se abrió tu correo con el mensaje listo para enviar. Si no ocurrió, escribe directamente a ' + (form.dataset.destino || 'hola@yeyovera.com') + '.';
      }

      window.setTimeout(function () {
        if (envio) {
          envio.disabled = false;
          envio.querySelector('span').textContent = texto;
        }
      }, 2500);
    });
  });

  /* ---------- año en el pie ---------- */
  var anio = document.querySelector('[data-anio]');
  if (anio) anio.textContent = new Date().getFullYear();
})();
