# Turn 008 - assistant

- Source: `Talk.md`
- Speaker: `assistant`

Fragmento de código
@startuml
skinparam componentStyle rectangle
skinparam monochrome true
skinparam shadowing false

component "Composable Unit: main-project\n<<Rol: Project>>" as main_project {

    component "Project Local Code" as local_code

    component "Composition Index (main)" as ci_main {

        component "Composable Unit: diagnostics-platform\n<<Rol: Project + Repopackage>>" as diagnostics_platform {

            interface "Integration Contract\n(Exports)" as contract_diag

            component "Composition Index (diagnostics)" as ci_diag {

                component "code-quality-auditor\n<<Rol: Repopackage>>" as auditor
                component "testing-engine\n<<Rol: Repopackage>>" as testing
                component "task-context-engine\n<<Rol: Repopackage>>" as task_context

                auditor ..> task_context : consumes
                testing ..> task_context : consumes
            }

            contract_diag -down- ci_diag
        }

        component "Composable Unit: ui-kit\n<<Rol: Repopackage>>" as ui_kit {
            interface "Integration Contract" as contract_ui
        }
    }

    local_code ..> contract_diag : consumes
    local_code ..> contract_ui : consumes
}
@enduml
PlantUML nativo: El código anterior y este son sintaxis válida de PlantUML. plainuml no existe como lenguaje, se asume como un error tipográfico de PlantUML.

Jerarquía estructural: Se utiliza la envoltura component A { component B } repetidamente para demostrar cómo el sistema es puramente recursivo.

Aislamiento de índices: Cada nivel ensamblador (main-project, diagnostics-platform) posee su propio contenedor lógico (Composition Index), aislando el subgrafo de dependencias de sus repopackages internos.

Interfaces explícitas: Las dependencias de nivel superior solo interactúan con la interfaz (Integration Contract), ignorando la complejidad del Composition Index anidado.

Volvamos a este dibujo que hiciste antes

@startuml

skinparam monochrome true

skinparam shadowing false

skinparam classAttributeIconSize 0

abstract class ComposableUnit {

  + git_repository

  + history

  + tests

}

class Repopackage {

  + role: reusable_module

}

class Project {

  + role: assembler

  + proprietary_code

}

class IntegrationContract {

  + exports

  + consumes

  + schemas

  + compatibility_rules

}

class LocalTraits {

  + formatter

  + test_runner

  + docs_style

}

class CentralLine {

  + branch: main

  + version: canonical

}

class DevelopmentLine {

  + branch: contextual

  + base_commit

  + integration_status

}

class CompositionIndex {

  + package_refs

  + branches

  + exact_commits

}

class FocusWorktree {

  + target_package

  + mock_ecosystem

}

Repopackage -up-|> ComposableUnit

Project -up-|> ComposableUnit

ComposableUnit *-- "1" IntegrationContract

ComposableUnit *-- "1" LocalTraits

Repopackage *-- "1" CentralLine

Repopackage *-- "0..*" DevelopmentLine

Project *-- "1" CompositionIndex

CompositionIndex --> "1..*" DevelopmentLine : resolves to (lock)

CompositionIndex --> "1..*" CentralLine : resolves to (lock)

Project "0..*" o-- "1..*" Repopackage : uses >

Repopackage "0..*" o-- "0..*" Repopackage : uses >

Project ..> Repopackage : can act as >

FocusWorktree ..> Repopackage : isolates >

FocusWorktree ..> Project : mocks context of >

note bottom of ComposableUnit

  Nodos en un Composition Graph

end note

@enduml
