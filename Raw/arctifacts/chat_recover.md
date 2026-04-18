Sí, totalmente. Eso es más específico que “execution journal”: estás hablando de un prompt/runtime capture layer por agente.
Yo lo separaría en 3 niveles:
- 1. Agent Run Contract
  - qué queremos preservar de cualquier corrida
- 2. Capture Adapter
  - cómo rescatarlo desde cada herramienta concreta
- 3. Normalized Run Package
  - cómo lo guardamos en un formato común del workflow
Lo modelaría así:
Nueva idea
- no solo prompt rescue
- sino agent trace ingestion
Qué rescatar
- prompt enviado
- instrucciones activas
- contexto/pills inyectadas
- archivos de entrada
- salida final
- pasos observables del agente
- comandos ejecutados
- archivos tocados
- logs nativos de la herramienta
- metadata:
  - herramienta
  - versión/modelo
  - modo de ejecución (cli, api, interactive)
  - timestamps
  - exit status
Importante
- no intentar rescatar “chain of thought” privada/interna
- sí rescatar:
  - observable reasoning artifacts
  - logs
  - transcript
  - command traces
  - summaries intermedias si la herramienta las expone
Yo agregaría estos contratos/instrucciones:
- contracts/agent_run_contract.md
  - ya lo tienes, pero habría que expandirlo
- contracts/agent_capture_contract.md
  - define cómo una herramienta entrega evidencia cruda
- contracts/agent_adapter_contract.md
  - define cómo normalizamos capturas por tool
- instructions/prompt-rescue-instructions.md
  - ritual de rescate
- instructions/agent-capture-instructions.md
  - cómo ejecutar y capturar por agente
Y este layout:
runs/RUN-XXX/
  normalized/
    prompt.md
    context_snapshot.md
    journal.md
    result_manifest.json
    tool_metadata.json
  raw/
    tool_stdout.log
    tool_stderr.log
    native_transcript.*
    native_metadata.*
  adapters/
    capture_report.md
Y además un subnivel por agente si hace falta:
runs/RUN-XXX/raw/claude/
runs/RUN-XXX/raw/gemini/
runs/RUN-XXX/raw/opencode/
runs/RUN-XXX/raw/pi/
Adapter por herramienta
Cada tool tendría un adapter con estrategia distinta:
- Claude
  - transcript/session files si existen
  - stdout/stderr
  - prompt file
- Gemini
  - logs locales
  - transcript export
  - invocación CLI como gemini -p ...
- OpenCode
  - prompt de entrada
  - tool calls observables
  - outputs
- pi
  - si corre como pi -p "...", guardar:
    - comando exacto
    - stdout
    - stderr
    - archivos de contexto usados
Contrato del adapter
Algo así:
{
  "tool": "gemini",
  "mode": "cli",
  "invocation": "gemini -p ...",
  "raw_artifacts": [
    "runs/RUN-XXX/raw/gemini/stdout.log"
  ],
  "normalized_outputs": [
    "runs/RUN-XXX/normalized/prompt.md"
  ],
  "capture_gaps": [
    "no native step trace available"
  ]
}
Clasificación útil
- capturable
  - prompt
  - output
  - logs
  - command trace
  - touched files
  - timestamps
- semi-capturable
  - intermediate visible summaries
  - tool call traces
- non-capturable / should not require
  - hidden chain-of-thought
En el workflow
Esto encaja entre ejecución y evaluación:
- ejecución
  -> capture
  -> evaluation
  -> integration
O incluso como subritual de ejecución:
- EXECUTION TRACE RITUAL
  1. snapshot prompt/instructions/context
  2. run agent
  3. rescue native logs/transcripts
  4. normalize to run package
  5. attach evidence to task/evaluation
Mi recomendación concreta
Sí, falta eso, y es distinto de solo execution_journal.
Yo agregaría:
1. contracts/agent_capture_contract.md
2. contracts/agent_adapter_contract.md
3. instructions/prompt-rescue-instructions.md
4. instructions/agent-capture-instructions.md
Y en ontología:
- agent tool
- capture mode
- run package
- raw trace
- normalized trace
Si quieres, te lo escribo ahora mismo dentro de dev_tools/workflow/ y además dejo una propuesta de adapters para:
- claude
- gemini
- opencode
- pi
