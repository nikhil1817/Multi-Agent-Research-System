import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


class CriticAgent:
    def __init__(self):
        self.model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

    def review(self, research_notes):
        prompt = f"""
You are a source critic agent.

Review the research notes below.

Find:
1. Missing information
2. Weak sources
3. Unsupported claims
4. Areas needing better evidence

Research notes:
{research_notes}

Return concise feedback.
"""

        response = client.responses.create(
            model=self.model,
            input=prompt
        )

        return response.output_text
