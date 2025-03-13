from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
from openai import OpenAI


class BaseLLM(ABC):
    """所有LLM模型的基类"""
    @abstractmethod
    def call_with_messages(self, messages: List[Dict[str, str]],  **kwargs) -> str:
        """统一的调用接口"""
        pass

class OpenAI_Model(BaseLLM):

    """兼容OpenAI模型的实现"""
    def __init__(self, model_name: str, api_key: str,**kwargs):
        self.ModelName = model_name
        self.ApiKey = api_key
        if "base_url" in kwargs:
            self.base_url = kwargs.get("base_url")
            self.client = OpenAI(api_key=self.ApiKey, base_url=self.base_url)
        else:
            self.client = OpenAI(api_key=self.ApiKey)
    def call_with_messages(self, messages: List[Dict[str, str]], **kwargs) -> str:
        if isinstance(messages, str):
            messages = [{"role": "user", "content": messages}]
        response = self.client.chat.completions.create(
            model=self.ModelName,
            messages=messages,
            **kwargs
        )
        return response.choices[0].message.content
    
class DeepSeek_Model(BaseLLM):
    """兼容DeepSeek模型的实现"""
    def __init__(self, model_name: str, api_key: str,**kwargs):
        self.ModelName = model_name
        self.ApiKey = api_key
        self.client = OpenAI(api_key=self.ApiKey, base_url=self.base_url)


class LLMFactory:
    """LLM工厂类"""
    _models: Dict[str, type] = {
        "gpt-4o": OpenAI_Model,
        "civilgpt": OpenAI_Model,
        "DeepSeek-R1": DeepSeek_Model,
    }
    
    @classmethod
    def create(cls, model_name: str, api_key: str,**kwargs) -> BaseLLM:
        """
        创建LLM实例
        :param model_name: 模型名称 (如 "gpt", "claude")
        :param api_key: API密钥
        :return: LLM实例
        """
        model_class = cls._models.get(model_name.lower())
        if not model_class:
            raise ValueError(f"Unsupported model: {model_name}")
        return model_class(model_name,api_key,**kwargs)
    
if __name__ == "__main__":
    model = LLMFactory.create(model_name="civilgpt", api_key="EMPTY",base_url='http://61.172.167.78:8001/v1')
    print(model.call_with_messages("你好，请介绍一下你自己"))