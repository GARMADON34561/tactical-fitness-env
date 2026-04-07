"""Tactical Fitness AI - Action and Observation models."""

from pydantic import Field
from openenv.core.env_server.types import Action, Observation, State


# Main classes for our custom environment
class FitnessAction(Action):
    weekly_plan: list[str] = Field(default_factory=list)
    rest_days: list[int] = Field(default_factory=list)
    nutrition_advice: str = Field(default="")


class FitnessObservation(Observation):
    mission_type: str = Field(default="")
    squad_readiness: dict = Field(default_factory=dict)
    injuries: list[str] = Field(default_factory=list)
    equipment: list[str] = Field(default_factory=list)
    days_to_deploy: int = Field(default=0)
    done: bool = Field(default=False)
    reward: float = Field(default=0.0)


class FitnessState(State):
    current_task_index: int = Field(default=0)
    total_reward: float = Field(default=0.0)


# Aliases for auto-generated code compatibility
TacticalFitnessAction = FitnessAction
TacticalFitnessObservation = FitnessObservation