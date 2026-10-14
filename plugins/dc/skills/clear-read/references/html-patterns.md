# HTML patterns for a clear-read page

Read this file when the output is an HTML page (a report, a dashboard, a guide, a published artifact).
Each pattern is a snippet to copy, with the rule it serves.
The markers are shown in English.
The Portuguese forms are "Como ler:", "Ponto-chave:", "Onde a analogia falha:", "Contexto extra" and the progress marker "Conceito N de M" (concept N of M).

The page stays self-contained: one file, no remote images, no remote scripts outside the hosts the platform allows.
Every pattern works in light and dark mode through the tokens below, and fits a phone (about 360px of content width).

## 1. Theme tokens, light and dark

Define the colors once as tokens, redefine them for dark mode, and give `body` an explicit background.
The two dark blocks are both needed: one follows the system setting, the other a `data-theme="dark"` attribute set by the host.

```html
<style>
:root{
  --bg:#F3F5F4;--surface:#FFFFFF;--ink:#18212B;--muted:#56616C;--line:#D6DDE0;
  --accent:#1F5E8C;--accent-soft:#E3EDF5;
  --good:#236648;--good-bg:#E4F2EA;--warn:#8A5A00;--warn-bg:#FBF0D9;--bad:#B3413B;--bad-bg:#F7E3E1;
  --extra-bg:#F1F3EA;--extra-edge:#8E9A5A;
  --body:system-ui,sans-serif;--mono:ui-monospace,monospace;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){color-scheme:dark;
  --bg:#11171D;--surface:#18212A;--ink:#E6ECF0;--muted:#9AA8B3;--line:#2C3843;
  --accent:#7DB3DE;--accent-soft:#1D3448;
  --good:#6CC79C;--good-bg:#16302A;--warn:#E4B04E;--warn-bg:#33291A;--bad:#EE8A83;--bad-bg:#3A2020;
  --extra-bg:#1F2A1C;--extra-edge:#9DB36B;}}
:root[data-theme="dark"]{color-scheme:dark;
  --bg:#11171D;--surface:#18212A;--ink:#E6ECF0;--muted:#9AA8B3;--line:#2C3843;
  --accent:#7DB3DE;--accent-soft:#1D3448;
  --good:#6CC79C;--good-bg:#16302A;--warn:#E4B04E;--warn-bg:#33291A;--bad:#EE8A83;--bad-bg:#3A2020;
  --extra-bg:#1F2A1C;--extra-edge:#9DB36B;}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--ink);font-family:var(--body);font-size:17px;line-height:1.6;margin:0;padding:0 16px}
.wrap{max-width:720px;margin:0 auto;padding:24px 0 64px}
p{margin:0 0 12px;max-width:68ch}
</style>
```

## 2. One sentence per line, one topic per block (Rule 1)

End each sentence with `<br>`, and wrap each topic in its own `<p>`.
The blank space between two `<p>` elements is the topic break.

```html
<p>A read-through cache is a fast store in front of the database.<br>
When the app asks for a value, the cache answers if it holds that value.<br>
Otherwise, the cache fetches the value and keeps a copy.</p>

<p><strong>Key point:</strong> the cache answers most reads, so the database sees only the misses.</p>
```

## 3. Progress marker at the top of each concept (Rule 1)

A reader who comes back after an interruption sees where he is without scrolling.
The marker carries the concept's position and the section heading carries its content.

```html
<style>
.marker{display:inline-block;font-family:var(--mono);font-size:.78rem;letter-spacing:.04em;color:var(--muted);text-transform:uppercase;margin:0 0 4px}
</style>

<section id="c2">
  <span class="marker">Concept 2 of 4</span>
  <h2>A short time limit keeps the copy fresh</h2>
  <p>The central idea here is that every copy expires.<br> ...</p>
</section>
```

## 4. A visual with its "How to read" line and its conclusion (Rule 7)

Every visual sits in a `<figure>`.
The caption starts with "How to read:" and says what the boxes, arrows, axes or colors mean.
The second line is the conclusion, in bold, so a reader who skips the picture still gets the point.

```html
<style>
figure.vis{margin:0 0 14px;background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:12px 14px}
figure.vis svg{max-width:100%;height:auto;display:block}
figure.vis figcaption{margin-top:8px;font-size:.92rem;color:var(--muted)}
figure.vis .conclusion{font-weight:700;color:var(--ink)}
</style>

<figure class="vis">
  <svg role="img" aria-label="Reads per second, before and after the cache" viewBox="0 0 320 120">
    <!-- draw with the tokens: fill="var(--accent)", stroke="var(--line)" -->
  </svg>
  <figcaption>How to read: each bar is one day, and the height is reads per second.<br>
  <span class="conclusion">After the cache, the database sees a third of the reads.</span></figcaption>
</figure>
```

For a Mermaid diagram, put the source in `<pre class="mermaid">` inside the same `<figure>`.
Keep every node label at 25 characters or fewer, with no `<br/>`, and at most 2 nodes side by side.
That is what lets the labels survive a phone.
Run `node scripts/check_mermaid.cjs page.html` before you deliver (setup: `npm install --no-save mermaid@11 playwright@1`, then `npx playwright install chromium` once).

## 5. Risk as a natural frequency: the icon array (Rule 7)

A health risk is shown as a grid of 100 figures with the affected ones filled in, never as a relative risk alone.
The element carries the numbers in `data-n` and `data-of`, and the script draws the dots and writes the label for screen readers.

```html
<style>
.icons{display:grid;grid-template-columns:repeat(10,1fr);gap:4px;max-width:260px;margin:8px 0}
.icons span{aspect-ratio:1;border-radius:50%;background:var(--line)}
.icons span.on{background:var(--bad)}
</style>

<figure class="vis">
  <div class="icons" data-n="3" data-of="100" data-label="{n} in every {of}"></div>
  <figcaption>How to read: each dot is one person out of 100, and a red dot is one who is affected.<br>
  <span class="conclusion">3 in every 100 people are affected, so 97 are not.</span></figcaption>
</figure>

<script>
[].slice.call(document.querySelectorAll(".icons")).forEach(function (box) {
  var n = parseInt(box.getAttribute("data-n"), 10) || 0, of = parseInt(box.getAttribute("data-of"), 10) || 100;
  var label = box.getAttribute("data-label") || "{n} in every {of}"; // pt: data-label="{n} em cada {of}"
  box.textContent = "";
  box.setAttribute("role", "img");
  box.setAttribute("aria-label", label.replace("{n}", n).replace("{of}", of));
  for (var i = 0; i < of; i++) { var d = document.createElement("span"); if (i < n) d.className = "on"; box.appendChild(d); }
});
</script>
```

## 6. Dated events: an HTML timeline, not a diagram (Rule 7)

Dates and one-sentence events wrap on a phone when they are a list.
A Mermaid timeline cuts the text, so never use one for dates.

```html
<style>
.timeline{list-style:none;padding:0;margin:0 0 14px;border-left:3px solid var(--line)}
.timeline li{padding:0 0 12px 14px;position:relative}
.timeline li::before{content:"";position:absolute;left:-8px;top:8px;width:11px;height:11px;border-radius:50%;background:var(--accent)}
.timeline time{display:block;font-family:var(--mono);font-size:.85rem;color:var(--muted)}
</style>

<ol class="timeline">
  <li><time>3 June 2026</time>The team turns the cache on for 10% of the traffic.</li>
  <li><time>17 June 2026</time>The cache serves every read, and the database load falls by two thirds.</li>
</ol>
```

## 7. Optional depth in a collapsed block (Rule 8)

Detail the reader may skip on a tired day goes into `<details>`.
The summary says what is inside, so the reader decides without opening it.
The same element holds a model answer under a "Stop and explain" prompt.

```html
<style>
details{border:1px solid var(--line);border-radius:10px;padding:0 14px;margin:0 0 12px;background:var(--surface)}
details summary{cursor:pointer;padding:12px 0;min-height:44px;font-weight:700}
details[open] summary{border-bottom:1px solid var(--line);margin-bottom:10px}
</style>

<details>
  <summary>Why the expiry time is 60 seconds and not 600</summary>
  <p>...</p>
</details>

<p><strong>Stop and explain:</strong> why does a longer expiry time make stale reads more likely?</p>
<details><summary>Model answer</summary><p>A copy lives longer, so the source has more time to change under it.</p></details>
```

## 8. Two layers, always visible: what the source says and what you added (Rule 4)

Added background, a fact-check or a counterpoint sits in a box that looks different from the body, with its source linked.
The reader always knows who says what.

```html
<style>
.extra{background:var(--extra-bg);border-left:4px solid var(--extra-edge);border-radius:0 10px 10px 0;padding:12px 14px;margin:0 0 14px}
.extra .tag{font-family:var(--mono);font-size:.76rem;color:var(--muted);text-transform:uppercase;letter-spacing:.04em}
.badge{display:inline-block;font-size:.78rem;padding:1px 8px;border-radius:999px;background:var(--line);white-space:nowrap}
.v-ok{background:var(--good-bg);color:var(--good)}.v-ctx{background:var(--warn-bg);color:var(--warn)}.v-bad{background:var(--bad-bg);color:var(--bad)}
</style>

<aside class="extra">
  <span class="tag">Added context</span>
  <p>The study behind this number followed 2,000 readers for one week.<br>
  Source: <a href="https://doi.org/...">Author, 2024</a>.</p>
</aside>

<p>The article says the cache cut the load by 70%. <span class="badge v-ctx">Needs context</span></p>
```

## 9. Analogy with its limit (Rule 5)

```html
<p>Think of the cache as a notebook on your desk: you copy the answers you look up often.<br>
<strong>Where the analogy fails:</strong> a notebook never forgets, but a cache drops old entries on its own.</p>
```

## 10. Resume where the reader stopped (optional)

On a long page, remember the last section the reader saw, and offer to jump back to it on the next visit.
Browser storage can be empty or throw (private window, cleared data), so every call sits in `try`.
Nothing here leaves the reader's browser.

The script starts saving only after the reader scrolls.
The reason is that the first section is on screen at load time.
Without the guard, it would overwrite the saved position before the reader could use it.
Put the script at the end of the body, after the sections, so they exist when it runs.

```html
<div class="resume" id="resume" hidden>
  <p>You stopped at <strong id="resume-where"></strong>.</p>
  <button type="button" id="resume-go">Continue there</button>
</div>

<script>
(function () {
  var key = "clear-read:" + location.pathname + ":position";
  function get() { try { return JSON.parse(localStorage.getItem(key)); } catch (e) { return null; } }
  function set(v) { try { localStorage.setItem(key, JSON.stringify(v)); } catch (e) {} }
  var sections = [].slice.call(document.querySelectorAll("section[id]"));
  var armed = false;
  addEventListener("scroll", function () { armed = true; }, { once: true, passive: true });
  var saved = get();
  if (saved && document.getElementById(saved.id)) {
    document.getElementById("resume-where").textContent = saved.title;
    document.getElementById("resume").hidden = false;
    document.getElementById("resume-go").onclick = function () {
      document.getElementById(saved.id).scrollIntoView();
      document.getElementById("resume").hidden = true;
    };
  }
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      if (!armed) return;
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          var h = e.target.querySelector("h2");
          set({ id: e.target.id, title: h ? h.textContent : e.target.id });
        }
      });
    }, { rootMargin: "-40% 0px -50% 0px" });
    sections.forEach(function (s) { io.observe(s); });
  }
})();
</script>
```

## Checklist before you deliver an HTML page

1. `python3 scripts/lint_clear_read.py page.html` prints `0 problems`.
2. `node scripts/check_mermaid.cjs page.html` prints `problems: 0` when the page has Mermaid diagrams (setup in pattern 4).
3. Open the page at 390px wide, in light and in dark mode. Nothing scrolls sideways, and no text is smaller than 12px.
4. Every visual has its "How to read:" line and its conclusion.
5. Every "Added context" box links its source.
