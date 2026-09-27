// Run with Playwright installed, or set PLAYWRIGHT_MODULE to its module path.
// BASE_URL defaults to the local Hugo server. CHROME_BIN can select a browser.
const assert = require("node:assert/strict");
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || "playwright");
const base = process.env.BASE_URL || "http://127.0.0.1:1313";

(async () => {
  const browser = await chromium.launch({
    headless: true,
    ...(process.env.CHROME_BIN
      ? { executablePath: process.env.CHROME_BIN }
      : {}),
  });
  try {
    const page = await browser.newPage({
      viewport: { width: 1440, height: 1000 },
    });
    const errors = [];
    const mediaRequests = [];
    page.on("pageerror", (error) => errors.push(error.message));
    page.on("request", (request) => {
      if (/\.mp4(?:[?#]|$)/.test(request.url()))
        mediaRequests.push(request.url());
    });
    const home = async () => {
      await page.goto(base);
      await page.waitForSelector("html.js");
      await page.locator("#main").focus();
    };
    const key = (value) => page.keyboard.press(value);
    const openCommand = async (value) => {
      await page.locator("#main").focus();
      await key(":");
      await page.locator("#command-input").fill(value);
      await key("Enter");
    };
    await home();
    assert.equal(mediaRequests.length, 0, "Home should not load video data");
    await key("Space");
    assert.equal(await page.locator("#key-hints").isVisible(), true);
    await key("Escape");
    assert.equal(await page.locator("#key-hints").isVisible(), false);
    await key("Space");
    await key("x");
    assert.equal(await page.locator("#key-hints").isVisible(), false);
    await key("Space");
    await page.keyboard.down("Shift");
    assert.equal(
      await page.locator("#key-hints").isVisible(),
      true,
      "Shift must preserve the pending Space sequence",
    );
    await key("?");
    await page.keyboard.up("Shift");
    assert.equal(await page.locator("#dialog-help").isVisible(), true);
    await key("Escape");
    assert.equal(
      await page
        .locator("#main")
        .evaluate((node) => node === document.activeElement),
      true,
    );

    await key("Space");
    await key("n");
    await page.locator("#navigator-query").fill("nothing-matches-this");
    assert.equal(await page.locator("#navigator-results li").count(), 0);
    await key("ArrowDown");
    await page.locator("#navigator-query").fill("plugins");
    await key("Enter");
    await page.waitForURL("**/plugins/");
    await openCommand("about");
    await page.waitForURL(`${base}/`);
    await openCommand("help");
    await page.waitForURL("**/docs/");
    assert.equal(await page.locator('.site-nav a[href="/docs/user-guide/"]').count(), 0);
    assert.equal(await page.locator('.site-nav a[href="/help/"]').count(), 0);
    await page.goBack();
    await page.waitForURL(`${base}/`);

    // Intercept GitHub so the check verifies navigation without external requests.
    const repositoryURL = "https://github.com/runyte/runyte";
    await page.route(repositoryURL, (route) =>
      route.fulfill({
        contentType: "text/html",
        body: "Repository destination",
      }),
    );
    await page.locator("#main").focus();
    await key("Space");
    await key("n");
    for (const term of ["github", "repo", "repository", "code", "source"]) {
      await page.locator("#navigator-query").fill(term);
      assert.equal(
        await page
          .locator(`#navigator-results a[href="${repositoryURL}"]`)
          .count(),
        1,
        `Repository must be searchable by ${term}`,
      );
    }
    await key("Enter");
    await page.waitForURL(repositoryURL);
    for (const command of ["github", "repository"]) {
      await home();
      await openCommand(command);
      await page.waitForURL(repositoryURL);
    }
    await home();

    await openCommand("unknown");
    assert.match(
      await page.locator("#command-message").textContent(),
      /Unknown command/,
    );
    await page.locator("#command-input").fill("de");
    await key("Tab");
    assert.equal(await page.locator("#command-input").inputValue(), "demo");
    await key("Enter");
    assert.equal(await page.locator("#dialog-demo").isVisible(), true);
    await page.locator("#overview-video").evaluate((video) => video.play());
    await key("Escape");
    await page.waitForFunction(
      () =>
        !document.querySelector("#editor-dialog").open &&
        document.querySelector("#overview-video").paused,
    );
    assert.equal(
      await page.locator("#overview-video").evaluate((video) => video.paused),
      true,
    );

    // A normal browser tab can refuse close; exercise that path without closing the test page.
    await page.evaluate(() => {
      window.close = () => {};
    });
    await openCommand("q");
    assert.equal(await page.locator("#dialog-quit").isVisible(), true);
    await page.locator("#dialog-quit [data-close]").click();
    assert.equal(await page.locator("#editor-dialog").isVisible(), false);

    await page.locator(".nav-keyboard").click();
    await page.locator("#shortcuts-enabled").uncheck();
    await key("Escape");
    assert.equal(
      await page
        .locator(".nav-keyboard")
        .evaluate((node) => node === document.activeElement),
      true,
    );
    await page.locator("#main").focus();
    await key("Space");
    assert.equal(await page.locator("#key-hints").isVisible(), false);
    await page.reload();
    await page.locator(".nav-keyboard").click();
    assert.equal(await page.locator("#shortcuts-enabled").isChecked(), false);
    await page.locator("#shortcuts-enabled").check();
    await key("Escape");

    mediaRequests.length = 0;
    await page.goto(`${base}/features/`);
    assert.equal(await page.locator("#key-hints").count(), 1);
    await page.locator("#main").focus();
    await key("Space");
    assert.equal(await page.locator(".key-hints").isVisible(), true);
    await key("Escape");
    assert.equal(await page.locator("#discover-keys").textContent(), "Key hints");
    assert.equal(await page.locator("[data-clip]").count(), 7);
    assert.equal(mediaRequests.length, 0, "Features should not load video data before play");
    const sources = await page.locator("[data-clip] video").evaluateAll(
      (videos) => videos.map((video) => video.src),
    );
    assert.equal(new Set(sources).size, 7, "Each feature has a dedicated recording");
    await page.locator("[data-clip]").first().locator("button").click();
    await page.waitForFunction(
      () => !document.querySelector("[data-clip] video").paused,
    );
    await page.locator("[data-clip]").nth(1).locator("button").click();
    await page.waitForFunction(() => {
      const videos = document.querySelectorAll("[data-clip] video");
      return !videos[1].paused && videos[0].paused;
    });
    assert.equal(
      await page
        .locator("[data-clip] video")
        .first()
        .evaluate((video) => video.paused),
      true,
    );
    const second = page.locator("[data-clip] video").nth(1);
    await second.evaluate((video) => {
      video.currentTime = video.duration - 0.05;
    });
    await page.waitForFunction(
      () => document.querySelectorAll("[data-clip] video")[1].paused,
    );
    await page.locator("[data-clip]").nth(1).locator("button").click();
    await page.waitForFunction(() => {
      const video = document.querySelectorAll("[data-clip] video")[1];
      return !video.paused && video.currentTime < 1;
    });

    await page.goto(`${base}/docs/user-guide/`);
    await page
      .locator(
        '.guide-toc a[href="/docs/user-guide/feature-reference/workspaces-and-modes/"]',
      )
      .click();
    await page.waitForURL("**/feature-reference/workspaces-and-modes/");
    assert.equal(
      await page.locator(".guide-toc [aria-current=page]").textContent(),
      "Workspaces and modes",
    );
    assert.equal(
      await page.locator(".guide-reading h1").textContent(),
      "Workspaces and modes",
    );
    assert.equal(
      await page.locator(".guide-reading #syntax-highlighting").count(),
      0,
    );
    const sidebarScroll = await page
      .locator(".guide-sidebar")
      .evaluate((node) => node.scrollTop);
    await page.locator(".guide-reading").evaluate((node) => {
      node.scrollTop = 500;
    });
    assert.equal(
      await page.locator(".guide-sidebar").evaluate((node) => node.scrollTop),
      sidebarScroll,
    );
    assert.equal(await page.evaluate(() => window.scrollY), 0);
    await page.locator(".guide-reading").evaluate((node) => {
      node.scrollTop = 0;
    });
    await page.screenshot({ path: "/tmp/runyte-guide-desktop.png" });
    await page.goto(`${base}/docs/user-guide/#terminals-1`);
    await page.waitForURL("**/key-bindings/terminals-1/#terminals-1");
    assert.equal(
      await page.locator(".guide-reading h1").textContent(),
      "Terminals",
    );
    await page.goBack();
    await page.waitForURL("**/feature-reference/workspaces-and-modes/");

    await home();
    await page.screenshot({ path: "/tmp/runyte-home-desktop.png" });
    await key("Space");
    await key("n");
    await page.screenshot({ path: "/tmp/runyte-navigator-desktop.png" });
    await key("Escape");
    await page.setViewportSize({ width: 390, height: 844 });
    await page.screenshot({ path: "/tmp/runyte-home-mobile.png" });
    for (const route of [
      "/",
      "/features/",
      "/installation/",
      "/plugins/",
      "/screenshots/",
      "/performance/",
      "/docs/",
      "/docs/user-guide/",
      "/docs/user-guide/install-and-run/windows-support/",
      "/guides/from-helix/",
    ]) {
      await page.goto(`${base}${route}`);
      assert.equal(
        await page.evaluate(
          () => document.documentElement.scrollWidth <= innerWidth,
        ),
        true,
        `Horizontal overflow on ${route}`,
      );
    }
    await page.goto(`${base}/docs/user-guide/`);
    assert.equal(
      await page.locator(".guide-contents").getAttribute("open"),
      null,
    );
    await page.locator(".guide-contents summary").click();
    await page
      .locator(
        '.guide-toc a[href="/docs/user-guide/install-and-run/windows-support/"]',
      )
      .click();
    await page.waitForURL("**/install-and-run/windows-support/");
    await page.screenshot({ path: "/tmp/runyte-guide-mobile.png" });
    const noJS = await browser.newContext({
      javaScriptEnabled: false,
      viewport: { width: 390, height: 844 },
    });
    const plain = await noJS.newPage();
    await plain.goto(`${base}/help/`);
    await plain.waitForURL("**/docs/");
    await plain.goto(base);
    await plain.locator(".site-nav a", { hasText: "Plugins" }).click();
    await plain.waitForURL("**/plugins/");
    await plain.goto(base);
    assert.equal(
      await plain.locator("[data-action=quit]").first().isVisible(),
      false,
    );
    await plain.locator(".about-links a", { hasText: "Install" }).click();
    await plain.waitForURL("**/installation/");
    await plain.goto(`${base}/docs/user-guide/#windows-support`);
    const legacy = plain.locator("#windows-support.guide-legacy-anchor");
    assert.equal(await legacy.isVisible(), true);
    await legacy.locator("a").click();
    await plain.waitForURL(
      "**/install-and-run/windows-support/#windows-support",
    );
    await plain
      .locator('.guide-toc a[href="/docs/user-guide/key-bindings/"]')
      .click();
    await plain.waitForURL("**/docs/user-guide/key-bindings/");
    assert.deepEqual(errors, [], "Browser errors");
    console.log(
      "Passed: key sequences, navigation, commands, completion, focus, quit fallback, shortcut settings, video playback, mobile overflow, and no-JS links.",
    );
  } finally {
    await browser.close();
  }
})().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
