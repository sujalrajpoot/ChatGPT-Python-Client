from typing import Optional, List, Dict, Any
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
import cloudscraper
import re
import json
import os
from urllib.parse import urljoin

class ChatModelEnum(Enum):
    """Supported chat model variants."""
    GPT4O = auto()
    GPT4O_MINI = auto()
    GPT4O_LATEST = auto()
    
    @classmethod
    def to_api_string(cls, model: 'ChatModelEnum') -> str:
        """Convert enum value to API string representation."""
        return {
            cls.GPT4O: 'gpt-4o',
            cls.GPT4O_MINI: 'gpt-4o-mini',
            cls.GPT4O_LATEST: 'chatgpt-4o-latest'
        }[model]

class ChatGPTError(Exception):
    """Base exception class for ChatGPT client errors."""
    pass

class ConnectionError(ChatGPTError):
    """Raised when network communication fails."""
    pass

class AuthenticationError(ChatGPTError):
    """Raised when authentication/authorization fails."""
    pass

class ParseError(ChatGPTError):
    """Raised when response parsing fails."""
    pass

@dataclass
class Message:
    """Represents a chat message."""
    role: str
    content: str

    def to_dict(self) -> Dict[str, str]:
        """Convert message to dictionary format."""
        return {"role": self.role, "content": self.content}

class ChatClientBase(ABC):
    """Abstract base class for chat clients."""
    
    @abstractmethod
    def chat(self, query: str, model: ChatModelEnum) -> str:
        """Send a chat message and get response."""
        pass

class ChatGPT(ChatClientBase):
    """ChatGPT client implementation."""
    
    BASE_URL = 'https://chatgpt.es'
    API_ENDPOINT = urljoin(BASE_URL, '/wp-admin/admin-ajax.php')
    
    def __init__(self, timeout: int = 30, stream_chunk_size: int = 1000):
        """
        Initialize ChatGPT client.
        
        Args:
            timeout: Request timeout in seconds
            stream_chunk_size: Size of streaming chunks
            
        Raises:
            ValueError: If invalid parameters are provided
        """
        assert timeout > 0, "Timeout must be positive"
        assert stream_chunk_size > 0, "Chunk size must be positive"
        
        self.timeout = timeout
        self.stream_chunk_size = stream_chunk_size
        self.session = cloudscraper.create_scraper()
        self._setup_headers()
        
    def _setup_headers(self) -> None:
        """Setup request headers."""
        self.initial_headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
            'Referer': 'https://www.google.com/',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
                     'image/avif,image/webp,image/apng,*/*;q=0.8,'
                     'application/signed-exchange;v=b3;q=0.7',
        }
        
        self.post_headers = {
            'User-Agent': self.initial_headers['User-Agent'],
            'Referer': self.BASE_URL,
            'Origin': self.BASE_URL,
            'Accept': '*/*',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }

    def _get_auth_tokens(self) -> tuple[str, str]:
        """
        Retrieve authentication tokens from the website.
        
        Returns:
            Tuple of (nonce, post_id)
            
        Raises:
            ConnectionError: If network request fails
            ParseError: If tokens cannot be parsed from response
        """
        try:
            response = self.session.get(
                self.BASE_URL,
                headers=self.initial_headers,
                timeout=self.timeout
            )
            response.raise_for_status()
        except Exception as e:
            raise ConnectionError(f"Failed to retrieve authentication tokens: {e}")

        nonce_match = re.search(r'data-nonce="(.+?)"', response.text)
        post_id_match = re.search(r'data-post-id="(.+?)"', response.text)

        if not nonce_match or not post_id_match:
            raise ParseError("Failed to parse authentication tokens from response")

        return nonce_match.group(1), post_id_match.group(1)

    def _prepare_conversation(self, messages: List[Message]) -> List[str]:
        """
        Prepare conversation history format.
        
        Args:
            messages: List of chat messages
            
        Returns:
            Formatted conversation history
        """
        conversation = ["Human: strictly respond in the same language as my prompt, preferably English"]
        for msg in messages:
            role = "Human" if msg.role == "user" else "AI"
            conversation.append(f"{role}: {msg.content}")
        return conversation

    def chat(self, query: str, model: ChatModelEnum = ChatModelEnum.GPT4O) -> str:
        """
        Send a chat message and get response.
        
        Args:
            query: User's message
            model: Chat model to use
            
        Returns:
            AI response text
            
        Raises:
            ChatGPTError: If any error occurs during the chat process
        """
        nonce, post_id = self._get_auth_tokens()
        
        messages = [Message(role="user", content=query)]
        conversation = self._prepare_conversation(messages)
        
        payload = {
            '_wpnonce': nonce,
            'post_id': post_id,
            'url': self.BASE_URL,
            'action': 'wpaicg_chat_shortcode_message',
            'message': messages[-1].content,
            'bot_id': '0',
            'chatbot_identity': 'shortcode',
            'wpaicg_chat_client_id': os.urandom(5).hex(),
            'wpaicg_chat_history': json.dumps(conversation)
        }

        try:
            response = self.session.post(
                self.API_ENDPOINT,
                headers=self.post_headers,
                data=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            response_data = response.json()
            assert isinstance(response_data, dict), "Invalid response format"
            
            message = response_data.get('data')
            if not isinstance(message, str):
                raise ParseError("Invalid message format in response")
                
            return message
            
        except Exception as e:
            raise ChatGPTError(f"Chat request failed: {str(e)}")

def main() -> None:
    """Main entry point for testing."""
    try:
        ai = ChatGPT()
        response = ai.chat('Hi', ChatModelEnum.GPT4O)
        print(response)
    except ChatGPTError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()