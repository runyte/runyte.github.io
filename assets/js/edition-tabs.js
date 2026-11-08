(() => {
  const root = document.querySelector("[data-edition-tabs]");
  const tabs = [...root.querySelectorAll('[role="tab"]')];
  const panelOf = (tab) => document.getElementById(tab.getAttribute("aria-controls"));

  const select = (active) => {
    tabs.forEach((tab) => {
      const selected = tab === active;
      tab.setAttribute("aria-selected", String(selected));
      tab.tabIndex = selected ? 0 : -1;
      panelOf(tab).hidden = !selected;
    });
  };

  // A link may point at a panel or at a heading inside one, so reveal it before scrolling.
  const followHash = () => {
    const id = decodeURIComponent(location.hash.slice(1));
    const target = id && document.getElementById(id);
    const panel = target && target.closest('[role="tabpanel"]');
    if (!panel) return false;
    select(tabs.find((tab) => panelOf(tab) === panel));
    target.scrollIntoView();
    return true;
  };

  tabs.forEach((tab, index) => {
    tab.addEventListener("click", () => {
      select(tab);
      history.replaceState(null, "", `#${tab.getAttribute("aria-controls")}`);
    });
    tab.addEventListener("keydown", (event) => {
      const step = { ArrowRight: 1, ArrowLeft: -1 }[event.key];
      if (!step) return;
      event.preventDefault();
      const next = tabs[(index + step + tabs.length) % tabs.length];
      next.focus();
      next.click();
    });
  });

  addEventListener("hashchange", followHash);
  if (!followHash()) select(tabs[0]);
})();
