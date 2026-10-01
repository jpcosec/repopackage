# ST-pipeline: End-to-end flow init → resolve → sync → validate

**Basado en:** UC-01, UC-02, UC-03, UC-06

## Script

```bash
# 1. Init new project
mkdir -p /tmp/rp-test-pipeline-e2e
cd /tmp/rp-test-pipeline-e2e
rp init
echo "Exit: $?"

# 2. Inspect generated compose.yaml
cat compose.yaml
echo "Exit: $?"

# 3. Resolve (no deps — standalone project)
rp resolve
echo "Exit: $?"
ls -la compose.lock.yaml 2>&1

# 4. Validate after resolve
rp validate
echo "Exit: $?"

# 5. Sync (should succeed or give helpful message)
rp sync 2>&1
echo "Exit: $?"

# 6. Status
rp status
echo "Exit: $?"

# 7. Generate (should find 0 contracts or scan workspace)
rp generate
echo "Exit: $?"

# 8. Graph (should show single node)
rp graph
echo "Exit: $?"

# 9. Exports
rp exports
echo "Exit: $?"

# 10. Pipeline with actual deps (uses compose.yaml with known deps)
# Use the project's own compose.yaml if dummy repos exist
if [ -d /tmp/dummy_repos ]; then
  echo "--- Testing with real compose.yaml ---"
  cd /tmp/rp-test-pipeline-e2e
  cp /home/jp/proyectos/hum-ecosystem/tools/repopackage/compose.yaml .
  cp /home/jp/proyectos/hum-ecosystem/tools/repopackage/compose.lock.yaml .
  rp resolve
  echo "Exit: $?"
  rp validate
  echo "Exit: $?"
fi

# 11. Pipeline cleanup: init → resolve twice (idempotency)
mkdir -p /tmp/rp-test-pipeline-idem
cd /tmp/rp-test-pipeline-idem
rp init
rp resolve
LOCK1_MD5=$(md5sum compose.lock.yaml 2>/dev/null || echo "no-lockfile")
rp resolve
LOCK2_MD5=$(md5sum compose.lock.yaml 2>/dev/null || echo "no-lockfile")
if [ "$LOCK1_MD5" = "$LOCK2_MD5" ]; then
  echo "Pipeline idempotent: YES"
else
  echo "Pipeline idempotent: NO"
  echo "  Run 1: $LOCK1_MD5"
  echo "  Run 2: $LOCK2_MD5"
fi

# 12. Pipeline break: init → validate (without resolve)
mkdir -p /tmp/rp-test-pipeline-noresolve
cd /tmp/rp-test-pipeline-noresolve
rp init
rp validate
echo "Exit: $?"
```

## Puntos de estrés

| Paso | Qué observar |
|------|-------------|
| 1 | ¿Init produce compose.yaml? ¿Feedback? |
| 2 | ¿compose.yaml tiene estructura válida? |
| 3 | ¿Resolve produce lockfile? (RP-06) |
| 4 | ¿Validate pasa después de resolve? |
| 5 | ¿Sync funciona o da error claro? |
| 6 | ¿Status muestra estado OK? |
| 7 | ¿Generate encuentra 0 contracts? |
| 8 | ¿Graph muestra un nodo? |
| 9 | ¿Exports muestra algo? |
| 10 | ¿Pipeline con deps reales funciona? |
| 11 | ¿Pipeline es idempotente? |
| 12 | ¿Validate sin resolve da error claro? |

## Modos de fracaso

- Pipeline se rompe en cualquier paso intermedio
- Resolve no produce lockfile pero dice éxito (RP-06)
- Validate pasa sin lockfile
- Sync depende de Google Repo tool y falla sin ella
- Status muestra estado incorrecto después de pipeline exitoso
- Pipeline no es idempotente (segunda ejecución produce distinto resultado)
- No hay un comando "one-shot" para todo el pipeline
