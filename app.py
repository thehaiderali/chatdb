from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import sqlite3
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# ---- Context / Schema ----
context = """
Table: users(id, name, email, created_at)
Table: posts(id, user_id, title, content, created_at)
Table: comments(id, post_id, user_id, content, created_at)
"""

# ---- Prompt Template ----
template = """
You are a helpful assistant that converts user requests into SQL queries.

Database Schema:
{context}

User Request:
{query}

Instructions:
- Use only the tables and fields from the schema.
- Generate a correct SQL query that matches the user request.
- Do not add explanations, comments, or markdown formatting.
- Only output the SQL query.
"""

sql_prompt = PromptTemplate(
    input_variables=["context", "query"],
    template=template,
)

# ---- Helpers ----
def clean_sql(sql: str) -> str:
    """Remove unwanted formatting like markdown fences from SQL output."""
    return sql.strip().replace("```sql", "").replace("```", "").strip()

def getResponse(query: str) -> str:
    """Ask the LLM to convert natural language into SQL."""
    formatted_prompt = sql_prompt.format(context=context, query=query)
    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        api_key=os.getenv("GEMINI_API_KEY")
    )
    sql = model.invoke(formatted_prompt)
    return clean_sql(sql.content)

def runSQL(sql: str):
    """Run the SQL query against SQLite and return DataFrame."""
    conn = sqlite3.connect("test.db")
    try:
        df = pd.read_sql_query(sql, conn)
    except Exception as e:
        st.error(f"⚠️ SQL Error: {e}")
        df = pd.DataFrame()
    conn.close()
    return df

# ---- Streamlit UI ----
st.title("🗄️ Talk to Database in English")

query = st.text_input("💬 Enter your query:")

if query:
    with st.spinner("🤖 Thinking... generating SQL query..."):
        sql = getResponse(query)
        st.code(sql, language="sql")  # Show the generated SQL

    with st.spinner("📊 Running SQL on database..."):
        result_df = runSQL(sql)

    if not result_df.empty:
        st.success("✅ Query executed successfully!")
        st.dataframe(result_df, use_container_width=True)
    else:
        st.warning("No results found or invalid query.")
