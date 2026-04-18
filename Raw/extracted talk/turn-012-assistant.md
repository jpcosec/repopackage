# Turn 012 - assistant

- Source: `Talk.md`
- Speaker: `assistant`

Fragmento de código
@startuml
skinparam monochrome true
skinparam shadowing false
skinparam classAttributeIconSize 0

' 1. Repopackage (Composable Unit fusionada)
class Repopackage {
  + git_repository
  + tests
}

' 2. Componentes internos de Repopackage
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

class CentralLine {
  + branch: main (default clone)
  + status: canonical
}

' 3. Project hereda de Repopackage
class Project {
  + proprietary_code
}

' 4. Instancias específicas de Project
class CompositionIndex {
  + lock_state
}

class DevelopmentLine {
  + branch: main (contextual)
  + base_commit
}

' Herencia
Project -up-|> Repopackage

' Relaciones estructurales del Repopackage
Repopackage *-- "1" IntegrationContract : expone >
Repopackage *-- "1" LocalTraits : rige >
Repopackage *-- "1" CentralLine : versión global >

' Relaciones estructurales del Project
Project *-- "1" CompositionIndex : gestiona >
Project *-- "0..*" DevelopmentLine : hospeda >

' Resolución de dependencias
CompositionIndex --> "1..*" Repopackage : compone >
CompositionIndex ..> CentralLine : puede apuntar a >
CompositionIndex ..> DevelopmentLine : puede apuntar a >
DevelopmentLine --> Repopackage : mutación contextual de >

@enduml
Cambios realizados:
Fusión Conceptual: ComposableUnit desaparece. Repopackage asume las responsabilidades base (git_repository, tests) y se convierte en el nodo fundamental del grafo.

Asignación al Nodo Base: IntegrationContract, LocalTraits y CentralLine ahora son atributos universales compuestos estáticamente (*--) dentro de cada Repopackage.

Asignación al Nodo Ensamblador: CompositionIndex y DevelopmentLine ahora pertenecen exclusivamente al dominio del Project.

Significado de DevelopmentLine: Una DevelopmentLine ya no vive "suelta" en el paquete original; se modela como un fork lógico hospedado/gestionado por el Project que lo requiere, apuntando de vuelta al Repopackage original.
