def get_llm():
    class DummyLLM:
        def invoke(self, prompt):
            class R:
                content = """1. Load the data
2. Analyze trends
3. Generate report"""
            return R()
    return DummyLLM()