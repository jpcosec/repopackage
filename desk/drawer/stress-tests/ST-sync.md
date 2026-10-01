# ST-sync: rp sync — materialize workspace

**Basado en:** UC-06

## Script

```bash
# 1. Help
rp sync --help

# 2. Sync sobre proyecto resuelto (con lockfile)
mkdir -p /tmp/rp-test-sync
cp /home/jp/proyectos/hum-ecosystem/tools/repopackage/compose.lock.yaml /tmp/rp-test-sync/
cp /home/jp/proyectos/hum-ecosystem/tools/repopackage/compose.yaml /tmp/rp-test-sync/
cd /tmp/rp-test-sync

# 3. Sync sobre directorio sin lockfile
cd /tmp/empty-dir
mkdir -p /tmp/empty-dir
rp sync 2>&1

# 4. ¿Sync tiene flag --force?
rp sync --force 2>&1 || echo "No --force flag"

# 5. ¿Sync muestra progreso?
# (clonando repo X, checkout commit Y)

# 6. ¿Qué pasa si ya existe el workspace? (idempotencia)
# Ejecutar sync dos veces

# 7. ¿Qué pasa si un repo está dirty?
# (modificar un archivo en el workspace y re-sync)

# 8. Sync requiere Google Repo tool? ¿O usa pygit2?
which repo 2>/dev/null && echo "Google Repo tool installed" || echo "Google Repo tool NOT installed"
python3 -c "import pygit2; print('pygit2 available')" 2>&1 || echo "pygit2 not available"
```

## Puntos de estrés

| Paso | Qué observar |
|------|-------------|
| 1 | ¿El help explica qué hace sync? |
| 2 | ¿Progreso? ¿Clona? ¿Checkout? |
| 3 | ¿Error: lockfile not found? |
| 4 | ¿Hay --force? |
| 5 | ¿Muestra cada repo? ¿Commit hash? |
| 6 | ¿Idempotente? |
| 7 | ¿Dirty workspace = error o warning? |
| 8 | ¿Depende de tool externa? |

## Modos de fracaso

- No hay feedback de progreso
- Cuelga si un repo es grande o inaccesible (sin timeout)
- Error confuso si Google Repo tool no está instalado
- Dirty workspace silenciosamente sobrescrito (pérdida de datos)
- Sync exitoso pero faltan archivos (no verifica post-sync)
