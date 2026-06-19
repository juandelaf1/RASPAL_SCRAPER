import json
from raspal.models import LLMConfig


class LLMExtractor:
    def __init__(self, config: LLMConfig | None = None):
        self.config = config or LLMConfig()

    def extract(self, text: str, config: LLMConfig | None = None) -> dict:
        cfg = config or self.config
        prompt = self._build_prompt(text, cfg)
        response = self._ollama_chat(cfg.model, prompt)
        return self._parse_response(response, cfg.output_schema)

    def _build_prompt(self, text: str, cfg: LLMConfig) -> str:
        base = cfg.prompt or "Extract structured information from the following text."
        schema_instruction = ""
        if cfg.output_schema:
            schema_instruction = f"\n\nReturn a JSON object with this schema:\n{json.dumps(cfg.output_schema, indent=2)}"
        return f"{base}{schema_instruction}\n\nTEXT:\n{text[:8000]}"

    def _ollama_chat(self, model: str, prompt: str) -> str:
        import ollama

        resp = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
        return resp["message"]["content"]

    def _parse_response(self, response: str, schema: dict | None) -> dict:
        if schema:
            try:
                start = response.index("{")
                end = response.rindex("}") + 1
                return json.loads(response[start:end])
            except (ValueError, json.JSONDecodeError):
                return {"raw": response}
        return {"raw": response}
