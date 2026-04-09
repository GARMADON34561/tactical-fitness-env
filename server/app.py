"""FastAPI server for Tactical Fitness Environment."""

import uvicorn
from openenv.core.env_server import create_app

from models import FitnessAction, FitnessObservation
from server.tactical_fitness_environment import TacticalFitnessEnvironment

# Create the FastAPI app
app = create_app(
    TacticalFitnessEnvironment,
    FitnessAction,
    FitnessObservation,
    env_name="tactical_fitness_env"
)

def main():
    """Entry point for the server script."""
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=7860,
        log_level="info"
    )

if __name__ == "__main__":
    main()