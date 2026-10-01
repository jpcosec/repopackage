# ST-init: rp init — bootstrap a new project model

**Basado en:** UC-01

## Script

```bash
# 1. Help
rp init --help

# 2. Init en directorio temporal
mkdir -p /tmp/rp-test-init
cd /tmp/rp-test-init
rp init

# 3. Inspeccionar compose.yaml generado
cat compose.yaml

# 4. Init nuevamente (idempotencia)
rp init

# 5. Init en directorio sin permisos
mkdir -p /tmp/rp-test-noperm
chmod -w /tmp/rp-test-noperm
cd /tmp/rp-test-noperm
rp init 2>&1 || echo "Expected: permission error"

# 6. Init con repopackage (alias)
repopackage init

# 7. Diferencia entre "rp init" y "rp init ."
cd /tmp/rp-test-init
rm compose.yaml 2>/dev/null
rp init .

# 8. Init cuando ya existe compose.yaml con contenido
echo "# Custom content" > compose.yaml
rp init 2>&1 || echo "Expected: already exists error"
```

## Puntos de estrés

| Paso | Qué observar |
|------|-------------|
| 1 | ¿Muestra flags disponibles? |
| 2 | ¿Output? ¿Dice "created compose.yaml"? |
| 3 | ¿El YAML generado es válido? ¿Tiene estructura esperada? |
| 4 | ¿Error o idempotente? |
| 5 | ¿Error claro de permisos? |
| 6 | ¿Mismo comportamiento que rp? |
| 7 | ¿. vs sin path: mismo resultado? |
| 8 | ¿Error: "compose.yaml already exists"? |

## Modos de fracaso

- Sin feedback de qué archivo se creó
- compose.yaml generado inválido
- No idempotente (falla en segunda ejecución)
- `rp` y `repopackage` se comportan distinto
