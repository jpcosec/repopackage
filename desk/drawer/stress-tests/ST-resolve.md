# ST-resolve: rp resolve — dependency resolution

**Basado en:** UC-02

## Script

```bash
# 1. Help
rp resolve --help

# 2. Resolver sobre el proyecto actual (tiene compose.yaml con dependencias reales)
# Usar el compose.yaml de ejemplo que ya existe
cd /tmp/rp-test-resolve
cp /home/jp/proyectos/hum-ecosystem/tools/repopackage/compose.yaml .
cp /home/jp/proyectos/hum-ecosystem/tools/repopackage/compose.lock.yaml .
rp resolve

# 3. Inspeccionar compose.lock.yaml generado
cat compose.lock.yaml | head -30

# 4. Resolver donde no hay compose.yaml
cd /tmp && rp resolve

# 5. Resolver con compose.yaml que tiene URL de git inválida
cat > /tmp/rp-test-bad-url/compose.yaml << 'EOF'
name: test-project
url: https://github.com/nonexistent-org/nonexistent-repo.git
branch: main
uses: {}
EOF
cd /tmp/rp-test-bad-url
rp resolve 2>&1 || echo "Expected: git error"

# 6. Resolver con dependencia cíclica
cat > /tmp/rp-test-cycle/compose.yaml << 'EOF'
name: project-a
url: https://github.com/example/a.git
uses:
  b:
    url: https://github.com/example/b.git
    line: main
EOF
cat > /tmp/rp-test-cycle/compose-b.yaml << 'EOF'
name: project-b
url: https://github.com/example/b.git
uses:
  a:
    url: https://github.com/example/a.git
    line: main
EOF
cd /tmp/rp-test-cycle
# Nota: esto requiere que los repos existan o se mockeen
# Alternativa: verificar que detecta ciclos en el resolver
rp resolve 2>&1 || true

# 7. Resolve idempotency: misma entrada, misma salida
cp /tmp/rp-test-resolve/compose.yaml /tmp/rp-test-resolve/compose.yaml.bak
rm -f /tmp/rp-test-resolve/compose.lock.yaml
cd /tmp/rp-test-resolve
rp resolve
md5sum compose.lock.yaml > /tmp/lock1.md5
rp resolve
md5sum compose.lock.yaml > /tmp/lock2.md5
diff /tmp/lock1.md5 /tmp/lock2.md5 && echo "Idempotent: YES" || echo "Idempotent: NO"

# 8. Resolve con versión conflictiva (si el resolver soporta version constraints)
```

## Puntos de estrés

| Paso | Qué observar |
|------|-------------|
| 1 | ¿El help explica qué hace resolve? |
| 2 | ¿Output? ¿Muestra qué dependencias resolvió? |
| 3 | ¿El lockfile tiene estructura esperada? |
| 4 | ¿Error: "compose.yaml not found"? |
| 5 | ¿Error de git claro? |
| 6 | ¿Detección de ciclo? ¿Mensaje claro? |
| 7 | ¿Idempotente? ¿Timestamp en lockfile? |
| 8 | ¿Version conflict detectado? |

## Modos de fracaso

- Sin feedback de progreso (clonando, resolviendo)
- Lockfile no deterministico (distinto hash cada vez)
- Errores de git con traceback interno
- Ciclos detectados pero sin indicar el camino del ciclo
- Sin mensaje de error si falta compose.yaml
