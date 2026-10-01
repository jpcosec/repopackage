# ST-lockfile: compose.lock.yaml format and edge cases

**Basado en:** UC-02, UC-03

## Script

```bash
# Reference: copy a real lockfile
cp /home/jp/proyectos/hum-ecosystem/tools/repopackage/compose.lock.yaml /tmp/rp-test-lock-base.yaml

# 1. Lockfile con versión desconocida
mkdir -p /tmp/rp-test-lock-v1
cp /tmp/rp-test-lock-base.yaml /tmp/rp-test-lock-v1/compose.lock.yaml
cd /tmp/rp-test-lock-v1
python3 -c "
import yaml
lock = yaml.safe_load(open('compose.lock.yaml'))
lock['version'] = '99.99'
yaml.dump(lock, open('compose.lock.yaml', 'w'))
"
rp validate 2>&1
echo "Exit: $?"

# 2. Lockfile sin version field
mkdir -p /tmp/rp-test-lock-nover
cp /tmp/rp-test-lock-base.yaml /tmp/rp-test-lock-nover/compose.lock.yaml
cd /tmp/rp-test-lock-nover
python3 -c "
import yaml
lock = yaml.safe_load(open('compose.lock.yaml'))
del lock['version']
yaml.dump(lock, open('compose.lock.yaml', 'w'))
"
rp validate 2>&1
echo "Exit: $?"

# 3. Lockfile con commit hash inválido
mkdir -p /tmp/rp-test-lock-badcommit
cp /tmp/rp-test-lock-base.yaml /tmp/rp-test-lock-badcommit/compose.lock.yaml
cd /tmp/rp-test-lock-badcommit
python3 -c "
import yaml
lock = yaml.safe_load(open('compose.lock.yaml'))
key = list(lock['packages'].keys())[0]
lock['packages'][key]['commit'] = 'not-a-valid-sha'
yaml.dump(lock, open('compose.lock.yaml', 'w'))
"
rp validate 2>&1
echo "Exit: $?"

# 4. Lockfile completamente vacío
mkdir -p /tmp/rp-test-lock-empty
echo "" > /tmp/rp-test-lock-empty/compose.lock.yaml
cd /tmp/rp-test-lock-empty
rp validate 2>&1
echo "Exit: $?"
rp status 2>&1
echo "Exit: $?"

# 5. Lockfile con YAML válido pero estructura inesperada
mkdir -p /tmp/rp-test-lock-weird
cat > /tmp/rp-test-lock-weird/compose.lock.yaml << 'EOF'
packages: []
version: "1.0"
project: weird
EOF
cd /tmp/rp-test-lock-weird
rp validate 2>&1
echo "Exit: $?"

# 6. Lockfile con paquete duplicado
mkdir -p /tmp/rp-test-lock-dup
cp /tmp/rp-test-lock-base.yaml /tmp/rp-test-lock-dup/compose.lock.yaml
cd /tmp/rp-test-lock-dup
python3 -c "
import yaml
lock = yaml.safe_load(open('compose.lock.yaml'))
# Duplicate the first package with a different key
key = list(lock['packages'].keys())[0]
lock['packages']['duplicate-' + key] = lock['packages'][key].copy()
yaml.dump(lock, open('compose.lock.yaml', 'w'))
"
rp validate 2>&1
echo "Exit: $?"

# 7. Lockfile con manifest_hash incorrecto
mkdir -p /tmp/rp-test-lock-badhash
cp /tmp/rp-test-lock-base.yaml /tmp/rp-test-lock-badhash/compose.lock.yaml
cd /tmp/rp-test-lock-badhash
python3 -c "
import yaml
lock = yaml.safe_load(open('compose.lock.yaml'))
lock['manifest_hash'] = '0' * 64
yaml.dump(lock, open('compose.lock.yaml', 'w'))
"
rp validate 2>&1
echo "Exit: $?"

# 8. Lockfile con resolved_at en el futuro
mkdir -p /tmp/rp-test-lock-future
cp /tmp/rp-test-lock-base.yaml /tmp/rp-test-lock-future/compose.lock.yaml
cd /tmp/rp-test-lock-future
python3 -c "
import yaml
lock = yaml.safe_load(open('compose.lock.yaml'))
lock['resolved_at'] = '2099-12-31T23:59:59Z'
yaml.dump(lock, open('compose.lock.yaml', 'w'))
"
rp validate 2>&1
echo "Exit: $?"

# 9. Lockfile con encoding UTF-8 BOM
mkdir -p /tmp/rp-test-lock-bom
cp /tmp/rp-test-lock-base.yaml /tmp/rp-test-lock-bom/compose.lock.yaml
cd /tmp/rp-test-lock-bom
# Add UTF-8 BOM
python3 -c "
content = open('compose.lock.yaml', 'rb').read()
open('compose.lock.yaml', 'wb').write(b'\\xef\\xbb\\xbf' + content)
"
rp validate 2>&1
echo "Exit: $?"

# 10. ¿Lockfile puede ser pipeado/leído por herramientas externas?
python3 -c "
import yaml
try:
    lock = yaml.safe_load(open('/tmp/rp-test-lock-base.yaml'))
    print('YAML parseable: YES')
    print('Keys:', list(lock.keys()))
    print('Packages:', list(lock.get('packages', {}).keys()))
except Exception as e:
    print(f'YAML parseable: NO — {e}')
"
```

## Puntos de estrés

| Paso | Qué observar |
|------|-------------|
| 1 | ¿Versión desconocida = warning o error? |
| 2 | ¿Version field es requerido? |
| 3 | ¿SHA inválido detectado? |
| 4 | ¿Lockfile vacío = error claro? |
| 5 | ¿Estructura inesperada validada? |
| 6 | ¿Paquetes duplicados detectados? |
| 7 | ¿manifest_hash verificado contra compose.yaml? |
| 8 | ¿resolved_at en futuro validado? |
| 9 | ¿BOM causa error de parsing? |
| 10 | ¿Lockfile es YAML estándar? |

## Modos de fracaso

- Lockfile sin validación de esquema (cualquier YAML pasa)
- Versión no checkeada (mayor backward compat = error)
- SHA inválido no detectado hasta sync
- Duplicados silenciosamente aceptados
- manifest_hash no verificado (pierde integridad)
- BOM rompe parser YAML sin mensaje claro
- Lockfile no es YAML estándar (usa ruamel.yaml features no compatibles)
