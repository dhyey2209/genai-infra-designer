#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
import re  # For Terraform block extraction

from devops_ai_project.crew import InfraArchitectProject


"""
    This script serves as the entry point for running the AI Infra Architect crew. It provides functions to run the crew, train it, replay tasks, and test with different models.
    
    run(): Executes the AI Infra Architect crew with a high-level system idea as input and saves the output.
    train(): Optionally trains the crew using agent memory and iterative refinement based on a specified number of iterations and input file.
    replay(): Replays the crew execution from a specific task ID.
    test(): Tests the crew execution with a specific model and a specified number of iterations.
    
"""

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

    

def run():
    """
    Run the AI Infra Architect crew with a high-level system idea as input.
    """
    topic = "Design a scalable e-commerce platform on AWS for 100k daily users"

    inputs = {'topic': topic}

    try:
        output = InfraArchitectProject().crew().kickoff(inputs=inputs)

        print("\nInfra design completed.\n")

        # Save markdown output
        filename = f"infra_design_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(filename, "w") as f:
            f.write(output)
        print(f"Infra design saved to '{filename}'.")

        # Extract and save Terraform code blocks
        tf_blocks = re.findall(r"```terraform(.*?)```", output, re.DOTALL)
        if tf_blocks:
            with open("infra.tf", "w") as tf_file:
                tf_file.write("\n\n".join([block.strip() for block in tf_blocks]))
            print("Terraform blocks saved to 'infra.tf'")
        else:
            print("No Terraform blocks found to save.")

    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Optional: Train the crew (if you use agent memory and iterative refinement).
    """
    topic = "Design a scalable e-commerce platform on AWS for 100k daily users"
    inputs = {'topic': topic}

    try:
        InfraArchitectProject().crew().train(
            n_iterations=int(sys.argv[1]),
            filename=sys.argv[2],
            inputs=inputs
        )
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        InfraArchitectProject().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution with a specific model (if needed).
    """
    topic = "Design a scalable e-commerce platform on AWS for 100k daily users"
    inputs = {'topic': topic}

    try:
        InfraArchitectProject().crew().test(
            n_iterations=int(sys.argv[1]),
            openai_model_name=sys.argv[2],
            inputs=inputs
        )
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")


if __name__ == "__main__":
    run()
