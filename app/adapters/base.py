from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class BaseAdapter(ABC):
    """
    The Abstract Base Class for all Enterprise Context Mesh Adapters.
    Ensures a standardized 'Read-Only' interface for Agentic tool use.
    """

    @abstractmethod
    async def connect(self) -> None:
        """Establishes a secure, authenticated connection to the data source."""
        pass

    @abstractmethod
    async def execute_read_only(self, query: str) -> List[Dict[str, Any]]:
        """
        The primary interface for AI Agents.
        Must enforce read-only constraints and prevent data modification.
        
        Args:
            query: The platform-specific query string (SQL, NoSQL, or API endpoint).
        
        Returns:
            A list of dictionaries representing the structured data records.
        """
        pass

    @abstractmethod
    async def close(self) -> None:
        """Gracefully closes all connections and releases system resources."""
        pass

    def sanitize_input(self, input_str: str) -> str:
        """
        A helper to strip potentially malicious characters from incoming queries.
        Can be overridden by specific adapters for custom injection protection.
        """
        # Basic protection: Remove common command-chaining characters
        chars_to_strip = [";", "--", "/*", "*/", "xp_"]
        sanitized = input_str
        for char in chars_to_strip:
            sanitized = sanitized.replace(char, "")
        return sanitized.strip()
