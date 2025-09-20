"""
Cerebras Cloud LLM Integration for CrewAI
Provides a custom LLM implementation compatible with CrewAI agents.
"""

import os
from typing import List, Dict, Any, Optional
import logging
from urllib.parse import urljoin

from crewai.llm import BaseLLM
from cerebras.cloud.sdk import Cerebras
from pydantic import Field

logger = logging.getLogger(__name__)


class CerebrasLLM(BaseLLM):
    """
    Custom LLM class for integrating Cerebras Cloud with CrewAI agents.
    Compatible with CrewAI's LLM interface for agent-based task execution.
    """

    # Cerebras-specific configuration
    client: Cerebras = Field(default=None, description="Cerebras client instance")
    model: str = Field(default="gpt-oss-120b", description="Cerebras model to use")
    api_key: str = Field(default=None, description="Cerebras API key")
    temperature: float = Field(default=0.7, description="Sampling temperature")
    max_tokens: int = Field(default=4096, description="Maximum tokens in response")
    reasoning_effort: str = Field(default="medium", description="Reasoning effort level")

    # Required for CrewAI compatibility
    api_version: str = Field(default="", description="API version (not used)")
    api_base: str = Field(default="", description="API base URL (not used)")

    def __init__(
        self,
        model: str = "gpt-oss-120b",
        api_key: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        reasoning_effort: str = "medium"
    ):
        """
        Initialize Cerebras LLM with configuration.

        Args:
            model: Cerebras model name
            api_key: Cerebras API key (if not provided, uses env var)
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens in response
            reasoning_effort: Reasoning effort level (low, medium, high)
        """
        # Get API key from parameter or environment variable
        self.api_key = api_key or os.getenv("CEREBRAS_API_KEY")

        if not self.api_key:
            raise ValueError("CEREBRAS_API_KEY not found in environment variables or parameters")

        # Initialize Cerebras client
        try:
            self.client = Cerebras(api_key=self.api_key)
        except Exception as e:
            raise ValueError(f"Failed to initialize Cerebras client: {e}")

        # Set configuration
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.reasoning_effort = reasoning_effort

        super().__init__()

    def call(
        self,
        messages: List[Dict[str, Any]],
        stop: Optional[List[str]] = None,
        callbacks: Optional[List[Any]] = None,
        **kwargs
    ) -> str:
        """
        Make a call to Cerebras Cloud API with formatted messages.

        Args:
            messages: List of message dictionaries with 'role' and 'content'
            stop: Optional stop sequences
            callbacks: Optional callback functions
            **kwargs: Additional parameters

        Returns:
            Response text from Cerebras API
        """
        try:
            # Format messages for Cerebras API
            formatted_messages = self._format_messages(messages)

            # Set up parameters
            params = {
                "model": self.model,
                "messages": formatted_messages,
                "max_completion_tokens": kwargs.get("max_tokens", self.max_tokens),
                "temperature": kwargs.get("temperature", self.temperature),
                "reasoning_effort": kwargs.get("reasoning_effort", self.reasoning_effort),
                "stream": False
            }

            # Add stop sequences if provided
            if stop:
                params["stop"] = stop

            # Make API call
            logger.info(f"Making Cerebras API call with model {self.model}")
            response = self.client.chat.completions.create(**params)

            # Extract response text
            if hasattr(response, 'choices') and response.choices:
                content = response.choices[0].message.content
                return content or ""
            else:
                logger.error("No choices in Cerebras response")
                return ""

        except Exception as e:
            logger.error(f"Cerebras API call failed: {e}")
            # Return empty string instead of raising to prevent CrewAI task failures
            return ""

    def _format_messages(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Format CrewAI messages for Cerebras API compatibility.

        Args:
            messages: CrewAI formatted messages

        Returns:
            Cerebras API formatted messages
        """
        formatted = []

        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")

            # Ensure role is valid for Cerebras API
            if role == "human":
                role = "user"

            formatted.append({
                "role": role,
                "content": content
            })

        return formatted

    @property
    def _llm_type(self) -> str:
        """Return LLM type identifier for CrewAI."""
        return "cerebras"

    def __str__(self) -> str:
        """String representation of the LLM."""
        return f"CerebrasLLM(model={self.model}, client={bool(self.client)})"

    def __repr__(self) -> str:
        """Detailed representation of the LLM."""
        return f"CerebrasLLM(model={self.model}, api_key={'*' * 8 + '...'}, temperature={self.temperature})"
