---
phase: "00-funda-o"
plan: "004"
type: execute
wave: 4
depends_on:
  - "00-003"
files_modified:
  - .github/workflows/export.yml
autonomous: false
requirements:
  - EXPORT-03

must_haves:
  truths:
    - "GitHub Actions pipeline exporta Web, Windows e macOS ao criar tag v*"
    - "Pull Requests apenas verificam que o projeto compila (sem deploy)"
    - "Checkout usa lfs: true em todos os jobs"
    - "Credencial BUTLER_CREDENTIALS usa ${{ secrets.BUTLER_CREDENTIALS }} — nunca hardcoded"
    - "Comando de export usa --headless --export-release (não --export)"
    - "ITCH_USER é placeholder até conta itch.io ser criada"
    - "Push da tag v0.0 dispara o pipeline no GitHub"
  artifacts:
    - path: ".github/workflows/export.yml"
      provides: "Pipeline CI/CD com 3 jobs de export + deploy condicional"
      contains: "barichello/godot-ci:4.4.1"
  key_links:
    - from: ".github/workflows/export.yml"
      to: "export_presets.cfg"
      via: "nome do preset no comando godot --export-release"
      pattern: "--export-release \"Web\""
    - from: "BUTLER_CREDENTIALS step"
      to: "GitHub Secrets"
      via: "secrets.BUTLER_CREDENTIALS"
      pattern: "\\$\\{\\{ secrets\\.BUTLER_CREDENTIALS \\}\\}"
    - from: "checkout step"
      to: "Git LFS"
      via: "lfs: true parameter"
      pattern: "lfs: true"

user_setup:
  - service: github-remote
    why: "O repositório precisa estar no GitHub para o pipeline funcionar. O CI não pode ser testado localmente."
    steps:
      - task: "Criar repositório no GitHub"
        location: "https://github.com/new — nome sugerido: jogo-natalia (público para Actions grátis)"
      - task: "Adicionar remote e fazer push"
        command: "git -C /Users/renatojaf/jogo-natalia remote add origin https://github.com/SEU_USER/jogo-natalia.git && git push -u origin main"
    verification: "https://github.com/SEU_USER/jogo-natalia mostra os commits"
  - service: itch-io-placeholder
    why: "BUTLER_CREDENTIALS é necessário para o step de deploy. O workflow funciona sem ele (apenas export sem deploy) mas o step de deploy falha se o secret não existir."
    steps:
      - task: "Nota: deploy falha sem BUTLER_CREDENTIALS configurado"
        location: "O step de deploy usa 'if: startsWith(github.ref, refs/tags/v)' — só roda em tags. Para testar apenas o export (sem deploy), fazer push de uma branch, não uma tag."
      - task: "Quando pronto para deploy: criar conta em itch.io, criar página do jogo, gerar API key em itch.io/user/settings/api-keys"
        location: "https://itch.io/user/settings/api-keys"
      - task: "Adicionar secret BUTLER_CREDENTIALS no repositório GitHub"
        location: "https://github.com/SEU_USER/jogo-natalia/settings/secrets/actions/new"
    verification: "GitHub Actions job 'Web Export' fica verde em push de branch (sem deploy). Job 'Deploy to itch.io' só roda em tag v*."
---

<objective>
Criar o pipeline GitHub Actions (.github/workflows/export.yml) com 3 jobs paralelos de export (Web, Windows, macOS) e deploy condicional para itch.io via butler. O pipeline verifica exports em PRs e faz deploy completo em tags v*.

Purpose: CI/CD na Phase 0 garante que cada fase futura entrega um build testável desde o início — sem ter que configurar pipeline depois quando o projeto estiver complexo.

Output: .github/workflows/export.yml commitado. Pipeline verde no GitHub para push de branch (export sem deploy). Tag v0.0 pode disparar deploy completo quando BUTLER_CREDENTIALS estiver configurado.
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
@/Users/renatojaf/jogo-natalia/.planning/phases/00-funda-o/00-003-SUMMARY.md

<interfaces>
<!-- Padrão completo do export.yml (RESEARCH.md Pattern 4 + PATTERNS.md Pattern .github/workflows/export.yml) -->

Decisões travadas para o workflow (D-14 a D-18):
  D-14: trigger em tags 'v*' → export completo + deploy itch.io; PRs → apenas export
  D-15: container: image: barichello/godot-ci:4.4.1
  D-16: ITCH_USER placeholder="ITCH_USER"; secret=BUTLER_CREDENTIALS; jogo=destiny-tales-of-natalia
  D-17: checkout com lfs: true (obrigatório — sem isso assets chegam como ponteiros de 130 bytes)
  D-18: godot --headless --verbose --export-release (não --export)

Nome do executável de export do container: "godot" (já disponível no PATH dentro do container barichello/godot-ci)

Setup do template de export no container:
  mkdir -p ~/.local/share/godot/export_templates/
  mv /root/.local/share/godot/export_templates/${GODOT_VERSION}.stable ~/.local/share/godot/export_templates/${GODOT_VERSION}.stable

Import de assets antes do export (resolve Pitfall 2):
  godot --headless --editor --quit --path ${{ env.PROJECT_PATH }}

Canais itch.io (D-16):
  Web → CHANNEL: html5
  Windows → CHANNEL: windows
  macOS → CHANNEL: osx
</interfaces>
</context>

<tasks>

<task type="auto" tdd="false">
  <name>Task 1: Criar .github/workflows/export.yml</name>
  <files>.github/workflows/export.yml</files>
  <read_first>
    /Users/renatojaf/jogo-natalia/.planning/phases/00-funda-o/00-PATTERNS.md (seção ".github/workflows/export.yml" — padrão completo)
    /Users/renatojaf/jogo-natalia/.planning/phases/00-funda-o/00-CONTEXT.md (decisões D-14, D-15, D-16, D-17, D-18)
    /Users/renatojaf/jogo-natalia/.planning/phases/00-funda-o/00-RESEARCH.md (seção "Pitfall 2: godot --headless falha sem .godot/ importado" e Security Domain)
  </read_first>
  <action>
    Criar /Users/renatojaf/jogo-natalia/.github/workflows/export.yml.

    O workflow tem três jobs paralelos (export-web, export-windows, export-macos). Cada job:
    - Roda em ubuntu-latest com container barichello/godot-ci:4.4.1 (per D-15)
    - Faz checkout com lfs: true (per D-17 — NUNCA omitir)
    - Move templates de export de /root/.local/share/... para ~/.local/share/... (padrão do godot-ci)
    - Roda import de assets: godot --headless --editor --quit --path ${{ env.PROJECT_PATH }} (resolve Pitfall 2)
    - Cria pasta de destino com mkdir -p
    - Roda export: godot --headless --verbose --export-release "NOME_PRESET" caminho/arquivo (per D-18)
    - Upload artifact com actions/upload-artifact@v4
    - Step de deploy com if: startsWith(github.ref, 'refs/tags/v') usando manleydev/butler-publish-itchio-action@master (per D-14, D-16)

    Env vars globais no topo do workflow:
      GODOT_VERSION: "4.4.1"
      EXPORT_NAME: "destiny-tales-of-natalia"
      PROJECT_PATH: "."

    Triggers (per D-14):
      push.tags: ['v*']
      pull_request.branches: ['main']

    Segurança obrigatória em todos os steps de deploy (per T-00-01):
      BUTLER_CREDENTIALS: ${{ secrets.BUTLER_CREDENTIALS }}  — sempre via secret, nunca hardcoded
      ITCH_USER: ITCH_USER  — placeholder per D-16
      ITCH_GAME: destiny-tales-of-natalia

    Nomes dos presets no comando export devem ser exatamente:
      "Web", "Windows Desktop", "macOS" — correspondendo ao export_presets.cfg

    Commitar após criar:
    git -C /Users/renatojaf/jogo-natalia add .github/workflows/export.yml
    git -C /Users/renatojaf/jogo-natalia commit -m "feat(00): add GitHub Actions CI/CD pipeline for Web/Windows/macOS export (D-14, D-15, D-16, D-17, D-18)"
  </action>
  <verify>
    <automated>
      cd /Users/renatojaf/jogo-natalia && grep "lfs: true" .github/workflows/export.yml | wc -l && grep -v '^[[:space:]]*#' .github/workflows/export.yml | grep "BUTLER_CREDENTIALS:" | grep -v "secrets\." | wc -l && grep "barichello/godot-ci:4.4.1" .github/workflows/export.yml && grep "export-release" .github/workflows/export.yml | grep -v "^[[:space:]]*#"
    </automated>
  </verify>
  <acceptance_criteria>
    - .github/workflows/export.yml existe
    - `grep "lfs: true" .github/workflows/export.yml | wc -l` retorna 3 (um por job)
    - O comando de verificação de BUTLER_CREDENTIALS hardcoded retorna 0 (nenhuma ocorrência sem secrets.)
    - `grep "barichello/godot-ci:4.4.1" .github/workflows/export.yml` retorna 3 linhas (uma por job)
    - `grep "export-release" .github/workflows/export.yml` retorna linhas com --headless --verbose --export-release
    - `grep 'refs/tags/v' .github/workflows/export.yml` retorna linhas com o filtro de tag nos steps de deploy
    - `grep '"Web"' .github/workflows/export.yml` retorna linha com --export-release "Web"
    - `grep '"Windows Desktop"' .github/workflows/export.yml` retorna linha de export
    - `grep '"macOS"' .github/workflows/export.yml` retorna linha de export
    - `git show --stat HEAD` mostra .github/workflows/export.yml no commit
  </acceptance_criteria>
</task>

<task type="checkpoint:human-action" gate="blocking">
  <name>Task 2: Fazer push para GitHub e verificar pipeline</name>
  <read_first>
    /Users/renatojaf/jogo-natalia/.github/workflows/export.yml
    /Users/renatojaf/jogo-natalia/.planning/phases/00-funda-o/00-CONTEXT.md (D-14, D-16)
  </read_first>
  <what-built>O executor criou e commitou o workflow. Agora o repositório precisa de um remote GitHub para que o pipeline seja acionado. Esta é uma ação manual porque requer autenticação no GitHub e criação de repositório.</what-built>
  <how-to-verify>
    1. Criar repositório no GitHub (se ainda não existir):
       Acessar https://github.com/new
       Nome: "jogo-natalia" (público para GitHub Actions gratuitas)
       Não inicializar com README (o repositório local já tem commits)

    2. Adicionar remote e fazer push:
       `git -C /Users/renatojaf/jogo-natalia remote add origin https://github.com/SEU_USUARIO/jogo-natalia.git`
       `git -C /Users/renatojaf/jogo-natalia push -u origin main`
       (substituir SEU_USUARIO pelo seu username do GitHub)

    3. Verificar pipeline no GitHub:
       Acessar https://github.com/SEU_USUARIO/jogo-natalia/actions
       Aguardar o job disparado pelo push (pull_request ou push para main)
       Os 3 jobs (Web Export, Windows Export, macOS Export) devem ficar verdes

    NOTA SOBRE DEPLOY: O step "Deploy to itch.io" vai aparecer como "skipped" nos jobs
    (porque o trigger é push para branch, não tag). Isso é correto — deploy só roda em tags v*.
    Se aparecer como "failed" em vez de "skipped", verificar o conteúdo do export.yml.

    NOTA SOBRE BUTLER_CREDENTIALS: O secret ainda não existe — o step de deploy vai ser
    "skipped" por causa do filtro `if: startsWith(github.ref, 'refs/tags/v')`, não por falta
    do secret. Se quiser testar o deploy completo, adicionar o secret e criar uma tag v0.0.
  </how-to-verify>
  <resume-signal>Digite "ci-verde" após confirmar que todos os 3 jobs de export ficaram verdes no GitHub Actions. Se algum job falhou, descreva o erro para correção.</resume-signal>
  <acceptance_criteria>
    - https://github.com/SEU_USUARIO/jogo-natalia existe e está acessível
    - GitHub Actions tab mostra um workflow run disparado
    - Jobs "Web Export", "Windows Export", "macOS Export" estão com status "success" (verde)
    - Step "Deploy to itch.io" dentro de cada job está com status "skipped" (não "failed")
    - Artifacts "web", "windows", "macos" estão disponíveis para download na run do Actions
  </acceptance_criteria>
</task>

<task type="checkpoint:human-action" gate="blocking">
  <name>Task 3: Criar tag v0.0 e verificar deploy completo (opcional — quando itch.io estiver pronto)</name>
  <read_first>
    /Users/renatojaf/jogo-natalia/.planning/phases/00-funda-o/00-CONTEXT.md (D-14, D-16)
    /Users/renatojaf/jogo-natalia/.github/workflows/export.yml
  </read_first>
  <what-built>Esta task é opcional mas completa o pipeline end-to-end. Se BUTLER_CREDENTIALS não estiver configurado, o step de deploy falha mas o export continua. O executor faz push da tag — o usuário verifica o resultado no GitHub.</what-built>
  <how-to-verify>
    PRÉ-REQUISITO (pode pular se não tiver itch.io ainda):
    Se quiser testar o deploy completo:
    1. Criar conta em https://itch.io se não tiver
    2. Criar página do jogo: https://itch.io/dashboard > Create new project
       Título: "Destiny — Tales of Natalia"
       URL: destiny-tales-of-natalia
    3. Gerar API key: https://itch.io/user/settings/api-keys
    4. Adicionar secret no GitHub:
       https://github.com/SEU_USUARIO/jogo-natalia/settings/secrets/actions/new
       Nome: BUTLER_CREDENTIALS
       Valor: a API key do itch.io
    5. Atualizar ITCH_USER no export.yml para seu username itch.io (substituir o placeholder "ITCH_USER")

    CRIAR A TAG v0.0:
    `git -C /Users/renatojaf/jogo-natalia tag v0.0`
    `git -C /Users/renatojaf/jogo-natalia push origin v0.0`

    Verificar no GitHub Actions:
    - Os 3 jobs de export ficam verdes
    - Os steps "Deploy to itch.io" ficam verdes (se BUTLER_CREDENTIALS configurado)
    - Ou ficam "failed" com erro de auth (se secret não configurado) — aceitável neste ponto

    Se não quiser configurar itch.io agora:
    Criar a tag v0.0 mesmo assim para confirmar que o trigger de tag funciona.
    Os jobs de export ficam verdes, os steps de deploy falham por falta de secret — isso é esperado.
  </how-to-verify>
  <resume-signal>Digite "tag-criada" após fazer push da tag v0.0 e verificar o resultado no GitHub Actions (export verde). Descreva se os steps de deploy ficaram "green" ou "failed" e por quê.</resume-signal>
  <acceptance_criteria>
    - `git -C /Users/renatojaf/jogo-natalia tag` mostra "v0.0"
    - GitHub Actions mostra uma run disparada pela tag v0.0
    - Jobs "Web Export", "Windows Export", "macOS Export" têm status "success" na run da tag
    - Artifacts gerados estão disponíveis para download
    - Se BUTLER_CREDENTIALS configurado: steps de deploy têm status "success" e o jogo aparece no itch.io
    - Se BUTLER_CREDENTIALS não configurado: steps de deploy têm status "failed" com erro de auth (aceitável — export funcionou)
  </acceptance_criteria>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| GitHub Actions runner → secrets | BUTLER_CREDENTIALS deve transitar apenas via secrets — nunca no YAML |
| export.yml → itch.io (deploy) | Deploy condicional em tags: garante que apenas builds intencionais vão para produção |
| repositório público → export.yml | O arquivo é público — credenciais hardcoded seriam expostas imediatamente |

## STRIDE Threat Register

| Threat ID | Category | Component | Disposition | Mitigation Plan |
|-----------|----------|-----------|-------------|-----------------|
| T-00-01 | Information Disclosure | BUTLER_CREDENTIALS em export.yml | mitigate | Task 1 verifica com grep que nenhuma ocorrência de "BUTLER_CREDENTIALS:" existe sem "secrets." na linha; se grep retorna > 0, é bloqueante |
| T-00-11 | Elevation of Privilege | Deploy acidental em push de branch (não tag) | mitigate | Todos os steps de deploy têm condição "if: startsWith(github.ref, 'refs/tags/v')"; Task 2 verifica que deploy ficou "skipped" (não "success") em push de branch |
| T-00-12 | Tampering | Assets LFS chegam como ponteiros no CI | mitigate | "lfs: true" em todos os 3 jobs verificado por grep retornando 3; falta de LFS no checkout causaria export com sprites faltando — falha visível |
| T-00-13 | Denial of Service | Versão errada do container godot-ci | mitigate | "barichello/godot-ci:4.4.1" especificado explicitamente (não :latest) — tag fixa garante paridade com Godot 4.4.1 local |
</threat_model>

<verification>
Após completar todos os tasks deste plano:

1. `grep "lfs: true" /Users/renatojaf/jogo-natalia/.github/workflows/export.yml | wc -l` retorna 3
2. Nenhuma ocorrência de BUTLER_CREDENTIALS sem "secrets." na linha do export.yml
3. `grep "barichello/godot-ci:4.4.1" /Users/renatojaf/jogo-natalia/.github/workflows/export.yml` retorna 3 linhas
4. GitHub Actions: jobs "Web Export", "Windows Export", "macOS Export" verdes
5. GitHub Actions: steps "Deploy to itch.io" em status "skipped" em push de branch (não "failed")
6. `git -C /Users/renatojaf/jogo-natalia log --oneline` mostra commit do export.yml
</verification>

<success_criteria>
.github/workflows/export.yml está commitado com 3 jobs paralelos de export. BUTLER_CREDENTIALS usa exclusivamente ${{ secrets.BUTLER_CREDENTIALS }}. Checkout usa lfs: true nos 3 jobs. Export usa --headless --export-release. Deploy é condicional em tags v*. GitHub Actions ficou verde para push de branch (export funcionou, deploy ficou skipped). Success Criteria 1 do ROADMAP confirmado via CI: pipeline exporta Web sem erro. Phase 0 completa.
</success_criteria>

<output>
Após completar, criar /Users/renatojaf/jogo-natalia/.planning/phases/00-funda-o/00-004-SUMMARY.md com:
- URL do repositório GitHub
- Confirmação de cada segurança: lfs: true (3 jobs), BUTLER_CREDENTIALS via secret, deploy condicional
- Status dos jobs no GitHub Actions (verde/vermelho)
- Se tag v0.0 foi criada e resultado do deploy
- Decisões D-14, D-15, D-16, D-17, D-18 implementadas
- Status final de todos os 4 Success Criteria do ROADMAP.md Phase 0
</output>
