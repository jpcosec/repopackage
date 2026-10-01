# ST-exports: rp exports — enumerate package capabilities

**Basado en:** UC-05

## Script

```bash
# 1. Help
rp exports --help

# 2. Exports sobre el proyecto actual
cd /home/jp/proyectos/hum-ecosystem/tools/repopackage
rp exports

# 3. Exports output redirection
rp exports > /tmp/rp-exports.txt 2>&1
cat /tmp/rp-exports.txt

# 4. Exports sobre directorio sin lockfile
cd /tmp && rp exports 2>&1

# 5. Exports con --format json
rp exports --format json 2>&1 || echo "No --format flag"

# 6. Exports por paquete específico
rp exports --package repopackage 2>&1 || echo "No --package flag"

# 7. Exports sobre workspace recién clonado (sin resolver)
# Si el comando solo lee el lockfile, no necesita workspace
cd /home/jp/proyectos/hum-ecosystem/tools/repopackage
rp exports 2>&1
echo "---"
# Ver qué información da: commands? contracts? procedures?
```

## Puntos de estrés

| Paso | Qué observar |
|------|-------------|
| 1 | ¿El help explica qué lista exports? |
| 2 | ¿Muestra cada paquete con sus capabilities? |
| 3 | ¿Output estructurado? |
| 4 | ¿Error: lockfile required? |
| 5 | ¿Hay formato JSON? |
| 6 | ¿Filtro por paquete? |
| 7 | ¿Distingue entre commands, contracts, procedures? |

## Modos de fracaso

- Output monolítico sin separación por paquete
- Sin formato machine-parseable
- No distingue tipos de export (commands vs contracts vs procedures)
- Requiere workspace materializado cuando solo necesita el lockfile
- Packages sin exports no se listan (usuario no sabe si el scan falló o no hay exports)
