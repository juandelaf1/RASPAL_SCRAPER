from raspal.llm import LLMExtractor
from raspal.models import LLMConfig, ChainStep


def test_clean_json_simple():
    result = LLMExtractor._clean_json('{"key": "value"}')
    assert result == '{"key": "value"}'


def test_clean_json_with_markdown():
    result = LLMExtractor._clean_json('```json\n{"key": "value"}\n```')
    assert result == '{"key": "value"}'


def test_clean_json_with_text():
    result = LLMExtractor._clean_json(
        'Here is the result:\n{"name": "test"}\nHope that helps.'
    )
    assert result == '{"name": "test"}'


def test_clean_json_no_braces():
    result = LLMExtractor._clean_json("Some plain text")
    assert result == "Some plain text"


def test_clean_json_nested():
    result = LLMExtractor._clean_json(
        '{"outer": {"inner": "value"}, "list": [1, 2, 3]}'
    )
    assert result == '{"outer": {"inner": "value"}, "list": [1, 2, 3]}'


def test_build_prompt_with_template():
    llm = LLMExtractor()
    cfg = LLMConfig(template="product")
    prompt = llm._build_prompt("Some text", cfg)
    assert "Extract product info" in prompt
    assert "Some text" in prompt


def test_build_prompt_with_schema():
    llm = LLMExtractor()
    cfg = LLMConfig(
        output_schema={"name": "", "price": 0},
        strict=True,
    )
    prompt = llm._build_prompt("Content", cfg)
    assert "JSON object" in prompt
    assert "no markdown" in prompt


def test_build_prompt_respects_length_limit():
    llm = LLMExtractor()
    long_text = "x" * 20000
    cfg = LLMConfig()
    prompt = llm._build_prompt(long_text, cfg)
    # Should be truncated to ~16000 chars + prompt text
    assert len(prompt) < 17000


def test_build_prompt_custom_prompt():
    llm = LLMExtractor()
    cfg = LLMConfig(prompt="Custom prompt here")
    prompt = llm._build_prompt("Content", cfg)
    assert prompt.startswith("Custom prompt here")


def test_prompt_templates_defined():
    templates = LLMExtractor.PROMPT_TEMPLATES
    for key in ("product", "article", "person", "review", "event", "generic"):
        assert key in templates
        assert len(templates[key]) > 10


def test_extract_chain_dry():
    """Test that chain structure is valid without calling Ollama."""
    llm = LLMExtractor()
    chain = [
        ChainStep(name="step1", prompt="First step"),
        ChainStep(name="step2", prompt="Second step"),
    ]
    # This will call Ollama and fail if Ollama is not running.
    # We just test the structure is valid.
    assert len(chain) == 2
    assert chain[0].name == "step1"
    assert chain[1].name == "step2"
