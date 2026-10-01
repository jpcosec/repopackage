# UC-05: Export and inspect capabilities

El usuario quiere saber qué exporta cada paquete en el ecosystem: qué comandos CLI ofrece, qué contratos expone, y qué procedimientos tiene disponibles.

## Pasos

1. Ejecutar `rp exports` sobre un proyecto resuelto
2. Filtrar exports por paquete o tipo (commands, contracts, procedures)
3. Inspeccionar el formato de output

## Preguntas de estrés

- ¿`rp exports` requiere lockfile o puede operar sobre el workspace?
- ¿El output muestra el nombre del paquete, versión, y capabilities?
- ¿Hay formato `--format json` para consumo programático?
- ¿Qué pasa si un paquete no declara exports?
- ¿Qué pasa si un contrato exportado no existe físicamente?
- ¿Los exports son discoverables desde `--help`?
