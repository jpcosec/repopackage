# UC-04: Visualize dependency graph

El usuario quiere entender las relaciones entre los paquetes de su ecosystem: quién depende de quién, qué contratos se consumen, y cómo fluyen las dependencias.

## Pasos

1. Ejecutar `rp graph` sobre un proyecto resuelto
2. Inspeccionar el output Mermaid
3. Renderizar el Mermaid a una imagen o diagrama

## Preguntas de estrés

- ¿El output Mermaid es válido sintácticamente?
- ¿Los nombres de los nodos son legibles?
- ¿Las edges tienen labels (tipo de dependencia, versión)?
- ¿Hay opciones de filtrado (--focus, --depth)?
- ¿El output se puede redirigir a un archivo? (o solo stdout)
- ¿Hay alternativa a Mermaid (DOT, JSON)?
