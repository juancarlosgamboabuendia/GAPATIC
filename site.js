(function () {
  var toggle = document.querySelector(".nav-toggle");
  var panel = document.getElementById("nav-panel");
  if (!toggle || !panel) return;

  function setOpen(open) {
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    toggle.setAttribute("aria-label", open ? "Cerrar menú" : "Abrir menú");
    document.body.classList.toggle("nav-open", open);
  }

  toggle.addEventListener("click", function () {
    setOpen(toggle.getAttribute("aria-expanded") !== "true");
  });

  panel.querySelectorAll("a").forEach(function (link) {
    link.addEventListener("click", function () { setOpen(false); });
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") setOpen(false);
  });
})();

(function () {
  var header = document.querySelector(".site-header");
  if (!header) return;
  function onScroll() {
    header.classList.toggle("is-scrolled", window.scrollY > 40);
  }
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });
})();

(function () {
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var reveals = document.querySelectorAll(".reveal");

  function showHeroReveals() {
    document.querySelectorAll(".hero .reveal, .page-hero .reveal, .article-head.reveal").forEach(function (el) {
      el.classList.add("is-visible");
    });
  }

  if (reduceMotion) {
    reveals.forEach(function (el) { el.classList.add("is-visible"); });
    return;
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", showHeroReveals);
  } else {
    requestAnimationFrame(function () {
      requestAnimationFrame(showHeroReveals);
    });
  }

  if (!("IntersectionObserver" in window)) {
    reveals.forEach(function (el) { el.classList.add("is-visible"); });
    return;
  }

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        io.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });

  reveals.forEach(function (el) { io.observe(el); });
})();

(function () {
  var form = document.getElementById("contact-form");
  if (!form) return;

  var servicioMap = {
    ConsultoriaIA: "Consulta sobre Consultoría Estratégica en IA",
    DesarrolloIA: "Consulta sobre Soluciones de IA a medida",
    DatosIA: "Consulta sobre Innovación con datos",
    ConsultaIA: "Consulta IA"
  };

  try {
    var params = new URLSearchParams(window.location.search);
    var servicio = params.get("servicio");
    var asunto = params.get("asunto");
    var subjectEl = form.querySelector('[name="asunto"]');
    if (subjectEl) {
      if (servicio && servicioMap[servicio]) subjectEl.value = servicioMap[servicio];
      else if (asunto) subjectEl.value = servicioMap[asunto] || asunto;
    }
  } catch (err) {}

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var data = new FormData(form);
    var nombre = (data.get("nombre") || "").toString().trim();
    var org = (data.get("organizacion") || "").toString().trim();
    var correo = (data.get("correo") || data.get("email") || "").toString().trim();
    var asuntoVal = (data.get("asunto") || "").toString().trim();
    var mensaje = (data.get("mensaje") || "").toString().trim();
    var subject = asuntoVal || ("Consulta GAPATIC" + (nombre ? " — " + nombre : ""));
    var bodyLines = [
      "Nombre: " + nombre,
      "Organización: " + org,
      "Correo: " + correo
    ];
    if (asuntoVal) bodyLines.push("Asunto: " + asuntoVal);
    bodyLines.push("", mensaje);
    var addr = "juancarlosgamboabuendia@gapatic.com";
    window.location.href =
      "mailto:" + addr + "?subject=" + encodeURIComponent(subject) +
      "&body=" + encodeURIComponent(bodyLines.join("\n"));
  });
})();
