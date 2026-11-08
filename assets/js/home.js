(() => {
  const root = document.documentElement;
  const hero = document.querySelector("[data-hero]");
  const video = hero.querySelector("[data-window-video]");
  const motion = matchMedia("(prefers-reduced-motion: no-preference)");
  const wide = matchMedia("(min-width: 761px)");

  const clamp = (value) => Math.min(1, Math.max(0, value));
  const ramp = (from, to, value) => clamp((value - from) / (to - from));
  const ease = (t) => t * t * (3 - 2 * t);
  const mix = (a, b, t) => a + (b - a) * t;
  const set = (name, value) => hero.style.setProperty(name, value.toFixed(4));

  let inView = true;
  const sync = () => {
    const shouldPlay =
      inView && !document.hidden && (hero.dataset.playing === "yes" || !sequenceOn());
    if (!sequenceOn() && !motion.matches) return;
    if (shouldPlay && video.paused) video.play().catch(() => {});
    if (!shouldPlay && !video.paused) video.pause();
  };
  const sequenceOn = () => motion.matches && wide.matches;

  let queued = false;
  const paint = () => {
    queued = false;
    if (!sequenceOn()) return;
    const box = hero.getBoundingClientRect();
    const p = clamp(-box.top / (box.height - innerHeight));

    const leave = ease(ramp(0, 0.13, p));
    set("--copy", 1 - leave);
    set("--copy-y", -7 * leave);
    hero.style.setProperty("--copy-events", leave > 0.5 ? "none" : "auto");

    const rise = ease(ramp(0.06, 0.3, p));
    const grow = ease(ramp(0.5, 0.74, p));
    set("--win-y", mix(46, 0, rise));
    set("--win-s", mix(mix(0.62, 0.8, rise), 1, grow));

    set("--strip", ease(ramp(0.22, 0.32, p)));
    set("--typed", ramp(0.36, 0.5, p));
    const swap = ease(ramp(0.5, 0.64, p));
    set("--swap", swap);
    set("--lit", grow);

    // The still in the terminal frame is the video's first frame, so start there.
    const playing = p > 0.42 ? "yes" : "no";
    if (playing === "yes" && hero.dataset.playing !== "yes" && video.readyState)
      video.currentTime = 0;
    hero.dataset.playing = playing;
    sync();
  };
  const request = () => {
    if (queued) return;
    queued = true;
    requestAnimationFrame(paint);
  };

  addEventListener("scroll", request, { passive: true });
  addEventListener("resize", request);
  motion.addEventListener("change", request);
  wide.addEventListener("change", request);
  document.addEventListener("visibilitychange", sync);
  new IntersectionObserver((entries) => {
    inView = entries[entries.length - 1].isIntersecting;
    sync();
  }).observe(video);
  if (!motion.matches) video.controls = true;
  paint();

  const reveals = document.querySelectorAll(".reveal");
  if (root.classList.contains("fx")) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("in");
          observer.unobserve(entry.target);
        });
      },
      { rootMargin: "0px 0px -8% 0px" },
    );
    reveals.forEach((element) => observer.observe(element));
  }

  const install = document.querySelector("[data-install]");
  const tabs = [...install.querySelectorAll('[role="tab"]')];
  const select = (active) => {
    tabs.forEach((tab) => {
      const selected = tab === active;
      tab.setAttribute("aria-selected", String(selected));
      document.getElementById(tab.getAttribute("aria-controls")).hidden = !selected;
    });
  };
  tabs.forEach((tab) => tab.addEventListener("click", () => select(tab)));
  select(tabs[0]);

  install.querySelectorAll("[data-copy-line]").forEach((button) => {
    button.addEventListener("click", async () => {
      const text = button.parentElement.querySelector("code").textContent;
      try {
        await navigator.clipboard.writeText(text);
        button.textContent = "Copied";
      } catch {
        button.textContent = "Press Ctrl-C";
        getSelection().selectAllChildren(button.parentElement.querySelector("code"));
      }
      setTimeout(() => {
        button.textContent = "Copy";
      }, 1600);
    });
  });
})();
