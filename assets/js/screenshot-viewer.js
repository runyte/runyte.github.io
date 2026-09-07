(() => {
  const viewer = document.querySelector(".screenshot-viewer");
  if (!viewer || typeof viewer.showModal !== "function") return;

  const image = viewer.querySelector(".screenshot-viewer__image");
  const caption = viewer.querySelector(".screenshot-viewer__caption");
  let opener;
  let pointerStartedOutside = false;

  document.querySelectorAll("[data-screenshot]").forEach((link) => {
    link.setAttribute("aria-haspopup", "dialog");
    link.addEventListener("click", (event) => {
      if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;

      event.preventDefault();
      opener = link;
      image.src = link.href;
      image.alt = link.querySelector("img").alt;
      caption.textContent = link.closest("figure").querySelector("figcaption").textContent;
      viewer.showModal();
      document.documentElement.classList.add("screenshot-viewer-open");
    });
  });

  const isOutside = (event) => {
    const rect = viewer.getBoundingClientRect();
    return event.clientX < rect.left || event.clientX > rect.right ||
      event.clientY < rect.top || event.clientY > rect.bottom;
  };

  viewer.addEventListener("pointerdown", (event) => {
    pointerStartedOutside = isOutside(event);
  });

  viewer.addEventListener("click", (event) => {
    if (pointerStartedOutside && isOutside(event)) viewer.close();
    pointerStartedOutside = false;
  });

  viewer.addEventListener("close", () => {
    document.documentElement.classList.remove("screenshot-viewer-open");
    opener?.focus({ preventScroll: true });
  });
})();
