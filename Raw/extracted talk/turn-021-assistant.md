# Turn 021 - assistant

- Source: `Talk.md`
- Speaker: `assistant`

1. Terminología
Repopackage: Unidad modular reutilizable, con repositorio Git propio, versión central, líneas de desarrollo contextuales y contrato de integración hacia el exterior.

Project: Unidad ensambladora. Utiliza múltiples repopackages, contiene código propietario, declara contratos de composición y gestiona el índice de resolución.

Composition Index: Estructura de datos (compose.lock.yaml) que actúa como puntero exacto. Define qué repositorios, en qué ramas (canónicas o contextuales) y en qué commits conforman el ecosistema actual.

Development Line: Rama temporal o divergente de un repopackage creada específicamente para satisfacer el contexto de un project.

Central Line: Rama canónica (main o versión estable central) de un repopackage.

2. Archivos Físicos
compose.yaml (Project Model)

YAML
kind: project
name: main-project

repo:
  url: git@github.com:org/main-project.git
  branch: main

uses:
  code-quality-auditor:
    url: git@github.com:org/code-quality-auditor.git
    path: packages/code-quality-auditor
    line: contextual
    branch: main-project/auditor-rules
    fallback: main

  ui-kit:
    url: git@github.com:org/ui-kit.git
    path: packages/ui-kit
    line: central
    branch: main

contracts:
  project: contracts/project.contract.yaml
compose.lock.yaml (Composition Index)

YAML
kind: composition_index
project: main-project
resolved_at: "2026-04-18T12:00:00Z"

repopackages:
  code-quality-auditor:
    branch: main-project/auditor-rules
    commit: abc123
    base_branch: main
    base_commit: 999aaa
    contract: contracts/code-quality-auditor.contract.yaml
    status: resolved

  ui-kit:
    branch: main
    commit: def456
    contract: contracts/ui-kit.contract.yaml
    status: resolved

compatibility:
  status: passed
  results:
    - package: code-quality-auditor
      status: passed
    - package: ui-kit
      status: passed
contracts/project.contract.yaml (Project Contract)

YAML
kind: project_contract
name: main-project

accepts:
  - interface: AuditReport
    version: v1
  - interface: ComponentRegistry
    version: v1

composition_rules:
  - from: code-quality-auditor.exports.AuditReport
    to: diagnostics-ui.consumes.AuditReport
    must_match_schema: true
contracts/integration.contract.yaml (Integration Contract)

YAML
kind: integration_contract
name: code-quality-auditor
version: 0.3.0

exports:
  - name: AuditReport
    schema: schemas/audit_report.v1.schema.json

consumes:
  - name: CodebaseSnapshot
    schema: schemas/codebase_snapshot.v1.schema.json

compatibility:
  requires:
    task-context-engine: ">=0.2.0 <0.4.0"
contracts/local.traits.yaml (Local Traits)

YAML
kind: local_traits
formatter: ruff
test_runner: pytest
docs_style: mkdocs
branch_strategy: trunk_based
preferred_language: python
3. CLI (Modelo Operacional)
Comando	Responsabilidad
compose init	Inicializa estructura base de proyecto y genera compose.yaml inicial.
compose resolve	Calcula topología, verifica dependencias estáticas y genera plan temporal.
compose sync	Traduce plan a manifest.xml, ejecuta repo sync y materializa el workspace.
compose validate	Inspecciona workspace materializado, evalúa esquemas JSON e interfaces contra el contrato. Escribe compose.lock.yaml.
compose status	Imprime matriz de estado: repos locales, ramas, commits y flags de compatibilidad.
compose graph	Exporta grafo relacional de dependencias y exportaciones/consumos.
compose test	Infiere runners desde local.traits.yaml y orquesta la suite de pruebas locales e integración.
compose promote	Inicia secuencia de merge/PR desde una development line hacia la central line de un paquete.
4. Resolver y Ciclo de Vida
1
Leer compose.yaml
Pre-sync
Carga el modelo del proyecto en memoria.

2
Resolver composición esperada
Cálculo de grafo
Genera nodos y aristas (consume/exporta). Detecta ciclos (emitir FAILED_CYCLE en fase MVP). Resuelve ramas dando prioridad a contextual branch sobre fallback.

3
Generar manifest.xml
Traducción
Crea el archivo XML para compatibilidad con la herramienta Google Repo.

4
Ejecutar repo sync
Materialización física
Descarga los repositorios a disco según el manifiesto generado.

5
Leer commits del workspace
Post-sync
Inspecciona hashes criptográficos reales del código materializado mediante llamadas a Git.

6
Cargar contratos materializados
Validación estática
Lee los integration.contract.yaml descargados en el workspace de cada paquete.

7
Validar compatibilidad algorítmica
Resolución de tipos
Cruza los contratos del proyecto y los paquetes contra los JSON Schemas correspondientes.

8
Escribir compose.lock.yaml
Fijación de estado
Persiste el resultado exacto, permitiendo reproducibilidad del ecosistema.

5. Google Repo Integration
La integración será encapsulada y se operará exclusivamente vía subprocess.

Python
# Generación de manifiesto y sincronización física
subprocess.run(["repo", "init", "-u", manifest_repo_url, "-m", "manifest.xml"], check=True)
subprocess.run(["repo", "sync", "-j8"], check=True)

# Inspección de estado físico (captura de hash)
result = subprocess.run(
    ["repo", "forall", "-c", "echo $REPO_PROJECT $(git rev-parse HEAD)"],
    capture_output=True,
    text=True
)
6. Validación
Contratos: Verificación en memoria de que los consumes de un paquete son satisfechos por los exports de otro, coincidiendo en nombre y rangos de versiones (>=, <).

Schemas: Verificación en disco local validando los archivos .schema.json apuntados en los contratos usando un parser estandarizado.

Tests: Ejecución en cascada. Depende de la validación estricta de contratos. Si falla la topología, se bloquea la ejecución del orquestador de pruebas.

7. Estados y Errores
Máquina de estados (Compatibility Result):

PENDING: Operación iniciada, a la espera del resolver.

RESOLVING: Construcción de grafo en proceso.

SYNCED: Repositorios físicos materializados correctamente mediante Google repo.

VALIDATING: Cruzando contratos y esquemas.

RESOLVED: Ecosistema íntegro y compatible. lockfile generado.

FAILED_REPO_SYNC: Falla de red, autenticación o manifiesto corrupto durante la llamada subprocess.

FAILED_MISSING_CONTRACT: Un repopackage exigido en uses carece de archivo YAML de contrato.

FAILED_CONTRACT_MISMATCH: Interfaces incompatibles o falta de proveedor para un consumes obligatorio.

FAILED_SCHEMA_VALIDATION: Formato de output no calza con el JSON Schema exigido por el consumidor.

FAILED_CYCLE: Dependencia circular detectada estáticamente en el grafo.

Política de Rollback:
Ante cualquier estado FAILED_* posterior a SYNCED:

Se aborta la escritura de compose.lock.yaml.

El sistema preserva el lockfile anterior intacto.

El workspace físico queda sucio (materializado). Corresponde al operador auditar los contratos locales de los repositorios fallidos o ejecutar compose sync --revert para volver al último índice válido.
