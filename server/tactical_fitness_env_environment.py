"""Tactical Fitness AI - Core environment logic."""

from uuid import uuid4
from typing import Optional
from openenv.core.env_server.interfaces import Environment
from openenv.core.env_server.types import State

from ..models import FitnessAction, FitnessObservation, FitnessState

class TacticalFitnessEnvironment(Environment[FitnessAction, FitnessObservation, FitnessState]):
    """
    Tactical Fitness AI Environment.
    
    The agent must design safe, effective training plans for military personnel.
    """
    
    def __init__(self):
        """Initialize the environment with pre-defined test scenarios."""
        self._state = FitnessState(
            episode_id=str(uuid4()),
            step_count=0,
            current_task_index=0,
            total_reward=0.0
        )
        
        # Define 3 tasks (Easy → Medium → Hard)
        self.tasks = [
            # TASK 1: EASY - Safety Checker
            {
                "mission_type": "mountain_patrol",
                "squad_readiness": {"cardio": 7, "strength": 8, "ruck": 6},
                "injuries": ["lower_back_pain"],
                "equipment": ["barbell", "pullup_bar"],
                "days_to_deploy": 30,
                "expected_safe": False,
                "dangerous_exercise": "deadlift"
            },
            # TASK 2: MEDIUM - 3-Day Plan Generator
            {
                "mission_type": "urban_assault",
                "squad_readiness": {"cardio": 5, "strength": 6, "ruck": 4},
                "injuries": [],
                "equipment": ["resistance_bands", "pullup_bar"],
                "days_to_deploy": 14,
            },
            # TASK 3: HARD - 4-Week Mission Readiness
            {
                "mission_type": "desert_operation",
                "squad_readiness": {"cardio": 8, "strength": 7, "ruck": 5},
                "injuries": [],
                "equipment": ["barbell", "dumbbells", "pullup_bar", "resistance_bands"],
                "days_to_deploy": 28,
            }
        ]
    
    def reset(self, seed: Optional[int] = None, episode_id: Optional[str] = None, **kwargs) -> FitnessObservation:
        """Reset the environment to start a new episode."""
        self._state = FitnessState(
            episode_id=episode_id or str(uuid4()),
            step_count=0,
            current_task_index=0,
            total_reward=0.0
        )
        return self._get_current_observation()
    
    def step(self, action: FitnessAction, **kwargs) -> FitnessObservation:
        """Execute an action and return the next observation."""
        current_task = self.tasks[self._state.current_task_index]
        reward = 0.0
        done = False
        
        # ========== GRADING LOGIC ==========
        
        # Check 1: SAFETY (Highest priority)
        if current_task.get("injuries") and "lower_back_pain" in current_task["injuries"]:
            dangerous = current_task.get("dangerous_exercise", "")
            if dangerous and dangerous in str(action.weekly_plan).lower():
                reward = 0.0
                done = True
                return self._get_current_observation(reward=reward, done=done)
        
        # Check 2: EQUIPMENT COMPLIANCE (Partial credit)
        if current_task.get("equipment"):
            plan_text = " ".join(action.weekly_plan).lower()
            equipment_used = [eq for eq in current_task["equipment"] if eq.lower() in plan_text]
            equipment_score = len(equipment_used) / len(current_task["equipment"])
            reward += equipment_score * 0.4
        
        # Check 3: REST DAYS (Good practice)
        if len(action.rest_days) >= 1:
            reward += 0.2
        
        # Check 4: NUTRITION ADVICE (Bonus)
        if len(action.nutrition_advice) > 20:
            reward += 0.2
        
        # Check 5: PLAN COMPLETENESS
        if len(action.weekly_plan) >= 5:
            reward += 0.2
        
        # Clamp reward to [0, 1]
        reward = min(max(reward, 0.0), 1.0)
        
        # Move to next task or finish
        self._state.current_task_index += 1
        self._state.step_count += 1
        self._state.total_reward += reward
        
        if self._state.current_task_index >= len(self.tasks):
            done = True
        
        return self._get_current_observation(reward=reward, done=done)
    
    def _get_current_observation(self, reward: float = 0.0, done: bool = False) -> FitnessObservation:
        """Get the observation for the current task."""
        if self._state.current_task_index >= len(self.tasks):
            return FitnessObservation(
                mission_type="complete",
                squad_readiness={},
                injuries=[],
                equipment=[],
                days_to_deploy=0,
                done=True,
                reward=self._state.total_reward / len(self.tasks)
            )
        
        task = self.tasks[self._state.current_task_index]
        return FitnessObservation(
            mission_type=task["mission_type"],
            squad_readiness=task["squad_readiness"],
            injuries=task.get("injuries", []),
            equipment=task.get("equipment", []),
            days_to_deploy=task["days_to_deploy"],
            done=done,
            reward=reward
        )
    
    @property
    def state(self) -> FitnessState:
        """Return the current episode state."""
        return self._state