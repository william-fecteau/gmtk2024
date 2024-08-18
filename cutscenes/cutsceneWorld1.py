from cutscenes.cutsceneWorld import CutsceneWorld
from cutscenes.cutsceneWorld0 import CutsceneWorld0

class CutsceneWorld1(CutsceneWorld):
    def __init__(self, manager):
        super().__init__(manager, 1)

    def GetPreviousCutscene(self):
        return CutsceneWorld0(self.manager)

    def GetScalePercent(self, initialScale: float, minScale: float):
        if (initialScale == 0.5):
            initialScale = 1
            minScale = 0.5

        return super().GetScalePercent(initialScale, minScale)
