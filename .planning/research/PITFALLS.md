# Domain Pitfalls: 2D Pixel Art Narrative Platformer in Godot 4

**Project:** Jogo da Natália
**Domain:** Solo-developed 2D pixel art narrative platformer, Godot 4, 8 worlds, PC + Web export
**Researched:** 2026-05-15
**Confidence:** HIGH (most findings verified across multiple sources and official documentation)

---

## Critical Pitfalls

Mistakes that cause rewrites, project abandonment, or ship-blocking bugs.

---

### Pitfall 1: Scope Creep — The Silent Killer

**What goes wrong:** Each world, power, and boss added in isolation looks small. Collectively they compound: 8 worlds × unique boss mechanics × 6 powers × overworld + cutscenes + NPC companions + save system = a scope that would challenge a small studio. A solo developer adding "just one more mechanic" repeatedly hits the point where no single session makes visible progress, motivation collapses, and the project is abandoned half-finished.

**Why it happens:** Personal/emotional projects especially suffer because the story demands completeness — "I can't show the proposal in Santiago without building Worlds 1–4 first." Every feature feels non-negotiable. Invisible time costs (playtesting, bug-fixing, polish) are never counted in scope estimates.

**Consequences:** Burnout, permanent abandonment, the gift never delivered. Research consistently shows this is the #1 cause of failed indie games, not technical problems.

**Warning signs:**
- You're designing World 7 mechanics while World 1 is still a prototype
- Your TODO list grows faster than your Done list
- Each session starts with "before I can work on X I need to finish Y first"
- You've restarted the project architecture "to do it properly"
- You're adding new powers while none of the existing ones have been playtested

**Prevention strategy:**
1. Treat each world as a shippable unit. World 1 must be complete (level, boss, cutscene, save point, tested) before World 2 is designed in detail.
2. Freeze the feature list for the current world when you start building it. New ideas go to a "World X+" backlog file, never the active branch.
3. Set a vertical slice target: a 10-minute playable demo (World 1 complete + World 2 entry) is the first real milestone. Nothing else matters until that exists.
4. Use MoSCoW per world: Must (core gameplay + boss), Should (cutscene), Could (alternate paths), Won't (experimental mechanics).

**Phase it hits:** All phases, but most dangerous at project start (over-designing) and mid-project (mid-world restarts).

---

### Pitfall 2: Godot 4 Pixel Art Rendering — Three Settings That Must All Be Correct

**What goes wrong:** Sprites look blurry, shimmer when the camera moves, or have inconsistent pixel sizes at different window scales. These problems have three separate causes that all require separate fixes. Getting only two of three right still produces visible artifacts.

**Why it happens:** Godot 4 defaults are designed for 3D and hi-res 2D. The defaults (Linear filtering, no pixel snapping, canvas stretch) are actively wrong for pixel art.

**Consequences:** The game looks broken. Players immediately notice "blurry pixel art" as unprofessional. Cannot be fixed post-shipping without re-exporting.

**Warning signs:**
- Sprites look soft or "fuzzy" at native resolution
- Sprites shimmer or wobble when the camera pans slowly
- Some pixels appear larger than others at 2x or 3x window scale
- Fonts look anti-aliased when they shouldn't be

**Prevention strategy — all three settings required:**

1. **Texture filtering:** Project Settings → Rendering → Textures → Canvas Textures → Default Texture Filter → set to **Nearest**. This is the single most common cause of blurry pixel art. Godot defaults to Linear.

2. **Pixel snapping:** Project Settings → Rendering → 2D → Snap → enable **snap_2d_transforms_to_pixel**. Without this, camera positions at fractional coordinates (x = 12.34) cause sprite shimmer even with Nearest filtering.

3. **Integer scaling:** Display → Window → Stretch → Mode → **viewport** AND Scale Mode → **integer**. This ensures the game renders at its native resolution and scales only by whole numbers (2x, 3x), never 2.7x. Non-integer scaling makes some pixels appear larger than neighbors.

**Also:** All imported sprite assets should have their import settings set to Lossless compression and filter disabled individually as a backup.

**Phase it hits:** Project setup (Phase 0 / first session). Must be done before any art is placed.

---

### Pitfall 3: Floaty, Imprecise Movement Feel

**What goes wrong:** The jump arc is symmetric (same gravity up and down), movement stops immediately or has too much momentum, and precision jumps feel like luck rather than skill. The game feels like controlling a balloon.

**Why it happens:** Using physics defaults or naive velocity math. `velocity.y += gravity * delta` with a fixed gravity value produces a parabolic arc that feels floaty. Real good-feeling platformers use asymmetric gravity — stronger downward pull after the peak of the jump.

**Consequences:** Players report the game "feels bad" without being able to articulate why. This tanks enjoyment of every level regardless of art quality or narrative.

**Warning signs:**
- The jump arc looks like a perfect parabola
- Holding jump vs. tapping jump makes no difference
- The character drifts to a stop horizontally after releasing direction
- Missing a platform ledge by one pixel when visually on it
- Players feel "cheated" by deaths

**Prevention strategy:**
- Use **asymmetric gravity**: apply normal gravity on the way up, multiply gravity by 2.0–2.5 after jump peak (when `velocity.y > 0`). Also apply high gravity when the jump button is released early (variable-height jumps).
- Implement **coyote time**: allow jumping for 5–8 frames after walking off a platform edge. Celeste uses exactly 5 frames. This is non-optional for a precision platformer.
- Implement **jump buffering**: store a jump input for 6–10 frames. If the player lands within that window, execute the jump immediately. Makes chained jumps feel crisp.
- Add **corner correction**: if the player barely clips the corner of a ceiling or platform edge (1–4 pixels), push them to the side rather than stopping dead.
- Use `CharacterBody2D`, not `RigidBody2D`. Rigid body physics simulation is physically correct but feels wrong for platform games. `CharacterBody2D` with manual velocity math gives full control.
- Separate horizontal and vertical drag/acceleration. Air control (slower direction changes mid-air) adds skill expression without being unfair.

**Phase it hits:** Phase 1 (character controller). Must be correct before level design begins — levels built around a wrong-feeling controller will need to be redesigned.

---

### Pitfall 4: Godot 4 Architecture — Monolithic Player Script

**What goes wrong:** All player logic (movement, health, powers, animation, sound) ends up in one 800-line script. Adding the 3rd power requires touching movement code. Fixing the jump breaks animation triggers. By World 3 the file is unmaintainable.

**Why it happens:** Starting simple is correct, but no refactor boundary is planned. Each new feature is "just a few more lines."

**Consequences:** Feature-adding velocity drops to near zero mid-project. Bugs multiply because side effects are untraceable.

**Warning signs:**
- The player script is over 300 lines by World 1
- Adding a new power requires touching `_physics_process()`
- You can't add an animation state without reading the whole file first
- The same variable is read in 5+ unrelated functions

**Prevention strategy:**
- Never use `CharacterBody2D` as the scene root. Use a plain `Node2D` root, with `CharacterBody2D` as a child. This makes attaching independent sub-components (HealthComponent, PowersComponent, AnimationComponent) clean.
- Separate movement state machines from combat/power state machines. They can communicate through signals, not shared variables.
- Use a dedicated `PowersManager` autoload or node for the progressive power system. Each power is its own `Resource` or `Node`, not a flag in the player script.
- Use Godot signals for cross-component communication. Never direct node access from unrelated systems.

**Phase it hits:** Phase 1 (foundation). Refactoring this later is very expensive.

---

### Pitfall 5: Godot 4 Web Export — Platform Compatibility and Audio

**What goes wrong:** The game runs perfectly in the Godot editor but fails or sounds broken in the browser. Specifically: (a) the game doesn't load at all on itch.io due to CrossOriginIsolation requirements; (b) audio crackles or distorts in single-threaded web builds; (c) the exported `.pck` + `.wasm` file is 40MB+ for an empty project, making first-load intolerable.

**Why it happens:** Godot 4 web export defaults use SharedArrayBuffers which require COOP/COEP HTTP headers that most hosting platforms don't set. Audio in single-threaded mode is tied to frame rate.

**Consequences:** The game is unplayable for the primary web audience (itch.io players using browsers other than Chrome).

**Warning signs:**
- Testing web export for the first time late in development
- "It works on my machine" but only in the desktop build
- Audio works in the editor but crackles in browser
- itch.io page loads but game shows a black screen or error

**Prevention strategy:**
- Use **Godot 4.3+** and export with **threads disabled** (single-threaded build). This removes the SharedArrayBuffer requirement. As of 4.3, the cracking audio issue in single-threaded builds was also resolved via sample playback support.
- If using a host that doesn't set COOP/COEP headers, use the `godot-coi-serviceworker` plugin, which injects the required headers via a Service Worker without needing server config.
- On itch.io specifically: enable "SharedArrayBuffer support" in Embed Options → Frame Options. Be aware this only works in Chromium browsers; Firefox users will get errors.
- For audio autoplay policy: all browsers block audio until user interaction. Always show a "tap to start" screen or catch the AudioServer initialization.
- Set output latency in web builds: `AudioServer.set("driver/output_latency", 50)` in an autoload to prevent buffer underruns.
- Test the web export after EVERY world is complete, not at the end. Web bugs caught late are catastrophic for a personal gift with a delivery date.
- Godot 4 web exports are GDScript-only. Do not start using C# — it cannot export to web.

**Phase it hits:** First web test should happen in Phase 1. Full validation at end of each world milestone.

---

## Moderate Pitfalls

Mistakes that require significant rework but don't necessarily kill the project.

---

### Pitfall 6: TileMap API Deprecated in Godot 4.3+

**What goes wrong:** Tutorials written before 4.3 use `TileMap` (single node with layers). In Godot 4.3+, `TileMap` is deprecated and replaced by multiple `TileMapLayer` nodes. Following old tutorials produces deprecation warnings and eventually code that breaks on future Godot versions.

**Warning signs:** Any tutorial showing `$TileMap.get_cell_tile_data(layer, ...)` with a `layer` int parameter is using the deprecated API.

**Prevention:** Use `TileMapLayer` nodes from the start. Each visual/physics layer is a separate `TileMapLayer` child node. Physics layer index mismatches (1-indexed in UI, 0-indexed internally) are a frequent collision bug — verify physics layer numbers explicitly in each TileSet.

**Phase it hits:** Level design phases (Worlds 1+). If discovered late, collision behavior may be subtly broken in all existing levels.

---

### Pitfall 7: Level Design Difficulty Spikes and Geometry Ambiguity

**What goes wrong:** A section that was designed knowing the solution feels obvious in hindsight but is genuinely confusing to a first-time player. Off-screen platforms that look like deadly gaps, precision jumps introduced without teaching them first, and sudden difficulty walls after easy sections all destroy pacing.

**This project's specific risk:** The emotional arc requires early worlds to be mechanically harder and later worlds lighter. Overbuilding the "hard early" portion can make players quit before the emotional payoff of Worlds 6–8.

**Warning signs:**
- You know where the hidden platform is because you placed it
- A section requires a mechanic that hasn't appeared before in that world
- A checkpoint is placed before a short easy section rather than before a hard section
- Playtesters die in unexpected locations (not the intended hard spots)

**Prevention:**
- Apply the "first time, second time" rule: every hard mechanic must appear once in a safe, low-stakes context before it's used in a challenging context.
- Distinguish visually between "deadly gap" and "platform just out of frame" — parallax scrolling, screen hints, or visible landing zones.
- Place checkpoints immediately before the hardest section in a room, not before the easy approach to that section.
- Design levels left-to-right, play them left-to-right as a fresh run. Never playtest your own level within 24 hours of building it.
- For this project specifically: World 1–4 should be mechanically challenging but emotionally grounded. Never punish players so hard that they quit before the catharsis of the Spain worlds.

**Phase it hits:** Every world's level design phase. Most dangerous when the designer is close to the material (as all worlds here are).

---

### Pitfall 8: Save System Data Loss and Path Bugs

**What goes wrong:** Save data disappears after a game update, writes to `res://` instead of `user://` (which is read-only in exports), silently fails when a subdirectory doesn't exist, or becomes unreadable after a variable rename.

**Specific Godot pitfalls:**
- Writing to `res://` works in the editor, fails silently in exported builds (the PCK is read-only).
- `user://saves/slot1.json` fails silently if the `saves/` subdirectory doesn't exist — Godot does not auto-create subdirectories.
- JSON save files break when you rename a GDScript variable that was used as a dictionary key.
- Windows is case-insensitive; Linux (web/server) is not. `SaveGame.json` vs `savegame.json` creates two different files on Linux.

**Warning signs:**
- Save works in editor but not in the exported build
- Players report losing progress after updates
- Save slots silently fail to write with no error logged

**Prevention:**
- Always save to `user://`. Never `res://`.
- Always call `DirAccess.make_dir_recursive_absolute(path)` before writing to any subdirectory.
- Use a `SaveVersion` field in every save file. On load, check the version and run a migration function if needed.
- Maintain two rotating save slots (slot A and slot B). Write to the opposite of the last-used slot. If the new write fails, the old save survives.
- Use Godot's `FileAccess` with error checking: always check `file != null` and verify `Error.OK` on open.
- Prefer `ConfigFile` over raw JSON for simple save data — it handles Godot types (Vector2, Color) natively and is more resilient to partial writes.

**Phase it hits:** Phase 1 when save system is built. Most dangerous at World 3+ when save data accumulates game state complexity.

---

### Pitfall 9: Boss Fight Design — Unfair Patterns and Boring Loops

**What goes wrong:** Bosses either feel arbitrary (attacks are unpredictable, player dies without learning anything) or boring (same pattern repeated 15 times until the health bar empties). The "bullet sponge" variant is the most common indie mistake — padding fight length by adding HP instead of adding depth.

**This project's specific risk:** 8 bosses with unique thematic mechanics is ambitious. The "O Gestor Tóxico" (drains mental health HP) and "O Pai Desconfiante" (convinced through dialogue) suggest non-standard win conditions — these require very careful fairness design.

**Warning signs:**
- The boss has more than 3 phases but only 2 distinct attack patterns
- You need to tell playtesters what the boss's "tell" is before they can beat it
- The boss fight lasts more than 90 seconds on a practiced run
- Players say "I don't know what killed me" after dying

**Prevention:**
- Every attack must have a **3-frame visual telegraph** before it activates. Players must be able to read and react.
- Vary attack frequency and order, not just pattern. A boss with 4 attacks in randomized order feels richer than one with 8 attacks in fixed sequence.
- Design the boss to **teach its own mechanics**: Phase 1 introduces one attack slowly, Phase 2 combines it with a second. Players learn by doing.
- Cap boss health such that a competent player finishes in 60–90 seconds. Long boss fights punish players who almost-but-not-quite win.
- For non-standard win conditions (dialogue boss, mental health drain boss): always give clear feedback on what the player is supposed to be doing. A hidden loss condition (mental health silently draining) is frustrating if not telegraphed.
- Add a brief invincibility flash and knockback on hit — missing this makes the character feel like it isn't registering hits.

**Phase it hits:** Each world's boss design phase. The final boss (O Medo da Mudança) requires all 7 powers — must be designed last, with the combined power system tested first.

---

### Pitfall 10: Narrative Pacing — Cutscenes That Break Flow

**What goes wrong:** Long unskippable cutscenes between gameplay sections frustrate players, especially on death + retry loops. The emotional storytelling goal conflicts with good game flow design: a player who died at a boss and has to watch a 90-second cutscene again will mash buttons to skip, or worse, close the game.

**This project's specific risk:** The proposal cutscene in Santiago (World 5) is a centrepiece emotional moment. If it plays before a hard segment and is unskippable, players will resent it.

**Warning signs:**
- Any cutscene over 60 seconds that plays on retry
- Dialogue that explains what the player just saw (instead of showing it)
- The player cannot move for more than 30 seconds at the start of a world
- A narrative moment placed immediately before the hardest section in a world

**Prevention:**
- All cutscenes over 15 seconds must be skippable after the first viewing. Track a `seen_cutscenes` array in save data.
- Prefer in-world storytelling (dialogue during walking, environmental storytelling, NPC reactions) over full-stop cutscenes where possible.
- Place cutscenes after checkpoints and after boss victories, never before them. Victory is the emotional peak — the cutscene rewards the fight, not precedes it.
- The Santiago proposal cutscene specifically should play after the World 5 boss is defeated, as its emotional climax. Not during a retry loop.
- Dialogue boxes during exploration (Renato NPC conversations) should be optional/skippable always. Never block forward movement with mandatory dialogue.

**Phase it hits:** World 5 and beyond as cutscene ambition grows. Script the skip system in Phase 1 so it's available from the start.

---

### Pitfall 11: Pixel Art Animation — Frame Count and Pivot Points

**What goes wrong:** A 16-frame walk cycle made by a beginner looks worse than a 4-frame one by the same artist because every inconsistency is multiplied by 4. Pivot points that shift between frames cause the character to float, teleport, or wobble during transitions.

**Warning signs:**
- The character appears to bounce up/down during the walk cycle even on flat ground
- Transitioning from idle to run has a visual "pop" (character shifts position)
- The walk cycle looks mechanical (all frames are evenly timed)
- The run animation doesn't look faster than the walk, just "busier"

**Prevention:**
- Start with 4 frames for walk, 2 for idle, 4 for run. Add frames only if it reads as jerky during in-engine playback — not because "it should have more."
- Use onion skinning always. The character's contact foot position must land on the same pixel row in every frame. If the hip shifts 2px between frames, the character floats.
- Establish a canonical "origin pixel" for the character (typically the bottom-center of the feet) and never let it drift between frames of the same animation.
- Use **easing**, not constant timing. A walk cycle with even frame timing sounds correct but feels mechanical. Slow-out on the contact pose, fast-through on the passing pose.
- For a 32x32 sprite based on a real person: the face needs to read from a distance. Spend 80% of pixel art effort on the silhouette and the face; background details are largely invisible in motion.

**Phase it hits:** Early art production (pre-World 1). Pivot point bugs are cheap to fix early, expensive to fix after 6 worlds of animation are built.

---

## Minor Pitfalls

Mistakes that cause friction but are recoverable.

---

### Pitfall 12: Git with Binary Game Assets — Repository Bloat

**What goes wrong:** Committing raw Aseprite files, uncompressed PNGs, audio OGG files, and Godot's `.import` cache to Git causes the repository to grow to gigabytes. `git clone` becomes slow. `git diff` on binary files is meaningless. Merge conflicts on `.tres` resource files are hard to resolve.

**Warning signs:**
- `git status` is slow (over 2 seconds)
- Repository size over 1GB for a small 2D game
- `.import/` directory is tracked in git
- Committing a new sprite adds 50MB to the repository history

**Prevention:**
- Add to `.gitignore` immediately: `.godot/`, `*.import`, `*.tmp`, any audio/video source files not needed for build.
- For art source files (`.aseprite`, `.psd`): if they are large, use Git LFS (`git lfs track "*.aseprite"`). For pixel art at 16x32px the files are tiny — standard Git is fine, but set up LFS early so it's available when needed.
- Commit exported `.png` sprites (the build artifact), not necessarily the Aseprite source (the work-in-progress tool file). Decide this policy once and document it.
- Godot's `.tres` and `.tscn` files are text-based and diff correctly in Git. Prefer them over binary `.res` and `.scn` formats where possible (Project Settings → General → Editor → Save Resources as Text).

**Phase it hits:** Project setup. Very cheap to fix at day 1, expensive to rewrite history later.

---

### Pitfall 13: Godot 4 Node Structure — `@onready` and `_ready()` Initialization Order

**What goes wrong:** Code that accesses child nodes in `_ready()` fails with null errors because the child's own `_ready()` hasn't run yet, or because `@onready` variables are populated before child nodes are added to the tree. Signals connected in `_ready()` to nodes that don't exist yet cause silent failures.

**Warning signs:**
- Null reference errors that only appear at runtime, not in the editor
- A variable is definitely set but reads as null in certain conditions
- Adding a child node in `_ready()` and immediately accessing it fails

**Prevention:**
- Use `@onready var node = $NodePath` for all node references. Never store node references in regular vars that are set at class level.
- If adding child nodes dynamically in `_ready()`, access them via `call_deferred("method")` or connect to their `ready` signal.
- Avoid heavy logic in `_ready()`. Move complex initialization to a dedicated `initialize(data)` method called after the scene is fully in the tree.
- Use `await get_tree().process_frame` as a last resort when order-of-initialization issues are unavoidable.

**Phase it hits:** Throughout development, but most frequently when building NPC and companion systems (Renato, the dog) with complex signal trees.

---

### Pitfall 14: Testing — What Actually Matters for a Platformer

**What goes wrong:** Solo developers either don't test at all (ship with obvious bugs) or write automated unit tests for movement math (correct but low value) and miss the actual bugs: edge-of-screen collisions, power interactions, out-of-order world completion, save file edge cases.

**Warning signs:**
- "I never need to test that, I'd never do that as a player" — but playtesters always do
- The level was only tested left-to-right, never backtracked
- The dog companion was never tested in a world designed before the dog existed
- A power acquired in World 3 was never tested in World 1's geometry

**High-value tests for this project:**

| Test Category | Specific Cases to Test |
|---------------|----------------------|
| Collision edge cases | Corner clipping, thin platforms, one-way platforms, slope tops |
| Power interactions | Each power used in each world's geometry, not just its unlock world |
| Dog companion | Pathfinding in World 4–8 levels, dog + boss, dog + tight corridors |
| Save/load cycle | Load mid-world, load with each power state, load after boss victory |
| Web export | Audio on Chrome/Firefox/Safari, first-load time, mobile browser |
| Boss retry loop | What happens after death: correct respawn, cutscene skip, HP reset |
| Difficulty arc | Record death counts per world — spike detection (should decrease W6–W8) |
| Language boss (W6) | Mini-game vocabulary mechanic specifically, not just normal combat |

**Prevention:**
- After finishing each level: run a dedicated 20-minute "break it" session trying to go backwards, clip through geometry, use powers in wrong contexts.
- Keep a playtest log in `.planning/playtests/` with date, world, what was tested, bugs found.
- Give the game to a non-gamer to playtest Worlds 1–2. If they can't pass the first hour, difficulty calibration is needed.

**Phase it hits:** End of each world. Most missed during "just one more feature" rushes.

---

### Pitfall 15: Sprite-Based Real-Person Likeliness — Art Scope Risk

**What goes wrong:** Sprites based on real photos require iterative approval from the real people. The Natália and Renato sprites are the emotional core of the project but also the hardest to get "right." Over-referencing the photo produces a realistic portrait that doesn't read as a game character. Under-referencing produces a generic sprite that doesn't feel personal.

**Warning signs:**
- The sprite silhouette doesn't read as the person from a distance
- You've redrawn the face sprite more than 3 times
- The sprite looks different in motion than in the editor static view
- The pixel character doesn't match the emotional tone of the world

**Prevention:**
- Work at 16x16 or 32x32, not higher. At small sizes, aim for emotional resemblance (hairstyle silhouette, clothing color palette) rather than facial accuracy.
- Establish a "character sheet" reference: all idle, walk, and jump frames side by side on a white background. Get approval on the sheet before building any world.
- Use palettes that match each world's emotional tone. The same sprite should feel darker in Worlds 1–4 and brighter in 6–8 through palette swaps, not redraws.
- The Renato NPC sprite needs a consistent "recognizable moment" pose (the proposal in Santiago) — design the cutscene sprite for that moment specifically, separate from the NPC walking sprite.

**Phase it hits:** Pre-production art phase. Approval loops are slow. Build the character sheet in Week 1.

---

## Phase-Specific Warnings

| Development Phase | Likely Pitfall | Mitigation |
|-------------------|---------------|------------|
| Project setup (Day 1) | Pixel art rendering misconfigured | Set all 3 render settings before placing any sprite |
| Project setup (Day 1) | `.godot/` and `.import/` committed to git | Configure `.gitignore` before first commit |
| Character controller (Phase 1) | Floaty jump, no coyote time | Implement asymmetric gravity + coyote time + jump buffer before level design |
| Character controller (Phase 1) | Monolithic player script | Design component structure (Health, Powers, Animation as separate nodes) from the start |
| Save system (Phase 1) | Writing to `res://`, missing subdirectory creation | Use `user://`, `DirAccess.make_dir_recursive_absolute()`, rotating save slots |
| World 1 level design | Over-difficulty early game | Track death counts; World 1 should be the tutorial, not a gauntlet |
| World 1 boss | Missing telegraph animations | Every boss attack needs a 3-frame wind-up animation |
| World 2+ | Scope creep between worlds | Lock World N feature list before starting World N+1 |
| World 4 (dog companion) | NPC pathfinding in levels not designed for it | Test dog in all previous worlds' geometry |
| World 5 cutscene | Proposal cutscene on retry loop | Implement cutscene skip system before building World 5 |
| TileMap usage | Using deprecated `TileMap` API | Use `TileMapLayer` from the start (Godot 4.3+) |
| Web export | Discovered late, multiple platform bugs | First web export test after World 1 is complete |
| Web export | Audio crackles in browser | Use Godot 4.3+ single-threaded build; set output latency to 50ms |
| Boss design (any world) | Bullet sponge with too much HP | Time boss fights; 60–90 seconds max for a practiced player |
| Animation production | Too many frames, drifting pivot | Start with 4-frame cycles; use onion skinning always |
| Mid-project | Burnout from invisible progress | World-complete milestones are deliverable demos, not internal checkmarks |
| Final boss (World 8) | Requires all 7 powers — complex to balance | Design final boss last; requires all prior powers to be stable first |

---

## Sources

- Wayline.io scope creep series: multiple articles on solo indie scope and burnout
- GDQuest: Setting up pixel art graphics in Godot 4 — https://www.gdquest.com/library/pixel_art_setup_godot4/
- Godot Documentation: Saving games — https://docs.godotengine.org/en/stable/tutorials/io/saving_games.html
- Godot Documentation: Exporting for the Web — https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_web.html
- Godot Engine blog: Web Export in 4.3 — https://godotengine.org/article/progress-report-web-export-in-4-3/
- Ludonauta: 5 Common Mistakes in Godot 4 Platformer Games — https://ludonauta.itch.io/platformer-essentials/devlog/1137232/5-common-mistakes-in-godot-4-platformer-games
- Medium: 5 Subtle Mistakes to Avoid When Programming Games in Godot 4.3 — https://medium.com/@maxslashwang/5-subtle-mistakes-to-avoid-when-programming-games-in-godot-4-3-45fb821f0210
- GameDeveloper.com: Boss Battle Design and Structure — https://www.gamedeveloper.com/design/boss-battle-design-and-structure
- GameRant: How Celeste's "Coyote Time" Mechanic Elevates the Platforming Experience — https://gamerant.com/celeste-coyote-time-mechanic-platforming-impact-hidden-mechanics/
- Sprite-AI: Pixel art animation: from first frame to game engine — https://www.sprite-ai.art/blog/pixel-art-animation
- GitHub: godot-coi-serviceworker plugin — https://github.com/nisovin/godot-coi-serviceworker
- Meta for Developers: Save Game Best Practices — https://developers.meta.com/horizon/documentation/unity/ps-save-game-best-practices/
- GameFromscratch: Godot TileMap Replaced with TileMapLayers — https://gamefromscratch.com/godot-tilemap-replaced-with-tilelayers/
- SUPERJUMP: How Poor Pacing Ruins Your Gameplay — https://www.superjumpmagazine.com/how-poor-pacing-ruins-your-gameplay/
