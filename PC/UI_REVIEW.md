# OmniPad — quick interface review

17 October 2026. Requested skill: make-interfaces-feel-better. Mode: **quick**, maximum five HIGH/MEDIUM findings.

## Scope and boundary

Inspected `omnipad/web/index.html`, the corresponding server key allowlist and input/reset tests. This workspace contains Vanilla JavaScript with inline plain CSS. **No Settings page, Tailwind configuration, React components, or package.json were supplied.** Changes use the existing styling system. The scope is the OmniPad Mouse/Media/Game remote, not an unseen settings screen. The attached screenshot was unavailable at the supplied scratch path; it was not visually inspected.

The earlier UX Writing and Minimalist UI instructions remain applied. This revision prioritizes the user's explicit contrast and PS-style controller requirements over the earlier skill's faint borders and compact corner limits.

## Coverage

| Category | Evidence inspected | Result |
|---|---|---|
| Typography | Status, latency, count, hints, headings; CSS and DOM | Numeric stability, text wrapping and font rendering updated |
| Surfaces | Card/input nesting, inset trackpad, game-stage, selected/disabled controls | Radius, contrast and touch target fixes |
| Animations | Button transitions, entrance class, held states and joystick updates | Unnecessary entrance removed; no repeated game-button animation; physical timing not reviewed |
| Icons | Inline currentColor SVG symbols, face glyphs, Start/play alignment | Same assets retained; optically align Start glyph; state follows currentColor |
| Performance | Explicit transitions, movement requestAnimationFrame, no new will-change | No transition:all; motion restrained; no browser profiling performed |

## Findings and changes

| Severity | Location | Before | After | Why |
|---|---|---|---|---|
| HIGH | `omnipad/web/index.html:15` contrast tokens and states | Disabled text pale; disabled trackpad opacity .55; faint button boundaries; selected tab white | Remove trackpad opacity; readable disabled labels; darker text/borders; charcoal selected tab and hover; explicit status colors | Legibility and state distinction: measured text-secondary 7.01:1, disabled label 5.74:1, button boundary 3.61:1 on canvas |
| MEDIUM | `omnipad/web/index.html:100` surface polish | Card radius 12 with child radius 6 and padding 24; inset trackpad radius 12 with inner radius 8/inset16 | Card 30 = 6+24, mobile card26 = 6+20; text container26 = 6+20; trackpad24 = 8+16; flat surfaces and zero button shadows | Concentric radius and structural borders: nested corners read consistently; preserve the minimalist hierarchy without invented elevation |
| HIGH | `omnipad/web/index.html:48`, `:100`, `:175`, `:231`, `:237` game/touch controls | Some face buttons36px, L3/R3 targets34px, quiet actions40px; earlier game only keyboard direction/actions | CSS target minimum44px, standard buttons48px; reflow portrait controller to avoid overlapping targets; full PS-style face/shoulder/system buttons, dual virtual analogs, source-aware held-key ownership, reset on pointercancel/rotation/disconnect | Minimum hit area and reliable input: touch controls must be usable, and one input source must not release another source's held direction |
| MEDIUM | `omnipad/web/index.html:100`, `:168`, `:173` typography/status | Dynamic counters had no explicit tabular-nums; headings/body no wrapping policy | Explicit tabular-nums/lining-nums on latency/count/game state/kbd; minimum text footprint; balance headings, pretty body text, root font smoothing | Tabular numbers and stable typography keep changing values from wobbling; improve wrapping and rendering |
| MEDIUM | `omnipad/web/index.html:100` interactions and system-button glyph | .98 press scale, generic entrance class, game repeated press animation; triangle appears optically left | .96 for infrequent ordinary button presses; immediate static held color for game inputs, no game scale/transition; remove entrance; precise transition list; reduced-motion override; Start glyph optical +1px | Motion restraint and optical alignment: frequent controls need immediate cues, not repeated animation, while ordinary buttons keep a restrained response |

The game controls were added to fulfill the active PS-layout request, not as part of an invented Settings page. They send keyboard input: two sticks are digital direction mappings, not analog game-controller axes. Face glyph colors, trigger styles, mapping help, immersive view/back controls, and preview/dry-run copy are included in this change.

## Considered but rejected

| Location | Candidate | Rejected because |
|---|---|---|
| All surfaces | Add visible layered shadows | Existing product is intentionally flat. Borders identify control boundaries and states; no elevated overlays require a shadow |
| Whole project | Introduce Tailwind for the requested polish | There is no Tailwind setup in the supplied project. Adding a second styling system conflicts with the skill and adds unnecessary build dependencies |
| Game | Animate every press or add a true-PS-controller badge | Repeated movement distracts from fast input. The backend remains keyboard mapping, not a PlayStation controller driver |

## Verification

- `node --check /tmp/omnipad-client.js`: PASS.
- `python -m unittest discover -s tests -v`: **8 PASS**, including the 20-key game mapping and release-all test.
- jsdom interaction regression: preview, tabs, retained text, disabled controls, field validation, friendly auth error, mocked ready/ack/disconnect: PASS, no script errors.
- jsdom controller test: all PS-layout button mappings, immersive/back controls, D-pad + right-analog shared-key ownership, left-analog diagonal directions, pointercancel key release, release-all visual reset: PASS, no script errors.
- Color-pair checks: PASS for the pairs listed in `CONTRAST_UPDATE.md`. This is not a complete accessibility certification.
- **Not verified:** rendered browser layout at mobile/desktop sizes, actual hit-area bounding boxes, physical multitouch, mobile fullscreen/browser behavior, Safari, live PC/game input, browser performance, or animation playback at 10% speed. Browser executable unavailable; browser download failed. DOM tests do not establish these visual or hardware results.

## Verdict

**Needs changes before visual/UAT sign-off:** code-level fixes and DOM/backend checks pass; rendered layout, physical hit areas, touch/game input and 10%-speed browser motion review remain unverified. No claim of approval for the absent Settings/Tailwind page.


## Final visual direction requested afterward

The default Media surface was replaced with a narrow, modern TV-remote silhouette and circular navigation/OK. The editorial hero/sidebar was removed from the visible layout. Mouse and full PS-style controls remain tabs. The power control disconnects the session, explicitly not device power. New navigation/volume/media controls use the same key allowlist and state handling; no TV receiver was introduced. Dark-remote labels and boundaries use explicit contrasting colors, with 48px touch targets on its main controls. DOM regression and controller tests were re-run and passed after this update. Physical/rendered layout remains unverified.

## Penyesuaian ui-ux-pro-max — 18 Oktober 2026

Panduan yang dilampirkan diterapkan pada remote yang sudah ada. Arah visual tetap remote TV ringkas sesuai tujuan project, dengan warna terang netral di halaman dan permukaan remote charcoal. Tidak ada script `skills/ui-ux-pro-max/scripts/search.py` di lampiran atau ZIP, sehingga token desain dipilih dari panduan tertulis dan palet kontras yang sudah tercatat.

- Label fungsi remote yang sebelumnya 9–10 px dinaikkan menjadi 12 px; keterangan remote menjadi 13 px.
- Pemilih monitor memakai font, border, target sentuh 48 px, warna teks eksplisit, dan fokus keyboard yang terlihat.
- Grup remote TV, navigasi, stik, D-pad, dan tombol aksi diberi role semantik agar label grup dibaca pembaca layar.
- Tombol transport mempertahankan target minimum 48 px; transisi tombol umum menjadi 160 ms. Kontrol yang sering ditahan tetap memberi status langsung dan reduced-motion tetap aktif.
- `Preview.html` diselaraskan dengan gaya dan semantik baru; pilihan awal preview tetap Layar.

Validasi pada paket ini: JavaScript inline lolos `node --check`. Backend dan tes DOM belum dapat dijalankan di runtime ini karena `aiohttp` dan `jsdom` tidak tersedia; tidak dilakukan instalasi dependency. Belum ada QA visual browser atau uji perangkat fisik, jadi ukuran hasil render, multitouch, fullscreen, dan perilaku receiver tetap perlu UAT.
