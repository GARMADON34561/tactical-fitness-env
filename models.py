from pydantic import Field
from openenv.core.env_server.types import Action, Observation, State

class FitnessAction(Action):
    message: str = Field(default="", description="Message to send")

class FitnessObservation(Observation):
    echoed_message: str = Field(default="", description="Message echoed back")
    step: int = Field(default=0, description="Step number")
    task_id: str = Field(default="", description="Task identifier")

class FitnessState(State):
    step: int = Field(default=0)
    task_id: str = Field(default="")

# Aliases
TacticalFitnessAction = FitnessAction
TacticalFitnessObservation = FitnessObservation