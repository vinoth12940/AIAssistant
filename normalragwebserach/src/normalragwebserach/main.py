#!/usr/bin/env python
import warnings
from normalragwebserach.ui import run_ui
from normalragwebserach.crew import Normalragwebserach

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """Run the application with Streamlit UI"""
    run_ui()

def run_cli():
    """Run in CLI mode for testing or scripting"""
    crew = Normalragwebserach()
    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() in ['exit', 'quit']:
                break
            
            response = crew.crew().kickoff(inputs={'topic': user_input})
            print(f"\nAssistant: {response}")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\nError: {str(e)}")

if __name__ == "__main__":
    run()
