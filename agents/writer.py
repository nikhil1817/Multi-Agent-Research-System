import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


class WriterAgent:
    def __init__(self):
        self.model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

    def write_report(self, user_query, plan, research_notes, critic_feedback):
        prompt = f"""
You are a professional AI research writer.

Create a structured report for this user query:

{user_query}

Plan:
{plan}

Research notes:
{research_notes}

Critic feedback:
{critic_feedback}

Report format:
# Title
## Executive Summary
## Key Findings
## Comparison
## Risks
## Recommendation
## Sources Used

Use clear simple language.
Do not invent facts.
Mention source titles and links when available.
"""

        response = client.responses.create(
            model=self.model,
            input=prompt
        )

        return response.output_text
