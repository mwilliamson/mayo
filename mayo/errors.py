class MayoUserError(RuntimeError):
    pass

class UnrecognisedSourceControlSystem(MayoUserError):
    pass
