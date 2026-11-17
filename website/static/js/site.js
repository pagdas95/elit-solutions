// Mobile navigation and header state. The site works without JavaScript; this only adds the menu toggle.
(function () {
  var body = document.body;
  var toggle = document.querySelector("[data-nav-toggle]");
  var header = document.querySelector("[data-header]");

  function setOpen(open) {
    body.classList.toggle("nav-open", open);
    if (toggle) toggle.setAttribute("aria-expanded", String(open));
  }
  if (toggle) {
    toggle.addEventListener("click", function () { setOpen(!body.classList.contains("nav-open")); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") setOpen(false); });
    document.querySelectorAll("#site-nav a").forEach(function (a) {
      a.addEventListener("click", function () { setOpen(false); });
    });
  }
  function onScroll() { if (header) header.classList.toggle("scrolled", window.scrollY > 8); }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();
})();
