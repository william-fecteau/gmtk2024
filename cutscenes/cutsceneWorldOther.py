from cutscenes.cutsceneWorld import CutsceneWorld
from cutscenes.cutsceneWorld1 import CutsceneWorld1

class CutsceneWorldOther(CutsceneWorld):
    def __init__(self, manager, id):
        super().__init__(manager, id)
        self.id = id

    def GetPreviousCutscene(self):
        if (self.id == 2):
            return CutsceneWorld1(self.manager)

        return CutsceneWorldOther(self.manager, self.id - 1)
