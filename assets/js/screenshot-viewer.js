(() => {
  const viewer = document.querySelector(".screenshot-viewer");
  if (!viewer || typeof viewer.showModal !== "function") return;

  const image = viewer.querySelector(".screenshot-viewer__image");
  const caption = viewer.querySelector(".screenshot-viewer__caption");
  const links = [...document.querySelectorAll("[data-screenshot]")];
  const previous = viewer.querySelector(".screenshot-viewer__previous");
  const next = viewer.querySelector(".screenshot-viewer__next");
  const hasGallery = links.length > 1;
  let currentIndex = 0;
  let opener;
  let pointerStartedOutside = false;

  previous.hidden = next.hidden = !hasGallery;
  viewer.querySelector(".screenshot-viewer__stage").classList.toggle("screenshot-viewer__stage--gallery", hasGallery);

  const showScreenshot = (index) => {
    currentIndex = (index + links.length) % links.length;
    const link = links[currentIndex];
    image.src = link.href;
    image.alt = link.querySelector("img").alt;
    caption.textContent = link.closest("figure").querySelector("figcaption").textContent;
  };

  previous.addEventListener("click", () => showScreenshot(currentIndex - 1));
  next.addEventListener("click", () => showScreenshot(currentIndex + 1));

  viewer.addEventListener("keydown", (event) => {
    if (!hasGallery || event.altKey || event.ctrlKey || event.metaKey) return;
    if (event.key !== "ArrowLeft" && event.key !== "ArrowRight") return;
    event.preventDefault();
    showScreenshot(currentIndex + (event.key === "ArrowRight" ? 1 : -1));
  });

  links.forEach((link, index) => {
    link.setAttribute("aria-haspopup", "dialog");
    link.addEventListener("click", (event) => {
      if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;

      event.preventDefault();
      opener = link;
      showScreenshot(index);
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
