# TenProject Download Site

Este é o site de downloads oficial do TenProject, construído com [Streamlit](https://streamlit.io/).

## 📁 Estrutura

- `app.py`: Código principal do site.
- `downloads/`: Pasta onde ficam os executáveis (.exe) que serão oferecidos para download.
- `requirements.txt`: Dependências do Python.

## 🚀 Como Rodar Localmente

1.  **Instale as dependências**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Coloque o executável**:
    Certifique-se de que o arquivo `TenProject.exe` está dentro da pasta `downloads`.

3.  **Inicie o site**:
    ```bash
    streamlit run app.py
    ```

## ☁️ Como Hospedar no Streamlit Community Cloud (Grátis)

Para colocar este site no ar gratuitamente pelo Streamlit:

### 1. Preparar o Repositório GitHub
Como seu arquivo `.exe` tem **mais de 100MB**, você **PRECISA** usar o **Git LFS (Large File Storage)**, caso contrário o GitHub rejeitará o envio.

1.  **Instale o Git LFS**:
    - Baixe e instale: https://git-lfs.com/
    - No terminal, na pasta do projeto, rode:
      ```bash
      git lfs install
      ```

2.  **Configure o LFS para rastrear o executável**:
    ```bash
    git lfs track "downloads/*.exe"
    ```
    *(Isso cria um arquivo `.gitattributes` que deve ser commitado)*

3.  **Suba para o GitHub**:
    Crie um **novo repositório** no GitHub (ex: `TenProject-Downloads`) e suba os arquivos:
    ```bash
    git init
    git add .
    git commit -m "Initial commit with LFS"
    git branch -M main
    git remote add origin https://github.com/SEU_USUARIO/NOME_DO_REPO.git
    git push -u origin main
    ```

### 2. Conectar ao Streamlit Cloud
1.  Acesse [share.streamlit.io](https://share.streamlit.io/).
2.  Faça login com seu GitHub.
3.  Clique em **"New app"**.
4.  Selecione o repositório que você acabou de criar.
5.  Em "Main file path", coloque `app.py`.
6.  Clique em **"Deploy!"**.

O Streamlit vai baixar seu repositório (incluindo o arquivo grande via LFS) e colocar o site no ar.
