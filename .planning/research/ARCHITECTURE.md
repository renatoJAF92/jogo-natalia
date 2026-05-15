# Architecture Patterns — Jogo da Natália

**Domain:** 2D Pixel Art Narrative Platformer (Godot 4)
**Researched:** 2026-05-15
**Confidence:** HIGH (official Godot docs + GDQuest + community consensus)

---

## Recommended Architecture

This game has four distinct runtime contexts that must interoperate cleanly:

1. **Overworld** — map navigation, world unlocking
2. **Level** — platformer gameplay, enemies, collectibles, NPCs
3. **Boss** — special encounter scene loaded within a level
4. **Cutscene/Dialogue** — narrative interruptions within any context

The architecture below keeps these contexts cleanly separated while sharing global state through a small set of Autoloads.

---

## Autoload Layer (Global Singletons)

Use exactly three Autoloads. No more. Autoload sprawl is the most common Godot architecture mistake.

```
Project Settings > Globals > Autoload:

GameManager    res://autoloads/game_manager.gd
SaveManager    res://autoloads/save_manager.gd
AudioManager   res://autoloads/audio_manager.gd
```

### GameManager
Central signal bus and game state.

```gdscript
# autoloads/game_manager.gd
extends Node

signal level_completed(world_index: int, level_index: int)
signal boss_defeated(world_index: int)
signal power_unlocked(power_id: String)
signal cutscene_started
signal cutscene_finished
signal player_died
signal game_paused(is_paused: bool)

var current_world: int = 0
var current_level: int = 0
var is_paused: bool = false
```

Rules:
- Nodes emit signals TO GameManager, then GameManager re-emits to other subscribers.
- Never call `get_node()` to reach a sibling scene through GameManager. Use signals only.
- Do not call `free()` or `queue_free()` on any Autoload — engine crash.

### SaveManager
Owns all disk I/O. Only node that touches the filesystem.

```gdscript
# autoloads/save_manager.gd
extends Node

const SAVE_PATH = "user://save.res"

var save_data: SaveData  # custom Resource (see Resource System section)

func save() -> void:
    ResourceSaver.save(save_data, SAVE_PATH)

func load_or_create() -> void:
    if ResourceLoader.exists(SAVE_PATH):
        save_data = ResourceLoader.load(SAVE_PATH, "", ResourceLoader.CACHE_MODE_IGNORE)
    else:
        save_data = SaveData.new()
```

### AudioManager
Manages music and SFX buses. Handles world-specific music transitions with fade.

---

## Scene Tree Architecture

```
Main (Node)                          # persistent container, never freed
├── UI (CanvasLayer)                 # HUD, menus — always on top
│   ├── HUD
│   ├── PauseMenu
│   └── TransitionLayer              # fade-to-black overlay
└── World (Node)                     # replaced on scene transitions
    └── [current scene instance]     # Overworld | Level | BossArena | Cutscene
```

The `Main` scene is the one set in Project Settings > Application > Run > Main Scene. It never changes. Only the `World` child is swapped.

### Scene Transition Pattern

```gdscript
# main.gd
func change_scene(path: String) -> void:
    $UI/TransitionLayer.fade_out()
    await $UI/TransitionLayer.fade_finished
    if $World.get_child_count() > 0:
        $World.get_child(0).queue_free()
    var new_scene = load(path).instantiate()
    $World.add_child(new_scene)
    $UI/TransitionLayer.fade_in()
```

Use `change_scene_to_file()` only for prototyping. In production use the manual pattern above so the HUD and transition layer persist without being freed.

---

## Player Scene Structure

```
Player (CharacterBody2D)
├── Sprite2D                         # or AnimatedSprite2D
├── AnimationPlayer                  # for programmatic animations (hurt flash, etc.)
├── CollisionShape2D                 # CapsuleShape2D recommended for slopes
├── StateMachine (Node)              # see State Machine section
│   ├── StateIdle (Node)
│   ├── StateRun (Node)
│   ├── StateJump (Node)
│   ├── StateFall (Node)
│   ├── StateHurt (Node)
│   └── StateDead (Node)
├── PowerManager (Node)              # manages unlocked powers, delegates to PowerState
├── HitboxComponent (Area2D)         # detects damage received
├── CoyoteTimer (Timer)              # coyote time for jumps off ledges
├── JumpBufferTimer (Timer)          # input buffer for jump
└── CompanionAnchor (Marker2D)       # position Renato/dog should follow
```

**Use CharacterBody2D, not RigidBody2D.** Kinematic control is mandatory for responsive platformer feel. RigidBody2D introduces physics lag.

---

## State Machine (Player Movement)

Use the **node-based pattern** for the player. It is more code to set up once, but it makes adding new states (power-activated states, boss-specific states) straightforward without touching existing states.

Do NOT use enum-based for the player. The player has too many states (normal movement + 7 power variations) for a single-script approach to stay readable.

```
StateMachine (Node)
  - current_state: State
  - change_state(new_state: State) -> void
      calls current_state.exit()
      calls new_state.enter()

State (base class, extends Node)
  - parent: Player              # set by StateMachine.init()
  - enter() -> void
  - exit() -> void
  - process_input(event) -> State   # return null = no transition
  - process_physics(delta) -> State
```

Each state script is ~30-60 lines. The StateMachine script is ~40 lines. States call `parent.velocity`, `parent.is_on_floor()`, `parent.animations.play()` directly — they own the parent reference.

State transitions are explicit: `process_physics()` returns the next state object (or null to stay). The StateMachine calls `change_state()` when a non-null state is returned.

**Gravity is applied in every state that can be airborne.** Do not rely on a "global gravity application" outside states — it creates coupling.

---

## Level Scene Structure

```
Level (Node2D)
├── TileMapLayer (TileMapLayer)      # ground, walls, one-way platforms
├── TileMapLayer_Background          # parallax background tiles
├── TileMapLayer_Foreground          # decorative foreground
├── Spawns (Node2D)                  # spawn point markers
│   └── PlayerSpawn (Marker2D)
├── Enemies (Node2D)                 # all enemy instances
├── Collectibles (Node2D)            # items, power fragments
├── NPCCompanions (Node2D)           # Renato, dog (if unlocked)
├── Triggers (Node2D)                # Area2D nodes for events, checkpoints
│   ├── LevelEndTrigger
│   ├── CheckpointTrigger
│   └── DialogueTrigger
├── BossEntrance (Node2D)            # null unless level has boss
└── LevelController (Node)          # script: spawns Player, connects signals
```

**TileMapLayer vs TileMap:** In Godot 4.3+ use `TileMapLayer` (the successor node). Each layer is a separate node. Three layers is the typical split: background, main gameplay surface, foreground decoration.

**Physics layers on TileSet:**
- Layer 0: solid collision
- Layer 1: one-way platforms
- Layer 2: damage zones (spikes, etc.)
- Layer 3: water/special traversal

This keeps collision detection code clean: `is_on_floor()` tests Layer 0 only.

---

## World / Level Loading

Levels within a world live in a flat directory:

```
res://worlds/
  world_01_osasco/
    world_01.tscn          # the level itself
    world_01_boss.tscn     # boss arena (loaded inside level via signal)
  world_02_faculdade/
    ...
  overworld/
    overworld.tscn
```

Do NOT use `ResourceLoader.load_threaded_request()` for MVP. Use synchronous loading behind a fade transition — loads are fast for 2D games with reasonable asset sizes. Add async loading in a later pass only if measured load times exceed 1 second.

The LevelController script on each level emits `level_completed` to GameManager, which then:
1. Updates SaveManager.save_data.completed_levels
2. Triggers scene change back to Overworld (or to next level)

---

## Overworld Map Scene

```
Overworld (Node2D)
├── MapBackground (Sprite2D or TileMapLayer)
├── Worlds (Node2D)                  # all 8 world entry points
│   ├── WorldNode_1 (Area2D)         # clickable/navigatable world icon
│   │   ├── Sprite2D
│   │   ├── CollisionShape2D
│   │   └── LockIcon (Node2D)        # visible when locked
│   └── WorldNode_2..8
├── PlayerCursor (CharacterBody2D)   # the overworld navigation character
│   └── (simplified movement, no full state machine needed)
├── PathConnectors (Node2D)          # visual lines connecting nodes
└── OverworldUI (CanvasLayer)        # world name, completion status
```

The overworld does NOT use the full player state machine. Use a simple script with `move_and_slide()` and no gravity — the player walks left/right between world nodes.

World unlock logic: `WorldNode.locked = SaveManager.save_data.worlds_completed < world_index`. This is evaluated once on `_ready()` and again whenever SaveManager emits a `save_updated` signal.

---

## Boss Fight Architecture

Each boss is a **self-contained scene** that is instantiated inside the level, replacing the level gameplay but sharing the same Main tree.

```
BossArena (Node2D)
├── Boss (CharacterBody2D or AnimatableBody2D)
│   ├── Sprite2D
│   ├── AnimationPlayer
│   ├── CollisionShape2D
│   ├── BossStateMachine (Node)
│   │   ├── Phase1_Idle
│   │   ├── Phase1_Attack
│   │   ├── Phase2_Enraged
│   │   └── Phase_Defeated
│   ├── HealthComponent (Node)       # emits health_changed, died
│   └── HurtboxComponent (Area2D)    # receives damage from player hitboxes
├── Arena (TileMapLayer)             # boss room tiles
├── BossHealthBar (CanvasLayer)      # boss-specific UI
└── BossController (Node)           # orchestrates phase transitions, connects signals
```

**Phase transitions** are driven by `HealthComponent.health_changed` signal. When HP crosses the 50% threshold, BossStateMachine switches to the enraged phase. BossController connects this:

```gdscript
func _ready():
    $Boss/HealthComponent.health_changed.connect(_on_health_changed)

func _on_health_changed(new_hp: float, max_hp: float):
    if new_hp / max_hp <= 0.5:
        $Boss/BossStateMachine.change_state($Boss/BossStateMachine/Phase2_Enraged)
```

Use a **node-based state machine for every boss**, even simple ones. Boss behaviour complexity always grows after the first playtest.

---

## Cutscene / Dialogue System

**Use Dialogic 2.** Do not build a custom dialogue system for v1.

Rationale: Dialogic 2 provides branching timelines, character portraits, text effects, signal hooks to trigger GDScript functions (unlock powers, play animations), and CSV translation. Building equivalent functionality from scratch takes 3-6 weeks. Dialogic 2 compresses this to days.

Dialogic 2 requires **Godot 4.3+**. The project should target 4.3 or later.

### Integration Pattern

```gdscript
# In a Trigger Area2D or LevelController:
func _on_dialogue_trigger_body_entered(body):
    if body is Player:
        Dialogic.start("timeline_world1_intro")
        GameManager.cutscene_started.emit()

# Dialogic emits its own signal when finished:
func _ready():
    Dialogic.timeline_ended.connect(_on_dialogue_finished)

func _on_dialogue_finished():
    GameManager.cutscene_finished.emit()
```

### Cutscene Pattern (non-dialogue, pure cinematic)

For the Santiago proposal cutscene (World 5) and the ending credits, use Godot's built-in **AnimationPlayer** driven by a `CutsceneController` node:

```
CutsceneController (Node)
├── AnimationPlayer              # drives camera, sprite positions, fades
├── Camera2D
├── CharacterSprites (Node2D)   # Natalia, Renato pixel art
└── SubtitleLabel (Label)       # optionally driven by AnimationPlayer tracks
```

Keep dialogue in Dialogic timelines. Keep motion/camera in AnimationPlayer. Do not mix them.

---

## Resource System (Game Data)

Custom Resources are Godot's equivalent to Unity's ScriptableObjects. Use them for all static data.

**Important:** When multiple instances need independent data (each enemy has its own health), always call `.duplicate()` on the shared resource in `_ready()`. Otherwise all instances share the same data object.

### Core Resource Definitions

```gdscript
# resources/save_data.gd
class_name SaveData
extends Resource

@export var worlds_completed: int = 0
@export var completed_levels: Array[String] = []
@export var unlocked_powers: Array[String] = []
@export var checkpoints: Dictionary = {}  # level_path -> checkpoint_index
@export var play_time_seconds: float = 0.0
```

```gdscript
# resources/power_data.gd
class_name PowerData
extends Resource

@export var id: String = ""
@export var display_name: String = ""
@export var icon: Texture2D
@export var world_unlocked_in: int = 0
@export var description: String = ""
```

```gdscript
# resources/enemy_stats.gd
class_name EnemyStats
extends Resource

@export var max_health: float = 10.0
@export var movement_speed: float = 80.0
@export var damage: float = 1.0
@export var xp_value: int = 0
```

All `.tres` files live in `res://data/`. Scripts live in `res://resources/`. This separates data (`.tres`) from schema (`.gd`).

---

## Communication Patterns

Three patterns are used, with strict rules about when to use each:

| Pattern | When to Use | When NOT to Use |
|---------|-------------|-----------------|
| **Signals (local)** | Parent-child or sibling within same scene | Cross-scene communication |
| **Signals via GameManager (global bus)** | Cross-scene events (level complete, power unlock, player death) | Events local to one scene |
| **Direct node reference** | Child accessing parent's exported properties (state machine accessing `parent.velocity`) | Nodes in different scene branches |
| **Autoload property access** | Reading save data, checking global state | Triggering behaviour (use signals instead) |

**Never use `get_node("/root/...")` absolute paths.** They break when scenes are reorganized. Export node references via `@export var` or pass via `init()` method.

---

## Component / Composition Pattern

Godot 4's node tree IS the composition system. Use small focused nodes as components, not inheritance chains.

**Recommended components (reusable Node scripts):**

```
HealthComponent (Node)
  - max_health: float
  - current_health: float
  - signal health_changed(new, max)
  - signal died
  - take_damage(amount)
  - heal(amount)

HitboxComponent (Area2D)
  - damage: float
  - on_body_entered: connects to target's HealthComponent

HurtboxComponent (Area2D)
  - signal hit_received(hitbox: HitboxComponent)
  - filters by collision layer

KnockbackComponent (Node)
  - apply_knockback(direction, force)
  - requires parent CharacterBody2D

FlashComponent (Node)
  - requires parent with material supporting shader
  - flash_white(duration)  # hit feedback
```

Attach these as children to any entity that needs them. An enemy that needs health but not knockback just has HealthComponent. No inheritance required.

**Avoid extending CharacterBody2D directly in a deep hierarchy.** The pattern `Enemy extends CharacterBody2D` is fine. The pattern `FlyingEnemy extends GroundEnemy extends Enemy extends CharacterBody2D` is a maintenance trap.

---

## Multiplatform Export Architecture

### Rendering Method

For all platforms, use the **Compatibility** renderer (WebGL 2.0 equivalent). Do NOT use Forward+ or Mobile renderer for this project.

Rationale: HTML5 export only supports Compatibility renderer. Since the game targets Web as a priority platform, lock Compatibility from day one. Pixel art 2D games do not need Forward+'s features.

### Input Abstraction

All input goes through InputMap actions. No hardcoded key checks.

```gdscript
# Always:
Input.is_action_pressed("jump")

# Never:
Input.is_key_pressed(KEY_SPACE)
```

Define separate action layers:
- `move_left`, `move_right`, `jump`, `attack`, `power_1`..`power_7`, `interact`, `pause`

On mobile, virtual buttons emit these same InputMap actions. The player script never knows the input source.

### Web-Specific Constraints

- Audio: Godot 4.3+ web exports use Sample playback mode. AudioEffects and reverb buses do not work on web. Keep audio design simple: direct playback, no reverb chains.
- Threads: Web export runs without threads by default. Avoid background loading threads.
- File system: `user://` maps to browser IndexedDB on web. Save/load with ResourceSaver/ResourceLoader works correctly.
- Screen: Use a fixed viewport size (e.g. 480x270 at 2x scale = 960x540) with `stretch_mode = canvas_items` and `stretch_aspect = keep`. This works identically on desktop, web, and mobile.

### Mobile

Mobile export is deferred to post-v1 per PROJECT.md. When adding it:
- Virtual joystick plugin (e.g. `GodotVirtualJoystick`) emits InputMap actions.
- Touch area buttons for jump/attack emit InputMap actions.
- The player script requires zero changes.

---

## Suggested Scene / File Structure

```
res://
├── autoloads/
│   ├── game_manager.gd
│   ├── save_manager.gd
│   └── audio_manager.gd
├── scenes/
│   ├── main/
│   │   └── main.tscn              # entry point
│   ├── player/
│   │   ├── player.tscn
│   │   ├── player.gd
│   │   └── states/
│   │       ├── state_machine.gd
│   │       ├── state.gd           # base class
│   │       ├── state_idle.gd
│   │       ├── state_run.gd
│   │       ├── state_jump.gd
│   │       ├── state_fall.gd
│   │       └── state_hurt.gd
│   ├── overworld/
│   │   ├── overworld.tscn
│   │   └── world_node.tscn        # reusable world icon
│   ├── levels/                    # template and shared level pieces
│   │   └── level_base.tscn        # inherited scene base
│   ├── ui/
│   │   ├── hud.tscn
│   │   ├── pause_menu.tscn
│   │   └── transition_layer.tscn
│   └── components/
│       ├── health_component.tscn
│       ├── hitbox_component.tscn
│       └── hurtbox_component.tscn
├── worlds/
│   ├── world_01_osasco/
│   │   ├── world_01.tscn
│   │   └── world_01_boss.tscn
│   └── world_02..08/
├── resources/                     # Resource class scripts (.gd)
│   ├── save_data.gd
│   ├── power_data.gd
│   └── enemy_stats.gd
├── data/                          # Resource instance files (.tres)
│   ├── powers/
│   │   ├── power_sketch.tres
│   │   └── power_mapa_urbano.tres
│   └── enemies/
│       └── gremlin_de_prazo.tres
├── assets/
│   ├── sprites/
│   ├── tilemaps/
│   ├── audio/
│   └── fonts/
└── dialogic/                      # Dialogic 2 auto-creates this
    ├── characters/
    └── timelines/
```

---

## Suggested Build Order

Build in this order. Each step produces something testable before moving to the next.

**Step 1 — Core Player Loop (1-2 weeks)**
Build `player.tscn` with state machine (Idle, Run, Jump, Fall). One placeholder level. Verify movement feels right on all target platforms. This is the most iterated thing in the game — get it right first.

**Step 2 — Level Infrastructure (1 week)**
Build `main.tscn`, scene transition system, `LevelController`, TileMapLayer setup with physics layers. Build one complete World 1 level without enemies.

**Step 3 — Enemy + Combat Foundation (1 week)**
Build HealthComponent, HitboxComponent, HurtboxComponent as reusable components. One enemy type (the Malandro de Rolê from World 1). Verify hit/hurt/death loop.

**Step 4 — Save System (3-5 days)**
Build SaveData resource. Build SaveManager autoload. Integrate checkpoint save on level completion. Test save/load on both PC and browser (IndexedDB).

**Step 5 — Overworld Map (1 week)**
Build overworld scene with all 8 world nodes. Connect to SaveData for unlock state. Transition to/from levels.

**Step 6 — Dialogic + First Cutscene (3-5 days)**
Install Dialogic 2. Wire up one dialogue trigger in World 1. Build the Santiago proposal cutscene with AnimationPlayer. Validate the Dialogic/AnimationPlayer integration pattern.

**Step 7 — Power System (1 week)**
Build PowerManager on the player. Implement Sketch (World 2 power) as the reference implementation. Wire power unlock to SaveData. All subsequent powers follow this pattern.

**Step 8 — First Boss (1 week)**
Build Boss 1 (O Pai Desconfiante) with node-based state machine, 2 phases, health bar. This is the reference implementation for all 7 remaining bosses.

**Step 9 — World-by-world iteration**
Now that all infrastructure exists, build each world's levels, enemies, boss, and cutscenes. One world at a time.

---

## Patterns Summary — What to Use for This Project

| Concern | Pattern | Why |
|---------|---------|-----|
| Player movement | Node-based state machine | 7 power states + normal states — too complex for enums |
| Boss phases | Node-based state machine | Phase transitions are explicit and testable |
| Enemy behaviour | Node-based state machine (or enum if simple) | Simple enemies can use enum |
| Cross-scene events | GameManager signal bus | Avoids tight coupling between scenes |
| Game data | Custom Resource (.tres) | Static typing, works with Godot types, no JSON conversion |
| Save/Load | ResourceSaver/ResourceLoader + SaveData Resource | Cleanest Godot-native approach |
| Dialogue/Cutscenes | Dialogic 2 timelines | Weeks of work avoided |
| Cinematic cutscenes | AnimationPlayer driven by script | Direct control, no plugin needed |
| NPC companions | Simple follow script + NavigationAgent2D | Dog + Renato don't need complex AI |
| Reusable behaviours | Component nodes (HealthComponent, etc.) | Composition over inheritance |
| Input handling | InputMap actions only | Platform-agnostic from day one |
| Rendering | Compatibility mode only | Required for HTML5 export |

---

## Sources

- [Godot 4 Singletons (Autoload) — Official Docs](https://docs.godotengine.org/en/stable/tutorials/scripting/singletons_autoload.html) — HIGH confidence
- [Godot Recipes: Platform Character — KidsCanCode](https://kidscancode.org/godot_recipes/4.x/2d/platform_character/index.html) — HIGH confidence
- [Finite State Machine in Godot 4 — GDQuest](https://www.gdquest.com/tutorial/godot/design-patterns/finite-state-machine/) — HIGH confidence
- [Saving and Loading Games in Godot 4 — GDQuest](https://www.gdquest.com/library/save_game_godot4/) — HIGH confidence
- [Starter State Machines in Godot 4 — The Shaggy Dev](https://shaggydev.com/2023/10/08/godot-4-state-machines/) — HIGH confidence
- [Dialogic 2 Documentation](https://docs.dialogic.pro/) — HIGH confidence
- [Node-Based State Machine — Godot Foundry](https://godotfoundry.com/blog/godot-4-state-machine-tutorial) — MEDIUM confidence
- [Godot 4 Web Export — Official Docs](https://docs.godotengine.org/en/latest/tutorials/export/exporting_for_web.html) — HIGH confidence
- [Godot Mobile Update April 2026 — Official Blog](https://godotengine.org/article/godot-mobile-update-apr-2026/) — HIGH confidence
- [Using TileMaps — Official Docs](https://docs.godotengine.org/en/latest/tutorials/2d/using_tilemaps.html) — HIGH confidence
- [Custom Resources for Game Data — UhiyamaLab](https://uhiyama-lab.com/en/notes/godot/custom-resource-data-driven/) — MEDIUM confidence
- [Boss State Machine Pattern — Ludonauta Devlog](https://ludonauta.itch.io/platformer-essentials/devlog/1089921/hollow-knight-inspired-boss-fight-in-godot-4) — MEDIUM confidence
