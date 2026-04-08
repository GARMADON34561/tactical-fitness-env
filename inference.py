import os
import asyncio
import json
from typing import List, Optional
from openai import OpenAI

# Import your environment and action class
from tactical_fitness_env import TacticalFitnessEnvironment, TacticalFitnessAction

# ========== MANDATORY: Use injected proxy environment variables ==========
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
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
    env = TacticalFitnessEnvironment()
    
    rewards = []
    steps_taken = 0
    total_reward = 0.0
    
    # Choose a task – you can also loop over tasks, but for validation just pick one
    task_id = "easy"   # change to "medium" or "hard" if you want, but validator will test all three separately
    log_start(task=task_id, env=BENCHMARK, model=MODEL_NAME)
    
    try:
        obs = env.reset(task_id=task_id)
        
        for step in range(1, MAX_STEPS + 1):
            # Build prompt
            prompt = f"""
You are an echo bot. The current task is: {task_id}
- If task is 'easy': reply with exactly the same message you received.
- If task is 'medium': reply with the reversed message.
- If task is 'hard': reply with the message in uppercase.

Last echoed message: {obs.echoed_message}
Step number: {step}

Send your next message (just the text, no extra words).
"""
            # API call through the proxy (mandatory)
            completion = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are an echo bot. Reply with a short message."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=50
            )
            response_text = completion.choices[0].message.content.strip()
            
            # Create action
            action = TacticalFitnessAction(message=response_text)
            
            # Step the environment – returns (observation, reward, done, info)
            obs, reward, done, info = env.step(action)
            
            rewards.append(reward)
            steps_taken = step
            total_reward += reward
            
            log_step(step=step, action=response_text[:50], reward=reward, done=done, error=None)
            
            if done:
                break
        
        # Dummy score – the actual score will be computed by the grader from trajectory
        # This is just for the log; the validator uses the grader's output.
        max_possible_reward = 1.0
        score = total_reward / max_possible_reward if max_possible_reward > 0 else 0.0
        success = score >= 0.5
        
    except Exception as e:
        print(f"Fatal error: {e}", flush=True)
        success = False
        score = 0.0
        steps_taken = 0
        rewards = []
    
    finally:
        log_end(success=success, steps=steps_taken, score=score, rewards=rewards)

if __name__ == "__main__":
    asyncio.run(main())