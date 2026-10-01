# ST-edge-cases: repopackage OS/IO edge cases

**Basado en:** UC-01, UC-02, UC-03

## Script

```bash
# 1. Directorio sin permisos de escritura
mkdir -p /tmp/rp-test-noperm
chmod -w /tmp/rp-test-noperm
cd /tmp/rp-test-noperm
rp init 2>&1
rp resolve 2>&1

# 2. Path traversal en urls de dependencias
cat > /tmp/rp-test-traversal/compose.yaml << 'EOF'
name: test
url: https://github.com/../../etc/passwd
branch: main
uses: {}
EOF
mkdir -p /tmp/rp-test-traversal
cd /tmp/rp-test-traversal
rp resolve 2>&1

# 3. Lockfile corrupto
echo "corrupted lockfile" > /tmp/rp-test-corrupt-lock/compose.lock.yaml
mkdir -p /tmp/rp-test-corrupt-lock
cd /tmp/rp-test-corrupt-lock
rp validate 2>&1
rp status 2>&1

# 4. Workspace con symlinks
mkdir -p /tmp/rp-test-symlinks
ln -s /nonexistent /tmp/rp-test-symlinks/broken-link
cd /tmp/rp-test-symlinks
rp validate 2>&1

# 5. Múltiples --format flag (si existe)
rp status --format json --format yaml 2>&1 || echo "Multiple format handling unclear"

# 6. Muy largo nombre de proyecto
mkdir -p /tmp/rp-test-long-name
LONG_NAME=$(python3 -c "print('p' * 1000)")
cat > /tmp/rp-test-long-name/compose.yaml << EOF
name: $LONG_NAME
url: https://github.com/example/test.git
branch: main
uses: {}
EOF
cd /tmp/rp-test-long-name
rp resolve 2>&1

# 7. Whitespace en paths
mkdir -p "/tmp/rp test spaces"
cd "/tmp/rp test spaces"
rp init 2>&1

# 8. Signal handling: Ctrl+C durante resolve largo
timeout 3 rp resolve 2>&1 || echo "timeout exit: $?"
```

## Puntos de estrés

| Paso | Qué observar |
|------|-------------|
| 1 | ¿Error de permisos claro? |
| 2 | ¿Path traversal detectado? |
| 3 | ¿Error: lockfile corrupto? |
| 4 | ¿Symlinks rotos? |
| 5 | ¿Múltiples formatos? |
| 6 | ¿Nombre muy largo? |
| 7 | ¿Espacios en path? |
| 8 | ¿Signal handling graceful? |

## Modos de fracaso

- Permisos: crash con traceback de Python
- Path traversal: no validado
- Lockfile corrupto: Pydantic traceback
- Signal handling: ctrl+c deja estado inconsistente
- Espacios en paths: comandos internos fallan
