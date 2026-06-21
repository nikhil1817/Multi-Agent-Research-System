import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


class EvaluatorAgent:
    def __init__(self):
        self.model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

    def evaluate(self, report):
        prompt = f"""
You are an evaluator agent.

Score this report from 1 to 10.

Check:
1. Completeness
2. Accuracy
3. Structure
4. Citation quality
5. Hallucination risk

Report:
{report}

Return:
Score:
Strengths:
Weaknesses:
Improvements:
"""

        response = client.responses.create(
            model=self.model,
            input=prompt
        )

        return response.output_text
