from openai import AzureOpenAI
from dataclasses import dataclass, asdict
from typing import Literal

@dataclass(frozen=True)
class Message:
    role: Literal["system", "user", "assistant"]
    content: str
    
    def asdict(self):
        return asdict(self)


class ChatBot:
    def __init__(self, azure_endpoint, api_version, api_key, engine):
        self._client = AzureOpenAI(azure_endpoint=azure_endpoint, api_version=api_version, api_key=api_key)
        self._default_engine = engine
        
    
    def create(self, message_list: list[Message]):
        completion = self._client.chat.completions.create(model=self._default_engine,
                                            messages=message_list,
                                            temperature=0.7,
                                            max_tokens=800,
                                            top_p=0.95,
                                            frequency_penalty=0,
                                            presence_penalty=0,
                                            stop=None)
        print(completion)
        return [Message(choice.message.role, choice.message.content) for choice in completion.choices]