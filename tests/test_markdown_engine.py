import pytest
from src.repopackage.engines.markdown_engine import MarkdownEngine

def test_extract_sections():
    content = "# T-01 - Title\n## Section 1\nContent 1\n## Section 2\nContent 2"
    engine = MarkdownEngine(content)
    sections = engine.extract_sections()
    assert sections["section_1"] == "Content 1"
    assert sections["section_2"] == "Content 2"

def test_update_section():
    content = "# T-01 - Title\n## Section 1\nContent 1\n## Section 2\nContent 2"
    engine = MarkdownEngine(content)
    updated_content = engine.update_section("Section 1", "Updated")
    
    assert "## Section 1\nUpdated" in updated_content
    assert "## Section 2\nContent 2" in updated_content
    assert "Content 1" not in updated_content

def test_read_metadata_list():
    content = "## Traits\n[A] | [B] | [C]"
    engine = MarkdownEngine(content)
    traits = engine.read_metadata_list("Traits")
    assert traits == ["A", "B", "C"]

def test_read_bullet_list():
    content = "## Depends On\n- T-01\n- T-02"
    engine = MarkdownEngine(content)
    deps = engine.read_metadata_list("Depends On")
    assert deps == ["T-01", "T-02"]

def test_read_key_value_pairs():
    content = "## Metadata\n- ID: PILL-01\n- Type: guardrail"
    engine = MarkdownEngine(content)
    meta = engine.read_key_value_pairs("Metadata")
    assert meta["ID"] == "PILL-01"
    assert meta["Type"] == "guardrail"
