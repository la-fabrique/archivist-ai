from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True)
class AgentReply:
    session_id: str
    text: str


class AgentError(Exception):
    def __init__(self, message: str, session_id: str | None = None) -> None:
        super().__init__(message)
        self.session_id = session_id


class Agent(ABC):
    VERSION: ClassVar[int] = 1

    @abstractmethod
    def send(self, message: str, session_id: str | None = None) -> AgentReply:
        """Envoie un message à l'agent.

        Sans session_id : démarre une nouvelle session.
        Avec session_id : reprend cette session.
        Lève AgentError si l'appel échoue ou si la réponse est inexploitable.
        """
