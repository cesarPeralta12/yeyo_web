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
  var ASUNTOS = {
    contacto: 'Nueva conversación desde la web',
    conferencia: 'Invitación a una conferencia',
    boletin: 'Nueva suscripción al boletín'
  };

  document.querySelectorAll('form[data-form]').forEach(function (form) {
    var salida = form.querySelector('.respuesta');
    var envio = form.querySelector('[type="submit"]');
    var rotulo = envio ? envio.querySelector('span') : null;
    var trampa = form.querySelector('[name="_honey"]');
    var tipo = form.dataset.form;
    var destino = form.dataset.destino;

    function responder(texto, error) {
      if (!salida) return;
      salida.hidden = false;
      salida.textContent = texto;
      salida.classList.toggle('respuesta--error', !!error);
    }

    function ocupado(si) {
      if (!envio) return;
      envio.disabled = si;
      if (rotulo) {
        if (si) {
          rotulo.dataset.previo = rotulo.textContent;
          rotulo.textContent = 'Enviando…';
        } else if (rotulo.dataset.previo) {
          rotulo.textContent = rotulo.dataset.previo;
        }
      }
    }

    // Si no hay endpoint, se abre el correo del visitante con el mensaje listo.
    function respaldoCorreo(datos) {
      var lineas = [];
      datos.forEach(function (v, k) {
        if (k.charAt(0) !== '_' && String(v).trim()) lineas.push(k + ': ' + v);
      });
      window.location.href = 'mailto:' + destino +
        '?subject=' + encodeURIComponent(ASUNTOS[tipo] || ASUNTOS.contacto) +
        '&body=' + encodeURIComponent(lineas.join('\n'));
      responder('Se abrió tu correo con el mensaje listo para enviar. Si no ocurrió, escribe a ' + destino + '.');
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();

      if (trampa && trampa.value) return;          // lo llenó un bot
      if (!form.checkValidity()) { form.reportValidity(); return; }

      var datos = new FormData(form);
      var endpoint = form.dataset.endpoint;

      if (!endpoint) { respaldoCorreo(datos); return; }

      var cuerpo = { _subject: ASUNTOS[tipo] || ASUNTOS.contacto, _template: 'table', _captcha: 'false' };
      datos.forEach(function (v, k) { cuerpo[k] = v; });

      ocupado(true);
      responder('');
      if (salida) salida.hidden = true;

      fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify(cuerpo)
      })
        .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return { ok: r.ok, j: j }; }); })
        .then(function (res) {
          ocupado(false);
          if (res.ok && String(res.j.success) !== 'false') {
            form.reset();
            responder(tipo === 'boletin'
              ? 'Listo. Te llegarán las nuevas ideas al correo.'
              : 'Gracias. Mensaje recibido, te respondo pronto.');
          } else {
            respaldoCorreo(datos);
          }
        })
        .catch(function () {
          ocupado(false);
          respaldoCorreo(datos);
        });
    });
  });

  /* ---------- año en el pie ---------- */
  var anio = document.querySelector('[data-anio]');
  if (anio) anio.textContent = new Date().getFullYear();
})();
