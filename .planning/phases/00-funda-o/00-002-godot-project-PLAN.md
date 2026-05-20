---
phase: "00-funda-o"
plan: "002"
type: execute
wave: 2
depends_on:
  - "00-001"
files_modified:
  - project.godot
  - icon.svg
  - scenes/main.tscn
autonomous: false
requirements:
  - EXPORT-03

must_haves:
  truths:
    - "Godot 4.4.x está instalado em /Applications/ e acessível via alias no terminal"
    - "project.godot existe com renderer Compatibility (gl_compatibility) e configurações pixel art completas"
    - "Viewport está configurado para 320x180 com stretch mode canvas_items e scale mode integer"
    - "Cena scenes/main.tscn existe com Node2D raiz e Label com texto 'v0.0 — Destiny: Tales of Natalia'"
    - "run/main_scene em project.godot aponta para res://scenes/main.tscn"
    - "Configurações persistem após fechar e reabrir o projeto no editor"
  artifacts:
    - path: "project.godot"
      provides: "Config central do projeto Godot com renderer Compatibility e pixel art settings"
      contains: "gl_compatibility"
    - path: "scenes/main.tscn"
      provides: "Cena mínima de teste com label de versão"
      contains: "v0.0 — Destiny: Tales of Natalia"
  key_links:
    - from: "project.godot"
      to: "Godot renderer"
      via: "rendering/renderer/rendering_method key"
      pattern: "rendering_method=\"gl_compatibility\""
    - from: "project.godot"
      to: "scenes/main.tscn"
      via: "run/main_scene key"
      pattern: "run/main_scene=\"res://scenes/main.tscn\""
    - from: "scenes/main.tscn"
      to: "Label node"
      via: "node tree parent/child"
      pattern: "text = \"v0.0"

user_setup:
  - service: godot-444
    why: "Godot 4.4.x não está instalado na máquina. brew instala 4.6.2 por padrão — violaria D-01. Requer download manual."
    steps:
      - task: "Baixar Godot 4.4.1 standard (não .NET) para macOS"
        location: "https://godotengine.org/releases/4.4/ — arquivo: Godot_v4.4.1-stable_macos.universal.zip"
      - task: "Extrair e mover Godot.app para /Applications/"
        command: "unzip Godot_v4.4.1-stable_macos.universal.zip && mv Godot.app /Applications/"
      - task: "Adicionar alias ao shell"
        command: "echo 'alias godot=\"/Applications/Godot.app/Contents/MacOS/Godot\"' >> ~/.zshrc && source ~/.zshrc"
      - task: "Verificar versão instalada"
        command: "godot --version"
    verification: "godot --version retorna '4.4.1.stable' ou similar com 4.4.x"
---

<objective>
Instalar Godot 4.4.x e criar o projeto Godot com todas as configurações pixel art e renderer Compatibility aplicadas. Entregar uma cena mínima funcional (v0.0) que valida visualmente que o projeto existe e está corretamente configurado.

Purpose: As configurações de renderer e pixel art em project.godot são permanentes — mudar depois quebra exports. Este plano as define corretamente desde o início (per D-05, EXPORT-03).

Output: project.godot com renderer Compatibility e pixel art settings, icon.svg padrão, scenes/main.tscn com label de versão. Projeto abre no editor sem erros.
</objective>

<execution_context>
@/Users/renatojaf/.claude/get-shit-done/workflows/execute-plan.md
@/Users/renatojaf/.claude/get-shit-done/templates/summary.md
</execution_context>

<context>
@/Users/renatojaf/jogo-natalia/.planning/ROADMAP.md
@/Users/renatojaf/jogo-natalia/.planning/phases/00-funda-o/00-CONTEXT.md
@/Users/renatojaf/jogo-natalia/.planning/phases/00-funda-o/00-RESEARCH.md
@/Users/renatojaf/jogo-natalia/.planning/phases/00-funda-o/00-PATTERNS.md
@/Users/renatojaf/jogo-natalia/.planning/phases/00-funda-o/00-001-SUMMARY.md

<interfaces>
<!-- Decisões travadas do CONTEXT.md que definem os valores exatos do project.godot -->

Chaves obrigatórias do project.godot (D-05):
  rendering/renderer/rendering_method = "gl_compatibility"
  rendering/renderer/rendering_method.mobile = "gl_compatibility"
  textures/canvas_textures/default_texture_filter = 0  (0 = Nearest)
  2d/snap/snap_2d_transforms_to_pixel = true
  window/size/viewport_width = 320
  window/size/viewport_height = 180
  window/size/window_width_override = 1280
  window/size/window_height_override = 720
  window/stretch/mode = "canvas_items"
  window/stretch/scale_mode = "integer"

Nome do projeto (D-03): config/name = "Destiny — Tales of Natalia"
Main scene (D-13): run/main_scene = "res://scenes/main.tscn"
</interfaces>
</context>

<tasks>

<task type="checkpoint:human-action" gate="blocking">
  <name>Task 1: Instalar Godot 4.4.x localmente</name>
  <read_first>
    /Users/renatojaf/jogo-natalia/.planning/phases/00-funda-o/00-RESEARCH.md (seção "Pitfall 4: Godot 4.4.x vs brew padrão" e "Environment Availability")
    /Users/renatojaf/jogo-natalia/.planning/phases/00-funda-o/00-CONTEXT.md (decisão D-01)
  </read_first>
  <what-built>Godot 4.4.x não está instalado. brew instala 4.6.2 por padrão, o que viola D-01. Download manual é necessário para garantir paridade com o container CI barichello/godot-ci:4.4.1.</what-built>
  <how-to-verify>
    1. Acesse https://godotengine.org/releases/4.4/ no browser
    2. Baixe "Godot_v4.4.1-stable_macos.universal.zip" (versão Standard, não .NET)
    3. Extraia o zip e mova Godot.app para /Applications/:
       `mv ~/Downloads/Godot.app /Applications/`
    4. Adicione o alias ao ~/.zshrc:
       `echo 'alias godot="/Applications/Godot.app/Contents/MacOS/Godot"' >> ~/.zshrc`
       `source ~/.zshrc`
    5. Verifique: `godot --version`
       Deve retornar "4.4.1.stable.official [..." ou similar com 4.4.x

    IMPORTANTE: macOS pode pedir para "Abrir mesmo assim" nas preferências de segurança (System Settings > Privacy & Security) na primeira vez que o app é aberto.
  </how-to-verify>
  <resume-signal>Digite "godot-instalado" após confirmar que `godot --version` retorna 4.4.x</resume-signal>
  <acceptance_criteria>
    - `godot --version` retorna string contendo "4.4." (ex: "4.4.1.stable.official [...]")
    - O alias "godot" está definido no shell atual (não apenas no ~/.zshrc)
    - /Applications/Godot.app existe no filesystem
  </acceptance_criteria>
</task>

<task type="checkpoint:human-action" gate="blocking">
  <name>Task 2: Criar projeto Godot via editor e configurar pixel art settings</name>
  <files>project.godot, icon.svg, scenes/main.tscn</files>
  <read_first>
    /Users/renatojaf/jogo-natalia/.planning/phases/00-funda-o/00-PATTERNS.md (seção "project.godot" e "scenes/main.tscn")
    /Users/renatojaf/jogo-natalia/.planning/phases/00-funda-o/00-CONTEXT.md (decisões D-03, D-04, D-05, D-09, D-13)
    /Users/renatojaf/jogo-natalia/.planning/phases/00-funda-o/00-RESEARCH.md (seção "Pitfall 6: Renderer não é Compatibility por padrão")
  </read_first>
  <what-built>O projeto Godot deve ser criado via editor para garantir estrutura interna válida. Criar manualmente do zero causa erros silenciosos. O editor gera UIDs, config_version e outros campos internos corretamente.</what-built>
  <how-to-verify>
    Abrir o editor Godot e seguir estes passos exatos:

    CRIAÇÃO DO PROJETO:
    1. Abrir Godot.app — aparece o Project Manager
    2. Clicar "Create" (novo projeto)
    3. Project Name: "Destiny — Tales of Natalia" (per D-03)
    4. Project Path: /Users/renatojaf/jogo-natalia
    5. Renderer: selecionar "Compatibility" (per D-05 e EXPORT-03) — NÃO usar Forward+ ou Mobile
    6. Clicar "Create & Edit"

    CONFIGURAÇÕES PIXEL ART (Project > Project Settings):

    Display > Window > Size:
    - Viewport Width: 320 (per D-04)
    - Viewport Height: 180 (per D-04)
    - Window Width Override: 1280
    - Window Height Override: 720

    Display > Window > Stretch:
    - Mode: canvas_items (per D-05)
    - Scale Mode: integer (per D-05)

    Rendering > Textures > Canvas Textures:
    - Default Texture Filter: Nearest (per D-05) — se o valor do enum for "Nearest"

    Rendering > 2D > Snap:
    - Snap 2D Transforms to Pixel: On (per D-05)

    Clicar "Save" e fechar Project Settings.

    CENA DE TESTE (per D-13):
    1. Scene > New Scene
    2. Selecionar "2D Scene" como raiz (cria Node2D)
    3. Renomear raiz para "Main"
    4. Adicionar filho: Node2D > Add Child Node > Label
    5. Selecionar o Label, no Inspector: Text = "v0.0 — Destiny: Tales of Natalia"
    6. Save Scene: salvar como "scenes/main.tscn"

    DEFINIR MAIN SCENE:
    Project > Project Settings > Application > Run > Main Scene
    Selecionar "scenes/main.tscn"

    FECHAR E REABRIR para confirmar que as configurações persistem.

    Verificar em Project Settings após reabrir:
    - Rendering > Renderer deve mostrar "Compatibility"
    - Display > Window > Size deve mostrar 320x180
  </how-to-verify>
  <resume-signal>Digite "projeto-criado" após criar o projeto, a cena e confirmar que as configurações persistem após reabrir</resume-signal>
  <acceptance_criteria>
    - /Users/renatojaf/jogo-natalia/project.godot existe
    - `grep "gl_compatibility" /Users/renatojaf/jogo-natalia/project.godot` retorna pelo menos uma linha
    - `grep "320" /Users/renatojaf/jogo-natalia/project.godot` retorna linha com viewport_width=320
    - `grep "canvas_items" /Users/renatojaf/jogo-natalia/project.godot` retorna linha com stretch/mode
    - /Users/renatojaf/jogo-natalia/scenes/main.tscn existe
    - `grep "v0.0" /Users/renatojaf/jogo-natalia/scenes/main.tscn` retorna o texto do Label
    - `grep "main_scene" /Users/renatojaf/jogo-natalia/project.godot` retorna linha apontando para scenes/main.tscn
    - /Users/renatojaf/jogo-natalia/icon.svg existe (gerado automaticamente pelo editor)
  </acceptance_criteria>
</task>

<task type="auto" tdd="false">
  <name>Task 3: Verificar project.godot e fazer commit inicial do projeto</name>
  <files>project.godot, icon.svg, scenes/main.tscn</files>
  <read_first>
    /Users/renatojaf/jogo-natalia/project.godot
    /Users/renatojaf/jogo-natalia/scenes/main.tscn
    /Users/renatojaf/jogo-natalia/.planning/phases/00-funda-o/00-RESEARCH.md (seção "Verificar renderer no project.godot após criação" e "Assumptions Log")
  </read_first>
  <action>
    Ler project.godot e verificar que todas as configurações obrigatórias estão presentes. Checar especificamente:

    1. rendering/renderer/rendering_method="gl_compatibility" existe (per D-05, EXPORT-03)
    2. window/size/viewport_width=320 e viewport_height=180 existem (per D-04)
    3. window/stretch/mode="canvas_items" e scale_mode="integer" existem (per D-05)
    4. textures/canvas_textures/default_texture_filter=0 existe (per D-05 — valor 0 = Nearest)
    5. 2d/snap/snap_2d_transforms_to_pixel=true existe (per D-05)
    6. config/name="Destiny — Tales of Natalia" existe (per D-03)
    7. run/main_scene="res://scenes/main.tscn" existe (per D-13)

    Se alguma configuração estiver faltando, editá-la diretamente no project.godot com cautela — apenas adicionar dentro da seção [rendering] ou [display] correta. Não recriar o arquivo.

    Após verificação, fazer commit com todos os arquivos do projeto Godot (mas NÃO commitar .godot/ que está no .gitignore):

    git -C /Users/renatojaf/jogo-natalia add project.godot icon.svg scenes/main.tscn
    git -C /Users/renatojaf/jogo-natalia commit -m "feat(00): create Godot project with Compatibility renderer and pixel art settings (D-03, D-04, D-05, D-09, D-13, EXPORT-03)"

    Verificar que .godot/ NÃO está no commit (git show --stat HEAD não deve mostrar .godot/).
  </action>
  <verify>
    <automated>
      cd /Users/renatojaf/jogo-natalia && grep "gl_compatibility" project.godot && grep "viewport_width=320" project.godot && grep "canvas_items" project.godot && grep "main.tscn" project.godot && git show --stat HEAD | grep -v ".godot/" | head -20
    </automated>
  </verify>
  <acceptance_criteria>
    - `grep "gl_compatibility" project.godot` retorna linha com rendering_method="gl_compatibility"
    - `grep "viewport_width=320" project.godot` retorna a linha de configuração
    - `grep "canvas_items" project.godot` retorna linha com stretch/mode
    - `grep "main.tscn" project.godot` retorna linha com run/main_scene
    - `grep "v0.0" scenes/main.tscn` retorna o texto do Label
    - `git show --stat HEAD` mostra project.godot, icon.svg e scenes/main.tscn como arquivos no commit
    - `git show --stat HEAD` NÃO mostra nenhum arquivo sob .godot/ no commit
    - `git log --oneline -3` mostra o commit desta task como o mais recente
  </acceptance_criteria>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| editor local → project.godot | Configurações do renderer são definidas pelo editor e lidas pelo CI |
| project.godot → CI headless | O arquivo define o renderer usado no export; erro aqui causa falha silenciosa no web export |

## STRIDE Threat Register

| Threat ID | Category | Component | Disposition | Mitigation Plan |
|-----------|----------|-----------|-------------|-----------------|
| T-00-04 | Spoofing | Godot version mismatch (local 4.6 vs CI 4.4.1) | mitigate | Task 1 é checkpoint bloqueante com verificação explícita de "godot --version retorna 4.4.x"; paridade garantida com barichello/godot-ci:4.4.1 |
| T-00-05 | Tampering | .godot/ cache commitado acidentalmente | mitigate | .gitignore criado no plano 001 exclui .godot/; Task 3 verifica explicitamente que git show --stat HEAD não inclui .godot/ |
| T-00-06 | Denial of Service | Renderer Forward+ no projeto quebraria web export | mitigate | Task 2 instrui explicitamente selecionar "Compatibility" na criação; Task 3 verifica "gl_compatibility" no project.godot antes de commitar |
| T-00-07 | Information Disclosure | export_presets.cfg com script_encryption_key não vazia | mitigate | export_presets.cfg só é criado no plano 003; verificar que script_encryption_key="" antes de commitar (per T-00-02 do contexto de segurança) |
</threat_model>

<verification>
Após completar todos os tasks deste plano:

1. `godot --version` retorna versão 4.4.x
2. `grep "gl_compatibility" /Users/renatojaf/jogo-natalia/project.godot` retorna a linha de configuração
3. `grep "viewport_width=320" /Users/renatojaf/jogo-natalia/project.godot` retorna a linha
4. `grep "v0.0" /Users/renatojaf/jogo-natalia/scenes/main.tscn` retorna o texto do Label
5. `git -C /Users/renatojaf/jogo-natalia show --stat HEAD` mostra project.godot e scenes/main.tscn
6. `git -C /Users/renatojaf/jogo-natalia show --stat HEAD` NÃO mostra arquivos de .godot/
</verification>

<success_criteria>
Godot 4.4.x está instalado e acessível via alias. project.godot existe com renderer Compatibility e todas as configurações pixel art definidas em D-05. scenes/main.tscn exibe "v0.0 — Destiny: Tales of Natalia". As configurações persistem após reabrir o projeto no editor. EXPORT-03 está satisfeito: rendering/renderer/rendering_method="gl_compatibility" está presente no project.godot commitado.
</success_criteria>

<output>
Após completar, criar /Users/renatojaf/jogo-natalia/.planning/phases/00-funda-o/00-002-SUMMARY.md com:
- Versão do Godot instalada
- Confirmação de cada configuração D-05 aplicada (com grep proof)
- Hash do commit de criação do projeto
- Decisões D-01, D-03, D-04, D-05, D-09, D-13 implementadas
- Status de EXPORT-03: satisfeito
</output>
