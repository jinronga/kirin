import datetime
from typing import Optional
from typing import Literal
from pydantic import Field

from src.models.schemas.base import BaseSchemaModel


class ChatInMessage(BaseSchemaModel):
    """
    Object for the request body of the chatbot endpoint.

    Attributes:
    -----------
    sessionUuid: Optional[str] | None
        Session UUID
    message: str
        Message
    temperature: float
        Temperature for inference(float)
    top_k: int
        Top_k parameter for inference(int)
    top_p: float
        Top_p parameter for inference(float)
    n_predict: int
        n_predict parameter for inference(int)

    """

    sessionUuid: Optional[str] | None = Field(..., title="Session UUID", description="Session UUID")
    message: str = Field(..., title="Message", description="Message")
    temperature: float = Field(..., title="Temperature", description="Temperature for inference(float)")
    top_k: int = Field(..., title="Top_k", description="Top_k parameter for inference(int)")
    top_p: float = Field(..., title="Top_p", description="Top_p parameter for inference(float)")
    n_predict: int = Field(..., title="n_predict", description="n_predict parameter for inference(int)")


class ChatInResponse(BaseSchemaModel):
    sessionUuid: str = Field(..., title="Session UUID", description="Session UUID")
    message: str = Field(..., title="Message", description="Message")


class ChatUUIDResponse(BaseSchemaModel):
    """
    Object for the response body of the chat session endpoint.

    Attributes:
    -----------
    sessionUuid: str
        Session UUID
    """

    sessionUuid: str = Field(..., title="Session UUID", description="Session UUID")


class SessionUpdate(BaseSchemaModel):
    """
    Object for the request body of update session.

    Attributes:
    -----------
    sessionUuid: str
        Session UUID
    name: str
        session name
    type: str
        type of session: rag or chat
    """

    sessionUuid: str = Field(..., title="Session UUID", description="Session UUID")
    name: Optional[str] = Field(default=None, title="Name", description="Name")
    type: Optional[Literal["rag", "chat"]] = Field(default=None, title="Type", description="Type")


class Session(BaseSchemaModel):
    sessionUuid: str = Field(..., title="Session UUID", description="Session UUID")
    name: str | None = Field(..., title="Name", description="Name")
    type: str | None = Field(..., title="Type", description="Type")
    created_at: datetime.datetime | None = Field(..., title="Creation time", description="Creation time")


class Chats(BaseSchemaModel):
    """
    Object for the response body of the chat history endpoint.

    Attributes:
    -----------
    role: str
        Role of chat user or assistant
    message: str
        Message
    """

    role: str = Field(..., title="Role", description="Role ")
    message: str = Field(..., title="Message", description="Message")


class ChatsWithTime(BaseSchemaModel):
    """
    Object for the response body of the chat history endpoint.

    Attributes:
    -----------
    role: str
        Role of chat user or assistant
    message: str
        Message
    create_at: timestamp
    """

    role: str = Field(..., title="Role", description="Role ")
    message: str = Field(..., title="Message", description="Message")
    create_at: datetime.datetime | None = Field(..., title="Creation time", description="Creation time")


class SaveChatHistory(BaseSchemaModel):
    """
    Object for the response body of the chat history endpoint.

    Attributes:
    -----------
    sessionUuid: str
        Session UUID
    role: str
        Role of chat user or assistant
    message: str
        Message
    """

    sessionUuid: str = Field(..., title="Session UUID", description="Session UUID")
    chats: list[Chats] = Field(..., title="Chat history", description="Chat history")


class MessagesResponse(BaseSchemaModel):
    role: str = Field(..., title="Role", description="Role")
    content: str = Field(..., title="Content", description="Content")
