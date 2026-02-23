
# Azure Cloud Native — Product Catalog (Streamlit)

This repository contains a lightweight Azure-backed product catalog web app built with Streamlit. It demonstrates upload and storage of product images in Azure Blob Storage and persistence of product metadata in an Azure SQL (MSSQL) database.

**What was done:**
- Implemented a Streamlit UI (`main.py`) for registering products with `name`, `price`, `description`, and an image upload.
- Added image upload handling and storage in Azure Blob Storage using `azure-storage-blob`.
- Implemented persistence of product metadata to an Azure SQL database using `pymssql` (see `infos.txt` for the table DDL).
- Extracted configuration via environment variables (.env support) for secure credentials handling.

**Key files:**
- [main.py](main.py) : Streamlit application and core app logic.
- [requirements.txt](requirements.txt) : Python dependencies required to run the app.
- [infos.txt](infos.txt) : Database table DDL and informational notes.

**Environment variables** (use a `.env` file or your platform's secret store):
- `BLOB_CONNECTION_STRING`
- `BLOB_CONTAINER_NAME`
- `BLOB_ACCOUNT_NAME`
- `SQL_SERVER`
- `SQL_DATABASE`
- `SQL_USER`
- `SQL_PASSWORD`

**Database:**
Create the `Produtos` table in your Azure SQL instance using the DDL in `infos.txt`. Example schema is included in that file.

**Setup & Run (local):**
1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Provide environment variables (create a `.env` at repo root or set them in your environment).

4. Run the app:

```powershell
streamlit run main.py
```

**Usage:**
- Use the web UI to add a product (name, price, description, optional image). Images are uploaded to the configured Blob container and the app stores the resulting image URL alongside product metadata in the SQL table. Use the "Listar Produtos" button to view stored products.

**Notes & Next steps:**
- Do not commit secrets—use Azure Key Vault or pipeline secret storage for production.
- Improve input validation and parameterize SQL statements to avoid SQL injection (use parameterized queries instead of string formatting).
- Add authentication and RBAC for the app before exposing publicly.


