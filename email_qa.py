import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
from langchain_community.document_loaders import CSVLoader

load_dotenv()

loader = CSVLoader(file_path="relatorio_chamados.csv")
documents = loader.load()

embeddings = OpenAIEmbeddings()
db = FAISS.from_documents(documents, embeddings)

def retrieve_info(query):  # Corrigir nome da função
    similar_response = db.similarity_search(query, k=3)
    return [doc.page_content for doc in similar_response]

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-16k-0613")

template = """
Você é un assistente virtual de uma escola de programação focada na linguagem Python.
Sua função será responder e-mails que recebemos de potenciais clientes.
Vou The passar alguns e-mails antigos enviados por nosso time de vendas para que você use como mode
Siga todas as regras abaixo:
1/ Você deve buscar se comportar de maneira semelhante à Equipe PNCP.
2/ Suas respostas devem ser bem similares ou até identicas às enviadas por ela no passado, tanto en termos de comprimento, ton de voz, argumentos lógicos e demais detalhes.
3/ Alguns dos e-mails podem conter links e informações irrelevantes. Preste atenção apenas ao conteúdo útil da mensagem.
Aqui esta uma mensagen recebida de um novo cliente.
{message}
Aqui está uma lista de e-mails trocados anteriormente entre outros clientes e nossa atendente.Aqui está uma lista de e-mails trocados anteriormente entre outros clientes e nossa atendente. Este histórico de conversa servirá de base para que você compreenda nossos produto e forma de atender
{best_practice}
Escreva a melhor resposta que eu deveria enviar para este potencial cliente:"""

prompt = PromptTemplate(
    input_variables=["message", "best_practice"],
    template=template
)

chain = LLMChain(llm=llm, prompt=prompt)

def generate_response(message):
    best_practice = retrieve_info(message)
    response = chain.run(message=message, best_practice=best_practice)
    return response

generate_response("""como se cadastrar no PNCP?""")

resposta = """'Olá,\n\nObrigado pelo seu interesse em se cadastrar no PNCP!\n\nPara se cadastrar no PNCP, você precisa seguir os seguintes passos:\n\n1. Acesse o site oficial do PNCP: https://treina.pncp.gov.br/app/\n2. Clique no botão "Cadastrar" localizado na página inicial.\n3. Preencha o formulário de cadastro com suas informações pessoais, como nome, e-mail e telefone.\n4. Após preencher o formulário, clique em "Enviar" para concluir o cadastro.\n5. Aguarde a confirmação do seu cadastro por e-mail. Certifique-se de verificar sua caixa de entrada e também a pasta de spam.\n\nCaso você já tenha realizado o cadastro e esteja enfrentando dificuldades para acessar o PNCP devido a um erro de não reconhecimento do certificado, recomendamos que siga as seguintes orientações:\n\n1. Verifique se o seu navegador está atualizado para a versão mais recente. Caso não esteja, atualize-o e tente novamente.\n2. Limpe o cache e os cookies do seu navegador. Isso pode ajudar a resolver problemas de carregamento de páginas.\n3. Certifique-se de que o certificado de segurança do PNCP está instalado corretamente no seu navegador. Caso contrário, entre em contato com o suporte técnico para obter assistência na instalação do certificado.\n\nEsperamos que essas informações sejam úteis para você. Se tiver mais alguma dúvida ou precisar de mais assistência, não hesite em nos contatar.\n\nAtenciosamente,\nEquipe PNCP'
"""

print(resposta)

# def main():
#     st.set_page_config(
#         page_title="E-mail menager", page_icon=":bird")
#     st.header("E-mail menager")
#     message = st.text_area("E-mail do cliente")

#     if message:
#         st.write("gerando um e-mail baseado nas melhores praticas...")

#         result = generate_response(message)

#         st.info(result)
# if __name__== '__main__':
#     main()
