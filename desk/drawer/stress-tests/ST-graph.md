# ST-graph: rp graph — dependency graph visualization

**Basado en:** UC-04

## Script

```bash
# 1. Help
rp graph --help

# 2. Graph sobre proyecto con dependencias
cd /home/jp/proyectos/hum-ecosystem/tools/repopackage
rp graph

# 3. Redirigir output Mermaid a archivo
rp graph > /tmp/rp-graph.mmd 2>&1
cat /tmp/rp-graph.mmd

# 4. Verificar que el Mermaid es válido (sintaxis básica)
head -20 /tmp/rp-graph.mmd
# Debería empezar con graph TD o flowchart

# 5. Graph sobre directorio sin compose.yaml
cd /tmp && rp graph 2>&1

# 6. Graph sobre proyecto sin dependencias (solo proyecto raíz)
# Crear compose.yaml minimal sin uses
mkdir -p /tmp/rp-test-graph-empty
cat > /tmp/rp-test-graph-empty/compose.yaml << 'EOF'
name: standalone
url: https://github.com/example/standalone.git
branch: main
uses: {}
EOF
cd /tmp/rp-test-graph-empty
rp graph

# 7. ¿Hay flag --focus para filtrar por paquete?
rp graph --focus repopackage 2>&1 || echo "No --focus flag"

# 8. ¿Hay flag --depth?
rp graph --depth 1 2>&1 || echo "No --depth flag"

# 9. ¿Hay --format alternativo (dot, json)?
rp graph --format dot 2>&1 || echo "No --format flag"
```

## Puntos de estrés

| Paso | Qué observar |
|------|-------------|
| 1 | ¿El help explica formato de output? |
| 2 | ¿Mermaid válido? ¿Nombres de nodos legibles? |
| 3 | ¿Output se puede redirigir? |
| 4 | ¿Empieza con declaración válida de Mermaid? |
| 5 | ¿Error claro? |
| 6 | ¿Output con solo 1 nodo? |
| 7 | ¿Soporta filtrado? |
| 8 | ¿Soporta límite de profundidad? |
| 9 | ¿Formatos alternativos? |

## Modos de fracaso

- Mermaid inválido sintácticamente
- Sin labels en edges (no se ve tipo de dependencia)
- Sin opciones de filtrado (grafo grande = inútil)
- Nombres de nodos no descriptivos (URLs completas en vez de nombres)
- No se puede redirigir (output conmezclado con logs/stderr)
