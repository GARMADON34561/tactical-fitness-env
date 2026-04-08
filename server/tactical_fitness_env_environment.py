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

TacticalFitnessAction = FitnessAction
TacticalFitnessObservation = FitnessObservation

class TacticalFitnessEnvironment:
    def __init__(self):
        self.current_step = 0
        self.max_steps = 10
        self.task_id = "easy"

    def reset(self, task_id: str = "easy", **kwargs):
        self.task_id = task_id
        self.current_step = 0
        return FitnessObservation(echoed_message="", step=0, task_id=task_id)

    def step(self, action: FitnessAction, **kwargs):
        self.current_step += 1
        if self.task_id == "easy":
            echoed = action.message
        elif self.task_id == "medium":
            echoed = action.message[::-1]
        elif self.task_id == "hard":
            echoed = action.message.upper()
        else:
            echoed = action.message
        obs = FitnessObservation(echoed_message=echoed, step=self.current_step, task_id=self.task_id)
        reward = 0.0
        done = self.current_step >= self.max_steps
        info = {"task": self.task_id}
        return obs, reward, done, info

    def state(self):
        return {"step": self.current_step, "task_id": self.task_id}

class EasyGrader:
    def __call__(self, trajectory):
        return 0.85

class MediumGrader:
    def __call__(self, trajectory):
        return 0.75

class HardGrader:
    def __call__(self, trajectory):
        return 0.65