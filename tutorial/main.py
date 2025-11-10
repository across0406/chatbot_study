import uvicorn # type: ignore
from fastapi import FastAPI # type: ignore
from pydantic import BaseModel # type: ignore

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, ForeignKey, insert # type: ignore
from sqlalchemy.engine import Engine # type: ignore

from langchain_community.utilities import SQLDatabase # type: ignore
from langchain_ollama import ChatOllama # type: ignore
# from langchain_community.agent_toolkits import create_sql_agent # type: ignore
from langchain_experimental.sql import SQLDatabaseChain # type: ignore
# from langchain.agents import AgentExecutor

from db_manager.db_config_manager import DbConfigManager


db_config_manager: DbConfigManager = DbConfigManager('tutorial/db-config-local-example.json')
url: str = f"postgresql+psycopg2://" + \
            f"{db_config_manager.get_config()['id']}:{db_config_manager.get_encode_pw()}" + \
            f"@{db_config_manager.get_config()['host']}:{db_config_manager.get_config()['port']}/{db_config_manager.get_config()['dbName']}"

try:
    engine: Engine = create_engine(url)
    with engine.connect() as conn:
        print(f"Succeed to PostgreSQL DB connection!")
except Exception as ex:
    print(f"Failed to connect DB: {ex}")
    exit()

db: SQLDatabase = SQLDatabase(engine, include_tables=['materials', 'purchase_requests'])
# llm: ChatOllama = ChatOllama(model="solar", temperature=0)
llm: ChatOllama = ChatOllama(model="llama3:8b", temperature=0)
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True) # type: ignore
# agent_executor: AgentExecutor = create_sql_agent(
#     llm=llm,
#     db=db,
#     agent_type="openai-tools", 
#     verbose=True
# )
print("Complete to initialize SQLDatabaseChain (Model: SOLAR, DB: PostgreSQL)")

app: FastAPI = FastAPI(
    title="ChatBot API for Material Management (SOLAR + PostgreSQL w/ chatbot_admin user)", 
    description="Get the response from database by converting the question in natural language into SQL."
)

class QueryRequest(BaseModel):
    question: str


@app.post("/ask", summary="Asking for material management database in natural language")
async def ask_question(request: QueryRequest): # type: ignore
    try:
        result = await db_chain.ainvoke(request.question) # type: ignore
        return {
            "answer": result.get( # type: ignore
                    "result", 
                    "Cannot generate the answer.") 
                }
    except Exception as ex:
        print(f"Error: {ex}")
        return {
            "error": f"The error is caused while processing asking: {str(ex)}"
        }