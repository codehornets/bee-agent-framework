# Copyright 2025 IBM Corp.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from datetime import UTC, datetime

from pydantic import BaseModel

from beeai_framework.template import PromptTemplate, PromptTemplateInput


class ToolCallingAgentSystemPromptInput(BaseModel):
    instructions: str | None = None


ToolCallingAgentSystemPrompt = PromptTemplate(
    PromptTemplateInput(
        schema=ToolCallingAgentSystemPromptInput,
        functions={
            "formatDate": lambda data: datetime.now(tz=UTC).strftime("%A, %B %d, %Y at %I:%M:%S %p"),
        },
        defaults={"role": "A helpful AI assistant", "instructions": ""},
        template="""Assume the role of {{role}}.

{{#instructions}}
Your instructions are:
{{.}}
{{/instructions}}

When the user sends a message, figure out a solution and provide a final answer.
You can use tools to improve your answers if available.

# Best practices
- Use markdown syntax to format code snippets, links, JSON, tables, images, and files.
- When the message is unclear, ask for a clarification.
- Do not refer to tools or tool outputs by name when responding.

The current date and time is: {{formatDate}}
""",
    )
)


class ToolCallingAgentTaskPromptInput(BaseModel):
    prompt: str
    context: str | None = None
    expected_output: str | type[BaseModel] | None = None


ToolCallingAgentTaskPrompt = PromptTemplate(
    PromptTemplateInput(
        schema=ToolCallingAgentTaskPromptInput,
        template="""{{#context}}This is the context that you are working with:
{{.}}

{{/context}}
{{#expected_output}}
This is the expected criteria for your output:
{{.}}

{{/expected_output}}
Your task: {{prompt}}
""",
    )
)


class ToolCallingAgentToolErrorPromptInput(BaseModel):
    reason: str


ToolCallingAgentToolErrorPrompt = PromptTemplate(
    PromptTemplateInput(
        schema=ToolCallingAgentToolErrorPromptInput,
        template="""The tool has failed; the error log is shown below. If the tool cannot accomplish what you want, use a different tool or explain why you can't use it.

{{&reason}}""",  # noqa: E501
    )
)
