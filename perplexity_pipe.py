"""
title: Perplexity AI Pipe
author: dotcomdudee
author_url: https://github.com/dotcomdudee
date: 2025-01-06
version: 1.0
license: MIT
description: A pipe for integrating Perplexity AI models into Open WebUI
requirements: requests
"""

from typing import List, Union, Generator, Iterator
from pydantic import BaseModel, Field
import requests
import json


class Pipe:
    class Valves(BaseModel):
        PERPLEXITY_API_KEY: str = Field(
            default="",
            description="Your Perplexity API key from https://www.perplexity.ai/settings/api"
        )
        PERPLEXITY_API_BASE_URL: str = Field(
            default="https://api.perplexity.ai",
            description="Base URL for Perplexity API"
        )

    def __init__(self):
        self.type = "manifold"
        self.id = "perplexity"
        self.name = "Perplexity AI"
        self.valves = self.Valves()

    def pipes(self) -> List[dict]:
        """Return list of available Perplexity models"""
        return [
            {"id": "sonar-pro", "name": "Sonar Pro"},
            {"id": "sonar", "name": "Sonar"},
            {"id": "sonar-reasoning", "name": "Sonar Reasoning"},
            {"id": "sonar-reasoning-pro", "name": "Sonar Reasoning Pro"},
        ]

    def pipe(
        self, body: dict, __user__: dict = None, __event_emitter__=None
    ) -> Union[str, Generator, Iterator]:
        """
        Process the request and forward to Perplexity API

        :param body: Request body containing messages and model info
        :param __user__: User context (optional)
        :param __event_emitter__: Event emitter for status updates (optional)
        """

        if not self.valves.PERPLEXITY_API_KEY:
            return "Error: PERPLEXITY_API_KEY is not set. Please configure it in the pipe settings."

        # Prepare headers
        headers = {
            "Authorization": f"Bearer {self.valves.PERPLEXITY_API_KEY}",
            "Content-Type": "application/json"
        }

        # Extract model ID
        model_id = body.get("model", "sonar")
        if model_id.startswith("perplexity."):
            model_id = model_id.replace("perplexity.", "")

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
        if "top_k" in body:
            payload["top_k"] = body["top_k"]
        if "frequency_penalty" in body:
            payload["frequency_penalty"] = body["frequency_penalty"]
        if "presence_penalty" in body:
            payload["presence_penalty"] = body["presence_penalty"]

        # Handle streaming
        stream = body.get("stream", False)
        payload["stream"] = stream

        try:
            url = f"{self.valves.PERPLEXITY_API_BASE_URL}/chat/completions"

            if stream:
                return self._handle_stream(url, headers, payload, __event_emitter__)
            else:
                return self._handle_non_stream(url, headers, payload)

        except requests.exceptions.RequestException as e:
            return f"Error: Failed to connect to Perplexity API - {str(e)}"
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
            return "Error: No response from Perplexity API"

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
