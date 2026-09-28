// Runs in <head>, before first paint: sets the classes style.css uses to gate motion and the intro.
(function (h) {
  h.classList.add("js");
  if (!window.matchMedia || matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  h.classList.add("motion");
  var force = /[?&]intro\b/.test(location.search);
  try { if (sessionStorage.getItem("bc-intro") && !force) return; sessionStorage.setItem("bc-intro", "1"); } catch (e) {}
  if (window.scrollY === 0 && !location.hash) h.classList.add("intro", "intro-ink");
})(document.documentElement);
