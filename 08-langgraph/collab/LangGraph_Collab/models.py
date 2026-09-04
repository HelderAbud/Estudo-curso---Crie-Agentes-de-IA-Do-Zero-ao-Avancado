from dotenv import load_dotenv
import os

from langchain_openai import ChatOpenAI


# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()
# Obtém as chaves de API das variáveis de ambiente
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Debug: Verifica se a chave foi carregada
print(f"Chave API carregada: {'Sim' if OPENAI_API_KEY else 'Não'}")
print(f"Primeiros 4 caracteres da chave: {OPENAI_API_KEY if OPENAI_API_KEY else 'N/A'}")

# Mapa de provedores para suas respectivas classes de modelo Langchain
# Facilita a adição de novos provedores no futuro.
_PROVIDER_MAP = {
    "openai": ChatOpenAI,
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
        "key_name": "gpt_4_1",
        "provider": "openai",
        "model_name": "gpt-4.1-2025-04-14",
        # Temperatura padrão do modelo será usada
    }
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