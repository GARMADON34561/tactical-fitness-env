"""Wrapper to use our custom environment."""

from tactical_fitness_env.server.tactical_fitness_environment import TacticalFitnessEnvironment
from tactical_fitness_env.models import FitnessAction as TacticalFitnessAction, FitnessObservation as TacticalFitnessObservation

__all__ = ["TacticalFitnessEnvironment", "TacticalFitnessAction", "TacticalFitnessObservation"]