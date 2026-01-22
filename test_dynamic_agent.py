from utils.dynamic_career_agent import (
    create_initial_state,
    run_career_discovery
)

# Step 1: create fresh state
state = create_initial_state()

# Step 2: simulate user input
user_input = "I like Python and data analysis"

# Step 3: run the agent once
reply, state = run_career_discovery(user_input, state)

# Step 4: print outputs
print("AI reply:")
print(reply)

print("\nCurrent state:")
print(state)

