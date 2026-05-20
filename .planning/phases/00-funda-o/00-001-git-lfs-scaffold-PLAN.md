---
phase: "00-funda-o"
plan: "001"
type: execute
wave: 1
depends_on: []
files_modified:
  - .gitattributes
  - .gitignore
  - serve.py
  - scenes/.gitkeep
  - assets/sprites/player/.gitkeep
  - assets/sprites/enemies/.gitkeep
  - assets/sprites/ui/.gitkeep
  - assets/audio/sfx/.gitkeep
  - assets/audio/music/.gitkeep
  - scripts/.gitkeep
  - autoloads/.gitkeep
autonomous: false
requirements:
  - EXPORT-03

must_haves:
  truths:
    - "Git LFS está instalado e ativo no repositório (git lfs version retorna versão)"
    - "Arquivos .png, .jpg, .wav, .ogg, .mp3, .ttf, .otf, .scn, .res são rastreados via LFS segundo .gitattributes"
    - "Pasta .godot/ e export/ estão excluídas do controle de versão via .gitignore"
    - "Estrutura de pastas completa existe e está commitada com .gitkeep files"
    - "serve.py com CORS headers existe na raiz do projeto para teste web local"
  artifacts:
    - path: ".gitattributes"
      provides: "Git LFS tracking rules para todos os tipos de asset binário"
      contains: "*.png filter=lfs"
    - path: ".gitignore"
      provides: "Exclusão de cache Godot, traduções compiladas e artifacts de export"
      contains: ".godot/"
    - path: "serve.py"
      provides: "Servidor HTTP local com CORS headers para testar web export"
      contains: "Cross-Origin-Opener-Policy"
    - path: "scenes/.gitkeep"
      provides: "Pasta scenes/ versionada no git"
    - path: "autoloads/.gitkeep"
      provides: "Pasta autoloads/ versionada (D-09: vazia nesta fase)"
  key_links:
    - from: ".gitattributes"
      to: "Git LFS"
      via: "filter=lfs directive por tipo de arquivo"
      pattern: "filter=lfs diff=lfs merge=lfs -text"
    - from: ".gitignore"
      to: "pasta .godot/"
      via: "exclusão de cache da engine"
      pattern: "\\.godot/"

user_setup:
  - service: git-lfs
    why: "Git LFS precisa ser instalado localmente antes de qualquer commit de asset binário"
    steps:
      - task: "Instalar Git LFS via Homebrew"
        command: "brew install git-lfs"
      - task: "Ativar LFS no repositório"
        command: "git -C /Users/renatojaf/jogo-natalia lfs install"
    verification: "git lfs version retorna git-lfs/3.x.x ou superior"
---

<objective>
Configurar a fundação de controle de versão: Git LFS ativo, estrutura de pastas completa versionada, .gitignore e .gitattributes corretos, e serve.py para teste web local. Nenhum arquivo Godot é criado aqui — apenas a infraestrutura de VCS que protege os assets binários das fases futuras.

Purpose: Git LFS deve ser configurado ANTES do primeiro commit de qualquer asset binário (.png, .wav, .ogg). Migrar binários para LFS depois é um processo complexo e destrutivo. Este plano garante que a fundação está certa desde o início.

Output: Repositório com LFS ativo, estrutura de pastas commitada, arquivos de configuração VCS no lugar.
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
</context>

<tasks>

<task type="checkpoint:human-action" gate="blocking">
  <name>Task 1: Instalar Git LFS localmente</name>
  <read_first>
    /Users/renatojaf/jogo-natalia/.planning/phases/00-funda-o/00-RESEARCH.md (seção "Environment Availability" e "Pitfall 1")
  </read_first>
  <what-built>Git LFS não está instalado na máquina (confirmado na pesquisa: git lfs retorna "not a git command"). Esta etapa manual é necessária porque brew install requer interação do usuário no terminal.</what-built>
  <how-to-verify>
    Execute no terminal:
    1. `brew install git-lfs` — instala Git LFS via Homebrew
    2. `git -C /Users/renatojaf/jogo-natalia lfs install` — ativa LFS no repositório
    3. `git lfs version` — deve retornar "git-lfs/3.x.x" (qualquer versão 3.x é válida)

    Se o passo 1 falhar por falta de Homebrew, instale Homebrew primeiro: https://brew.sh
  </how-to-verify>
  <resume-signal>Digite "lfs-instalado" após confirmar que `git lfs version` retorna uma versão válida</resume-signal>
  <acceptance_criteria>
    - `git lfs version` retorna string no formato "git-lfs/3.x.x (GitHub; ..." sem erro
    - `git -C /Users/renatojaf/jogo-natalia lfs env` mostra "git config filter.lfs.smudge = git-lfs smudge"
  </acceptance_criteria>
</task>

<task type="auto" tdd="false">
  <name>Task 2: Criar .gitattributes, .gitignore e estrutura de pastas</name>
  <files>
    .gitattributes,
    .gitignore,
    scenes/.gitkeep,
    assets/sprites/player/.gitkeep,
    assets/sprites/enemies/.gitkeep,
    assets/sprites/ui/.gitkeep,
    assets/audio/sfx/.gitkeep,
    assets/audio/music/.gitkeep,
    scripts/.gitkeep,
    autoloads/.gitkeep
  </files>
  <read_first>
    /Users/renatojaf/jogo-natalia/.planning/phases/00-funda-o/00-PATTERNS.md (seções ".gitattributes", ".gitignore", "Estrutura de Pastas")
    /Users/renatojaf/jogo-natalia/.planning/phases/00-funda-o/00-CONTEXT.md (decisões D-06, D-07, D-08, D-09)
  </read_first>
  <action>
    Trabalhar no diretório /Users/renatojaf/jogo-natalia/.

    Criar .gitattributes com as seguintes regras LFS (per D-06): *.png, *.jpg, *.webp, *.wav, *.ogg, *.mp3, *.scn, *.res, *.ttf, *.otf — cada linha com o formato "*.ext filter=lfs diff=lfs merge=lfs -text". Incluir comentários de seção (Imagens, Áudio, Godot binary resources, Fontes).

    Criar .gitignore com três entradas (per D-07): ".godot/" (cache da engine), "*.translation" (traduções compiladas), "export/" (artifacts de build). Adicionar ".DS_Store" como cortesia macOS.

    Criar estrutura de pastas (per D-08) com .gitkeep em cada pasta versionável: scenes/, assets/sprites/player/, assets/sprites/enemies/, assets/sprites/ui/, assets/audio/sfx/, assets/audio/music/, scripts/, autoloads/. A pasta export/ também deve ser criada mas SEM .gitkeep (está no .gitignore, não vai para o git).

    Criar também .github/workflows/ como estrutura vazia (receberá export.yml no plano 004).

    Commit após criar tudo: "chore(00): configure Git LFS, gitignore, and folder structure (D-06, D-07, D-08)"
  </action>
  <verify>
    <automated>
      cd /Users/renatojaf/jogo-natalia && grep -c "filter=lfs" .gitattributes && grep ".godot/" .gitignore && ls scenes/.gitkeep assets/sprites/player/.gitkeep autoloads/.gitkeep
    </automated>
  </verify>
  <acceptance_criteria>
    - .gitattributes contém pelo menos 10 linhas com "filter=lfs diff=lfs merge=lfs -text" (uma por tipo de arquivo)
    - .gitattributes cobre: *.png, *.jpg, *.wav, *.ogg, *.mp3, *.scn, *.res, *.ttf, *.otf
    - .gitignore contém ".godot/" em linha própria
    - .gitignore contém "*.translation" em linha própria
    - .gitignore contém "export/" em linha própria
    - Pastas scenes/, assets/sprites/player/, assets/sprites/enemies/, assets/sprites/ui/, assets/audio/sfx/, assets/audio/music/, scripts/, autoloads/ existem com .gitkeep
    - git status mostra .gitattributes, .gitignore e os .gitkeep files como rastreados
    - export/ existe no filesystem mas NÃO aparece em git status (está no .gitignore)
  </acceptance_criteria>
</task>

<task type="auto" tdd="false">
  <name>Task 3: Criar serve.py para teste web local</name>
  <files>serve.py</files>
  <read_first>
    /Users/renatojaf/jogo-natalia/.planning/phases/00-funda-o/00-PATTERNS.md (seção "serve.py")
    /Users/renatojaf/jogo-natalia/.planning/phases/00-funda-o/00-RESEARCH.md (seção "Pitfall 3: SharedArrayBuffer")
  </read_first>
  <action>
    Criar serve.py na raiz do projeto /Users/renatojaf/jogo-natalia/serve.py.

    O script é um servidor HTTP Python com CORS headers obrigatórios para SharedArrayBuffer (necessário para web exports com threads). Implementar uma subclasse de SimpleHTTPRequestHandler que sobrescreve end_headers() para adicionar dois headers: "Cross-Origin-Opener-Policy: same-origin" e "Cross-Origin-Embedder-Policy: require-corp". Ler porta do argv[1] ou usar 8000 como padrão. Incluir docstring explicando o propósito e uso:

    Uso esperado: cd export/web && python3 /Users/renatojaf/jogo-natalia/serve.py
    URL: http://localhost:8000

    Commitar com: "chore(00): add serve.py for local web export testing (CORS headers)"
  </action>
  <verify>
    <automated>
      cd /Users/renatojaf/jogo-natalia && python3 -c "import ast; ast.parse(open('serve.py').read()); print('syntax OK')" && grep -c "Cross-Origin-Opener-Policy" serve.py
    </automated>
  </verify>
  <acceptance_criteria>
    - serve.py existe em /Users/renatojaf/jogo-natalia/serve.py
    - python3 -c "import ast; ast.parse(open('serve.py').read())" não retorna erro (sintaxe válida)
    - serve.py contém "Cross-Origin-Opener-Policy" e "same-origin"
    - serve.py contém "Cross-Origin-Embedder-Policy" e "require-corp"
    - serve.py contém lógica para ler porta do sys.argv com fallback para 8000
    - git log mostra os dois commits desta task acima do commit inicial
  </acceptance_criteria>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| repositório local → GitHub | Git push expõe conteúdo do .gitattributes e .gitignore publicamente |
| CI → itch.io (futuro) | BUTLER_CREDENTIALS transitará pelo runner — não pode estar hardcoded |

## STRIDE Threat Register

| Threat ID | Category | Component | Disposition | Mitigation Plan |
|-----------|----------|-----------|-------------|-----------------|
| T-00-01 | Information Disclosure | .gitattributes / .gitignore | accept | Estes arquivos são convencionalmente públicos; não contêm dados sensíveis |
| T-00-02 | Tampering | Git LFS não inicializado antes de commit binário | mitigate | Task 1 é checkpoint bloqueante: executor só avança após confirmar "lfs-instalado"; Task 2 cria .gitattributes antes de qualquer asset |
| T-00-03 | Information Disclosure | serve.py exposto na raiz do projeto | accept | serve.py é utilitário de desenvolvimento local; não é executado em produção; não contém credenciais |
</threat_model>

<verification>
Após completar todos os tasks deste plano:

1. `git lfs version` retorna versão 3.x sem erro
2. `grep -c "filter=lfs" /Users/renatojaf/jogo-natalia/.gitattributes` retorna 10 ou mais
3. `grep ".godot/" /Users/renatojaf/jogo-natalia/.gitignore` retorna a linha
4. `ls /Users/renatojaf/jogo-natalia/scenes/.gitkeep` não retorna erro
5. `ls /Users/renatojaf/jogo-natalia/autoloads/.gitkeep` não retorna erro
6. `python3 -c "import ast; ast.parse(open('/Users/renatojaf/jogo-natalia/serve.py').read())"` não retorna erro
7. `git -C /Users/renatojaf/jogo-natalia log --oneline` mostra pelo menos 2 commits novos
</verification>

<success_criteria>
Git LFS está instalado e ativo. .gitattributes rastreia todos os tipos de asset binário. .gitignore exclui .godot/, *.translation e export/. Estrutura de pastas completa está commitada com .gitkeep files. serve.py com CORS headers está disponível para testes web locais. Tudo isso acontece ANTES de qualquer arquivo Godot ser criado — garantindo que nenhum binário entre no git regular acidentalmente.
</success_criteria>

<output>
Após completar, criar /Users/renatojaf/jogo-natalia/.planning/phases/00-funda-o/00-001-SUMMARY.md com:
- Arquivos criados e seus propósitos
- Confirmação de que git lfs ls-files funciona
- Hash do último commit
- Decisões D-06, D-07, D-08, D-09 implementadas
</output>
