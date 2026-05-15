# Feature Landscape: Narrative 2D Platformer

**Domain:** Narrative pixel art 2D platformer (Celeste / Shovel Knight tier)
**Project:** Jogo da Natalia
**Researched:** 2026-05-15

---

## Table Stakes

Features players expect from this genre. Missing one = the game feels unfinished or feels bad to control. These are not optional.

### Movement Feel

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Coyote time | Industry standard since 1990s; absent = players constantly miss jumps they "should have made" | Low | 6-10 frames after leaving platform edge; Celeste uses ~5 frames. Godot 4 has Timer-based solutions in Asset Library. |
| Jump buffering | Removes frame-perfect timing frustration on landings | Low | Buffer window of 6-10 frames where a jump input before landing still fires on the landing frame. |
| Variable jump height | Holding jump = higher arc; tap = shorter hop. Players expect control over arc. | Low | Achieved by halving gravity when jump button held near apex. Celeste does exactly this. |
| Responsive air control | Character must steer in the air; "floaty" = unplayable for precision sections | Medium | Tune air friction separately from ground friction; Natalia should feel tight, not slippery. |
| Corner correction | Clips player around a corner's edge when running into a wall at near-miss distance | Low-Medium | Celeste does this for both horizontal dash and standard wall collision within 4 pixels. Prevents constant "invisible wall" frustration. |
| Consistent ground feel | No ice-physics, no random momentum loss on landing | Low | Default Godot CharacterBody2D requires tuning — the default is too slidey. |

### Narrative Delivery

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Skippable dialogue | Players on second runs or impatient players will quit if dialogue blocks gameplay | Low | Every dialogue line must be advance-on-button-press; cutscenes need a skip option after first viewing. |
| Character portraits in dialogue | Without a face, dialogue is anonymous and emotionally flat in pixel art | Low | Even 16x16 portrait thumbnails work. Celeste uses small pixel art busts. For Natalia, tie to real-person sprites. |
| Speaker indicator | Player must know who is talking at a glance | Low | Name tag above box OR portrait on the active speaker's side. |
| Pre/post world story beats | Players expect a narrative moment at world start and world end, minimum | Medium | Can be cutscene, dialogue box sequence, or even a static illustrated panel. |

### Checkpoint / Save

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Autosave after each screen/section | Modern players don't manually save; unexpected closing = lost progress = rage quit | Low | Save after every completed screen. Godot's FileAccess is straightforward. |
| Respawn at last checkpoint, not world start | Losing 10 minutes of progress to one death destroys momentum | Low | Celeste respawns at screen start — that granularity is the gold standard. |
| Instant respawn (< 1 second) | Long death animation or reload screen = rhythm broken | Low | Skip death anim on any button press. Target < 500ms to playable state. |
| No lives system | Lives systems have no place in narrative games; they punish story engagement | Low | Simply do not implement lives. Progress is the only metric that matters. |

### Core Progression

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| World/level select after completion | Players expect to replay; locked progression post-completion is a wall | Low | Overworld map with completed worlds accessible. |
| Ability introduction teaching moment | New powers given without explanation = confused players. Teach in safe space first. | Medium | After unlock, give one room with no enemies designed to showcase and require the new ability. |
| Clear visual language for hazards | Red/danger colors, animated spikes, clear hitbox-matching visuals | Medium | Pixel art must READ clearly. Death from invisible or ambiguous hazards = immediate distrust. |

### Boss Fights

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Telegraphed attacks | Boss attacks must have wind-up animations the player can learn | Medium | A unique pose/animation preceding each attack. Players die to learn, not to pixel-perfect dodge without warning. |
| Distinct phases or escalation | Single-pattern bosses bore players; at least one phase shift expected | Medium | Add one new pattern/attack at 50% HP. Signal phase shift with dramatic visual/sound. |
| No RNG in boss patterns | Bosses that randomly change patterns teach nothing and frustrate. | Low | Deterministic sequences. Pattern variance should come from PLAYER actions, not dice rolls. |

### Accessibility (Minimum Bar)

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Rebindable keys/controls | Standard expectation; particularly important for Web (HTML5) export | Low | Godot 4's InputMap supports this natively. Expose via settings menu. |
| Controller support | Many platformer players use gamepads; PC + Web both support this | Low | Godot 4 handles this natively. Test with a gamepad from day one. |
| Pause from any point | Players have lives outside the game; can't pause = platform abandoned | Low | Implement early; often missed in prototypes. |

### Juice / Game Feel (Minimum)

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Landing dust particle | "Thump" when landing; without it the character feels weightless | Low | 2-4 pixel dust particles on landing. Tied to landing velocity. |
| Squash on land, stretch on jump | Celeste does this at 1-pixel resolution. Without it, sprite feels like a rigid box. | Low | One frame squash frame before jump, one frame stretch at apex. |
| Enemy hit feedback | Hit sound + brief flash. Without it, attacking feels disconnected. | Low | White flash (shader) on enemy hit for 1-3 frames + hit sound. |
| Death effect | Character should "react" to death, not just disappear | Low | Brief particle burst or "poof" animation before respawn. |

---

## Differentiators

Features that make Jogo da Natalia specifically worth playing. These are what will make it memorable, not just functional. Prioritize based on emotional payoff relative to implementation cost.

### Emotional Narrative Mechanics

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Ludonarrative harmony: difficulty mirrors emotional state | Worlds 1-4 (hard) being mechanically harder, Worlds 5-8 gradually easier, is the entire thesis of the game. | High | This is how Celeste works — the mountain is Madeline's anxiety made physical. Do not sacrifice this for "balance." |
| Per-world color palette shift | Visual emotional progression from Osasco grey → Zaragoza vivid color. Player FEELS the journey without reading anything. | Medium | Plan palettes for all 8 worlds upfront. Reference the project doc tone descriptions. |
| Ability unlock tied to story beat | Powers feel earned when the story justifies them. Sketch unlocked in the university world IS the university chapter's payoff. | Medium | Already designed in PROJECT.md. The implementation must make the connection obvious — unlock cutscene should show Natalia drawing. |
| "Amor Power" shared mechanic | When Renato is nearby, a passive buff activates. No platformer reference game does this — it is unique to this story. | Medium | Proximity detection + visual aura. The mechanic should communicate: being together makes you stronger. |
| Real-world photo credits ending | Personal touch that no other game has. Natalia is a real person. | Low | Scrolling pixel art with intermixed real photos. Celeste used a credits sequence; going further here is affordable and meaningful. |

### NPC Companion Design

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Dog as gameplay companion (World 4+) | A Short Hike's lightness comes partly from having a companion. The dog breaking tension in the pandemic arc is emotionally correct. | High | Avoid the escort-mission trap: the dog must NEVER be something the player must protect or keep alive. It provides bonuses and charm. It should run ahead happily, not lag behind waiting to die. |
| Renato as optional puzzle element | Appearing in specific rooms to unlock shortcuts via "Amor Power" makes him feel present without being intrusive | Medium | He should appear, help, and move on. Not an escort. Not a follower. A cameo with mechanical weight. |

### Boss Fight Differentiation

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Bosses that reflect the narrative context | "O Pai Desconfiante" defeated via dialogue choices, not combat. "O Gestor Toxico" defeated without losing mental health HP. These are the game's thesis made playable. | High | Each boss needs a mechanic unique to its world theme. This is what separates a narrative platformer from a standard one. |
| Pre-boss world-tone contrast | The player enters the boss feeling the pressure of that world. The boss room should LOOK and FEEL like the climax, not just be a larger enemy. | Medium | Boss room design matters as much as boss mechanics. Use music shift, visual framing, and a brief loading pause to signal "this is the moment." |
| Vocabulary mini-game (Mundo 6) | The "Barreira do Idioma" boss requiring Spanish vocabulary is specific to the story and physically impossible to implement generically. | High | Keep it simple: present 3 Spanish word options, choose correct one to deal damage. Wrong answer = damage to player. Teaches actual Spanish. |

### Overworld Map

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Map that shows emotional geography | The overworld should visually show the journey from dark Osasco to bright Zaragoza — a map that reads as an emotional arc, not just a level select | Medium | Pan from left (grey/dark) to right (colorful/bright) as the player progresses. Completed worlds shift in palette on the map. |
| Animated world markers | A static dot per world is functional. An animated thumbnail showing each world's character (a small pixel art vignette) communicates the world's story instantly. | Medium | Even a 3-frame idle animation per world on the map is enough. |

### Polish and Memorable Moments

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Santiago proposal cutscene | Already in the design doc as a "special cutscene." This is THE moment of the game — the emotional center. | High | Invest disproportionate polish here. Use a wider aspect ratio for cinematic framing, dedicated music, slower pixel art animation style distinct from gameplay. |
| Per-world music palette | Music must shift emotionally across worlds the way the visuals do. This is how Celeste's OST works — each chapter has a distinct musical identity that mirrors the emotional state. | High | Budget for 8 distinct music themes. Even simple chiptune tracks work if each one FEELS different in tone. |
| Hit-stop on boss damage | A 2-4 frame game freeze when Natalia lands a meaningful hit on a boss communicates IMPACT. | Low | One of the highest ROI "juice" features. A single boolean freeze for 3 frames on key hits. |
| Screen shake on boss attacks | Amplifies bosses feeling threatening without needing elaborate graphics | Low | A 3-5 pixel position offset for 5-8 frames on heavy boss attacks. |

### Accessibility as Differentiator (Celeste Model)

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Assist Mode (Celeste-style) | Allow game speed reduction (0.5x), invincibility toggle, and infinite stamina. Frame it without judgment: "This is YOUR story, play it your way." | Medium | Celeste's assist mode is celebrated as respectful, not "easy mode." The framing is everything. |
| Colorblind-safe palette design | Design world palettes from the start to be colorblind-accessible. Retrofitting is expensive; baking it in is cheap. | Low | Use saturation/lightness contrast in addition to hue. Test palettes with colorblind simulators (Coblis). |

---

## Anti-Features

Things that narrative platformers commonly add that demonstrably hurt the experience. Deliberately avoid these.

### Anti-Feature 1: Unskippable Cutscenes and Dialogue

**What goes wrong:** Player dies just before a cutscene. Has to watch it again. Loses the rhythm. Closes the game.

**Why it happens:** Developer investment in cutscene leads to "players should see this" thinking. But players who have seen it have already seen it.

**Consequence:** Destroys the fast retry loop that makes hard platforming sections learnable. A player who dies 20 times learning a boss should never watch the pre-boss cutscene more than once.

**Prevention:** All cutscenes skippable after first play. Implement a "seen" flag per cutscene per save file. For boss intros especially: once seen, skip on any button press.

---

### Anti-Feature 2: Escort Mission Companion

**What goes wrong:** The dog or Renato has health. The player has to protect them. The player dies because the companion walked into a spike. This is now a frustrating escort mission, not an emotional companion story.

**Why it happens:** Developers conflate "the companion matters narratively" with "the companion must be mechanically vulnerable."

**Consequence:** Players start resenting the companion — the opposite of the intended emotional effect.

**Prevention:** Companions are invincible or trivially protected. The dog runs ahead but phases through hazards or has damage immunity. Renato appears, interacts, and leaves. They should feel like buffs, not liabilities.

---

### Anti-Feature 3: Collectible Bloat

**What goes wrong:** 300 collectibles scattered across 8 worlds. Players feel compelled to find them. The game becomes a checklist, not a story.

**Why it happens:** Collectibles increase playtime metrics. But this is a narrative experience; playtime is not the value.

**Consequence:** Pacing destroyed. Emotional moments interrupted by "I think I missed a collectible in that room." Story tone collapses under scavenger hunt logic.

**Prevention:** If collectibles exist (optional strawberries / memories / photos of real places), keep them at 3-5 per world maximum. Each one should have a story reason. No completion achievement that requires 100% collection.

---

### Anti-Feature 4: Punishing Mandatory Backtracking

**What goes wrong:** "The key to the next door is back in World 3." Players traverse already-seen content with no new gameplay. Pacing sags.

**Why it happens:** Metroidvania influence. But this is a LINEAR narrative game, not an interconnected world.

**Consequence:** Narrative momentum killed. "Oh, I need to go back" breaks immersion and emotional arc.

**Prevention:** This game is linear. Worlds 1-8 in order. New abilities may optionally reveal secrets in previous worlds (a light optional layer), but progression must never require backtracking.

---

### Anti-Feature 5: Random Enemy Spawn or RNG-dependent Sections

**What goes wrong:** Player learns a section, arrives in the same position, but enemies spawned differently. The lesson from the previous death is invalidated.

**Why it happens:** RNG creates "variety" — but in platformers, it creates unfairness.

**Consequence:** Players can't learn the level. "That was unavoidable" — the most frustrating sentence in platformers.

**Prevention:** Enemy placement and patterns are deterministic within a screen. Enemies reset to their exact starting positions on player respawn. The only variable is the player.

---

### Anti-Feature 6: Mechanical Tutorial Pop-Ups

**What goes wrong:** "Press [SPACE] to jump." Text box appears. Blocks screen. Player presses a button. Another box. "Press [X] to dash." This is not a game, it's a manual.

**Why it happens:** Developers fear players missing mechanics. Legitimate concern, wrong solution.

**Consequence:** Pacing destroyed in the first 5 minutes. Players who already know how to play are patronized. New players click through without reading.

**Prevention:** Teach through design. Celeste teaches the dash by placing an unreachable gem visible through a wall with an obvious gap. One deliberate room layout. No text box needed. For new abilities in Jogo da Natalia: the unlock cutscene, then one room requiring and rewarding the ability. The room teaches it; nothing is explained.

---

### Anti-Feature 7: Lives System or Continues

**What goes wrong:** Player runs out of lives. "GAME OVER." Sent back to level start. The entire emotional arc of the world must be replayed to reach the same point.

**Why it happens:** Old arcade design. Not appropriate for 2026.

**Consequence:** Players who die frequently are specifically punished. The narrative game becomes inaccessible. The exact opposite of "every player deserves to experience this story."

**Prevention:** Infinite attempts. No lives. No game over screen. Respawn instantly. The death counter (optional, hidden in stats) exists only if the player wants to see it — it is never used to punish.

---

### Anti-Feature 8: Tonal Inconsistency from Humor Forced into Dark Worlds

**What goes wrong:** Worlds 1-4 have a specific dark/heavy emotional tone per the design doc. Comic relief enemies or joke dialogue in these sections undercut the weight.

**Why it happens:** Developers fear "too dark" and inject humor to lighten. But tone is earned — and inconsistency destroys it.

**Consequence:** Players don't believe in the emotional stakes. The Celeste comparison is instructive: Theo's jokes are funny because the rest of the game earns the tension. One snarky enemy in the pandemic world breaks the pandemic world.

**Prevention:** Hold tone rigorously per world. Dark worlds (1-4) can have warmth (Renato appearing), but not comedy. Light worlds (6-8) can have humor. Per the project design, this is already planned — maintain discipline during implementation.

---

## Feature Dependencies

```
Coyote Time + Jump Buffer → All movement sections (must exist before any level design)
Ability unlock system → Power teaching room (teach room requires ability to already exist)
Checkpoints → Boss fights (boss rooms need checkpoint before entrance)
Checkpoint system → Death counter display (optional)
Per-world palette → Overworld map emotional geography
Boss unique mechanic → Boss pre-boss narrative moment (the mechanic must reinforce the story)
Companion dog intro → Amor Power proximity buff (dog is introduced World 4; Amor Power World 5)
Santiago cutscene → Amor Power unlock (cutscene IS the unlock trigger for Mundo 5)
All 7 powers → Combo Final boss (boss is mechanically blocked if any prior power missing)
```

---

## MVP Recommendation

Build in this priority order for the playable prototype:

**Non-negotiable (nothing works without these):**
1. Coyote time + jump buffer + variable jump height — these are the foundation; get them right before building a single level
2. Checkpoints per screen + instant respawn + no lives — without this, playtesting is painful for the tester
3. Basic dialogue system (skippable, portrait, speaker name) — narrative is the product; need this early

**World 1 complete requires:**
4. Basic attack / dash (Natalia's baseline moveset)
5. Overworld map with at least 1 world selectable
6. One boss fight with telegraphed patterns and 2 phases
7. Landing dust particle + enemy hit flash + screen shake (minimum juice)
8. Autosave

**Defer until World 2+:**
- Assist Mode — needed before public release, not needed for internal playtesting
- Colorblind palette audit — design with it in mind from start, formal audit before release
- Real-photo credits sequence — World 8 content, last thing built
- Santiago proposal cutscene — Mundo 5 content, build when reaching that milestone

---

## Sources

- Matt Thorson (Celeste dev) on game feel mechanics: https://threadreaderapp.com/thread/1238338574220546049.html
- Celeste & Forgiveness design article: https://www.maddymakesgames.com/articles/celeste_and_forgiveness/index.html
- Celeste and emotional/mental health narrative analysis: https://medium.com/@felixxiang27/celeste-mental-health-ludonarrative-harmony-and-community-065d38318c87
- Celeste difficulty and assist mode: https://www.vice.com/en/article/celeste-difficulty-assist-mode/
- Boss Battle Design and Structure: https://www.gamedeveloper.com/design/boss-battle-design-and-structure
- Enemy attack telegraphing: https://www.gamedeveloper.com/design/enemy-attacks-and-telegraphing
- Shovel Knight design lessons: https://code.tutsplus.com/4-game-design-lessons-we-can-learn-from-shovel-knight--cms-21966a
- Checkpoints and accessibility: https://access-ability.uk/2022/04/25/checkpoints-save-states-and-save-availability/
- Environmental storytelling: https://gamedesignskills.com/game-design/environmental-storytelling/
- Celeste Godot 4 coyote time recipe: https://kidscancode.org/godot_recipes/4.x/2d/coyote_time/index.html
- Squash and stretch pixel art: https://www.sprite-ai.art/guides/animation-principles
- Gameplay design patterns for dialogues: https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=3c9e5c7f0552c3de3b420a1acc09d686d3b3e15e
- Common indie game mistakes: https://www.positech.co.uk/cliffsblog/2021/10/14/common-mistakes-by-indie-game-developers/
- Celeste death and progress design: https://medium.com/super-jump/celeste-and-the-celebration-of-progress-through-death-398a3c0e5cc0
- NPC companion design: https://dl.acm.org/doi/fullHtml/10.1145/3464327.3464371
- Even the Ocean world map design: https://medium.com/@han_tani/even-the-ocean-designing-a-game-s-world-map-f26edf282d99
