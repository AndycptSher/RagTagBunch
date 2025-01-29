
__all__ = ["raiseNotImplementedBy"]

def raiseNotImplementedBy(funcName: str, inst):
  if type(funcName) != str:
    raise TypeError(f"funcName should be str, not {type(funcName).__name__}")
  raise NotImplementedError(f"{funcName+' ' if funcName != str(None) else ''}Not Implemented by {type(inst).__name__}")

