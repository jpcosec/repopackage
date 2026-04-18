# Turn 019 - assistant

- Source: `Talk.md`
- Speaker: `assistant`

No, la descripción es estructuralmente válida pero operativamente insuficiente para iniciar el desarrollo del código. El diagrama define la topología del dominio (Data/Class Model), pero omite el comportamiento y los contratos de implementación.

Faltan los siguientes componentes arquitectónicos para programar el sistema:

Interfaces de Interacción (CLI/API): Ausencia de comandos de entrada, argumentos de terminal o firmas de métodos públicos (ej. compose init, compose validate, compose sync).

Algoritmos de Resolución (Dependency Resolver): No se especifica la lógica de grafos para validar compatibilidad entre project_contract y múltiples int_contract, ni cómo resolver conflictos cíclicos de dependencias.

Esquemas de Datos Físicos (Serialización): No se define el formato de persistencia en disco de los modelos (repopackage_model, project_model). Se requiere especificar si serán YAML, JSON, TOML y sus respectivos esquemas de validación estricta (ej. JSON Schema).

Protocolo de Integración con Google Repo: Falta definir si la comunicación con el componente Google repo será mediante llamadas a sistema (subprocess/CLI) o mediante manipulación directa de archivos (manifest.xml).

Flujos de Ejecución Temporales: El modelo estático no define el ciclo de vida. No está definido si el Composition Index se calcula antes o después de materializar el Repo Workspace.

Gestión de Estados y Excepciones: No se describen las transiciones de Compat Result (ej. PENDING, RESOLVED, FAILED_CONTRACT_MISMATCH) ni las políticas de rollback ante fallos en Git o Repo.

Solución técnica:
Para que la especificación sea programable, se debe expandir la documentación técnica incluyendo:

Esquemas de datos (YAML/JSON) para cada contrato.

Diagramas de secuencia o diagramas de flujo de actividad para las operaciones base (resolver, sincronizar, validar).

Especificación de la interfaz de línea de comandos (CLI) que orquestará el programa.

Te dijeron algo razonable. Tu UML actual responde:

¿Qué entidades existen y cómo se relacionan?

Pero todavía no responde:

¿Cómo se opera el sistema?

¿Qué archivos lee/escribe?

Qué comandos existen?

Qué pasa si falla?

Cómo se resuelve una composición?

Yo lo ordenaría en tres capas de especificación.

1. Modelo estático

Esto es lo que ya tienes.

Git

Google repo

Desarrollo propio

Project Model

Repopackage Model

Contracts

Composition Index

Compatibility Result

Sirve para definir el vocabulario.

Pero no basta para programar.

2. Modelo físico de datos

Aquí defines los archivos reales.

Yo usaría YAML, porque permite comentarios y es legible.

Estructura mínima:

compose.yaml # Project model

compose.lock.yaml # Composition index resuelto

contracts/

project.contract.yaml # Project contract

integration.contract.yaml # Si este project también se expone como paquete

repopackages/

auditor.package.yaml

ui.package.yaml

.repo/

manifest.xml # Google repo manifest

Ejemplo de compose.yaml:

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

Ejemplo de repopackage.contract.yaml:

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

Ejemplo de project.contract.yaml:

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

Ejemplo de compose.lock.yaml:

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

3. Modelo operacional

Aquí defines comandos.

MVP de CLI:

compose init

compose sync

compose resolve

compose validate

compose status

compose graph

compose test

compose promote

Con responsabilidades:

ComandoQué hacecompose initCrea estructura base del proyecto.compose syncGenera/usa manifest.xml y ejecuta repo sync.compose resolveCalcula qué branches/commits/contracts componen el sistema.compose validateValida contratos, schemas y compatibilidad.compose statusMuestra estado de repos, branches, commits y compatibilidad.compose graphConstruye grafo de dependencias.compose testEjecuta tests relevantes según traits/contratos.compose promoteAyuda a mover una variante contextual hacia la línea central.Flujo base

El ciclo mínimo debería ser:

flowchart TD

A["compose.yaml"] --> B["resolve dependencies"]

B --> C["generate repo manifest"]

C --> D["repo sync"]

D --> E["read workspace state"]

E --> F["load contracts"]

F --> G["validate compatibility"]

G --> H["write compose.lock.yaml"]

H --> I["run tests"]

I --> J["report result"]

La pregunta que te hicieron sobre el orden es clave.

Yo lo haría así:

1. Leer compose.yaml

2. Resolver composición esperada

3. Generar/actualizar manifest.xml

4. Ejecutar repo sync

5. Leer commits reales del workspace

6. Cargar contratos desde los repos materializados

7. Validar compatibilidad

8. Escribir compose.lock.yaml

O sea:

Composition Index se calcula en dos etapas:

pre-sync:

qué quiero materializar

post-sync:

qué quedó efectivamente materializado y si es válido

Integración con Google repo

Para el MVP, yo no tocaría internals de repo.

Usaría dos mecanismos:

1. generar manifest.xml

2. ejecutar repo por subprocess

Ejemplo conceptual:

subprocess.run(["repo", "init", "-u", manifest_repo, "-m", manifest_file])

subprocess.run(["repo", "sync"])

subprocess.run(["repo", "forall", "-c", "git rev-parse HEAD"])

Más adelante podrías manipular manifests de manera más fina, pero partiría simple.

Estados

Compatibility Result debería tener estados claros:

PENDING

RESOLVING

SYNCED

VALIDATING

RESOLVED

FAILED_REPO_SYNC

FAILED_MISSING_CONTRACT

FAILED_CONTRACT_MISMATCH

FAILED_SCHEMA_VALIDATION

FAILED_TESTS

FAILED_CYCLE

Ejemplo:

compatibility:

status: FAILED_CONTRACT_MISMATCH

errors:

- package: diagnostics-ui

consumes: AuditReport.v2

available: AuditReport.v1

producer: code-quality-auditor

Resolver

El resolver mínimo debería hacer esto:

input:

compose.yaml

project.contract.yaml

integration contracts disponibles

output:

composition plan

manifest.xml

compose.lock.yaml

Algoritmo básico:

1. Leer project uses.

2. Crear nodos del grafo.

3. Agregar edges por consumes/exports.

4. Detectar ciclos.

5. Para cada edge:

- buscar export compatible

- validar schema

- validar versión

6. Elegir branch:

- si hay contextual branch, usarla

- si no, usar central line

7. Emitir plan.

Ciclos:

No todo ciclo es malo.

Pero para el MVP yo sería estricto:

si A consume B y B consume A → FAILED_CYCLE

Más adelante puedes permitir ciclos solo si son de tipo runtime/plugin o si están declarados explícitamente.

Lo que habría que escribir ahora

El siguiente documento técnico debería tener esta estructura:

1. Terminología

- repopackage

- project

- composition index

- development line

- central line
