# ST-compose: compose.yaml format and edge cases

**Basado en:** UC-01, UC-02

## Script

```bash
# 1. compose.yaml mínimo válido
mkdir -p /tmp/rp-test-compose
cat > /tmp/rp-test-compose/compose.yaml << 'EOF'
name: test-project
url: https://github.com/example/test.git
branch: main
uses: {}
EOF
cd /tmp/rp-test-compose
rp resolve 2>&1 || echo "resolve failed (expected: may need real repos)"

# 2. compose.yaml sin campos required
echo "name: incomplete" > /tmp/rp-test-compose-invalid/compose.yaml
mkdir -p /tmp/rp-test-compose-invalid
cd /tmp/rp-test-compose-invalid
rp resolve 2>&1

# 3. compose.yaml con YAML inválido
echo "invalid: yaml: :" > /tmp/rp-test-compose-bad/compose.yaml
mkdir -p /tmp/rp-test-compose-bad
cd /tmp/rp-test-compose-bad
rp resolve 2>&1

# 4. compose.yaml con dependencias sin URL
cat > /tmp/rp-test-compose-bad-dep/compose.yaml << 'EOF'
name: test
url: https://github.com/example/test.git
branch: main
uses:
  dep1:
    line: main
EOF
cd /tmp/rp-test-compose-bad-dep
rp resolve 2>&1

# 5. compose.yaml con tags desconocidos
cat > /tmp/rp-test-compose-extra/compose.yaml << 'EOF'
name: test
url: https://github.com/example/test.git
branch: main
uses: {}
unknown_field: should_not_be_here
EOF
cd /tmp/rp-test-compose-extra
rp resolve 2>&1

# 6. compose.yaml con encoding UTF-8 (ñ, emojis en nombre)
cat > /tmp/rp-test-compose-utf8/compose.yaml << 'EOF'
name: proyecto-ñoño-🎉
url: https://github.com/example/test.git
branch: main
uses: {}
EOF
cd /tmp/rp-test-compose-utf8
rp resolve 2>&1
```

## Puntos de estrés

| Paso | Qué observar |
|------|-------------|
| 1 | ¿El mínimo válido funciona? |
| 2 | ¿Error de validación claro? |
| 3 | ¿YAML parse error claro? |
| 4 | ¿Error: dependency missing required field? |
| 5 | ¿Tags desconocidos ignorados o error? |
| 6 | ¿UTF-8 en nombres? |

## Modos de fracaso

- Validación de compose.yaml no existe o es muy permisiva
- Errores de YAML parse con traceback
- Campos requeridos no documentados
- UTF-8 produce error de encoding en lugar de funcionar
