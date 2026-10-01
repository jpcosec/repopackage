# ST-generate: rp generate — scan workspace for contracts

**Basado en:** UC-05

## Script

```bash
# 1. Help
rp generate --help

# 2. Generate sobre proyecto actual
cd /home/jp/proyectos/hum-ecosystem/tools/repopackage
rp generate

# 3. Generate sobre directorio sin workspace
cd /tmp && rp generate 2>&1

# 4. Generate output: ¿qué produce? ¿Archivos? ¿Stdout?
rp generate 2>&1
ls -la generated/ 2>/dev/null || echo "No generated/ dir"
ls -la out/ 2>/dev/null || echo "No out/ dir"

# 5. ¿Hay flag --output?
rp generate --output /tmp/rp-generated 2>&1 || echo "No --output flag"

# 6. ¿Generate requiere lockfile o workspace?
cd /home/jp/proyectos/hum-ecosystem/tools/repopackage
ls compose.lock.yaml 2>/dev/null && echo "lockfile exists" || echo "no lockfile"
```

## Puntos de estrés

| Paso | Qué observar |
|------|-------------|
| 1 | ¿El help explica qué genera? |
| 2 | ¿Output? ¿Dice qué encontró? |
| 3 | ¿Error claro? |
| 4 | ¿Produce archivos o solo stdout? ¿En qué directorio? |
| 5 | ¿Flag de output? |
| 6 | ¿Depende de lockfile? |

## Modos de fracaso

- No está claro qué produce `generate` (archivos? stdout? dónde?)
- Sin flag de output (siempre escribe al CWD)
- Mensajes de progreso insuficientes ("scanning... found X contracts")
- No hay flag `--dry-run`
