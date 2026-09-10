(() => {
  const players = document.querySelectorAll("[data-video-player]");
  if (!players.length) return;

  const formatTime = (seconds) => {
    if (!Number.isFinite(seconds)) return "0:00";
    const total = Math.max(0, Math.round(seconds));
    const minutes = Math.floor(total / 60);
    const secs = String(total % 60).padStart(2, "0");
    return `${minutes}:${secs}`;
  };

  players.forEach((player) => {
    const video = player.querySelector(".video-player__media");
    const frame = player.querySelector(".video-player__frame");
    const bigPlay = player.querySelector(".video-player__big-play");
    const playButton = player.querySelector(".video-player__play");
    const muteButton = player.querySelector(".video-player__mute");
    const fullscreenButton = player.querySelector(".video-player__fullscreen");
    const seek = player.querySelector("[data-seek]");
    const seekFill = player.querySelector("[data-seek-fill]");
    const seekThumb = player.querySelector("[data-seek-thumb]");
    const currentEl = player.querySelector("[data-current]");
    const durationEl = player.querySelector("[data-duration]");
    if (!video || !playButton || !seek) return;

    const setPlayingState = (playing) => {
      player.classList.toggle("is-playing", playing);
      playButton.setAttribute("aria-pressed", String(playing));
      playButton.setAttribute("aria-label", playing ? "Pause" : "Play");
      playButton.querySelector(".icon-play").hidden = playing;
      playButton.querySelector(".icon-pause").hidden = !playing;
    };

    const togglePlay = () => {
      if (video.paused || video.ended) video.play();
      else video.pause();
    };

    const setSeekRatio = (ratio) => {
      const percent = Math.min(100, Math.max(0, ratio * 100));
      seekFill.style.width = `${percent}%`;
      seekThumb.style.left = `${percent}%`;
      seek.setAttribute("aria-valuenow", String(Math.round(percent)));
    };

    const seekToClientX = (clientX) => {
      const rect = seek.getBoundingClientRect();
      const ratio = rect.width ? (clientX - rect.left) / rect.width : 0;
      const clamped = Math.min(1, Math.max(0, ratio));
      if (Number.isFinite(video.duration)) video.currentTime = clamped * video.duration;
      setSeekRatio(clamped);
    };

    bigPlay?.addEventListener("click", togglePlay);

    frame?.addEventListener("click", (event) => {
      if (bigPlay?.contains(event.target)) return;
      togglePlay();
    });

    playButton.addEventListener("click", togglePlay);

    video.addEventListener("play", () => setPlayingState(true));
    video.addEventListener("pause", () => setPlayingState(false));
    video.addEventListener("ended", () => setPlayingState(false));

    video.addEventListener("loadedmetadata", () => {
      if (durationEl) durationEl.textContent = formatTime(video.duration);
    });

    video.addEventListener("timeupdate", () => {
      if (currentEl) currentEl.textContent = formatTime(video.currentTime);
      if (video.duration) setSeekRatio(video.currentTime / video.duration);
    });

    let dragging = false;

    seek.addEventListener("pointerdown", (event) => {
      dragging = true;
      seek.setPointerCapture(event.pointerId);
      seekToClientX(event.clientX);
    });

    seek.addEventListener("pointermove", (event) => {
      if (dragging) seekToClientX(event.clientX);
    });

    const stopDragging = () => {
      dragging = false;
    };

    seek.addEventListener("pointerup", stopDragging);
    seek.addEventListener("pointercancel", stopDragging);

    seek.addEventListener("keydown", (event) => {
      if (!Number.isFinite(video.duration)) return;
      const step = 5;
      if (event.key === "ArrowRight") {
        event.preventDefault();
        video.currentTime = Math.min(video.duration, video.currentTime + step);
      } else if (event.key === "ArrowLeft") {
        event.preventDefault();
        video.currentTime = Math.max(0, video.currentTime - step);
      } else if (event.key === "Home") {
        event.preventDefault();
        video.currentTime = 0;
      } else if (event.key === "End") {
        event.preventDefault();
        video.currentTime = video.duration;
      }
    });

    const setMutedState = (muted) => {
      if (!muteButton) return;
      muteButton.setAttribute("aria-pressed", String(muted));
      muteButton.setAttribute("aria-label", muted ? "Unmute" : "Mute");
      muteButton.querySelector(".icon-unmuted").hidden = muted;
      muteButton.querySelector(".icon-muted").hidden = !muted;
    };

    muteButton?.addEventListener("click", () => {
      video.muted = !video.muted;
      setMutedState(video.muted);
    });

    fullscreenButton?.addEventListener("click", () => {
      if (document.fullscreenElement) document.exitFullscreen();
      else player.requestFullscreen?.();
    });

    setPlayingState(false);
    setMutedState(video.muted);
    setSeekRatio(0);
  });
})();
