(() => {
  const dialog = document.querySelector("#editor-dialog");
  if (!dialog?.showModal) return;
  const pages = JSON.parse(
    document.querySelector("#site-navigation").textContent,
  );
  const hints = document.querySelector("#key-hints");
  const mode = document.querySelector("#status-mode");
  const overview = document.querySelector("#overview-video");
  const navInput = document.querySelector("#navigator-query");
  const navResults = document.querySelector("#navigator-results");
  const commandInput = document.querySelector("#command-input");
  const commandResults = document.querySelector("#command-results");
  const commandMessage = document.querySelector("#command-message");
  const setting = document.querySelector("#shortcuts-enabled");
  let enabled = true;
  try {
    enabled = localStorage.getItem("runyte-shortcuts") !== "off";
  } catch (_) {
    /* Storage is optional. */
  }
  setting.checked = enabled;
  let pending = false;
  let view = null;
  let opener = null;
  let navIndex = 0;
  let filteredPages = [];
  let commandIndex = 0;
  let filteredCommands = [];
  let commandSelection = false;

  const actions = [
    {
      id: "help",
      keys: "Space ?",
      next: "?",
      label: "Help for this page",
      run: () => open("help"),
    },
    {
      id: "navigator",
      keys: "Space n",
      next: "n",
      label: "Navigate the website",
      run: () => open("navigator"),
    },
    {
      id: "documentation",
      keys: ":help",
      command: "help",
      label: "Open documentation",
      run: () => location.assign("/docs/"),
    },
    {
      id: "about",
      keys: ":about",
      command: "about",
      label: "Return to About",
      run: () => location.assign("/"),
    },
    {
      id: "demo",
      keys: ":demo",
      command: "demo",
      label: "Watch the demo (website command)",
      run: () => open("demo"),
    },
    {
      id: "command",
      keys: ":",
      label: "Open the command palette",
      run: () => open("command"),
    },
    {
      id: "quit",
      keys: ":q",
      command: "q",
      label: "Quit",
      run: () => {
        window.close();
        if (!window.closed) open("quit");
      },
    },
    {
      id: "features",
      command: "features",
      label: "Explore features",
      run: () => location.assign("/features/"),
    },
    {
      id: "install",
      command: "install",
      label: "Install Runyte",
      run: () => location.assign("/installation/"),
    },
    {
      id: "docs",
      command: "docs",
      label: "Browse documentation",
      run: () => location.assign("/docs/"),
    },
    ...["github", "repository"].map((command) => ({
      id: command,
      command,
      label: "Open the Runyte repository on GitHub",
      run: () => location.assign(pages.find((page) => page.id === "repository").url),
    })),
  ];
  const resetPrefix = () => {
    pending = false;
    hints.hidden = true;
  };
  const element = (tag, text, className) => {
    const node = document.createElement(tag);
    if (text) node.textContent = text;
    if (className) node.className = className;
    return node;
  };
  const run = (id) => {
    resetPrefix();
    actions.find((action) => action.id === id)?.run();
  };
  const title = {
    help: "[help] [RO]",
    navigator: "[navigator]",
    demo: "[demo]",
    quit: "[closed]",
    command: "[command]",
  };
  function open(nextView) {
    resetPrefix();
    if (!dialog.open) opener = document.activeElement;
    if (view === "demo") overview.pause();
    view = nextView;
    dialog.dataset.view = view;
    dialog.querySelectorAll(":scope > section").forEach((section) => {
      section.hidden = section.id !== `dialog-${view}`;
    });
    document.querySelector("#dialog-title").textContent = title[view];
    mode.textContent = view === "command" ? "CMD" : "NOR";
    if (view === "navigator") {
      navInput.value = "";
      navIndex = Math.max(
        0,
        pages.findIndex((page) => page.url === location.pathname),
      );
      renderNavigator();
    }
    if (view === "command") {
      commandInput.value = "";
      commandIndex = 0;
      commandSelection = false;
      renderCommands();
    }
    if (view === "help") {
      document.querySelector("#help-context").textContent =
        `You are viewing ${document.body.dataset.page}. Use Navigator to open another page, or :help to browse documentation.`;
    }
    if (view === "demo" && !overview.getAttribute("src"))
      overview.src = overview.dataset.src;
    if (!dialog.open) dialog.showModal();
    if (view === "navigator") navInput.focus();
    else if (view === "command") commandInput.focus();
    else dialog.querySelector("[data-close]").focus();
  }
  dialog.addEventListener("cancel", () => overview.pause());
  dialog.addEventListener("close", () => {
    overview.pause();
    view = null;
    mode.textContent = "NOR";
    if (opener?.isConnected) opener.focus();
  });
  dialog.addEventListener("click", (event) => {
    if (event.target.closest("[data-close]")) dialog.close();
    if (event.target === dialog) {
      const box = dialog.getBoundingClientRect();
      if (
        event.clientX < box.left ||
        event.clientX > box.right ||
        event.clientY < box.top ||
        event.clientY > box.bottom
      )
        dialog.close();
    }
  });
  function renderNavigator() {
    const words = navInput.value.trim().toLowerCase().split(/\s+/);
    filteredPages = pages.filter((page) =>
      words.every((word) =>
        `${page.title} ${page.description} ${(page.keywords || []).join(" ")}`
          .toLowerCase()
          .includes(word),
      ),
    );
    navIndex = Math.max(0, Math.min(navIndex, filteredPages.length - 1));
    navResults.replaceChildren(
      ...filteredPages.map((page, index) => {
        const row = element("li", "", index === navIndex ? "selected" : "");
        const link = element("a");
        link.href = page.url;
        if (page.url === location.pathname)
          link.setAttribute("aria-current", "page");
        link.append(
          element(
            "span",
            `${page.title}${page.url === location.pathname ? " [current]" : ""}`,
          ),
          element("small", page.description),
        );
        row.append(link);
        return row;
      }),
    );
    document.querySelector("#navigator-count").textContent =
      filteredPages.length
        ? `${filteredPages.length} pages · ${filteredPages[navIndex].title} selected`
        : "No matching pages.";
  }
  navInput.addEventListener("input", () => {
    navIndex = 0;
    renderNavigator();
  });
  navInput.addEventListener("keydown", (event) => {
    if (event.key === "ArrowDown" || event.key === "ArrowUp") {
      event.preventDefault();
      navIndex =
        (navIndex +
          (event.key === "ArrowDown" ? 1 : -1) +
          filteredPages.length) %
        (filteredPages.length || 1);
      renderNavigator();
      navResults
        .querySelector(".selected")
        ?.scrollIntoView({ block: "nearest" });
    } else if (event.key === "Enter" && filteredPages[navIndex]) {
      event.preventDefault();
      location.assign(filteredPages[navIndex].url);
    }
  });
  function renderCommands() {
    const query = commandInput.value.trim().replace(/^:/, "").toLowerCase();
    filteredCommands = actions.filter((action) =>
      action.command?.startsWith(query),
    );
    commandIndex = Math.max(
      0,
      Math.min(commandIndex, filteredCommands.length - 1),
    );
    commandResults.replaceChildren(
      ...filteredCommands.map((action, index) => {
        const row = element("li", "", index === commandIndex ? "selected" : "");
        const button = element("button");
        button.type = "button";
        button.dataset.action = action.id;
        button.append(
          element("span", `:${action.command}`),
          element("small", action.label),
        );
        row.append(button);
        return row;
      }),
    );
    commandMessage.textContent = filteredCommands.length
      ? "Tab complete · ↑ ↓ select · Enter run"
      : "Unknown command. Try :help, :about, or :demo.";
  }
  commandInput.addEventListener("input", () => {
    commandIndex = 0;
    commandSelection = false;
    renderCommands();
  });
  commandInput.addEventListener("keydown", (event) => {
    if (["ArrowDown", "ArrowUp"].includes(event.key)) {
      event.preventDefault();
      commandSelection = true;
      commandIndex =
        (commandIndex +
          (event.key === "ArrowDown" ? 1 : -1) +
          filteredCommands.length) %
        (filteredCommands.length || 1);
      renderCommands();
      commandResults
        .querySelector(".selected")
        ?.scrollIntoView({ block: "nearest" });
    } else if (
      event.key === "Tab" &&
      !event.shiftKey &&
      filteredCommands.length &&
      commandInput.value !== filteredCommands[commandIndex].command
    ) {
      event.preventDefault();
      commandInput.value = filteredCommands[commandIndex].command;
      commandSelection = false;
      commandIndex = 0;
      renderCommands();
    }
  });
  document
    .querySelector("#command-form")
    .addEventListener("submit", (event) => {
      event.preventDefault();
      const command = commandInput.value.trim().replace(/^:/, "").toLowerCase();
      const action = commandSelection
        ? filteredCommands[commandIndex]
        : actions.find((item) => item.command === command);
      if (action) run(action.id);
      else
        commandMessage.textContent =
          "Unknown command. Use Tab to complete, or type :help.";
    });
  const shortcutReference = document.querySelector("#shortcut-reference");
  actions
    .filter((action) => action.keys)
    .forEach((action) => {
      const button = element("button");
      button.type = "button";
      button.dataset.action = action.id;
      button.append(element("kbd", action.keys), element("span", action.label));
      shortcutReference.append(button);
    });
  hints.append(element("span", "Space", "hint-prefix"));
  actions
    .filter((action) => action.next)
    .forEach((action) => {
      const button = element("button");
      button.type = "button";
      button.dataset.action = action.id;
      button.append(element("kbd", action.next), element("span", action.id));
      hints.append(button);
    });
  hints.append(element("span", "Esc to cancel", "muted"));
  setting.addEventListener("change", () => {
    enabled = setting.checked;
    resetPrefix();
    try {
      localStorage.setItem("runyte-shortcuts", enabled ? "on" : "off");
    } catch (_) {
      /* Storage is optional. */
    }
  });
  document.addEventListener("click", (event) => {
    const target = event.target.closest("[data-action]");
    if (
      !target ||
      event.ctrlKey ||
      event.metaKey ||
      event.shiftKey ||
      event.altKey
    )
      return;
    event.preventDefault();
    run(target.dataset.action);
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      resetPrefix();
      return;
    }
    if (
      !enabled ||
      event.defaultPrevented ||
      event.isComposing ||
      event.repeat ||
      event.key === "Shift" ||
      event.ctrlKey ||
      event.altKey ||
      event.metaKey
    )
      return;
    if (document.querySelector("dialog[open]")) return;
    if (
      event.target.closest(
        'input,textarea,select,button,a,summary,video,audio,[contenteditable]:not([contenteditable="false"])',
      )
    )
      return;
    if (pending) {
      const action = actions.find((item) => item.next === event.key);
      resetPrefix();
      if (action) {
        event.preventDefault();
        run(action.id);
      }
      return;
    }
    if (event.key === " ") {
      event.preventDefault();
      pending = true;
      hints.hidden = false;
    } else if (event.key === ":") {
      event.preventDefault();
      run("command");
    }
  });
  document.addEventListener("focusin", (event) => {
    if (!hints.contains(event.target)) resetPrefix();
  });
  window.addEventListener("blur", resetPrefix);
  window.addEventListener("pagehide", () => {
    resetPrefix();
    overview.pause();
  });
  document.addEventListener("visibilitychange", () => {
    if (document.hidden) {
      resetPrefix();
      overview.pause();
    }
  });
  document.addEventListener(
    "play",
    (event) => {
      if (event.target instanceof HTMLVideoElement)
        document.querySelectorAll("video").forEach((video) => {
          if (video !== event.target) video.pause();
        });
    },
    true,
  );
  document.documentElement.classList.add("js");
})();
