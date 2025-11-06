"""
title: Mistral AI Pipe
author: dotcomdudee
author_url: https://github.com/dotcomdudee
date: 2025-01-06
version: 1.0
license: MIT
description: A pipe for integrating Mistral AI models into Open WebUI
requirements: requests
"""

from typing import List, Union, Generator, Iterator
from pydantic import BaseModel, Field
import requests
import json


class Pipe:
    class Valves(BaseModel):
        MISTRAL_API_KEY: str = Field(
            default="",
            description="Your Mistral API key from https://console.mistral.ai"
        )
        MISTRAL_API_BASE_URL: str = Field(
            default="https://api.mistral.ai/v1",
            description="Base URL for Mistral API"
        )

    def __init__(self):
        self.type = "manifold"
        self.id = "mistral"
        self.name = "Mistral AI"
        self.valves = self.Valves()

    def pipes(self) -> List[dict]:
        """Return list of available Mistral models"""
        return [
            {"id": "mistral-large-latest", "name": "Mistral Large (Latest) - 123B params"},
            {"id": "mistral-large-2411", "name": "Mistral Large 2.1 (2411) - 123B params"},
            {"id": "mistral-small-latest", "name": "Mistral Small (Latest) - Multimodal"},
            {"id": "mistral-small-2506", "name": "Mistral Small 3.2 (2506)"},
            {"id": "mistral-small-2503", "name": "Mistral Small 3.1 (2503)"},
            {"id": "mistral-small-2501", "name": "Mistral Small 3 (2501)"},
            {"id": "mistral-medium-latest", "name": "Mistral Medium (Latest)"},
            {"id": "mistral-medium-2508", "name": "Mistral Medium 3.1 (2508)"},
            {"id": "codestral-latest", "name": "Codestral (Latest) - Code Generation"},
            {"id": "codestral-2501", "name": "Codestral (2501)"},
            {"id": "open-mistral-7b", "name": "Mistral 7B - Open Source"},
            {"id": "open-mixtral-8x7b", "name": "Mixtral 8x7B - Open Source"},
            {"id": "open-mixtral-8x22b", "name": "Mixtral 8x22B - Open Source"},
        ]

    def pipe(
        self, body: dict, __user__: dict = None, __event_emitter__=None
    ) -> Union[str, Generator, Iterator]:
        """
        Process the request and forward to Mistral API

        :param body: Request body containing messages and model info
        :param __user__: User context (optional)
        :param __event_emitter__: Event emitter for status updates (optional)
        """

        if not self.valves.MISTRAL_API_KEY:
            return "Error: MISTRAL_API_KEY is not set. Please configure it in the pipe settings."

        # Prepare headers
        headers = {
            "Authorization": f"Bearer {self.valves.MISTRAL_API_KEY}",
            "Content-Type": "application/json"
        }

        # Extract model ID
        model_id = body.get("model", "mistral-large-latest")
        if model_id.startswith("mistral."):
            model_id = model_id.replace("mistral.", "")

        # Prepare request payload
        payload = {
            "model": model_id,
            "messages": body.get("messages", []),
        }

        # Add optional parameters if present
        if "temperature" in body:
            payload["temperature"] = body["temperature"]
        if "max_tokens" in body:
            payload["max_tokens"] = body["max_tokens"]
        if "top_p" in body:
            payload["top_p"] = body["top_p"]
        if "min_tokens" in body:
            payload["min_tokens"] = body["min_tokens"]
        if "stop" in body:
            payload["stop"] = body["stop"]
        if "random_seed" in body:
            payload["random_seed"] = body["random_seed"]
        if "safe_prompt" in body:
            payload["safe_prompt"] = body["safe_prompt"]

        # Handle streaming
        stream = body.get("stream", False)
        payload["stream"] = stream

        try:
            url = f"{self.valves.MISTRAL_API_BASE_URL}/chat/completions"

            if stream:
                return self._handle_stream(url, headers, payload, __event_emitter__)
            else:
                return self._handle_non_stream(url, headers, payload)

        except requests.exceptions.RequestException as e:
            return f"Error: Failed to connect to Mistral API - {str(e)}"
        except Exception as e:
            return f"Error: {str(e)}"

    def _handle_non_stream(self, url: str, headers: dict, payload: dict) -> str:
        """Handle non-streaming requests"""
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()

        data = response.json()

        if "choices" in data and len(data["choices"]) > 0:
            return data["choices"][0]["message"]["content"]
        else:
            return "Error: No response from Mistral API"

    def _handle_stream(
        self, url: str, headers: dict, payload: dict, __event_emitter__=None
    ) -> Generator:
        """Handle streaming requests"""
        response = requests.post(url, json=payload, headers=headers, stream=True)
        response.raise_for_status()

        for line in response.iter_lines():
            if line:
                line = line.decode("utf-8")
                if line.startswith("data: "):
                    data_str = line[6:]  # Remove "data: " prefix

                    if data_str.strip() == "[DONE]":
                        break

                    try:
                        data = json.loads(data_str)

                        if "choices" in data and len(data["choices"]) > 0:
                            delta = data["choices"][0].get("delta", {})

                            if "content" in delta:
                                yield delta["content"]
                    except json.JSONDecodeError:
                        continue
