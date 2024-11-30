import datetime
import json
from enum import StrEnum
from pathlib import Path

import requests
from pydantic import BaseModel

from src.last.module_analys import analyze_module_structure
from src.last.prompts import PROMPTS
from src.last.services import parse_project_structure, print_project_structure, transform_tree_leaves, read_file


class LayerName(StrEnum):
    Domain = "Domain"
    Ports = "Ports"
    Adapters = "Adapters"
    Infrastructure = "Infrastructure"


class Message(BaseModel):
    role: str
    content: str

    def __str__(self):
        return f"Message({self.content}) from role={self.role}"


class Usage(BaseModel):
    prompt_tokens: int
    total_tokens: int
    tokens_per_second: float
    completion_tokens: int


class Timestamps(BaseModel):
    request_time: datetime.datetime
    start_time_generation: datetime.datetime
    end_time_generation: datetime.datetime
    queue_wait_time: float
    generation_time: float


class Choice(BaseModel):
    index: int
    message: Message


class Response(BaseModel):
    request_id: int
    response_id: int
    model: str
    provider: str
    choices: list[Choice]
    usage: Usage
    timestamps: Timestamps

    def print(self):
        print()
        for choice in self.choices:
            print(choice.message.content)

    def get_content(self):
        for choice in self.choices:
            return choice.message.content


class Request(BaseModel):
    model: str = "mistral-nemo-instruct-2407"
    messages: list[Message]
    max_tokens: int = 1_000
    temperature: float = 0.3


class LLMAdapter:
    def __init__(self):
        self._BASE_URL = "http://84.201.152.196:8020/v1/completions"
        self._headers = {
            "Authorization": "IoC25C2J4Efw6V2g1t74CxewKFzaXkdS",
            "Content-Type": "application/json",
        }

    def _request(self, messages: list[Message]):
        request = Request(messages=messages)
        url = self._BASE_URL
        data = request.model_dump(mode="json")
        response = requests.post(url, json=data, headers=self._headers)
        response.raise_for_status()
        return response.json()

    def send_system_prompts(self, prompts: list[str]):
        messages = [
            Message(role="system", content=prompt)
            for prompt in prompts
        ]

        jsons_data = self._request(messages)
        response = Response(**jsons_data)
        return response

    def send_prompts(self, prompts: list[str], role="user") -> Response:
        messages = []
        for prompt in prompts:
            message = Message(role=role, content=prompt)
            messages.append(message)

        json_data = self._request(messages)
        response = Response(**json_data)
        return response


def converter(root: Path, excludes: set[str]):
    structure = parse_project_structure(root, excludes)
    structure = transform_tree_leaves(structure, lambda path: read_file(path))
    structure = transform_tree_leaves(structure, lambda code: analyze_module_structure(code))
    return structure


def main():
    project_path = Path("D:/hakatons/files/RESTfulAPI-master 2/RESTfulAPI-master")
    excludes = {
        ".idea",
        ".venv",
        ".git",
        ".gitignore",
        ".env",
        "__pycache__",
    }
    structure = converter(project_path, excludes)

    prompts = [
        *PROMPTS,
        "show me the project structure",
        json.dumps(structure),
    ]

    llm = LLMAdapter()
    response = llm.send_prompts(prompts)

    content = response.get_content()
    prompts = [
        "Переведи это текст на русский",
        content,
    ]
    response = llm.send_system_prompts(prompts)
    response.print()


if __name__ == "__main__":
    main()
