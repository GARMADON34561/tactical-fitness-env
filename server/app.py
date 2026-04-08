"""FastAPI server for Tactical Fitness Environment."""

import uvicorn
from openenv.core.env_server import create_app

# Use absolute imports
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
    """Run the server."""
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()