from tools.search_tool import simple_web_search


class ResearchAgent:
    def research(self, plan):
        all_notes = []

        for step in plan:
            print(f"Researching: {step}")

            results = simple_web_search(step)

            all_notes.append({
                "task": step,
                "results": results
            })

        return all_notes
