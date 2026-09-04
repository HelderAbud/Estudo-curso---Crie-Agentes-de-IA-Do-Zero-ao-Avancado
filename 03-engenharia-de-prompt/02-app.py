import streamlit as st
from pathlib import Path
from langchain.memory import ConversationBufferMemory
import time 

folder_files = Path(__file__).parent / "files"
folder_files.mkdir(exist_ok=True)  # Garante que a pasta exista

def cria_chain_conversa():
    st.session_state["chain"] = True
    # Msgs fictícias
    memory = ConversationBufferMemory(return_messages=True)
    memory.chat_memory.add_user_message("Oi")
    memory.chat_memory.add_ai_message("Olá, sou uma assistente.")
    st.session_state["memory"] = memory
    
def chat_window():
    st.header("🤖Bem Vindo ao ChatPDF", divider=True)
    if not 'chain' in st.session_state:
        st.error("Faça o upload de PDFs para começar")
        st.stop()
        
    memory = st.session_state["memory"]
    mensagens = memory.load_memory_variables({})["history"]
    container = st.container()
    for mensagem in mensagens:
        chat = container.chat_message(mensagem.type)
        chat.markdown(mensagem.content)
        
    nova_mensagem = st.chat_input("Converse com seus documentos")
    if nova_mensagem:
        chat = container.chat_message("human")
        chat.markdown(mensagem.content)
        chat = container.chat_message("ai")
        chat.markdown("Gerando Resposta")
        time.sleep(2)
        memory.chat_memory.add_user_message(nova_mensagem)
        memory.chat_memory.add_ai_message("Assistente novamente.")
        st.rerun()

def save_uploaded_files(uploaded_files, folder):
    """Salva arquivos enviados na pasta especificada."""
    # Remove arquivos antigos na pasta
    for file in folder.glob("*.pdf"):
        file.unlink()
    # Salva novos arquivos enviados
    for file in uploaded_files:
        (folder / file.name).write_bytes(file.read())

def main():
    with st.sidebar:
        st.header("Upload de PDFs")
        uploaded_pdfs = st.file_uploader("Adicione arquivos PDF", 
                                         type="pdf", 
                                         accept_multiple_files=True)
        if uploaded_pdfs:
            save_uploaded_files(uploaded_pdfs, folder_files)
            st.success(f"{len(uploaded_pdfs)} arquivo(s) salvo(s) com sucesso!")
        
        label_botao = "Inicializar Chatbot"
        if "chain" in st.session_state:
            label_botao = "Atualizar Chatbot"
        if st.button(label_botao, use_container_width=True):
            if len(list(folder_files.glob("*.pdf"))) == 0:
                st.error("Adicione arquivos pdf para inicializar o chatbot")
            else:
                st.success("Inicializando o Chatbot...")
                cria_chain_conversa()
                st.rerun()
    chat_window()

if __name__ == "__main__":
    main()
