from cutscenes.cutsceneWorld import CutsceneWorld

class CutsceneWorld1(CutsceneWorld):
    Id = 1

    def __init__(self, manager):
        super().__init__(manager, self.Id)
