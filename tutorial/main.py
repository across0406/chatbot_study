import uvicorn # type: ignore
from fastapi import FastAPI # type: ignore
from pydantic import BaseModel # type: ignore

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, ForeignKey, insert # type: ignore
from sqlalchemy.engine import Engine # type: ignore

from langchain_community.utilities import SQLDatabase # type: ignore
from langchain_ollama import ChatOllama # type: ignore
# from langchain_community.agent_toolkits import create_sql_agent # type: ignore
# from langchain_experimental.sql import SQLDatabaseChain # type: ignore
# from langchain.agents import AgentExecutor
from langchain_core.prompts import ChatPromptTemplate # type: ignore
from langchain_core.output_parsers import StrOutputParser # type: ignore
from langchain_core.runnables import  RunnablePassthrough # type: ignore
from operator import itemgetter # type: ignore

from db_manager.db_config_manager import DbConfigManager


db_config_manager: DbConfigManager = DbConfigManager('tutorial/db-config-local-example.json')
url: str = f"postgresql+psycopg2://" + \
            f"{db_config_manager.get_config()['id']}:{db_config_manager.get_encode_pw()}" + \
            f"@{db_config_manager.get_config()['host']}:{db_config_manager.get_config()['port']}/{db_config_manager.get_config()['dbName']}"
engine: Engine = None

try:
    engine = create_engine(url) # type: ignore
    with engine.connect() as conn: # type: ignore
        print(f"Succeed to PostgreSQL DB connection!")
except Exception as ex:
    print(f"Failed to connect DB: {ex}")
    exit()

db: SQLDatabase = SQLDatabase(engine, include_tables=['materials', 'purchase_requests']) # type: ignore
# llm: ChatOllama = ChatOllama(model="solar", temperature=0) # type: ignore
llm: ChatOllama = ChatOllama(model="llama3:8b", temperature=0) # type: ignore

# ----------------- Begin Text-to-SQL -----------------
def get_schema(_): # type: ignore
    # db.get_table_info() is standard funciton of LangChain
    return db.get_table_info() # type: ignore

SQL_GENERATION_PROMPT = """
너는 PostgreSQL 전문가입니다. 다음 테이블 스키마 정보를 사용하여,
사용자의 질문에 답하는 유효한 SQL 쿼리를 하나만 생성해 주세요.
절대로 질문 외의 설명이나 주석을 포함하지 말고, 반드시 쿼리 자체만 출력해야 합니다.
사용 가능한 테이블 정보:
{schema}

사용자 질문: {question}

SQL 쿼리: 
"""
sql_prompt = ChatPromptTemplate.from_template(SQL_GENERATION_PROMPT) # type: ignore
sql_query_chain = ( # type: ignore
    # 1. RunnablePassthrough: question 입력을 그대로 다음으로 전달
    RunnablePassthrough.assign(schema=get_schema) # type: ignore
    | sql_prompt  # 2. 프롬프트를 생성 (schema와 question을 채움)
    | llm         # 3. LLM 호출 (SQL 쿼리 생성)
    | StrOutputParser() # 4. 결과(SQL)를 문자열로 추출
)
# ----------------- End Text-to-SQL -----------------

# ----------------- Begin Data-to-Text -----------------
ANSWER_PROMPT_TEMPLATE = """
너는 '자재관리' 데이터베이스 전문가입니다.
사용자의 원본 질문과 DB에서 검색한 결과를 바탕으로, 친절하고 명확한 한국어 문장으로 답변을 생성해 주세요.
답변에는 SQL 쿼리나 영어문장이나 영어단어는 없어야합니다. 한국어로만 구성하세요.
단, 질문 자체(A 나사, B 등)에 포함된 이름 형식의 영어는 포함되어야 합니다.

원본 질문: {question}
DB 검색 결과: {context}

생성된 답변:
"""
answer_prompt = ChatPromptTemplate.from_template(ANSWER_PROMPT_TEMPLATE) # type: ignore
answer_chain = answer_prompt | llm | StrOutputParser() # type: ignore
# ----------------- End Data-to-Text -----------------


# db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True) # type: ignore
# agent_executor: AgentExecutor = create_sql_agent(
#     llm=llm,
#     db=db,
#     agent_type="openai-tools", 
#     verbose=True
# )
print("Complete to initialize SQLDatabaseChain (Model: SOLAR, DB: PostgreSQL)")

app: FastAPI = FastAPI( # type: ignore
    title="ChatBot API for Material Management (SOLAR + PostgreSQL w/ chatbot_admin user)", 
    description="Get the response from database by converting the question in natural language into SQL."
)

class QueryRequest(BaseModel): # type: ignore
    question: str


@app.post("/ask", summary="Asking for material management database in natural language") # type: ignore
async def ask_question(request: QueryRequest): # type: ignore
    try:
        sql_query = await sql_query_chain.ainvoke({ # type: ignore
            "question": request.question
        })

        # Block non-select query
        if not 'select' in sql_query.strip().lower().split(' '): # type: ignore
            return {
                "error": f"This request query is blocked."
            }
        
        sql_result = db.run(sql_query) # type: ignore
        final_answer = await answer_chain.ainvoke({ # type: ignore
            "question": request.question, 
            "context": sql_result
        })

        return {
            "answer": final_answer
        } # type: ignore

        # result = await db_chain.ainvoke(request.question) # type: ignore
        # return {
        #     "answer": result.get( # type: ignore
        #         "result", 
        #         "Cannot generate the answer.") 
        # }
    except Exception as ex:
        print(f"Error: {ex}")
        return {
            "error": f"The error is caused while processing asking: {str(ex)}"
        }