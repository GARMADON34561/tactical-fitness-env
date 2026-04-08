"""Tactical Fitness AI - Action and Observation models."""

from pydantic import Field
from openenv.core.env_server.types import Action, Observation, State


class FitnessAction(Action):
    """What the AI agent can do - design a training plan."""
    
    weekly_plan: list[str] = Field(
        default_factory=list,
        description="List of 7 daily workout descriptions"
    )
    rest_days: list[int] = Field(
        default_factory=list,
        description="Days for rest/recovery (0=Monday, 6=Sunday)"
    )
    nutrition_advice: str = Field(
        default="",
        description="Dietary recommendation for the mission"
    )


class FitnessObservation(Observation):
    """What the AI agent sees - the current mission profile."""
    
    mission_type: str = Field(
        default="",
        description="mountain_patrol, urban_assault, or desert_operation"
    )
    squad_readiness: dict = Field(
        default_factory=dict,
        description="Fitness levels: cardio, strength, ruck"
    )
    injuries: list[str] = Field(
        default_factory=list,
        description="Injury list"
    )
    equipment: list[str] = Field(
        default_factory=list,
        description="Available equipment"
    )
    days_to_deploy: int = Field(
        default=0,
        description="Days until deployment"
    )
    done: bool = Field(default=False)
    reward: float = Field(default=0.0)


class FitnessState(State):
    """Episode state tracking."""
    
    current_task_index: int = Field(default=0)
    total_reward: float = Field(default=0.0)


# Aliases for compatibility
TacticalFitnessAction = FitnessAction
TacticalFitnessObservation = FitnessObservation