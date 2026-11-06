from pydantic import BaseModel


class TaskCreate(BaseModel):
    title: str
    description: str = ""
    completed: bool = False
    
class TaskPut(BaseModel):
    title: str
    description: str = ""
    completed: bool = False
    
    
    
class TaskPatch(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None