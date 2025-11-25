import logging
from app.config.llm_config import llm_model, base_url, temperature

logger = logging.getLogger(__name__)

try:
    from langchain_ollama import ChatOllama
    from langchain.schema import HumanMessage

    LC_AVAILABLE = True
except Exception:
    LC_AVAILABLE = False


class LLMAdapter:
    def __init__(self, model: str = llm_model, base_url: str = base_url, temperature: float = temperature):

        self._client = None

        if LC_AVAILABLE:
            try:
                self._client = ChatOllama(model=model, base_url=base_url, temperature=temperature)
                logger.info("ChatOllama client started")
            except Exception as e:
                logger.exception("Failed to create ChatOllama client: %s", e)
                self._client = None

        else:
            logger.info("Langchain Ollama not available; cannot create ChatOllama client")
            self._client = None


    def generate(self, prompt: str) -> str:
        if LC_AVAILABLE and isinstance(self._client, ChatOllama):

            try:
                # Preferred: invoke with HumanMessage (works in many LangChain versions)
                from langchain.schema import HumanMessage
                response = self._client.invoke([HumanMessage(content=prompt)])

                if hasattr(response, "content"):
                    return response.content

                try:
                    return response[0].content
                except Exception:
                    return str(response)

            except Exception as e:
                logger.exception("ChatOllama invocation failed: %s", e)
                return "LLM invocation failed"

        return "LLM not available"


# single global instance
llm = LLMAdapter()
