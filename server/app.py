from fastapi import FastAPI
from pydantic import BaseModel

# Import directly from the local environment file (same directory)
from .tactical_fitness_env_environment import TacticalFitnessEnvironment, TacticalFitnessAction

app = FastAPI()
env = TacticalFitnessEnvironment()

class ResetRequest(BaseModel):
    task_id: str = "easy"

class StepRequest(BaseModel):
    action: dict

@app.post("/reset")
async def reset(req: ResetRequest = None):
    task_id = req.task_id if req else "easy"
    obs = env.reset(task_id=task_id)
    return {"observation": obs.dict(), "done": False, "info": {}}

@app.post("/step")
async def step(req: StepRequest):
    action = TacticalFitnessAction(message=req.action.get("message", ""))
    obs, reward, done, info = env.step(action)
    return {"observation": obs.dict(), "reward": reward, "done": done, "info": info}

@app.get("/state")
async def get_state():
    return env.state()