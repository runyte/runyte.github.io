(() => {
  const anchors = JSON.parse(
    document.querySelector("#guide-anchors").textContent,
  );
  const followLegacyAnchor = () => {
    let anchor;
    try {
      anchor = decodeURIComponent(location.hash.slice(1));
    } catch (_) {
      return;
    }
    const destination = anchors[anchor];
    if (destination && destination !== location.pathname) {
      location.replace(
        `${destination}${location.search}#${encodeURIComponent(anchor)}`,
      );
    }
  };
  followLegacyAnchor();
  window.addEventListener("hashchange", followLegacyAnchor);
  const sidebar = document.querySelector(".guide-sidebar");
  const current = sidebar.querySelector('[aria-current="page"]');
  if (current)
    sidebar.scrollTop = Math.max(
      0,
      current.offsetTop - sidebar.clientHeight / 3,
    );
  const contents = sidebar.querySelector("details");
  const narrow = matchMedia("(max-width: 760px)");
  const setContents = () => {
    contents.open = !narrow.matches;
  };
  setContents();
  narrow.addEventListener("change", setContents);
})();
