# Turn 039 - assistant

- Source: `Talk.md`
- Speaker: `assistant`

Las pruebas End-to-End (E2E) en esta arquitectura no pertenecen a un repopackage individual, sino que son propiedad exclusiva del Project (el nodo ensamblador) o de un repositorio dedicado a QA que actúe como un Project.

Aquí te explico cómo se estructura y ejecuta:

1. Topología del Test E2E
Un test E2E evalúa el grafo completo ya resuelto y materializado.

El Project Contract: El archivo compose.yaml del proyecto principal (ej. main-project) define el ecosistema completo (frontend, backend, motores, auditor, etc.).

El Entorno de Pruebas: Se crea un directorio dentro del Project dedicado a las pruebas E2E (ej. main-project/tests/e2e/).

Local Traits: El project.local.traits.yaml define cómo se levanta el entorno E2E.

YAML
# main-project/contracts/project.local.traits.yaml
test_runner:
  unit: "pytest tests/unit"
  e2e: "playwright test tests/e2e"
e2e_setup: "docker-compose up -d --build"
e2e_teardown: "docker-compose down"
2. El Flujo de Ejecución (El Orquestador)
Cuando ejecutas compose test --e2e a nivel de proyecto, el motor realiza lo siguiente:

1
Validación y Sincronización
Preparación del Estado
El orquestador verifica que el Composition Index (compose.lock.yaml) esté validado y que todos los repositorios estén materializados en el disco.

2
Inyección de Entorno
Setup
Ejecuta el comando definido en e2e_setup. Generalmente, esto levanta los servicios dependientes (bases de datos, colas) y ensambla los binarios o contenedores de los repopackages basándose en el código recién descargado.

3
Ejecución de Pruebas
Disparo E2E
Lanza el test_runner.e2e del proyecto. El framework de pruebas E2E (ej. Playwright, Cypress o un script de Python) interactúa con las APIs públicas o la UI del sistema ensamblado.

4
Desmontaje
Teardown
Al finalizar (independientemente de si pasó o falló), ejecuta e2e_teardown para limpiar recursos.

3. Manejo de Variantes Contextuales (Development Lines)
La mayor ventaja de esta arquitectura para E2E es la Prueba de Ramas Cruzadas (Cross-Branch Testing).

Imagina que estás modificando el paquete ui-kit en una rama feature/new-button y quieres ver si rompe el flujo E2E del proyecto principal.

No necesitas hacer merge a main del ui-kit. Simplemente alteras el compose.yaml del proyecto para apuntar a tu rama:

YAML
uses:
  ui-kit:
    url: git@...
    branch: feature/new-button # Cambias esto temporalmente
Luego corres compose sync y compose test --e2e. El orquestador descargará tu rama del ui-kit, la rama canónica de todo lo demás, levantará el ecosistema y correrá el E2E. Si pasa, sabes que tu ui-kit es seguro para hacer merge.
