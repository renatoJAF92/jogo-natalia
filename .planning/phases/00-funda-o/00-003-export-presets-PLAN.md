---
phase: "00-funda-o"
plan: "003"
type: execute
wave: 3
depends_on:
  - "00-002"
files_modified:
  - export_presets.cfg
autonomous: false
requirements:
  - EXPORT-03

must_haves:
  truths:
    - "export_presets.cfg existe com 3 presets: Web, Windows Desktop, macOS"
    - "Preset Web usa plataforma 'Web' (não 'HTML5' — nome antigo do Godot 3)"
    - "export_path do preset Web aponta para export/web/index.html"
    - "export_path do preset Windows aponta para export/windows/destiny-tales-of-natalia.exe"
    - "export_path do preset macOS aponta para export/mac/destiny-tales-of-natalia.zip"
    - "Comando godot --headless --export-release 'Web' gera export/web/index.html sem erro"
    - "Build HTML5 gerado abre no navegador via serve.py e exibe 'v0.0 — Destiny: Tales of Natalia'"
    - "export_presets.cfg está commitado no repositório (obrigatório para CI funcionar)"
    - "script_encryption_key está vazio (sem dados sensíveis) em todos os presets"
  artifacts:
    - path: "export_presets.cfg"
      provides: "Configuração de export para 3 plataformas, consumida pelo CI"
      contains: "name=\"Web\""
    - path: "export/web/index.html"
      provides: "Build HTML5 gerado pelo export local (não versionado — apenas teste)"
  key_links:
    - from: "export_presets.cfg"
      to: "godot --export-release CLI"
      via: "preset name match exato"
      pattern: "name=\"Web\""
    - from: "export/web/index.html"
      to: "navegador via serve.py"
      via: "HTTP server na porta 8000"
      pattern: "http://localhost:8000"
---

<objective>
Criar os 3 export presets (Web, Windows Desktop, macOS) via editor Godot, commitar export_presets.cfg, executar export web local e verificar que o build HTML5 abre no navegador exibindo a label de versão.

Purpose: export_presets.cfg commitado é pré-requisito do CI/CD (plano 004). O teste de export local (D-12) prova que o pipeline funciona end-to-end antes de envolver GitHub Actions.

Output: export_presets.cfg com 3 presets commitado, build web gerado e verificado no navegador.
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
@/Users/renatojaf/jogo-natalia/.planning/phases/00-funda-o/00-002-SUMMARY.md

<interfaces>
<!-- Padrão do export_presets.cfg (RESEARCH.md Pattern 3) -->

Nomes dos presets (devem ser exatos — CI usa estes nomes no comando):
  preset 0: name="Web"              platform="Web"
  preset 1: name="Windows Desktop"  platform="Windows Desktop"
  preset 2: name="macOS"            platform="macOS"

Caminhos de export (D-11, D-12):
  Web:     export_path="export/web/index.html"
  Windows: export_path="export/windows/destiny-tales-of-natalia.exe"
  macOS:   export_path="export/mac/destiny-tales-of-natalia.zip"

Segurança (T-00-02):
  script_encryption_key="" em todos os presets (nunca usar valor real)
</interfaces>
</context>

<tasks>

<task type="checkpoint:human-action" gate="blocking">
  <name>Task 1: Criar export presets via editor Godot</name>
  <files>export_presets.cfg</files>
  <read_first>
    /Users/renatojaf/jogo-natalia/.planning/phases/00-funda-o/00-PATTERNS.md (seção "export_presets.cfg")
    /Users/renatojaf/jogo-natalia/.planning/phases/00-funda-o/00-RESEARCH.md (seção "Pitfall 5: Nome do preset deve bater com CLI" e "Pattern 3")
    /Users/renatojaf/jogo-natalia/.planning/phases/00-funda-o/00-CONTEXT.md (decisões D-10, D-11, D-12)
  </read_first>
  <what-built>export_presets.cfg deve ser criado via editor Godot (Project > Export). Criar manualmente do zero pode causar erros silenciosos porque o editor valida a estrutura interna e adiciona campos obrigatórios que não estão documentados.</what-built>
  <how-to-verify>
    Abrir o projeto em Godot (abrir /Applications/Godot.app, Project Manager > Import ou Open > selecionar /Users/renatojaf/jogo-natalia).

    Project > Export... (abre a janela de Export):

    PRESET 1 — WEB:
    1. Clicar "Add..." > "Web"
    2. Nome deve estar como "Web" (verificar — não mudar para "HTML5")
    3. Export Path: clicar na pasta e navegar para criar "export/web/index.html"
       Ou digitar diretamente: export/web/index.html
    4. Em "Options": verificar que "Use Threads" está DESMARCADO (sem threads = sem necessidade de CORS headers específicos, export mais simples)
    5. Não alterar outros campos

    PRESET 2 — WINDOWS DESKTOP:
    1. Clicar "Add..." > "Windows Desktop"
    2. Nome: "Windows Desktop"
    3. Export Path: export/windows/destiny-tales-of-natalia.exe
    4. Em "Options" > Binary Format: Architecture = "x86_64"
    5. Codesign/Enable: deixar desmarcado

    PRESET 3 — MACOS:
    1. Clicar "Add..." > "macOS"
    2. Nome: "macOS"
    3. Export Path: export/mac/destiny-tales-of-natalia.zip
    4. Codesign/Enable: deixar desmarcado (per deferred: macOS code signing)
    5. Notarization/Enable: deixar desmarcado

    Fechar a janela Export — o arquivo export_presets.cfg é criado automaticamente na raiz do projeto.

    NÃO exportar ainda — apenas configurar os presets.
  </how-to-verify>
  <resume-signal>Digite "presets-criados" após fechar a janela Export e confirmar que /Users/renatojaf/jogo-natalia/export_presets.cfg existe</resume-signal>
  <acceptance_criteria>
    - /Users/renatojaf/jogo-natalia/export_presets.cfg existe
    - `grep 'name="Web"' /Users/renatojaf/jogo-natalia/export_presets.cfg` retorna a linha (nome exato "Web", não "HTML5")
    - `grep 'name="Windows Desktop"' /Users/renatojaf/jogo-natalia/export_presets.cfg` retorna a linha
    - `grep 'name="macOS"' /Users/renatojaf/jogo-natalia/export_presets.cfg` retorna a linha
    - `grep 'script_encryption_key=""' /Users/renatojaf/jogo-natalia/export_presets.cfg` retorna pelo menos uma linha (chave vazia = sem dados sensíveis)
  </acceptance_criteria>
</task>

<task type="auto" tdd="false">
  <name>Task 2: Verificar export_presets.cfg e commitar</name>
  <files>export_presets.cfg</files>
  <read_first>
    /Users/renatojaf/jogo-natalia/export_presets.cfg
    /Users/renatojaf/jogo-natalia/.planning/phases/00-funda-o/00-RESEARCH.md (seção "Pitfall 5" e security domain T-00-02)
    /Users/renatojaf/jogo-natalia/.planning/phases/00-funda-o/00-CONTEXT.md (D-10: export_presets.cfg deve ser commitado)
  </read_first>
  <action>
    Ler export_presets.cfg e verificar:

    1. Existem 3 presets: [preset.0], [preset.1], [preset.2] — contar seções no arquivo
    2. Os nomes são exatamente "Web", "Windows Desktop", "macOS" (verificar com grep)
    3. script_encryption_key está vazio ("") em todos os presets — nunca deve ter valor real
    4. Os export_path dos presets apontam para dentro de "export/" (que está no .gitignore — correto, o export_presets.cfg em si vai para git, mas o conteúdo de export/ não)

    Se export_path estiver diferente do padrão, editar export_presets.cfg para corrigir os caminhos para:
    - preset Web: export_path="export/web/index.html"
    - preset Windows: export_path="export/windows/destiny-tales-of-natalia.exe"
    - preset macOS: export_path="export/mac/destiny-tales-of-natalia.zip"

    Verificar que script_encryption_key="" em TODOS os presets (linha por linha). Se houver qualquer valor não-vazio, remover antes de commitar.

    Commitar apenas export_presets.cfg:
    git -C /Users/renatojaf/jogo-natalia add export_presets.cfg
    git -C /Users/renatojaf/jogo-natalia commit -m "feat(00): add export presets for Web, Windows Desktop, macOS (D-10, D-11)"
  </action>
  <verify>
    <automated>
      cd /Users/renatojaf/jogo-natalia && grep -c 'name=' export_presets.cfg && grep 'name="Web"' export_presets.cfg && grep 'name="Windows Desktop"' export_presets.cfg && grep 'name="macOS"' export_presets.cfg && grep -v '^[[:space:]]*$' export_presets.cfg | grep 'script_encryption_key' | grep -v '=""' | wc -l
    </automated>
  </verify>
  <acceptance_criteria>
    - `grep -c 'name=' export_presets.cfg` retorna 3
    - `grep 'name="Web"' export_presets.cfg` retorna uma linha
    - `grep 'name="Windows Desktop"' export_presets.cfg` retorna uma linha
    - `grep 'name="macOS"' export_presets.cfg` retorna uma linha
    - O comando de verificação de script_encryption_key retorna 0 (nenhuma chave com valor não-vazio)
    - `git -C /Users/renatojaf/jogo-natalia log --oneline -1` mostra o commit de export presets
    - `git -C /Users/renatojaf/jogo-natalia show --stat HEAD` mostra export_presets.cfg no commit
  </acceptance_criteria>
</task>

<task type="checkpoint:human-verify" gate="blocking">
  <name>Task 3: Executar export web local e verificar no navegador</name>
  <read_first>
    /Users/renatojaf/jogo-natalia/.planning/phases/00-funda-o/00-RESEARCH.md (seção "Pitfall 2: godot --headless falha sem .godot/ importado" e "Pitfall 3: SharedArrayBuffer")
    /Users/renatojaf/jogo-natalia/.planning/phases/00-funda-o/00-CONTEXT.md (D-12: testar localmente antes de declarar fase completa)
    /Users/renatojaf/jogo-natalia/serve.py
  </read_first>
  <what-built>
    O executor automatiza o export web via linha de comando e inicia o servidor local. O usuário verifica visualmente no navegador que o build HTML5 exibe a label de versão corretamente.

    Executar os seguintes comandos:
    1. Importar assets (necessário para headless export funcionar sem erros):
       `godot --headless --editor --quit --path /Users/renatojaf/jogo-natalia`
    2. Criar pasta de destino:
       `mkdir -p /Users/renatojaf/jogo-natalia/export/web`
    3. Executar export:
       `godot --headless --export-release "Web" /Users/renatojaf/jogo-natalia/export/web/index.html --path /Users/renatojaf/jogo-natalia`
    4. Iniciar servidor web local em background:
       Abrir novo terminal: `cd /Users/renatojaf/jogo-natalia/export/web && python3 /Users/renatojaf/jogo-natalia/serve.py`
  </what-built>
  <how-to-verify>
    Após o executor rodar os comandos acima:
    1. Abrir http://localhost:8000 no Chrome ou Firefox
    2. Aguardar o carregamento (pode demorar alguns segundos — Godot web export carrega progressivamente)
    3. Confirmar que aparece o texto "v0.0 — Destiny: Tales of Natalia" na tela
    4. Confirmar que não há tela preta ou mensagens de erro no console do browser (F12)

    Se aparecer "SharedArrayBuffer is not defined" no console:
    - Verificar se o preset Web tem "Use Threads" desmarcado
    - Se tiver marcado, desmarcar no editor (Project > Export > Web > Options) e re-exportar

    Se o export falhar com "No export template found":
    - Os export templates precisam ser baixados: Editor > Manage Export Templates > Download
    - Ou verificar se o Godot foi aberto pelo menos uma vez antes do export headless
  </how-to-verify>
  <resume-signal>Digite "export-ok" se o navegador exibiu "v0.0 — Destiny: Tales of Natalia" sem erros. Se houver problema, descreva o erro para que o executor possa corrigir.</resume-signal>
  <acceptance_criteria>
    - /Users/renatojaf/jogo-natalia/export/web/index.html existe após o export
    - /Users/renatojaf/jogo-natalia/export/web/ contém pelo menos: index.html, index.js, index.wasm (ou index.pck)
    - http://localhost:8000 exibe texto "v0.0 — Destiny: Tales of Natalia" no navegador
    - Console do browser (F12) não mostra erros críticos (SharedArrayBuffer, tela preta)
    - O export/ directory NÃO aparece em `git status` (está corretamente no .gitignore)
  </acceptance_criteria>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| export_presets.cfg → git (público) | Arquivo commitado publicamente — verificar ausência de dados sensíveis |
| export/web/index.html → navegador | Build servido localmente — não é produção, mas deve funcionar |

## STRIDE Threat Register

| Threat ID | Category | Component | Disposition | Mitigation Plan |
|-----------|----------|-----------|-------------|-----------------|
| T-00-08 | Information Disclosure | export_presets.cfg com script_encryption_key não vazia | mitigate | Task 2 verifica explicitamente que todos os script_encryption_key="" antes de commitar; comando grep específico retorna 0 se todos estiverem vazios |
| T-00-09 | Tampering | Nome do preset "HTML5" em vez de "Web" | mitigate | Task 1 instrui verificar nome após criar; Task 2 verifica com grep 'name="Web"'; nome errado quebra CI com erro explícito |
| T-00-10 | Denial of Service | Export web falha por falta de templates | accept | Pitfall documentado no RESEARCH.md com solução (Editor > Manage Export Templates); aceitável pois é setup inicial de ambiente local |
</threat_model>

<verification>
Após completar todos os tasks deste plano:

1. `grep -c 'name=' /Users/renatojaf/jogo-natalia/export_presets.cfg` retorna 3
2. `grep 'name="Web"' /Users/renatojaf/jogo-natalia/export_presets.cfg` retorna linha
3. `git -C /Users/renatojaf/jogo-natalia show --stat HEAD` mostra export_presets.cfg
4. `/Users/renatojaf/jogo-natalia/export/web/index.html` existe (build gerado localmente)
5. http://localhost:8000 exibe "v0.0 — Destiny: Tales of Natalia" (verificação manual confirmada)
6. `git -C /Users/renatojaf/jogo-natalia status` não mostra export/ como arquivo rastreado
</verification>

<success_criteria>
export_presets.cfg com 3 presets (Web, Windows Desktop, macOS) está commitado. Nomes dos presets estão corretos ("Web", não "HTML5"). script_encryption_key está vazio em todos os presets. Export web local gerou build HTML5 funcional. Navegador exibe "v0.0 — Destiny: Tales of Natalia" sem erros. Success Criterion 1 do ROADMAP.md está satisfeito: `godot --export-release "Web"` gera build HTML5 que abre no navegador.
</success_criteria>

<output>
Após completar, criar /Users/renatojaf/jogo-natalia/.planning/phases/00-funda-o/00-003-SUMMARY.md com:
- Confirmação dos 3 presets e seus nomes exatos
- Hash do commit de export_presets.cfg
- Confirmação de export web local: URL testada, resultado visual
- Decisões D-10, D-11, D-12 implementadas
- Success Criterion 1 do ROADMAP: status (completo/pendente)
</output>
