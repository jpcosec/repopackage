# Turn 006 - assistant

- Source: `Talk.md`
- Speaker: `assistant`

Fragmento de código
@startuml
skinparam componentStyle rectangle
skinparam monochrome true
skinparam shadowing false

component "main-project\n<<Project>>" as main {

    component "Lógica Propia" as main_logic

    component "diagnostics-platform\n<<Project / Repopackage>>" as diag {

        () "Integration Contract\n(Diagnostics.v1)" as diag_contract
        diag_contract -down- diag

        component "code-quality-auditor\n<<Repopackage>>" as auditor
        component "testing-engine\n<<Repopackage>>" as testing
        component "task-context-engine\n<<Repopackage>>" as task_context

        auditor --> task_context : usa
        testing --> task_context : usa
    }

    component "ui-kit\n<<Repopackage>>" as ui {
        () "Integration Contract\n(ComponentRegistry.v1)" as ui_contract
        ui_contract -up- ui
    }

    main_logic --> diag_contract : consume
    main_logic --> ui_contract : consume
}

@enduml
Sintaxis de anidamiento: Se usa component Contenedor { component Contenido } para representar la recursividad topológica (un project contiene repopackages).

Contratos expuestos: Se utiliza la notación de interfaz (()) anclada a los bordes del componente para representar el Integration Contract visible hacia el exterior.

Aislamiento: Las dependencias internas (ej. auditor hacia task_context) ocurren exclusivamente dentro del contexto (Composition Index) de diagnostics-platform, ocultando esta complejidad a main-project.

Dualidad de rol: diagnostics-platform encapsula lógica de composición (comportamiento Project), pero expone un contrato único hacia el nivel superior (comportamiento Repopackage).
