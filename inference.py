"""
Tactical Fitness AI - Baseline Inference Script
Strictly follows hackathon requirements: uses injected LLM proxy.
"""

import os
import asyncio
import json
from typing import List, Optional
from openai import OpenAI

# Import your environment
from models import FitnessAction
from server.tactical_fitness_environment import TacticalFitnessEnvironment

# ========== MANDATORY: Use the injected proxy environment variables ==========
# These are provided by the hackathon platform – do NOT set defaults or fallbacks
API_BASE_URL = os.environ["API_BASE_URL"]   # Must exist, no default
API_KEY = os.environ["API_KEY"]             # Must exist, no default
MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-3.5-turbo")  # Optional default allowed

TASK_NAME = os.getenv("TASK_NAME", "tactical_fitness")
BENCHMARK = os.getenv("BENCHMARK", "tactical_fitness_env")
MAX_STEPS = 10

def log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model={model}", flush=True)

def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None:
    error_val = error if error else "null"
    done_val = str(done).lower()
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={done_val} error={error_val}", flush=True)

def log_end(success: bool, steps: int, score: float, rewards: List[float]) -> None:
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}", flush=True)

async def main():
    # Initialize client with the PROXY – no hardcoded URL or key
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
    
    env = TacticalFitnessEnvironment()
    
    rewards = []
    steps_taken = 0
    total_reward = 0.0
    
    log_start(task=TASK_NAME, env=BENCHMARK, model=MODEL_NAME)
    
    try:
        obs = env.reset()
        
        for step in range(1, MAX_STEPS + 1):
            if obs.done:
                break
            
            # Build prompt from observation
            prompt = f"""
You are a military strength and conditioning coach.

Current Mission: {obs.mission_type}
Squad Readiness: Cardio={obs.squad_readiness.get('cardio', 5)}/10, Strength={obs.squad_readiness.get('strength', 5)}/10, Ruck={obs.squad_readiness.get('ruck', 5)}/10
Injuries: {obs.injuries}
Available Equipment: {obs.equipment}
Days Until Deployment: {obs.days_to_deploy}

Design a training plan. Output a JSON with:
{{
    "weekly_plan": ["Monday: run 5km", "Tuesday: rest", ...],
    "rest_days": [1, 4],
    "nutrition_advice": "..."
}}
"""
            # ========== MANDATORY API CALL ==========
            # Do NOT wrap this in try/except that bypasses the call.
            # If it fails, the script fails – that's acceptable to the validator.
            completion = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are a military fitness expert. Output valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300
            )
            response_text = completion.choices[0].message.content.strip()
            
            # Parse JSON response (basic cleanup)
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            action_data = json.loads(response_text)
            
            action = FitnessAction(
                weekly_plan=action_data.get("weekly_plan", []),
                rest_days=action_data.get("rest_days", []),
                nutrition_advice=action_data.get("nutrition_advice", "")
            )
            
            # Execute step
            obs = env.step(action)
            reward = obs.reward if hasattr(obs, 'reward') else 0.0
            done = obs.done if hasattr(obs, 'done') else False
            
            rewards.append(reward)
            steps_taken = step
            total_reward += reward
            
            action_summary = str(action.weekly_plan[:2]) if action.weekly_plan else "[]"
            log_step(step=step, action=action_summary, reward=reward, done=done, error=None)
            
            if done:
                break
        
        max_possible_reward = 3.0
        score = total_reward / max_possible_reward if max_possible_reward > 0 else 0.0
        success = score >= 0.5
        
    except Exception as e:
        # If anything fails, log the error and exit – do NOT provide a fallback that avoids API calls
        print(f"Fatal error: {e}", flush=True)
        success = False
        score = 0.0
        steps_taken = 0
        rewards = []
    
    finally:
        log_end(success=success, steps=steps_taken, score=score, rewards=rewards)

if __name__ == "__main__":
    asyncio.run(main())