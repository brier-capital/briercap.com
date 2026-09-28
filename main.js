(function () {
  "use strict";
  var d = document, h = d.documentElement;
  if (!h.classList.contains("motion")) return;

  // Scroll reveal: sections rise in once as they enter the viewport.
  if ("IntersectionObserver" in window) {
    h.classList.add("reveal-on");
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px" });
    d.querySelectorAll(".row").forEach(function (el) { io.observe(el); });
  }

  if (!h.classList.contains("intro")) return;

  var curtain = d.querySelector(".curtain");
  var mono = d.querySelector(".hero .monogram");
  var word = d.querySelector(".masthead .wordmark");
  var gold = mono.querySelector(".m-gold");
  var ink = mono.querySelector(".m-navy");
  var copy = [].slice.call(d.querySelectorAll(".hero .copy, .nav"));
  var anims = [], timers = [], done = false;

  function end() {
    if (done) return;
    done = true;
    timers.forEach(clearTimeout);
    h.classList.remove("intro", "intro-ink");
    anims.forEach(function (a) { a.cancel(); });
    if (curtain) curtain.remove();
    ["click", "keydown", "wheel", "touchstart"].forEach(function (t) {
      window.removeEventListener(t, end, true);
    });
  }

  function play(el, frames, opts) {
    opts.fill = "both";
    var a = el.animate(frames, opts);
    anims.push(a);
    return a;
  }

  // Box that places `el` at (x, y) with width w, as a transform from where it sits in the page.
  function placed(r, x, y, w) {
    var s = w / r.width;
    return "translate(" + (x - r.left) + "px," + (y - r.top) + "px) scale(" + s + ")";
  }

  function run() {
    if (done) return;
    var vw = window.innerWidth, vh = window.innerHeight;
    var mr = mono.getBoundingClientRect(), wr = word.getBoundingClientRect();

    // Centered lockup: monogram over wordmark.
    var mw = Math.min(vw * 0.36, vh * 0.32, 250), mh = mr.height * (mw / mr.width);
    var ww = Math.min(vw * 0.66, 360), wh = wr.height * (ww / wr.width);
    var gap = Math.max(26, mh * 0.2);
    var top = (vh - (mh + gap + wh)) / 2 - vh * 0.03;
    // Stack the lockup in the order the pieces end up in, so they never cross in flight: on narrow
    // screens the wordmark lands directly above the monogram.
    var stacked = wr.left < mr.right && mr.left < wr.right;
    var mFrom = placed(mr, (vw - mw) / 2, stacked ? top + wh + gap : top, mw);
    var wFrom = placed(wr, (vw - ww) / 2, stacked ? top : top + mh + gap, ww);

    var ease = "cubic-bezier(0.2, 0.7, 0.2, 1)";
    var fly = "cubic-bezier(0.75, 0, 0.2, 1)";
    var HOLD = 1350, FLY = 850;

    // 1. Assemble: navy strokes rise in, gold wipes up from the base, wordmark wipes left to right.
    play(mono, [{ opacity: 1, transform: mFrom }, { opacity: 1, transform: mFrom }], { duration: HOLD });
    // Opacity and clip-path only on the groups: a CSS transform would replace their SVG transform attribute.
    play(ink, [{ opacity: 0 }, { opacity: 1 }], { duration: 650, easing: ease });
    play(gold, [{ clipPath: "inset(100% 0 0 0)" }, { clipPath: "inset(0 0 0 0)" }],
      { duration: 800, delay: 250, easing: ease });
    play(word, [{ opacity: 1, transform: wFrom, clipPath: "inset(0 100% 0 0)" },
                { opacity: 1, transform: wFrom, clipPath: "inset(0 0 0 0)" }],
      { duration: 700, delay: 450, easing: ease });

    // 2. Fly: each piece travels to its place on the navy, then the curtain and the ink swap quickly
    // together as they land. A slow crossfade passes through a point where logo and ground match.
    var SWAP = FLY * 0.7;
    timers.push(setTimeout(function () {
      if (done) return;
      play(mono, [{ opacity: 1, transform: mFrom }, { opacity: 1, transform: "none" }],
        { duration: FLY, easing: fly });
      play(word, [{ opacity: 1, transform: wFrom }, { opacity: 1, transform: "none" }],
        { duration: FLY, easing: fly });
      play(curtain, [{ opacity: 1 }, { opacity: 0 }], { duration: 380, delay: SWAP, easing: "ease-out" });
      timers.push(setTimeout(function () { h.classList.remove("intro-ink"); }, SWAP));
      copy.forEach(function (el, i) {
        play(el, [{ opacity: 0, transform: "translateY(16px)" }, { opacity: 1, transform: "none" }],
          { duration: 700, delay: SWAP + 150 + i * 110, easing: ease });
      });
      timers.push(setTimeout(end, SWAP + 150 + copy.length * 110 + 750));
    }, HOLD));
  }

  // Any interaction skips straight to the page.
  ["click", "keydown", "wheel", "touchstart"].forEach(function (t) {
    window.addEventListener(t, end, true);
  });

  // Wait briefly for the web font so the hero has its final layout before measuring.
  var fonts = d.fonts && d.fonts.ready ? d.fonts.ready : Promise.resolve();
  Promise.race([fonts, new Promise(function (r) { setTimeout(r, 500); })]).then(function () {
    requestAnimationFrame(run);
  });
})();
