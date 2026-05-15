# Technology Stack — Jogo da Natália

**Project:** Jogo da Natália — De Osasco à Espanha
**Researched:** 2026-05-15
**Type:** 2D pixel art narrative platformer
**Targets:** PC (Windows/Mac), Web (HTML5), Mobile (future)

---

## Recommended Stack

### Core Engine

| Technology | Version | Purpose | Rationale |
|------------|---------|---------|-----------|
| Godot 4 | **4.4.x or 4.5.x** | Game engine | 4.4 (March 2025) and 4.5 (June 2025) are the stable production targets. 4.6.x exists but was very recent at research time; stay on 4.4 or 4.5 unless a specific feature demands upgrading. Avoid Godot 3.x — TileMapLayer, physics interpolation, and improved web exports are 4.x-only. |
| GDScript | built-in | Scripting language | **Use GDScript, not C#.** C# cannot export to HTML5/Web in Godot 4 (confirmed as of 4.6). Since web export is a stated requirement, C# is disqualified entirely. GDScript also has faster iteration (no compile step), tighter editor integration, and all successful indie Godot games (Brotato, Dome Keeper, Cassette Beasts) used it. |

### Language Decision Detail: GDScript vs C#

**Use GDScript.** The deciding factor is non-negotiable: C# projects cannot export to HTML5 in Godot 4. Beyond that, GDScript is the right choice for this project on every other dimension too:

- `@export` variables appear instantly in the Inspector — critical for tweaking jump physics, enemy speeds, dialogue timing
- Hot-reload without compilation means faster level iteration
- All Godot 4 documentation, tutorials, and community answers default to GDScript
- For a project of this scope (8 worlds, 1 dev, narrative focus), GDScript is more than sufficient

**Do not use C#** even if you have .NET experience. The web export blocker alone is a dealbreaker for this project.

---

### Pixel Art Rendering Configuration

This is the most impactful early decision. Set these in **Project Settings** before writing any game code.

| Setting | Path | Value | Why |
|---------|------|-------|-----|
| Texture filter | Rendering > Textures > Canvas Textures > Default Texture Filter | **Nearest** | Prevents Godot's default linear filter from blurring pixel art during scaling. Without this, sprites look smeared. |
| Stretch mode | Display > Window > Stretch > Mode | **canvas_items** | Renders at full window resolution while keeping sprites pixel-perfect. Allows smooth camera movement. Alternative: `viewport` mode gives authentic low-res look but black bars on non-integer window sizes. |
| Scale mode | Display > Window > Stretch > Scale Mode | **integer** | Only scales by whole numbers (2x, 3x, 4x — never 2.7x). Prevents uneven pixel sizes where some pixels look larger than others. Available since Godot 4.3. |
| Snap transforms | Rendering > 2D > Snap 2D Transforms to Pixel | **On** | Prevents camera movement from causing sub-pixel jitter on sprites. Essential for pixel art cameras. |
| Base viewport | Display > Window > Size | **320x180** (or 640x360) | 320x180 is the pixel art standard for 16:9 that scales perfectly to 1280x720, 1920x1080, 2560x1440, and 4K. With 32x32 sprites, this gives ~10 tiles of vertical space — enough for a platformer. Use 640x360 if you want more screen real estate. |

**Recommended base resolution:** 320x180 with 32x32 sprites. This is the GDQuest and community consensus for indie pixel art platformers in 2024-2025.

---

### Sprite Sizes

| Asset Type | Recommended Size | Rationale |
|-----------|-----------------|-----------|
| Player (Natália) | **32x32** | Sweet spot for expressiveness: can show emotions, equipment detail, and animate cleanly. SNES/GBA-era feel. Professional pixel artists call this the production-speed/quality optimum for indie games. |
| Major NPCs (Renato, boss characters) | **32x32** | Consistent with player scale. Bosses can be 64x64 or larger as special cases. |
| Small enemies / collectibles | **16x16** | Enemies that are environmental hazards (gremlins, email projectiles) work well at 16x16 and are fast to animate. |
| Tiles / environment | **16x16** | Standard tile size. A 16x16 tile grid on a 320x180 viewport = 20 tiles wide × ~11 tiles tall. This is the right density for a platformer. |
| Boss sprites | **64x64 – 128x128** | Bosses like the Virus Chefão (full-screen boss) should be oversized. Use multiples of 16 or 32. |
| UI elements | **match native** | UI can be at higher resolution since it doesn't scroll. Design at 640x360 or native window size, not at 320x180 game resolution. |

**Do not mix arbitrary sizes.** Stick to the 16px grid system. If 32x32 feels too large for a character, use 24x24 — but always a multiple of 8.

---

### Audio

| Technology | Purpose | Format | Rationale |
|------------|---------|--------|-----------|
| Godot built-in AudioStreamPlayer2D | All SFX | **WAV** | Native, zero dependency, perfect for short sounds. WAV has no CPU decode cost, ideal for high-frequency sounds (footsteps, coin pickups, hit effects). |
| Godot built-in AudioStreamPlayer | Music / ambient | **OGG Vorbis** | Compressed, supports loop points natively, reduces file size for long tracks. The correct format for background music in Godot. |
| Godot 4.3+ AudioStreamInteractive | Adaptive music (optional) | OGG | New in 4.3, allows music to transition between states (tense → relaxed) — useful for the emotional arc of this game. Use if music composer delivers stems. |

**Do not use FMOD or Wwise** for this project. They add integration complexity, licensing overhead, and are overkill for an indie solo project. Godot 4.3's new `AudioStreamInteractive`, `AudioStreamPlaylist`, and `AudioStreamSynchronized` nodes cover 90% of what FMOD provides for a game at this scale.

**Audio production tools (external to Godot):**
- Music composition: Reaper or LMMS (free) + any VST library with Latin/Spanish flavors for thematic worlds
- SFX: sfxr/bfxr for chip-style sounds, or Freesound.org for real-world sounds
- Master to OGG at 44100Hz, 192kbps for music; export SFX as 44100Hz WAV (mono for most effects)

---

### Level Design: TileMap vs External Tools

**Use Godot's built-in TileMapLayer.** Do not use Tiled or LDtk as the primary level design tool.

| Tool | Verdict | Reason |
|------|---------|--------|
| Godot TileMapLayer (Godot 4.4+) | **Recommended** | TileMapLayer (replacing TileMap in 4.4) gives each layer its own node, enabling per-layer collision, navigation, and scripting. No import pipeline, no sync issues, physics chunks merged in 4.5 for better performance. |
| LDtk | Optional for complex world maps only | LDtk is the best external 2D editor (made by the Dead Cells creator), supports auto-tiling, entity layers, and custom properties. Has a Godot importer plugin. Use only if TileMapLayer becomes limiting for the overworld map. |
| Tiled | Do not use | Older codebase, inferior to LDtk for any new project. If you need an external editor, use LDtk instead. |

**For the overworld map** (navigating between the 8 worlds): this is a custom scene, not a tilemap. Build it as a Node2D with clickable/unlockable region nodes — not a TileMapLayer.

---

### Save System

| Approach | Use Case | Format |
|----------|----------|--------|
| Godot Resource (.tres) | Complex save data (player progress, world completion, powers unlocked) | Binary/text resource |
| `FileAccess.store_var()` | Simple persistent flags | Binary (Godot-native) |

Use **Godot Resources** for the save system. Create a `SaveData` resource class with typed fields for each world's completion state, unlocked powers, and collectibles. Resources are natively typed (no Vector2/Color conversion like JSON requires), inspectable in the editor, and require the least boilerplate. Avoid JSON for save data — it adds type conversion overhead for no benefit in a single-platform game.

---

### Version Control

| Area | Recommendation |
|------|---------------|
| .gitignore | Add `.godot/` (cache) and `*.translation` (compiled binary translations). Godot's project manager generates this automatically when you choose Git at project creation. |
| Binary assets (PNG, WAV, OGG) | Use **Git LFS** (Large File Storage). Configure `.gitattributes` to track `*.png`, `*.wav`, `*.ogg`, `*.mp3`, `*.ttf`, `*.otf`, `*.scn`, `*.res` via LFS. Set this up before the first commit — migrating after is painful. |
| Text assets | Regular Git tracking. All `.gd`, `.tscn`, `.tres`, `.import` files are text-diff friendly. |
| Branch strategy | Match the project's own plan: one branch per world or major mechanic. Tag each testable milestone (`v0.1-prototype`, `v0.2-world1-complete`). |
| Commit frequency | Commit after each working state. Godot scene files are XML-based and diff well, but partial `.tscn` edits can corrupt scenes — commit complete, playable states. |

**Do not commit the `.godot/` folder.** It is machine-generated cache. Committing it causes spurious diffs on every engine startup and bloats the repository.

**Git LFS for all binary assets is not optional** if this repository will ever be shared or stored on GitHub (1GB free LFS quota per repo). PNG spritesheets and audio files add up faster than expected.

#### Minimal .gitignore

```
# Godot cache
.godot/

# Compiled translations
*.translation

# Export artifacts
export/
build/
```

#### Minimal .gitattributes (Git LFS)

```
# Images
*.png filter=lfs diff=lfs merge=lfs -text
*.jpg filter=lfs diff=lfs merge=lfs -text
*.webp filter=lfs diff=lfs merge=lfs -text

# Audio
*.wav filter=lfs diff=lfs merge=lfs -text
*.ogg filter=lfs diff=lfs merge=lfs -text
*.mp3 filter=lfs diff=lfs merge=lfs -text

# Godot binary resources
*.scn filter=lfs diff=lfs merge=lfs -text
*.res filter=lfs diff=lfs merge=lfs -text

# Fonts
*.ttf filter=lfs diff=lfs merge=lfs -text
*.otf filter=lfs diff=lfs merge=lfs -text
```

---

### CI/CD — Export and Publish

**Use GitHub Actions + `abarichello/godot-ci` + butler for itch.io.**

| Tool | Role |
|------|------|
| GitHub Actions | CI/CD runner (free for public repos) |
| `abarichello/godot-ci` Docker image | Pre-built image with Godot headless + export templates |
| Itchio butler | Uploads build artifacts to itch.io channels |

**Workflow structure:**

```yaml
# .github/workflows/export.yml
name: Export and Deploy

on:
  push:
    tags:
      - 'v*'   # Only trigger on version tags, not every commit

jobs:
  export-web:
    runs-on: ubuntu-latest
    container:
      image: barichello/godot-ci:4.4.1   # Pin to your Godot version
    steps:
      - uses: actions/checkout@v4
        with:
          lfs: true   # REQUIRED — pulls LFS binary assets
      - name: Export HTML5
        run: |
          mkdir -p build/web
          godot --headless --export-release "Web" build/web/index.html
      - name: Deploy to itch.io
        uses: manleydev/butler-publish-itchio-action@master
        env:
          BUTLER_CREDENTIALS: ${{ secrets.BUTLER_CREDENTIALS }}
          CHANNEL: html5
          ITCH_GAME: jogo-da-natalia
          ITCH_USER: your-itch-username
          PACKAGE: build/web

  export-windows:
    runs-on: ubuntu-latest
    container:
      image: barichello/godot-ci:4.4.1
    steps:
      - uses: actions/checkout@v4
        with:
          lfs: true
      - name: Export Windows
        run: |
          mkdir -p build/windows
          godot --headless --export-release "Windows Desktop" build/windows/JogoDaNatalia.exe
      - name: Deploy to itch.io
        uses: manleydev/butler-publish-itchio-action@master
        env:
          BUTLER_CREDENTIALS: ${{ secrets.BUTLER_CREDENTIALS }}
          CHANNEL: windows
          ITCH_GAME: jogo-da-natalia
          ITCH_USER: your-itch-username
          PACKAGE: build/windows
```

**Critical notes:**
- Always use `--headless --export-release` (not `--export`) for Godot 4
- Set `lfs: true` on the checkout step or binary assets will be missing from the build
- Tag-triggered deploys only (not every push) — otherwise you'll deploy broken in-progress builds
- The `BUTLER_CREDENTIALS` secret is an itch.io API key, not your password — generate it at itch.io/user/settings/api-keys

**Web export and macOS/iOS:** As of Godot 4.3+, the SharedArrayBuffer requirement for web exports was resolved with single-threaded export mode. Web builds no longer require special COOP/COEP headers on the hosting server. Itch.io handles this correctly out of the box.

---

### Project Folder Structure

Godot uses snake_case for all file and folder names (except C# class files, which are not used here).

```
res://
├── addons/                  # Third-party plugins (e.g., LDtk importer if needed)
├── assets/
│   ├── audio/
│   │   ├── music/           # OGG files per world: world1_osasco.ogg
│   │   └── sfx/             # WAV files: jump.wav, hit.wav
│   ├── fonts/               # TTF/OTF files
│   └── sprites/
│       ├── characters/
│       │   ├── natalia/     # natalia_idle.png, natalia_run.png (spritesheets)
│       │   ├── renato/
│       │   └── cachorra/
│       ├── enemies/
│       │   ├── world1/
│       │   └── world2/
│       ├── bosses/
│       ├── tilesets/
│       │   ├── world1_osasco/
│       │   └── world2_faculdade/
│       └── ui/
├── scenes/
│   ├── autoloads/           # Global singletons: game_manager.gd, audio_manager.gd
│   ├── characters/
│   │   ├── natalia/         # natalia.tscn + natalia.gd together
│   │   ├── renato/
│   │   └── cachorra/
│   ├── enemies/
│   │   ├── world1/
│   │   └── shared/          # Shared enemy types (gremlins, fantasmas)
│   ├── bosses/
│   │   ├── boss_pai.tscn
│   │   └── boss_professor.tscn
│   ├── ui/
│   │   ├── hud.tscn
│   │   ├── pause_menu.tscn
│   │   └── dialogue/
│   ├── worlds/
│   │   ├── world1_osasco/
│   │   │   ├── level_01.tscn
│   │   │   ├── level_02.tscn
│   │   │   └── world1_tileset.tres
│   │   ├── world2_faculdade/
│   │   └── ...
│   └── overworld/
│       └── overworld_map.tscn
├── scripts/
│   └── resources/           # Typed resource classes: save_data.gd, power_data.gd
└── export_presets.cfg       # MUST be committed — CI/CD needs it
```

**Key conventions:**
- Keep `.tscn` and `.gd` files in the same folder (scene-centric organization)
- One scene per boss, per NPC, per world level segment
- `autoloads/` contains only global singletons: `GameManager`, `AudioManager`, `SaveManager`, `DialogueManager`
- Limit autoloads to 5-8 max — do not put everything there
- `export_presets.cfg` **must be committed** to the repository — it contains your export configuration and is required for CI/CD to work

---

## Alternatives Considered and Rejected

| Category | Recommended | Rejected | Reason Rejected |
|----------|-------------|----------|-----------------|
| Language | GDScript | C# | Cannot export to HTML5 in Godot 4. Hard blocker for this project. |
| Language | GDScript | C++ (GDExtension) | Massively increased complexity for no benefit at this scale |
| Level editor | Built-in TileMapLayer | Tiled | Old codebase, no active reasons to prefer over LDtk or built-in |
| Level editor | Built-in TileMapLayer | LDtk | Adds external tool dependency and import pipeline. Built-in is sufficient. |
| Audio middleware | Built-in AudioStream | FMOD | Licensing, integration complexity, overkill for solo indie project |
| Audio middleware | Built-in AudioStream | Wwise | Same as FMOD, plus Wwise has complex licensing tiers |
| Save format | Godot Resources | JSON | Type conversion overhead, no editor inspection, no benefit for offline game |
| CI image | abarichello/godot-ci | Custom Docker | Well-maintained community image with correct Godot versions pre-installed |
| Engine | Godot 4 | Unity | License changes (2023 runtime fee debacle), cost, closed-source |
| Engine | Godot 4 | GameMaker | Inferior scripting, weaker web exports, costs money |

---

## Installation / Setup Checklist

```bash
# 1. Download Godot 4.4.x or 4.5.x from godotengine.org
#    Use the standard build (not .NET/.mono) — GDScript does not need .NET

# 2. Initialize Git LFS before first commit
git lfs install
git lfs track "*.png" "*.wav" "*.ogg" "*.mp3" "*.ttf" "*.scn" "*.res"
git add .gitattributes
git commit -m "init: configure git lfs for binary assets"

# 3. In Godot Project Settings, apply pixel art settings:
#    - Rendering > Textures > Canvas Textures > Default Texture Filter = Nearest
#    - Display > Window > Stretch > Mode = canvas_items
#    - Display > Window > Stretch > Scale Mode = integer
#    - Display > Window > Size = 320 x 180 (viewport width/height)
#    - Rendering > 2D > Snap 2D Transforms to Pixel = On

# 4. Create export presets for: Windows Desktop, macOS, Web, Android (future)
#    Then commit export_presets.cfg
```

---

## Sources

- Godot 4.4 release: https://godotengine.org/releases/4.4/ (current stable)
- Godot 4.5 release: https://godotengine.org/releases/4.5/ (current stable)
- Godot 4.6 release: https://godotengine.org/releases/4.6/ (latest)
- GDScript vs C#, web export blocker: https://chickensoft.games/blog/gdscript-vs-csharp
- GDQuest pixel art setup guide: https://www.gdquest.com/library/pixel_art_setup_godot4/
- Godot 4.4 pixel art settings: https://itch.io/blog/806788/godot-44-settings-for-pixel-art
- Pixel art sprite sizing guide: https://pixelartapp.com/resolutions-guide
- Godot 4.3 web export fix (SharedArrayBuffer): https://godotengine.org/article/progress-report-web-export-in-4-3/
- Godot version control official docs: https://docs.godotengine.org/en/stable/tutorials/best_practices/version_control_systems.html
- godot-ci Docker image: https://github.com/abarichello/godot-ci
- Godot 4 audio formats: https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_audio_samples.html
- Godot 4.3 new audio features: https://blog.blips.fm/articles/the-new-music-features-in-godot-43-explained
- GDQuest save system guide: https://www.gdquest.com/library/save_game_godot4/
- Godot project organization: https://docs.godotengine.org/en/stable/tutorials/best_practices/project_organization.html
- TileMapLayer in Godot 4.4: https://gamefromscratch.com/godot-tilemap-replaced-with-tilelayers/
- Godot 4.5 TileMapLayer physics chunks: https://godotengine.org/releases/4.5/
