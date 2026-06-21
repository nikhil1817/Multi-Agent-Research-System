import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


class PlannerAgent:
    def __init__(self):
        self.model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

    def create_plan(self, user_query: str):
        prompt = f"""
You are a planning agent.

Break the user request into 5 clear research steps.

User request:
{user_query}

Return only a numbered list.
"""

        response = client.responses.create(
            model=self.model,
            input=prompt
        )

        text = response.output_text

        steps = []
        for line in text.split("\n"):
            line = line.strip()
            if line:
                steps.append(line)

        return steps

