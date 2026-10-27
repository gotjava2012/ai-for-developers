"""
The smallest possible "model" — to make TRAINING vs INFERENCE concrete.

A model is just: PARAMETERS (numbers) + a FUNCTION that uses them.

This linear model is  y = w*x + b.
Here we SET the parameters by hand (pretend they were already "trained").
Running predict() is INFERENCE — using the parameters to produce output.

In Module 2 you'll watch a real neural network LEARN parameters like these
from data instead of us hand-setting them.
"""

# --- The model's PARAMETERS (what "training" would normally learn) ---
w = 2.0   # weight
b = 1.0   # bias
# This "model" has exactly 2 parameters.
# For comparison: llama3.2:1b has ~1,000,000,000. Same idea, just scaled up.


def predict(x):
    """INFERENCE: use the trained parameters to turn an input into an output."""
    return w * x + b


if __name__ == "__main__":
    print("Model: y = w*x + b")
    print(f"Parameters:  w = {w},  b = {b}  (2 total)\n")
    print("Inference (running the model on some inputs):")
    for x in [0, 1, 2, 5, 10]:
        print(f"  input x={x:<3} ->  output y = {predict(x)}")

    print("\nTakeaway:")
    print("  - w and b are PARAMETERS (training would learn these).")
    print("  - predict() is INFERENCE (what your apps do every API call).")
    print("  - A billion-parameter LLM is this same idea at massive scale.")
