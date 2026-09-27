(() => {
  document.querySelectorAll("[data-clip]").forEach((figure) => {
    const video = figure.querySelector("video");
    const start = Number(figure.dataset.start || 0);
    const end = Number(figure.dataset.end || Infinity);
    const duration = Number(figure.dataset.duration || end - start);
    const reset = () => {
      video.currentTime = start;
    };
    video.addEventListener("loadedmetadata", reset, { once: true });
    video.addEventListener("play", () => {
      if (video.currentTime < start || video.currentTime >= end - 0.05) reset();
    });
    video.addEventListener("timeupdate", () => {
      if (!video.paused && video.currentTime >= end) video.pause();
    });
    const replay = document.createElement("button");
    replay.type = "button";
    replay.textContent = `▶ Play ${Number.isFinite(duration) ? `${Math.round(duration)}-second ` : ""}clip`;
    replay.addEventListener("click", () => {
      if (video.readyState) reset();
      video.play().catch(() => {
        /* Native controls remain available. */
      });
    });
    figure.insertBefore(replay, video);
  });
})();
