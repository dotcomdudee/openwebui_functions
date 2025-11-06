"""
title: Cloudflare Workers AI Pipe
author: dotcomdudee
author_url: https://github.com/dotcomdudee
date: 2025-11-05
version: 3.0
license: MIT
description: A pipe for connecting Open WebUI to Cloudflare Workers AI models
required_open_webui_version: 0.3.0
"""

from typing import List, Union, Generator, Iterator
from pydantic import BaseModel, Field
import requests
import json


class Pipe:
    class Valves(BaseModel):
        CLOUDFLARE_API_KEY: str = Field(
            default="",
            description="Your Cloudflare API Token with Workers AI Read and Edit permissions",
        )
        CLOUDFLARE_ACCOUNT_ID: str = Field(
            default="", description="Your Cloudflare Account ID"
        )
        BASE_URL: str = Field(
            default="https://api.cloudflare.com/client/v4/accounts",
            description="Cloudflare API base URL",
        )

    def __init__(self):
        self.type = "manifold"
        self.name = "cloudflare/"
        self.valves = self.Valves()

    def pipes(self) -> List[dict]:
        """Return list of available Cloudflare Workers AI models"""
        return [
            # Large Models
            {
                "id": "cf-gpt-oss-120b",
                "name": "gpt-oss-120b",
            },
            {"id": "cf-llama-3.1-70b-instruct", "name": "llama-3.1-70b-instruct"},
            {
                "id": "cf-llama-3.3-70b-instruct-fp8-fast",
                "name": "llama-3.3-70b-instruct-fp8-fast",
            },
            {
                "id": "cf-mistral-small-3.1-24b-instruct",
                "name": "mistral-small-3.1-24b-instruct",
            },
            # Medium Models
            {"id": "cf-llama-3.1-8b-instruct", "name": "llama-3.1-8b-instruct"},
            {"id": "cf-mistral-7b-instruct-v0.2", "name": "mistral-7b-instruct-v0.2"},
            {
                "id": "cf-qwen2.5-coder-32b-instruct",
                "name": "qwen2.5-coder-32b-instruct",
            },
            {"id": "cf-gemma-3-12b-it", "name": "gemma-3-12b-it"},
            # Lightweight Models
            {"id": "cf-gpt-oss-20b", "name": "gpt-oss-20b"},
            {"id": "cf-llama-3.2-1b-instruct", "name": "llama-3.2-1b-instruct"},
            {"id": "cf-llama-3.2-3b-instruct", "name": "llama-3.2-3b-instruct"},
        ]

    def get_cloudflare_model_name(self, model_id: str) -> str:
        """Convert Open WebUI model ID to Cloudflare model name"""
        # Remove "cf-" prefix and convert to Cloudflare format
        model_mapping = {
            "cf-gpt-oss-120b": "@cf/openai/gpt-oss-120b",
            "cf-llama-3.1-70b-instruct": "@cf/meta/llama-3.1-70b-instruct",
            "cf-llama-3.3-70b-instruct-fp8-fast": "@cf/meta/llama-3.3-70b-instruct-fp8-fast",
            "cf-mistral-small-3.1-24b-instruct": "@cf/mistral/mistral-small-3.1-24b-instruct",
            "cf-llama-3.1-8b-instruct": "@cf/meta/llama-3.1-8b-instruct",
            "cf-mistral-7b-instruct-v0.2": "@cf/mistral/mistral-7b-instruct-v0.2",
            "cf-qwen2.5-coder-32b-instruct": "@cf/qwen/qwen2.5-coder-32b-instruct",
            "cf-gemma-3-12b-it": "@cf/google/gemma-3-12b-it",
            "cf-gpt-oss-20b": "@cf/openai/gpt-oss-20b",
            "cf-llama-3.2-1b-instruct": "@cf/meta/llama-3.2-1b-instruct",
            "cf-llama-3.2-3b-instruct": "@cf/meta/llama-3.2-3b-instruct",
        }
        return model_mapping.get(model_id, model_id)

    def uses_responses_endpoint(self, cf_model_name: str) -> bool:
        """Check if model uses /responses endpoint (GPT-OSS) or /run endpoint (others)"""
        # GPT-OSS models use the /responses endpoint with "input" parameter
        return "openai/gpt-oss" in cf_model_name

    def messages_to_input(self, messages: List[dict]) -> str:
        """Convert OpenAI-style messages array to a single input string"""
        if not messages:
            return ""

        # If there's only one message, return its content directly
        if len(messages) == 1:
            return messages[0].get("content", "")

        # Format multiple messages as a conversation
        input_parts = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")

            if role == "system":
                input_parts.append(f"System: {content}")
            elif role == "assistant":
                input_parts.append(f"Assistant: {content}")
            elif role == "user":
                input_parts.append(f"User: {content}")
            else:
                input_parts.append(content)

        return "\n\n".join(input_parts)

    def pipe(self, body: dict) -> Union[str, Generator, Iterator]:
        """Process the request and return response from Cloudflare Workers AI"""

        # Validate configuration
        if not self.valves.CLOUDFLARE_API_KEY:
            return "Error: Cloudflare API Key is not set. Please configure it in the valve settings."

        if not self.valves.CLOUDFLARE_ACCOUNT_ID:
            return "Error: Cloudflare Account ID is not set. Please configure it in the valve settings."

        # Extract parameters from body
        model_id = body.get("model", "")
        messages = body.get("messages", [])

        # Strip any pipe prefix from model_id (e.g., "cfpipe.cf-gpt-oss-120b" -> "cf-gpt-oss-120b")
        if "." in model_id:
            model_id = model_id.split(".", 1)[1]

        # Get the Cloudflare model name
        cf_model_name = self.get_cloudflare_model_name(model_id)

        # Prepare headers
        headers = {
            "Authorization": f"Bearer {self.valves.CLOUDFLARE_API_KEY}",
            "Content-Type": "application/json",
        }

        # Determine endpoint and payload format based on model
        if self.uses_responses_endpoint(cf_model_name):
            # GPT-OSS models use /responses endpoint with "input" parameter
            url = f"{self.valves.BASE_URL}/{self.valves.CLOUDFLARE_ACCOUNT_ID}/ai/v1/responses"
            input_text = self.messages_to_input(messages)
            payload = {
                "model": cf_model_name,
                "input": input_text,
            }
        else:
            # Other models (Llama, Mistral, etc.) use /run endpoint with "messages" array
            url = f"{self.valves.BASE_URL}/{self.valves.CLOUDFLARE_ACCOUNT_ID}/ai/run/{cf_model_name}"
            payload = {
                "messages": messages,
            }

        # Add optional parameters from body if present
        if "temperature" in body:
            payload["temperature"] = body["temperature"]
        if "max_tokens" in body:
            payload["max_tokens"] = body["max_tokens"]
        if "top_p" in body:
            payload["top_p"] = body["top_p"]

        # Note: The /responses endpoint doesn't support streaming for all models
        # Disable streaming to ensure compatibility
        stream = False

        try:
            if stream:
                # Enable streaming
                payload["stream"] = True

                # Make streaming request
                response = requests.post(
                    url, headers=headers, json=payload, stream=True, timeout=120
                )

                if response.status_code != 200:
                    error_text = response.text
                    return f"Error: Cloudflare API returned status {response.status_code}: {error_text}"

                return self.stream_response(response)
            else:
                # Non-streaming request
                response = requests.post(
                    url, headers=headers, json=payload, timeout=120
                )

                if response.status_code != 200:
                    error_text = response.text
                    return f"Error: Cloudflare API returned status {response.status_code}: {error_text}"

                result = response.json()

                # Extract the response - format varies by endpoint
                # The response might be wrapped in "result" key or be the direct response
                response_data = result.get("result", result)

                # Handle string responses
                if isinstance(response_data, str):
                    return response_data

                # Handle dict responses with "response" key (standard /run endpoint format)
                if isinstance(response_data, dict) and "response" in response_data:
                    return response_data["response"]

                # Handle complex /responses endpoint format with output array (GPT-OSS models)
                if isinstance(response_data, dict) and "output" in response_data:
                    output_array = response_data["output"]
                    if isinstance(output_array, list):
                        # Look for message type in output array
                        for item in output_array:
                            if isinstance(item, dict) and item.get("type") == "message":
                                content = item.get("content", [])
                                if isinstance(content, list):
                                    # Find output_text in content array
                                    for content_item in content:
                                        if (
                                            isinstance(content_item, dict)
                                            and content_item.get("type")
                                            == "output_text"
                                        ):
                                            return content_item.get("text", "")

                # Fallback: return error with partial response data
                return f"Error: Could not extract text from response. Response keys: {list(response_data.keys()) if isinstance(response_data, dict) else 'not a dict'}"

        except requests.exceptions.Timeout:
            return "Error: Request to Cloudflare Workers AI timed out."
        except requests.exceptions.RequestException as e:
            return f"Error: Failed to connect to Cloudflare Workers AI: {str(e)}"
        except Exception as e:
            return f"Error: {str(e)}"

    def stream_response(self, response) -> Generator:
        """Handle streaming response from Cloudflare Workers AI"""
        try:
            for line in response.iter_lines():
                if line:
                    line = line.decode("utf-8")

                    # Server-sent events format: "data: {json}"
                    if line.startswith("data: "):
                        data = line[6:]  # Remove "data: " prefix

                        # Check for end of stream
                        if data == "[DONE]":
                            break

                        try:
                            json_data = json.loads(data)

                            # Extract content from the response
                            # Try different possible formats
                            if "response" in json_data:
                                yield json_data["response"]
                            elif "result" in json_data:
                                result = json_data["result"]
                                if isinstance(result, str):
                                    yield result
                                elif isinstance(result, dict) and "response" in result:
                                    yield result["response"]
                            elif "choices" in json_data:
                                # OpenAI-compatible format
                                for choice in json_data["choices"]:
                                    if "delta" in choice:
                                        content = choice["delta"].get("content", "")
                                        if content:
                                            yield content
                            elif "content" in json_data:
                                yield json_data["content"]

                        except json.JSONDecodeError:
                            # If it's not JSON, yield the data as-is
                            if data and data != "[DONE]":
                                yield data
        except Exception as e:
            yield f"\n\nError during streaming: {str(e)}"
