
from typing import TypedDict


class PlannerState(TypedDict):
    original_input: str     
    subtasks: str             
    classification: str       
    priority: str             
    smart_plan: str           