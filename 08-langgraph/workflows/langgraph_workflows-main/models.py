from dotenv import load_dotenv
import os

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_deepseek import ChatDeepSeek


# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()
# Obtém as chaves de API das variáveis de ambiente
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# Mapa de provedores para suas respectivas classes de modelo Langchain
# Facilita a adição de novos provedores no futuro.
_PROVIDER_MAP = {
    "openai": ChatOpenAI,
    "deepseek": ChatDeepSeek,
    "google": ChatGoogleGenerativeAI,
    # Adicione outros provedores aqui (ex: "anthropic": ChatAnthropic)
}

# Lista de configurações para cada modelo que será inicializado.
# Cada dicionário define:
# - key_name: A chave que será usada no dicionário 'models' final.
# - provider: O nome do provedor (deve corresponder a uma chave em _PROVIDER_MAP).
# - model_name: O nome específico do modelo para o provedor.
# - temperature (opcional): A temperatura para a geração do modelo. Se não fornecida, usa o padrão do modelo.
MODEL_CONFIGS = [
    {
        "key_name": "gemini_2.5_flash",
        "provider": "google",
        "model_name": "gemini-2.5-flash-preview-04-17",
        "temperature": 1.0,
    },
    {
        "key_name": "o4",
        "provider": "openai",
        "model_name": "o4-mini-2025-04-16",
    },
    {
        "key_name": "gpt_4o",
        "provider": "openai",
        "model_name": "gpt-4o-2024-08-06",
        # Temperatura padrão do modelo será usada
    },
    {
        "key_name": "gpt_4_1",
        "provider": "openai",
        "model_name": "gpt-4.1-2025-04-14",
        # Temperatura padrão do modelo será usada
    },
    {
        "key_name": "deepseek_r1",
        "provider": "deepseek",
        "model_name": "deepseek-reasoner",
    },
    {
        "key_name": "deepseek_v3",
        "provider": "deepseek",
        "model_name": "deepseek-chat",
        "temperature": 1.0,
    },
]

# Função auxiliar para criar uma instância de um modelo de chat.
# Args:
# model_name (str): O nome do modelo a ser usado.
# provider (str): O nome do provedor do modelo (ex: "openai", "google").
# temperature (float | None, opcional): A temperatura de amostragem a ser usada.
# Retorna:
# Uma instância do modelo de chat Langchain correspondente.
# Levanta:
# ValueError: Se o provedor não for suportado (não estiver em _PROVIDER_MAP).
def _create_chat_model(model_name: str, provider: str, temperature: float | None = None):
    if provider not in _PROVIDER_MAP:
        raise ValueError(f"Provedor não suportado: {provider}. Provedores suportados são: {list(_PROVIDER_MAP.keys())}")

    model_class = _PROVIDER_MAP[provider]

    params = {"model": model_name}
    if temperature is not None:
        params["temperature"] = temperature

    return model_class(**params)


# Dicionário final que armazenará todas as instâncias de modelo inicializadas.
# As chaves são definidas em MODEL_CONFIGS e os valores são as instâncias do modelo.
models = {}
# Itera sobre a lista de configurações e cria cada modelo.
for config in MODEL_CONFIGS:
    models[config["key_name"]] = _create_chat_model(
        model_name=config["model_name"],
        provider=config["provider"],
        temperature=config.get("temperature")  # Usa .get() para temperatura opcional
    )