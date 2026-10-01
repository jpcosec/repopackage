# ST-status: rp status — workspace sync status

**Basado en:** UC-03

## Script

```bash
# 1. Help
rp status --help

# 2. Status sobre el proyecto actual
cd /home/jp/proyectos/hum-ecosystem/tools/repopackage
rp status

# 3. Status sobre directorio sin workspace
cd /tmp && rp status

# 4. Status sobre directorio con lockfile pero sin workspace
cd /tmp/rp-test-validate 2>/dev/null || mkdir -p /tmp/rp-test-validate
cp /home/jp/proyectos/hum-ecosystem/tools/repopackage/compose.lock.yaml /tmp/rp-test-validate/ 2>/dev/null
cd /tmp/rp-test-validate
rp status

# 5. Status output redirection
rp status > /tmp/rp-status-output.txt 2>&1
cat /tmp/rp-status-output.txt

# 6. ¿Hay flag --format json?
rp status --format json 2>&1 || echo "No --format flag"

# 7. Comparar status con validate: ¿misma info?
cd /home/jp/proyectos/hum-ecosystem/tools/repopackage
rp status 2>&1
echo "---"
rp validate 2>&1
```

## Puntos de estrés

| Paso | Qué observar |
|------|-------------|
| 1 | ¿El help explica qué muestra status? |
| 2 | ¿Muestra cada paquete con su estado? |
| 3 | ¿Error claro? |
| 4 | ¿Detecta que falta el workspace? |
| 5 | ¿Output estructurado? |
| 6 | ¿Hay formato machine-parseable? |
| 7 | ¿Status y Validate muestran información diferente? |

## Modos de fracaso

- Status no da información útil por paquete (solo "ok" o "not ok")
- Sin diferenciar entre "not synced", "wrong commit", "dirty"
- Output no estructurado (no se puede pipear a grep/awk)
- Status y validate redundantes (misma información, distinto comando)
