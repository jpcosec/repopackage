# Turn 010 - assistant

- Source: `Talk.md`
- Speaker: `assistant`

Fragmento de código
@startuml
skinparam monochrome true
skinparam shadowing false
skinparam classAttributeIconSize 0

abstract class ComposableUnit {
  + git_repository
  + tests
}

class LocalTraits {
  + scope: internal
  + formatting
  + test_runner
}

class IntegrationContract {
  + scope: external
  + exports
  + consumes
  + schemas
}

class Repopackage {
  + git_history
}

class CentralLine {
  + branch: main (default clone)
  + status: canonical
}

class DevelopmentLine {
  + branch: main (contextual)
  + target_project
}

class Project {
  + proprietary_code
}

class CompositionIndex {
  + lock_state
}

class FocusWorktree {
  + target_package
  + mock_ecosystem
}

' Herencia corregida
Repopackage -up-|> ComposableUnit
Project -up-|> Repopackage

' Componentes base
ComposableUnit *-- "1" IntegrationContract : reglas hacia afuera
ComposableUnit *-- "1" LocalTraits : reglas hacia adentro

' Gestión de historia y ramas
Repopackage *-- "1" CentralLine : main global
Repopackage *-- "0..*" DevelopmentLine : mains por proyecto

' Lógica de ensamblaje
Project *-- "1" CompositionIndex
CompositionIndex --> "1..*" Repopackage : compone >
CompositionIndex ..> DevelopmentLine : apunta a
CompositionIndex ..> CentralLine : apunta a

' Entornos aislados
FocusWorktree ..> Repopackage : aísla >
FocusWorktree ..> Project : mockea ecosistema de >

@enduml
Jerarquía de herencia rectificada: Project ahora hereda directamente de Repopackage. Todo Project es funcionalmente un Repopackage, pero añade la capacidad de ensamblaje.

Composición de ComposableUnit: IntegrationContract (interfaz pública) y LocalTraits (implementación interna) pertenecen estrictamente a la abstracción base.

Gestión de líneas base:

CentralLine se define como la rama principal canónica obtenida por defecto al clonar el repositorio.

DevelopmentLine representa cada variante de la rama main atada al contexto de un Project específico.

Índice de composición: CompositionIndex pertenece exclusivamente a Project y establece los punteros exactos hacia las líneas (CentralLine o DevelopmentLine) de los Repopackages dependientes.
