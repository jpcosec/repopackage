# ST-validate: rp validate — workspace integrity

**Basado en:** UC-03

## Script

```bash
# 1. Help
rp validate --help

# 2. Validate sobre workspace sincronizado (desde el proyecto repopackage mismo)
cd /home/jp/proyectos/hum-ecosystem/tools/repopackage
rp validate

# 3. Validate sobre directorio sin workspace
cd /tmp && rp validate

# 4. Validate sobre directorio con lockfile pero sin workspace
mkdir -p /tmp/rp-test-validate
cp /home/jp/proyectos/hum-ecosystem/tools/repopackage/compose.lock.yaml /tmp/rp-test-validate/
cd /tmp/rp-test-validate
rp validate

# 5. Validate cuando falta un contrato declarado
# (Modificar lockfile para que referencie un contrato inexistente)
cd /tmp/rp-test-validate
python3 -c "
import yaml
lock = yaml.safe_load(open('compose.lock.yaml'))
# Add a package that references a nonexistent contract
lock['packages'].append({
    'name': 'fake-package',
    'url': 'https://github.com/fake/fake.git',
    'commit': 'abc123',
    'exports': {'contracts': [{'name': 'nonexistent', 'schema_ref': 'nonexistent.schema.json'}]}
})
yaml.dump(lock, open('compose.lock.yaml', 'w'))
"
rp validate

# 6. Validate con exit code
rp validate 2>&1
echo "Exit code: $?"

# 7. Validate en modo batch (múltiples proyectos)
# Si existe --workspace flag
rp validate --workspace /tmp/rp-test-validate 2>&1 || echo "No --workspace flag"

# 8. Validate con commit mismatch
# (modificar un commit en lockfile)
cd /tmp/rp-test-validate
python3 -c "
import yaml
lock = yaml.safe_load(open('compose.lock.yaml'))
if lock.get('packages'):
    lock['packages'][0]['commit'] = '0000000000000000000000000000000000000000'
yaml.dump(lock, open('compose.lock.yaml', 'w'))
"
rp validate
```

## Puntos de estrés

| Paso | Qué observar |
|------|-------------|
| 1 | ¿El help explica qué verifica validate? |
| 2 | ¿Output? ¿Lista verificaciones? |
| 3 | ¿Error claro? |
| 4 | ¿Detecta que falta el workspace? |
| 5 | ¿Error claro para contrato faltante? |
| 6 | ¿Exit code correcto (0 si ok, 1 si falla)? |
| 7 | ¿Soporta --workspace flag? |
| 8 | ¿Commit mismatch reportado claramente? |

## Modos de fracaso

- Validate pasa silenciosamente cuando debería fallar
- Sin detalle de qué verificaciones se corrieron
- Error messages genéricos ("validation failed" sin detalle)
- No distingue entre "workspace no existe", "commit mismatch", y "contrato faltante"
