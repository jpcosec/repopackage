# Turn 029 - assistant

- Source: `Talk.md`
- Speaker: `assistant`

Corrección sobre el formato de esquemas:
El formato físico de los archivos puede ser YAML (.schema.yaml) para aprovechar la legibilidad humana y comentarios. Sin embargo, el motor interno seguirá evaluando el estándar de validación "JSON Schema" (Draft 7 o 2020-12), ya que es el único protocolo con soporte matemático universal en todos los lenguajes.

Implementación de la capa de Interpretación (Brecha de Runtime):
Lo que describes resuelve la discrepancia entre el contrato estático (YAML) y el código de ejecución. La arquitectura debe incorporar un Módulo de Codegen (Generación de Código) y Contract Testing.

Este módulo operará de la siguiente manera:

Codegen Engine: Lee los .schema.yaml definidos en el Integration Contract y compila tipos seguros nativos para el lenguaje especificado en los Local Traits.

Python → Genera modelos Pydantic.

TypeScript → Genera esquemas Zod o interfaces TS.

Go → Genera Structs con tags.

Nota técnica: Para no reinventar la rueda, el motor debe usar librerías puente por debajo (como datamodel-code-generator para Python o quicktype para TS/Go).

Directorio Inmutable: El código autogenerado se deposita en una ruta estandarizada y bloqueada (ej. src/__generated__/contracts/). Está estrictamente prohibido editar este código a mano.

Contract Test Scaffolding: Además de los tipos, el motor genera fixtures y esqueletos de pruebas.

Genera un archivo temporal de test (ej. test_contract_compliance.py) que inyecta datos sintéticos (fuzzing) basados en el .schema.yaml hacia las funciones públicas del paquete.

Fuerza al desarrollador a mapear su lógica de negocio contra las entradas/salidas autogeneradas de Pydantic/Zod.

Actualización del Modelo Operacional
Se añade un nuevo comando al CLI para operar exclusivamente dentro del ciclo de desarrollo de un paquete individual:

Comando	Responsabilidad
compose generate	Ejecutado dentro de un repopackage. Lee sus esquemas YAML, verifica el preferred_language en local.traits.yaml, y sobrescribe el directorio __generated__ con los modelos de datos (Pydantic/Zod) y los tests templates.
Regla de Integridad Arquitectónica
El ciclo de vida del desarrollador cambia de Code-First a Contract-First:

El desarrollador altera el .schema.yaml.

Ejecuta compose generate.

El compilador de su lenguaje (o el linter) lanza errores (Type Errors) porque los modelos Pydantic/Zod generados ya no coinciden con su lógica interna.

El desarrollador corrige el código interno para satisfacer los nuevos tipos.

Los tests de contrato pasan. Se hace commit.
