# UX stress-test methodology (repopackage)

## Qué es

Un UX stress-test es una exploración sistemática de la interfaz CLI desde la perspectiva de un usuario. No busca "encuentra bugs en el código" sino "encuentra dónde la experiencia se rompe, confunde o contradice el modelo mental que el usuario construyó".

## Principios

1. **Read-only.** No se edita ningún archivo. No se modifica el sistema bajo test. Solo se ejecutan comandos y se observa.
2. **El usuario no sabe lo que sabe el desarrollador.** El test asume que el usuario no leyó el código fuente. Solo conoce `--help`, la documentación superficial, y su intuición.
3. **Modelo mental primero.** Cada test se basa en una `use-case` narrativa (UC-XX) que describe qué quiere lograr el usuario. El test verifica si el sistema lo deja lograr eso sin fricción.
4. **Anchor en atoms.** Si `atom-repopackage.md` dice "repopackage manage composable units with typed integration contracts", el test verifica: ¿el CLI expresa eso claramente? ¿O faltan conceptos? ¿O hay comandos que contradicen el modelo?
5. **Fricción es el hallazgo.** Un error con traceback es un hallazgo. Un comando que existe pero se comporta distinto a lo esperado es un hallazgo. Un output silencioso donde debería haber feedback es un hallazgo. Una inconsistencia entre formatos de salida es un hallazgo.

## Estructura de un test

Cada test vive en `desk/drawer/stress-tests/st-XX-nombre.md` y contiene:

```markdown
# ST-XX: Nombre

**Basado en:** UC-XX

## Script

Secuencia de comandos CLI que el usuario ejecuta. Textual, uno por línea.
Incluye casos felices, casos borde, y casos de error.

## Puntos de estrés

Tabla: por cada paso del script, qué observar.
No es "funciona o no funciona". Es "el output es claro?",
"el error sugiere qué hacer?", "el usuario queda en un estado conocido?".

## Modos de fracaso

Lista de formas en que la experiencia se rompe.
```

## Cómo se ejecuta

1. Elegir un ST basado en un UC
2. Preparar setup si hace falta (crear test fixture, compose.yaml)
3. Ejecutar el script manualmente o mediante subagente
4. **Observar**, no juzgar. Anotar outputs textuales, exit codes, comportamientos sorprendentes
5. Escribir hallazgos en `findings/round-NN-descripcion.md`

## Qué observar en cada comando

| Dimensión | Preguntas |
|---|---|
| **Discoverability** | ¿El comando aparece en `--help`? ¿Su nombre es obvio? ¿Hay `rp` y `repopackage` ambos? |
| **Error messages** | ¿El error es para un humano o para un desarrollador? ¿Muestra traceback interno o mensaje semántico? ¿Sugiere qué hacer? |
| **Exit codes** | ¿0 para éxito, 1 para error manejado, 2 para argparse? |
| **Silent failures** | ¿Hay comandos que devuelven 0 sin output cuando deberían haber fallado? |
| **Consistency** | ¿Subcomandos similares (validate vs status vs resolve) se comportan igual? |
| **Naming** | ¿Los nombres de subcomandos siguen un patrón? ¿init/resolve/sync son secuenciales? |
| **State** | ¿El comando deja al usuario en un estado conocido? ¿Produce archivos? ¿Modifica compose.yaml/lock.yaml? |
| **Output** | ¿El output es scrolleable? ¿Tiene estructura (tablas, columnas)? |
| **Edge cases** | ¿compose.yaml con ciclos, versiones conflictivas, repos inexistentes, git errors? |
| **CI readiness** | ¿Se puede pipear? ¿Hay `--format json`? ¿Colores ANSI? |

## Cobertura esperada

Cada superficie del CLI debe tener al menos un ST:

| Superficie | ST asociado |
|---|---|
| `rp init` | ST-init |
| `rp resolve` | ST-resolve |
| `rp sync` | ST-sync |
| `rp validate` | ST-validate |
| `rp status` | ST-status |
| `rp generate` | ST-generate |
| `rp graph` | ST-graph |
| `rp exports` | ST-exports |
| compose.yaml format y parsing | ST-compose |
| Lockfile format (compose.lock.yaml) | ST-lockfile |
| Edge cases (deps cíclicas, version conflict, git) | ST-edge-cases |
| Entry points (rp vs repopackage vs python -m) | ST-entrypoints |
| Python API | ST-api |

## Lo que NO es un UX stress-test

- No es un test unitario
- No es un test de integración
- No es un test de regresión
- No es una auditoría de seguridad
- No es una revisión de código
