import os
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from typing import Dict

class PromptRenderer:
    def __init__(self, template_dir: Path):
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            trim_blocks=True,
            lstrip_blocks=True
        )
        self.templates = {
            "instruction_prompt": self.env.get_template("instruction.jinja2")
        }

    def render_instruction_prompt(self, context: Dict) -> str:
        """Renders the full role and task instruction"""
        return self.templates["instruction_prompt"].render(context)