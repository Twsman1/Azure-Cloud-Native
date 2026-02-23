import streamlit as st
from azure.storage.blob import BlobServiceClient
import os
import pymssql
import uuid
import json
from dotenv import load_dotenv
load_dotenv()

BlobConnectionString = os.getenv("BLOB_CONNECTION_STRING")
BlobContainerName = os.getenv("BLOB_CONTAINER_NAME")
BlobAccountName = os.getenv("BLOB_ACCOUNT_NAME")

sql_server = os.getenv("SQL_SERVER")
sql_database = os.getenv("SQL_DATABASE")
sql_user = os.getenv("SQL_USER")
sql_password = os.getenv("SQL_PASSWORD")

st.title("Cadastro de Produtos")

# Formulário de cadastro de produtos
product_name = st.text_input("Nome do Produto")
product_price = st.number_input("Preço do Produto", min_value=0.0, format="%.2f")
product_description = st.text_area("Descrição do Produto")
product_image = st.file_uploader("Imagem do Produto", type=["jpg", "jpeg", "png"])

#Save image to Azure Blob Storage
def save_image_to_blob(image_file):
    if image_file is None:
        return None
    blob_service_client = BlobServiceClient.from_connection_string(BlobConnectionString)
    container_client = blob_service_client.get_container_client(BlobContainerName)
    blob_name = f"{uuid.uuid4()}_{image_file.name}"
    blob_client= container_client.get_blob_client(blob_name)
    blob_client.upload_blob(image_file.read(), overwrite=True)
    image_url = f"https://{BlobAccountName}.blob.core.windows.net/{BlobContainerName}/{blob_name}"
    return image_url

def insert_product_to_db(nome, descrição, preço, image_url):
    try:
        conn = pymssql.connect(server=sql_server, user= sql_user, password=sql_password, database=sql_database)
        cursor = conn.cursor()
        insert_sql = "INSERT INTO Produtos (nome, descrição, preço, image_url) VALUES ('{nome}', '{descrição}', {preço}, '{image_url}')".format(nome=nome, descrição=descrição, preço=preço, image_url=image_url)
        cursor.execute(insert_sql)
        print(insert_sql)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Error ao inserir o produto: {e}")
        return False
    
def list_products_from_db():
    try:
        conn = pymssql.connect(server=sql_server, user= sql_user, password=sql_password, database=sql_database)
        cursor = conn.cursor()
        select_sql = "SELECT id, nome, descrição, preço, image_url FROM Produtos"
        cursor.execute(select_sql)
        products = cursor.fetchall()
        cursor.close()
        conn.close()
        return products
    
    except Exception as e:
        st.error(f"Error ao listar os produtos: {e}")
        return []
    
def list_products_screen():
    products = list_products_from_db()
    if products:
        for product in products:
            st.subheader(product[1])  # Nome do produto
            st.write(f"Descrição: {product[2]}")  # Descrição do produto
            st.write(f"Preço: R$ {product[3]:.2f}")  # Preço do produto
            if product[4]:  # Verifica se há uma URL de imagem
                st.image(product[4], width=200)  # Exibe a imagem do produto


if st.button("Cadastrar Produto"):
    if insert_product_to_db(product_name, product_description, product_price, save_image_to_blob(product_image)):
        st.success("Produto cadastrado com sucesso!")
    

st.header("Produtos Cadastrados")

if st.button("Listar Produtos"):
    list_products_screen()
    return_message = "Produtos listados com sucesso!"