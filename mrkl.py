from langchain import OpenAI,LLMChain, LLMMathChain, SerpAPIWrapper, SQLDatabase, SQLDatabaseChain,PromptTemplate,Wikipedia
from langchain.agents import initialize_agent, Tool, AgentExecutor,ZeroShotAgent,AgentType
from langchain.agents import load_tools
from langchain.agents.react.base import DocstoreExplorer
from langchain.memory import ConversationBufferMemory, ReadOnlySharedMemory
from langchain.chat_models import ChatOpenAI
import os
import chainlit as cl
from dotenv import load_dotenv

load_dotenv()
input_database_url=os.environ["FOOBAR_DB_URL"]

@cl.on_chat_start
def start():
    llm = ChatOpenAI(temperature=0, streaming=True)
    llm1 = OpenAI(temperature=0, streaming=True)
    search = SerpAPIWrapper()
    llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)
    db = SQLDatabase.from_uri(input_database_url)
    db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)
    docstore = DocstoreExplorer(Wikipedia())

    template = """This is a conversation between a human and a bot:
    {chat_history}
    Write a summary of the conversation for {input}:
    """

    prompt = PromptTemplate(input_variables=["input", "chat_history"], template=template)
    memory = ConversationBufferMemory(memory_key="chat_history")
    readonlymemory = ReadOnlySharedMemory(memory=memory)
    summry_chain = LLMChain(
        llm=OpenAI(),
        prompt=prompt,
        verbose=True,
        memory=readonlymemory,  # use the read-only memory to prevent the tool from modifying the memory
    )

    tools = [
        Tool(
            name="Search",
            func=search.run,
            description="useful for when you need to answer questions about current events. You should ask targeted questions",
        ),
        Tool(
            name="Calculator",
            func=llm_math_chain.run,
            description="useful for when you need to answer questions about math",
        ),
   	 Tool(
            name="FooBar",
            func=db_chain.run,
          description="useful for when you need to answer questions about FooBar. Input should be in the form of a question containing full context"
       ),
       Tool(
           name="Summary",
           func=summry_chain.run,
           description="useful for when you summarize a conversation. The input to this tool should be a string, representing who will read this summary.",
       )
    ]

    ## more tools
    tools2 = load_tools(["terminal","wikipedia"], llm=llm1)
    tools2[0].name = "terminal"
    tools2[1].name = "wiki"

    agent_chain = initialize_agent(
        tools+tools2, llm1, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True, memory=memory
    )
    cl.user_session.set("cagent", agent_chain)

@cl.on_message
async def main(message):
    cagent = cl.user_session.get("cagent")  # type: AgentExecutor
    cb = cl.LangchainCallbackHandler(stream_final_answer=True)

    await cl.make_async(cagent.run)(message, callbacks=[cb])
