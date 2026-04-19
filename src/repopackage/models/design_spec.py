from typing import ClassVar
from repopackage.models.base import BaseArtifactModel

class DesignSpecModel(BaseArtifactModel):
    __template__: ClassVar[str] = """
# Design Spec: ⸢rev|name⸥

## Capa 0: Recolección (Contexto de Drawers)
⸢rev|layer_0⸥

## Capa 1: Microspec (El Mapa)
⸢rev|layer_1⸥

## Capa 2: Esqueleto (Las Fronteras)
⸢rev|layer_2⸥

## Capa 3: Pseudocode (El Cerebro)
⸢rev|layer_3⸥

## Capa 4: Patterns (El Estilo)
⸢rev|layer_4⸥

## Capa 5: Unit Tests (La Muralla)
⸢rev|layer_5⸥
""".strip()

    name: str
    layer_0: str
    layer_1: str
    layer_2: str
    layer_3: str
    layer_4: str
    layer_5: str
