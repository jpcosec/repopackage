# Turn 009 - user

- Source: `Talk.md`
- Speaker: `user`

- Repopackage es lo mismo que composable unit, un repo package es un tipo composable unit

- Project  es un repopackage que compone al menos otro repopackage mas. Para esto usa un composition Index.

- Un repopackage tiene "historias" en git, ademas de los brancheos que puedan haber piensa en cada historia como el main ya de produccion de cada repopackage. Una development line es el main que tiene cada repopackage en cada proyecto distinto donde pueda estar. Pero, ademas de esto cada repopackage tiene un main central, que es cierta forma de main de todos los mains que puede tener en distintos proyectos y seria la que uno "baja" al hacer el clone desde git, esa es la centralLine.

- Local traits y integration contract son componentes de composable unit. Local traits son "reglas" dentro del repopackage para el repopackage mismo. Integration contract son reglas dentro del repopackage hacia afuera.
