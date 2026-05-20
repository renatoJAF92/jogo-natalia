# Phase 0: Fundação — Research

**Researched:** 2026-05-20
**Domain:** Godot 4.4 project setup, Git LFS, pixel art config, CI/CD GitHub Actions, web export
**Confidence:** HIGH (stack já validado no STACK.md; decisões travadas no CONTEXT.md)

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

- **D-01:** Godot 4.4.x — versão estável com TileMapLayer, melhor suporte pixel art e imagem Docker godot-ci disponível. Não usar 4.5.x ou 4.6.x nesta fase.
- **D-02:** GDScript (não C#). C# bloqueia export HTML5 — decisão irrevogável para este projeto.
- **D-03:** Nome do projeto no project.godot: `"Destiny — Tales of Natalia"`. Este nome aparece na janela do jogo, builds e itch.io.
- **D-04:** Resolução base do viewport: **320×180**. Decisão permanente — não mudar depois sem quebrar todo o level design.
- **D-05:** Configurações pixel art obrigatórias em Project Settings:
  - Rendering > Textures > Canvas Textures > Default Texture Filter = **Nearest**
  - Display > Window > Stretch > Mode = **canvas_items**
  - Display > Window > Stretch > Scale Mode = **integer**
  - Display > Window > Size = **320 × 180**
  - Rendering > 2D > Snap 2D Transforms to Pixel = **On**
  - Rendering > Renderer = **Compatibility** (obrigatório para web export)
- **D-06:** Git LFS rastreia via .gitattributes: `*.png`, `*.jpg`, `*.wav`, `*.ogg`, `*.mp3`, `*.ttf`, `*.otf`, `*.scn`, `*.res`
- **D-07:** .gitignore mínimo: `.godot/`, `*.translation`, `export/`
- **D-08:** Estrutura de pastas: `scenes/`, `assets/sprites/player|enemies|ui/`, `assets/audio/sfx|music/`, `scripts/`, `autoloads/`, `export/`, `.github/workflows/`
- **D-09:** `autoloads/` vazio na Phase 0. Nenhum script criado aqui.
- **D-10:** `export_presets.cfg` commitado no repositório.
- **D-11:** 3 presets: Web (HTML5), Windows Desktop, macOS.
- **D-12:** Testar localmente com `godot --export-release "Web" ...` antes de declarar fase completa.
- **D-13:** Cena mínima `scenes/main.tscn` com Node2D + Label "v0.0 — Destiny: Tales of Natalia".
- **D-14:** CI/CD com dois comportamentos: tags `v*` → export completo + deploy itch.io; PRs → apenas build de verificação.
- **D-15:** Docker image: `barichello/godot-ci` com tag `4.4.1`.
- **D-16:** Target itch.io: placeholder `ITCH_USER/destiny-tales-of-natalia`; secret `BUTLER_CREDENTIALS`.
- **D-17:** Checkout step com `lfs: true`.
- **D-18:** Usar `--headless --export-release` (não `--export`).

### Claude's Discretion

- Ordem exata das seções no `export.yml` (jobs, steps, artefatos) — seguir convenções do `abarichello/godot-ci`.
- Versão patch exata do Godot 4.4 (4.4.0, 4.4.1, 4.4.2...) — usar a mais recente disponível no godot-ci no momento da execução.

### Deferred Ideas (OUT OF SCOPE)

- **Android export** — para v2.
- **macOS code signing** — deferred para fase de release/polish.

</user_constraints>

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| EXPORT-03 | Renderer Compatibility configurado desde o início do projeto | project.godot com `rendering/renderer/rendering_method="gl_compatibility"` + todas as config pixel art aplicadas antes do primeiro commit de código |

</phase_requirements>

---

## Summary

Phase 0 é pura configuração — zero gameplay. O objetivo é ter um repositório Git com LFS ativo, um projeto Godot 4.4.x com renderer Compatibility e pixel art configurados via `project.godot`, uma cena mínima de teste (`scenes/main.tscn`), `export_presets.cfg` versionado com 3 presets (Web, Windows, macOS), e um pipeline GitHub Actions que exporta e publica no itch.io ao criar tags `v*`.

**Estado inicial verificado:** O repositório `/Users/renatojaf/jogo-natalia/` existe mas está praticamente vazio — apenas `.git/`, `.planning/` e `CLAUDE.md`. Nenhum projeto Godot criado ainda. Git LFS **não está instalado** na máquina (confirmado: `git lfs` retorna "not a git command"; `brew info git-lfs` confirma "Not installed"). Godot também **não está instalado** — nem via Homebrew, nem em `/Applications/`. Ambos precisam ser instalados antes de qualquer trabalho no projeto.

A boa notícia é que todas as decisões de stack estão travadas e bem documentadas. A Docker image `barichello/godot-ci:4.4.1` existe e está disponível no Docker Hub. O pipeline de CI/CD usa o mesmo Godot headless que está dentro do container — não precisa de instalação local para o CI funcionar, mas o desenvolvimento local exige Godot instalado.

**Recomendação primária:** Instalar git-lfs e Godot 4.4.x localmente antes de criar o projeto. Criar `project.godot` manualmente com todas as configurações pixel art, depois exportar para confirmar que o pipeline funciona end-to-end antes de encerrar a fase.

---

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Renderer Compatibility | Engine Config (project.godot) | — | Define-se uma vez no arquivo de projeto; afeta todas as plataformas |
| Pixel art settings | Engine Config (project.godot) | — | Global para o projeto; não é por-cena |
| Git LFS | VCS (.gitattributes) | — | Configuração de repositório, não de engine |
| Estrutura de pastas | Repositório Git | — | Convenção de organização, sem lógica de engine |
| Cena de teste | Godot Scene (scenes/) | — | Valida que o export funciona |
| Export presets | Engine Config (export_presets.cfg) | CI/CD | Criado na engine, consumido pelo CI |
| CI/CD deploy | GitHub Actions | Docker (barichello/godot-ci) | Automação de build e publish |

---

## Standard Stack

### Core

| Componente | Versão | Propósito | Por que este |
|-----------|--------|-----------|--------------|
| Godot Engine | **4.4.1** (tag Docker disponível) | Engine + exportação | Versão estável mais recente com tag godot-ci disponível; D-01 travado |
| GDScript | built-in | Linguagem de scripting | Único que exporta para HTML5 em Godot 4; D-02 travado |
| Git LFS | 3.7.1 (disponível via brew) | Versionar assets binários | Previne binários grandes em git regular |

### Ferramentas de Build / CI

| Ferramenta | Versão | Propósito | Quando usar |
|-----------|--------|-----------|-------------|
| barichello/godot-ci | tag `4.4.1` | Container Docker com Godot headless + export templates | CI/CD no GitHub Actions |
| GitHub Actions | N/A | Runner de CI | Export automático em tags e PRs |
| butler (itch.io) | via `manleydev/butler-publish-itchio-action` | Upload para itch.io | Apenas em tags `v*` |

### Alternativas Consideradas e Rejeitadas

| Em vez de | Poderia usar | Tradeoff |
|-----------|-------------|----------|
| `barichello/godot-ci` | `firebelley/godot-export` GitHub Action | godot-ci é mais maduro e tem image Docker própria; firebelley é action-only |
| butler + itch.io | GitHub Pages | Decisão de negócio (itch.io é o target); GitHub Pages é alternativa para demos |

### Instalação — Ambiente Local

```bash
# 1. Instalar Git LFS via Homebrew (necessário — não está instalado)
brew install git-lfs

# 2. Ativar LFS no repositório
git -C /Users/renatojaf/jogo-natalia lfs install

# 3. Instalar Godot 4.4.x via Homebrew Cask
# ATENÇÃO: brew instala 4.6.2 por padrão — precisamos de 4.4.x para D-01
# Opcao A: download manual de godotengine.org/releases/4.4/
# Opcao B: brew install --cask godot (aceitar 4.6.2 apenas se D-01 for relaxado)
# Recomendação: download manual do .app para manter 4.4.x
```

**Verificação de versão:**

```bash
# Após instalar, confirmar versão
godot --version   # deve retornar 4.4.x
git lfs version   # deve retornar git-lfs/3.x.x
```

---

## Architecture Patterns

### System Architecture Diagram

```
[Desenvolvedor local]
        |
        | git push --tags v0.0
        v
[GitHub Repository]
        |-- .gitattributes  (LFS: *.png, *.wav, *.ogg, ...)
        |-- project.godot   (Compatibility renderer, 320x180, pixel art)
        |-- export_presets.cfg  (Web, Windows, macOS)
        |-- scenes/main.tscn    (Node2D + Label)
        |-- .github/workflows/export.yml
        |
        | (tag v* trigger)
        v
[GitHub Actions Runner]
        |
        | container: barichello/godot-ci:4.4.1
        |   - checkout com lfs: true
        |   - godot --headless --export-release "Web" build/web/index.html
        |   - godot --headless --export-release "Windows Desktop" build/windows/game.exe
        |   - godot --headless --export-release "macOS" build/mac/game.zip
        |
        | (parallel jobs)
        v
[butler deploy]
        |-- itch.io channel: html5
        |-- itch.io channel: windows
        |-- itch.io channel: osx
```

### Estrutura de Pastas Recomendada

```
jogo-natalia/               # raiz do repositório git
├── .github/
│   └── workflows/
│       └── export.yml      # CI/CD pipeline
├── .gitattributes          # Git LFS tracking rules
├── .gitignore              # Exclui .godot/, *.translation, export/
├── CLAUDE.md               # Instruções do projeto (já existe)
├── project.godot           # Config da engine (criar na Phase 0)
├── export_presets.cfg      # Export presets (criar na Phase 0)
├── icon.svg                # Ícone padrão Godot (auto-criado)
├── scenes/
│   └── main.tscn           # Cena mínima de teste (D-13)
├── assets/
│   ├── sprites/
│   │   ├── player/         # (vazio — Phase 1+)
│   │   ├── enemies/        # (vazio — Phase 3+)
│   │   └── ui/             # (vazio — Phase 2+)
│   └── audio/
│       ├── sfx/            # (vazio — Phase 3+)
│       └── music/          # (vazio — Phase 12)
├── scripts/                # (vazio — Phase 1+)
├── autoloads/              # (vazio — Phase 2, D-09)
└── export/                 # Ignorado via .gitignore
```

### Pattern 1: project.godot com Configurações Pixel Art + Compatibility

**O que é:** Arquivo de texto INI-like que define todas as configurações do projeto Godot.

**Quando usar:** Criado uma vez na Phase 0; todas as settings travadas em D-05.

**Exemplo — conteúdo mínimo verificado:**

```ini
; Source: Godot 4.4 docs + community projects verificados
[gd_version]
config_version=5

[application]
config/name="Destiny — Tales of Natalia"
config/features=PackedStringArray("4.4", "GL Compatibility")
config/icon="res://icon.svg"
run/main_scene="res://scenes/main.tscn"

[display]
window/size/viewport_width=320
window/size/viewport_height=180
window/size/window_width_override=1280
window/size/window_height_override=720
window/stretch/mode="canvas_items"
window/stretch/scale_mode="integer"

[rendering]
renderer/rendering_method="gl_compatibility"
renderer/rendering_method.mobile="gl_compatibility"
textures/canvas_textures/default_texture_filter=0
2d/snap/snap_2d_transforms_to_pixel=true
```

> **Nota sobre `default_texture_filter=0`:** O valor `0` corresponde a `Nearest` no enum interno do Godot (`TEXTURE_FILTER_NEAREST`). [ASSUMED] — baseado em conhecimento de treinamento; verificar no editor após criar o projeto.

**Como criar o projeto Godot sem editor (headless):**

```bash
# Criar estrutura mínima para o Godot reconhecer como projeto
mkdir -p /Users/renatojaf/jogo-natalia/scenes
touch /Users/renatojaf/jogo-natalia/project.godot

# Editar project.godot com o conteúdo acima
# Abrir o editor uma vez para importar assets e gerar .godot/ cache:
godot --editor --headless --quit --path /Users/renatojaf/jogo-natalia/
```

**Alternativa preferida:** Criar o projeto via GUI do Godot (File > New Project), depois editar `project.godot` com as settings de pixel art. Mais seguro pois o editor valida o arquivo.

### Pattern 2: .gitattributes para Git LFS

**O que é:** Regras que direcionam tipos de arquivo para o Git LFS.

**Quando usar:** Antes do primeiro commit de qualquer asset binário.

```
# Source: STACK.md verificado + decisão D-06

# Imagens
*.png filter=lfs diff=lfs merge=lfs -text
*.jpg filter=lfs diff=lfs merge=lfs -text
*.webp filter=lfs diff=lfs merge=lfs -text

# Áudio
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

### Pattern 3: export_presets.cfg — 3 presets

**O que é:** Arquivo de configuração de export gerado pelo Godot. Deve ser commitado (D-10).

**Conteúdo mínimo verificado para Web + Windows + macOS:**

```ini
; Source: crystal-bit/godot-game-template + godot docs verificados

[preset.0]
name="Web"
platform="Web"
runnable=true
advanced_options=false
dedicated_server=false
custom_features=""
export_filter="all_resources"
include_filter=""
exclude_filter=""
export_path="export/web/index.html"
script_export_mode=1
script_encryption_key=""

[preset.0.options]
custom_template/debug=""
custom_template/release=""
variant/export_type=0
vram_texture_compression/for_desktop=true
vram_texture_compression/for_mobile=false
html/export_icon=true
html/canvas_resize_policy=2
html/focus_canvas_on_start=true
html/experimental_virtual_keyboard=false
progressive_web_app/enabled=false

[preset.1]
name="Windows Desktop"
platform="Windows Desktop"
runnable=true
advanced_options=false
dedicated_server=false
custom_features=""
export_filter="all_resources"
include_filter=""
exclude_filter=""
export_path="export/windows/destiny-tales-of-natalia.exe"
script_export_mode=1
script_encryption_key=""

[preset.1.options]
binary_format/embed_pck=true
texture_format/s3tc_bptc=true
texture_format/etc2_astc=false
binary_format/architecture="x86_64"
codesign/enable=false

[preset.2]
name="macOS"
platform="macOS"
runnable=true
advanced_options=false
dedicated_server=false
custom_features=""
export_filter="all_resources"
include_filter=""
exclude_filter=""
export_path="export/mac/destiny-tales-of-natalia.zip"
script_export_mode=1
script_encryption_key=""

[preset.2.options]
binary_format/architecture="universal"
codesign/enable=false
notarization/enable=false
```

> **Nota:** O `export_presets.cfg` real é gerado pelo editor Godot. O conteúdo acima é uma aproximação. Criar os presets pelo editor (Project > Export) gera o arquivo correto e definitivo, depois commitá-lo.

### Pattern 4: GitHub Actions Workflow (export.yml)

**O que é:** Pipeline CI/CD com dois comportamentos — tags `v*` exportam e publicam; PRs apenas verificam build.

```yaml
# Source: abarichello/godot-ci docs + CONTEXT.md D-14 a D-18

name: Export and Deploy

on:
  push:
    tags:
      - 'v*'
  pull_request:
    branches:
      - main

env:
  GODOT_VERSION: "4.4.1"
  EXPORT_NAME: "destiny-tales-of-natalia"
  PROJECT_PATH: "."

jobs:
  export-web:
    name: Web Export
    runs-on: ubuntu-latest
    container:
      image: barichello/godot-ci:4.4.1
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          lfs: true

      - name: Setup export templates
        run: |
          mkdir -p ~/.local/share/godot/export_templates/
          mv /root/.local/share/godot/export_templates/${GODOT_VERSION}.stable \
             ~/.local/share/godot/export_templates/${GODOT_VERSION}.stable

      - name: Export Web
        run: |
          mkdir -p build/web
          godot --headless --verbose --export-release "Web" \
            build/web/index.html

      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: web
          path: build/web/

      - name: Deploy to itch.io
        if: startsWith(github.ref, 'refs/tags/v')
        uses: manleydev/butler-publish-itchio-action@master
        env:
          BUTLER_CREDENTIALS: ${{ secrets.BUTLER_CREDENTIALS }}
          CHANNEL: html5
          ITCH_GAME: destiny-tales-of-natalia
          ITCH_USER: ITCH_USER   # substituir quando página itch.io for criada
          PACKAGE: build/web

  export-windows:
    name: Windows Export
    runs-on: ubuntu-latest
    container:
      image: barichello/godot-ci:4.4.1
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          lfs: true

      - name: Setup export templates
        run: |
          mkdir -p ~/.local/share/godot/export_templates/
          mv /root/.local/share/godot/export_templates/${GODOT_VERSION}.stable \
             ~/.local/share/godot/export_templates/${GODOT_VERSION}.stable

      - name: Export Windows
        run: |
          mkdir -p build/windows
          godot --headless --verbose --export-release "Windows Desktop" \
            build/windows/${{ env.EXPORT_NAME }}.exe

      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: windows
          path: build/windows/

      - name: Deploy to itch.io
        if: startsWith(github.ref, 'refs/tags/v')
        uses: manleydev/butler-publish-itchio-action@master
        env:
          BUTLER_CREDENTIALS: ${{ secrets.BUTLER_CREDENTIALS }}
          CHANNEL: windows
          ITCH_GAME: destiny-tales-of-natalia
          ITCH_USER: ITCH_USER
          PACKAGE: build/windows

  export-macos:
    name: macOS Export
    runs-on: ubuntu-latest
    container:
      image: barichello/godot-ci:4.4.1
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          lfs: true

      - name: Setup export templates
        run: |
          mkdir -p ~/.local/share/godot/export_templates/
          mv /root/.local/share/godot/export_templates/${GODOT_VERSION}.stable \
             ~/.local/share/godot/export_templates/${GODOT_VERSION}.stable

      - name: Export macOS
        run: |
          mkdir -p build/mac
          godot --headless --verbose --export-release "macOS" \
            build/mac/${{ env.EXPORT_NAME }}.zip

      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: macos
          path: build/mac/

      - name: Deploy to itch.io
        if: startsWith(github.ref, 'refs/tags/v')
        uses: manleydev/butler-publish-itchio-action@master
        env:
          BUTLER_CREDENTIALS: ${{ secrets.BUTLER_CREDENTIALS }}
          CHANNEL: osx
          ITCH_GAME: destiny-tales-of-natalia
          ITCH_USER: ITCH_USER
          PACKAGE: build/mac
```

### Pattern 5: cena mínima main.tscn (D-13)

**O que é:** Cena de teste para validar que o export web abre no navegador sem erro.

```
; scenes/main.tscn
[gd_scene load_steps=1 format=3 uid="uid://XXXX"]

[node name="Main" type="Node2D"]

[node name="Label" type="Label" parent="."]
text = "v0.0 — Destiny: Tales of Natalia"
```

> O UID é gerado automaticamente pelo Godot ao criar a cena. Criar via editor para UID correto.

### Anti-Patterns a Evitar

- **Commitar `.godot/`:** Esta pasta é cache da engine. É regenerada ao abrir o projeto. Nunca commitar.
- **Usar `--export` sem `--export-release`:** Em Godot 4, `--export` é alias; `--export-release` é o correto para builds de produção (sem debug symbols).
- **Criar `export_presets.cfg` manualmente antes de abrir o editor:** O Godot valida estrutura interna do arquivo; edições manuais parciais causam erros silenciosos. Criar pelo editor, depois editar se necessário.
- **Inicializar LFS após o primeiro commit binário:** Binários já commitados sem LFS precisam de migração (`git lfs migrate`) — processo complexo e destrutivo.
- **Esquecer `lfs: true` no checkout do CI:** Assets binários ficam como ponteiros de 130 bytes em vez do arquivo real; export falha silenciosamente.

---

## Don't Hand-Roll

| Problema | Não construir | Usar em vez de | Por quê |
|----------|--------------|----------------|---------|
| Web server com CORS para teste local | Script Python custom | `python3 serve.py` (do Godot) ou script com CORS headers | SharedArrayBuffer requer headers específicos; http.server padrão não serve |
| Docker de CI com Godot | Dockerfile próprio | `barichello/godot-ci:4.4.1` | Export templates já inclusos e versionados |
| Upload para itch.io | Script shell com curl | `manleydev/butler-publish-itchio-action` | butler lida com diff, channels, versioning |
| LFS tracking manual | Scripts de verificação | `.gitattributes` + `git lfs` | Git LFS é o standard; não reinventar |

---

## Runtime State Inventory

> SKIPPED — Phase 0 é greenfield. Não há rename, refactor ou migration. O repositório existe mas está vazio de código. Nenhum estado em runtime para inventariar.

---

## Common Pitfalls

### Pitfall 1: Git LFS não instalado antes do primeiro commit de asset

**O que dá errado:** O arquivo `.png` vai para o git regular como binário. Mesmo depois de instalar LFS e criar `.gitattributes`, os arquivos já commitados não são movidos automaticamente para LFS.

**Por que acontece:** `.gitattributes` só afeta novos commits. Arquivos já rastreados pelo git regular precisam de migração explícita.

**Como evitar:** Instalar git-lfs → `git lfs install` → criar `.gitattributes` → `git add .gitattributes` → `git commit` — tudo ANTES de adicionar qualquer arquivo `.png`, `.wav`, `.ogg`.

**Sinais de alerta:** `git lfs ls-files` retorna vazio enquanto há assets no repositório. `du -sh .git` muito grande para um projeto sem assets reais.

### Pitfall 2: `godot --headless` falha sem .godot/ importado

**O que dá errado:** O export CI falha com `ERROR: Could not find any export preset...` ou `ERROR: No import data found for resource`.

**Por que acontece:** Godot precisa importar assets antes de exportar. No CI, o `.godot/` não existe porque está no `.gitignore`. A flag `--export-release` implica `--import` automaticamente desde o Godot 4.3+, mas assets mais complexos podem precisar de um passo explícito.

**Como evitar:** Adicionar passo de import antes do export no CI:
```bash
godot --headless --editor --quit --path .
```
O godot-ci container geralmente lida com isso, mas verificar se assets estão sendo importados corretamente nos logs.

**Sinais de alerta:** Log do CI mostra "Importing..." mas export falha logo depois.

### Pitfall 3: SharedArrayBuffer bloqueia web export local

**O que dá errado:** Abrir `index.html` diretamente no browser (file:///) falha com `SharedArrayBuffer is not defined` ou tela preta.

**Por que acontece:** Navegadores modernos exigem contexto seguro + CORS headers para SharedArrayBuffer, que é necessário quando threads estão ativas.

**Como evitar (opção A — sem threads, mais simples):** Exportar com "Use Threads" desativado nas options do preset Web. Funciona sem headers especiais. Desde Godot 4.3, single-threaded é a default para web.

**Como evitar (opção B — com servidor local):** Usar script Python com CORS headers:
```python
#!/usr/bin/env python3
from http.server import HTTPServer, SimpleHTTPRequestHandler, test
import sys

class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        self.send_header("Cross-Origin-Embedder-Policy", "require-corp")
        SimpleHTTPRequestHandler.end_headers(self)

if __name__ == '__main__':
    test(CORSRequestHandler, HTTPServer, port=int(sys.argv[1]) if len(sys.argv) > 1 else 8000)
```

**Sinais de alerta:** Console do browser mostra `ReferenceError: SharedArrayBuffer is not defined`.

### Pitfall 4: Godot 4.4.x vs brew padrão (4.6.2)

**O que dá errado:** `brew install --cask godot` instala 4.6.2 (versão atual do cask), não 4.4.x conforme D-01.

**Por que acontece:** Homebrew Cask mantém apenas a versão mais recente.

**Como evitar:** Baixar Godot 4.4.1 manualmente de `https://godotengine.org/releases/4.4/`. Usar o arquivo `.app` diretamente. Criar alias ou symlink se quiser usar `godot` no terminal:
```bash
# Adicionar ao ~/.zshrc após instalar manualmente
alias godot="/Applications/Godot_v4.4.1-stable.app/Contents/MacOS/Godot"
```

**Sinais de alerta:** `godot --version` retorna `4.6.x`.

### Pitfall 5: Nome do preset no export_presets.cfg deve bater exatamente com o comando CLI

**O que dá errado:** CI falha com `Invalid export preset name: Web` se o preset se chama `"HTML5"` mas o comando usa `"Web"`.

**Por que acontece:** Godot 4 renomeou a plataforma de "HTML5" para "Web" nas versões 4.x. Arquivos legados ou presets criados incorretamente usam "HTML5".

**Como evitar:** Criar presets pelo editor Godot 4.4.x — o nome será "Web" automaticamente. Verificar nome exato em `export_presets.cfg` antes de escrever o comando CI.

**Sinais de alerta:** `ERROR: Invalid export preset name: HTML5` no log do CI.

### Pitfall 6: Renderer não é Compatibility por padrão

**O que dá errado:** Projeto criado com renderer padrão (Forward+) falha no export web — a plataforma Web só suporta Compatibility.

**Por que acontece:** Godot usa Forward+ como padrão em projetos novos. Web export exige GL Compatibility.

**Como evitar:** Ao criar o projeto, selecionar "Compatibility" na tela de criação do projeto no editor. Verificar em `project.godot` que existe:
```
rendering/renderer/rendering_method="gl_compatibility"
```

**Sinais de alerta:** Export web falha. Ou em Project Settings, o renderer mostra "Forward+" ou "Mobile".

---

## Code Examples

### Verificar que LFS está ativo e rastreando

```bash
# Source: git lfs docs
git lfs install               # ativa LFS no repo
git lfs track "*.png"         # adiciona ao .gitattributes
git lfs ls-files              # lista arquivos no LFS
git lfs status                # estado atual
```

### Testar export web localmente

```bash
# Source: Godot 4.4 docs
cd /Users/renatojaf/jogo-natalia
mkdir -p export/web
godot --headless --export-release "Web" export/web/index.html

# Servir com CORS headers
cd export/web
python3 serve.py  # script acima
# Acessar: http://localhost:8000
```

### Verificar renderer no project.godot após criação

```bash
grep -A3 '\[rendering\]' /Users/renatojaf/jogo-natalia/project.godot
# Deve mostrar: renderer/rendering_method="gl_compatibility"
```

---

## State of the Art

| Abordagem Antiga | Abordagem Atual | Quando Mudou | Impacto |
|-----------------|-----------------|-------------|---------|
| Plataforma chamada "HTML5" | Plataforma chamada "Web" | Godot 4.0 | Nome no preset e CLI deve ser "Web" |
| `TileMap` (Godot 4.3 e anterior) | `TileMapLayer` (Godot 4.4+) | Godot 4.4 | Não afeta Phase 0, mas importante saber para fases futuras |
| SharedArrayBuffer obrigatório para web | Single-thread export disponível | Godot 4.3 | Web export funciona sem headers CORS especiais se threads desativados |
| `--export` flag | `--export-release` ou `--export-debug` | Godot 4 | `--export` ainda existe como alias, mas `--export-release` é explícito e correto |
| Renderer "GLES2"/"GLES3" (Godot 3) | "Forward+"/"Mobile"/"Compatibility" (Godot 4) | Godot 4.0 | Nomenclatura completamente diferente |

**Deprecated/outdated:**
- `--no-window`: substituído por `--headless` em Godot 4
- `TileMap` node: deprecado em Godot 4.4, usar `TileMapLayer`
- Plataforma "HTML5" em export presets: renomeada para "Web" em Godot 4

---

## Assumptions Log

| # | Claim | Section | Risco se Errado |
|---|-------|---------|-----------------|
| A1 | `textures/canvas_textures/default_texture_filter=0` corresponde a Nearest | project.godot exemplo | Sprites podem ter blur — verificar no editor após criar projeto |
| A2 | `window/size/window_width_override=1280` é necessário para janela inicial 1280x720 | project.godot exemplo | Janela pode abrir em 320x180 minúscula — corrigir no editor se necessário |
| A3 | `manleydev/butler-publish-itchio-action@master` é a action correta para butler | export.yml exemplo | CI de deploy falha — verificar GitHub Marketplace |
| A4 | O passo de "Setup export templates" move de `/root/.local/share/...` para `~/.local/share/...` | export.yml Pattern 4 | Export falha com "No export template found" — verificar logs do godot-ci |

---

## Open Questions

1. **Versão exata de Godot 4.4.x para instalar localmente**
   - O que sabemos: godot-ci tem tag `4.4.1` disponível no Docker Hub (verificado)
   - O que é incerto: Se Godot 4.4.2 foi lançado (existiria tag `4.4.2` no godot-ci?)
   - Recomendação: Usar 4.4.1 localmente para paridade com o CI container. Se precisar de 4.4.2, verificar tags em hub.docker.com/r/barichello/godot-ci

2. **Conta itch.io e página do jogo**
   - O que sabemos: D-16 diz usar placeholder `ITCH_USER/destiny-tales-of-natalia`
   - O que é incerto: Se a conta itch.io já existe e o `BUTLER_CREDENTIALS` secret pode ser configurado no GitHub
   - Recomendação: O planner deve incluir um task de "criar conta itch.io e configurar secret" como pré-requisito do CI deploy. O workflow funciona sem deploy (apenas export) até isso estar configurado.

3. **`config/features` no project.godot deve listar "GL Compatibility"?**
   - O que sabemos: Projetos Godot 4.x com Compatibility renderer incluem `"GL Compatibility"` no PackedStringArray de features
   - O que é incerto: Se isso é obrigatório ou apenas informativo
   - Recomendação: Deixar o editor gerar — não editar manualmente. Criar projeto no editor, checar o arquivo gerado.

---

## Environment Availability

| Dependência | Requerida por | Disponível | Versão | Fallback |
|------------|--------------|-----------|--------|----------|
| Git | VCS | ✓ | 2.50.1 (Apple Git-155) | — |
| Git LFS | Assets binários | ✗ | — | `brew install git-lfs` |
| Godot 4.4.x | Engine + export | ✗ | — | Download manual de godotengine.org/releases/4.4/ |
| Python 3 | Servidor web local de teste | ✓ (macOS built-in) | 3.x | — |
| Docker | Build local (opcional) | Não verificado | — | CI usa container; Docker não é necessário localmente |
| GitHub Actions | CI/CD | ✓ (cloud) | N/A | — |

**Dependências bloqueantes sem fallback:**
- **Git LFS:** Deve ser instalado antes de qualquer commit de asset binário. Instalar com `brew install git-lfs`.
- **Godot 4.4.x:** Deve ser instalado para criar o projeto, configurar presets e testar export local (D-12). Não há fallback — sem Godot, não há projeto.

**Como instalar as dependências bloqueantes:**

```bash
# Git LFS
brew install git-lfs
git lfs install  # ativar no sistema

# Godot 4.4.1 (download manual para versão específica)
# 1. Acessar: https://godotengine.org/releases/4.4/
# 2. Baixar: Godot_v4.4.1-stable_macos.universal.zip
# 3. Extrair Godot.app para /Applications/
# 4. Adicionar ao shell:
echo 'alias godot="/Applications/Godot.app/Contents/MacOS/Godot"' >> ~/.zshrc
source ~/.zshrc
```

---

## Validation Architecture

### Test Framework

| Propriedade | Valor |
|-------------|-------|
| Framework | Verificação manual + comandos shell (sem framework de testes automático na Phase 0) |
| Config file | N/A |
| Quick run command | `git lfs ls-files` + `godot --version` |
| Full suite command | `godot --headless --export-release "Web" export/web/index.html` + abrir no browser |

> **Nota:** Phase 0 é configuração pura — não há código GDScript para unit testing. A validação é smoke testing do pipeline end-to-end.

### Phase Requirements → Test Map

| Req ID | Comportamento | Tipo de Teste | Comando | Arquivo existe? |
|--------|--------------|---------------|---------|----------------|
| EXPORT-03 | Renderer Compatibility configurado | Verificação manual | `grep "gl_compatibility" project.godot` | ❌ Wave 0 |
| SC-1 | Export web gera build HTML5 que abre no browser | Smoke test | `godot --headless --export-release "Web" export/web/index.html` | ❌ Wave 0 |
| SC-2 | Git LFS rastreia .png/.wav/.ogg | Verificação VCS | `git lfs ls-files` após adicionar arquivo de teste | ❌ Wave 0 |
| SC-3 | Pasta structure criada e commitada | Verificação Git | `git log --oneline -1` + `git show --stat HEAD` | ❌ Wave 0 |
| SC-4 | Renderer persiste após reabrir projeto | Verificação manual | Reabrir projeto no editor, verificar Project Settings | ❌ Wave 0 |

### Sampling Rate

- **Por task commit:** `grep "gl_compatibility" project.godot && git lfs ls-files`
- **Por wave merge:** Export web completo + servir localmente + abrir no browser
- **Phase gate:** Todos os 4 success criteria do ROADMAP.md verificados antes de `/gsd-verify-work`

### Wave 0 Gaps

- [ ] Script `serve.py` para teste local web (CORS headers)
- [ ] `.gitattributes` com todas as regras LFS
- [ ] `.gitignore` com `.godot/`, `*.translation`, `export/`
- [ ] `project.godot` com configurações pixel art e Compatibility renderer
- [ ] `export_presets.cfg` com 3 presets
- [ ] `.github/workflows/export.yml`
- [ ] `scenes/main.tscn` com Label de versão

---

## Security Domain

> `security_enforcement` não está configurado explicitamente como `false` no config.json. Incluindo seção.

### Applicable ASVS Categories

| ASVS Category | Aplica | Controle Padrão |
|---------------|--------|-----------------|
| V2 Authentication | não | Sem auth na Phase 0 |
| V3 Session Management | não | Sem sessões na Phase 0 |
| V4 Access Control | não | Sem controle de acesso |
| V5 Input Validation | não | Sem input de usuário na Phase 0 |
| V6 Cryptography | não | Sem crypto na Phase 0 |

### Riscos de Segurança Específicos desta Phase

| Risco | Impacto | Mitigação |
|-------|---------|-----------|
| `BUTLER_CREDENTIALS` exposto em logs | Alto | Sempre usar `${{ secrets.BUTLER_CREDENTIALS }}` — nunca hardcodar no YAML |
| `export_presets.cfg` com dados sensíveis | Baixo | Verificar que não contém encryption keys antes de commitar |
| Assets binários em git regular (sem LFS) | Médio | Configurar LFS antes do primeiro commit — veja Pitfall 1 |

---

## Sources

### Primary (HIGH confidence)
- CONTEXT.md do projeto — todas as decisões travadas (D-01 a D-18)
- STACK.md do projeto — stack validada com fontes citadas
- Docker Hub `barichello/godot-ci` — tags verificadas via API: `4.4.1` confirmada disponível [VERIFIED: hub.docker.com]
- `brew info git-lfs` — versão 3.7.1 disponível, não instalada [VERIFIED: bash tool]
- `brew search godot` — Godot 4.6.2 disponível via cask; 4.4.x não disponível via brew [VERIFIED: bash tool]
- Godot 4.4 docs (docs.godotengine.org/en/4.4/) — export commands, web export requirements [CITED: docs.godotengine.org/en/4.4/tutorials/editor/command_line_tutorial.html]
- Godot 4.4 múltiplas resoluções — chaves project.godot para viewport e stretch [CITED: docs.godotengine.org/en/4.4/tutorials/rendering/multiple_resolutions.html]

### Secondary (MEDIUM confidence)
- `abarichello/godot-ci` workflow de referência — estrutura do YAML verificada [CITED: github.com/aBARICHELLO/godot-ci/blob/master/.github/workflows/godot-ci.yml]
- crystal-bit/godot-game-template — estrutura do export_presets.cfg [CITED: github.com/crystal-bit/godot-game-template]
- `nisovin` CORS Python server gist — script verificado [CITED: gist.github.com/nisovin/cf9dd74678641fb70902866c79692b17]
- Godot renderers docs — `rendering/renderer/rendering_method="gl_compatibility"` [CITED: docs.godotengine.org/en/4.4/tutorials/rendering/renderers.html]

### Tertiary (LOW confidence — verificar)
- `textures/canvas_textures/default_texture_filter=0` = Nearest [ASSUMED] — valor do enum não verificado na fonte oficial
- Setup step do export templates no godot-ci (`/root/.local/share/...`) [ASSUMED] — pode variar entre versões do container

---

## Metadata

**Confidence breakdown:**
- Environment availability: HIGH — verificado com bash tools
- Standard stack: HIGH — docker tags e brew confirmados
- project.godot syntax: MEDIUM — chaves de display/stretch verificadas em docs; rendering_method verificado; default_texture_filter=0 é ASSUMED
- export_presets.cfg: MEDIUM — estrutura verificada em projetos reais; valores exatos gerados pelo editor
- CI/CD workflow: MEDIUM — estrutura verificada no repo godot-ci; passo de template setup é ASSUMED
- Pitfalls: HIGH — maioria baseada em issues verificadas no GitHub e na documentação oficial

**Research date:** 2026-05-20
**Valid until:** 2026-07-01 (30 dias — stack estável, mas versões do godot-ci podem mudar)
