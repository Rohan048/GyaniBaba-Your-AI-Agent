# import streamlit as st
# from langchain_core.messages import HumanMessage, AIMessage

# # UI implement
# st.set_page_config(page_title="GyaniBaba.ai", page_icon="🤖", layout="wide")

# # Adding CSS
# st.markdown("""
#    <style>
#    .stChatMessage {
#        border-radius: 10px;
#        padding: 10px;
#        margin-bottom: 10px;
#    }

#    .stChatMessage.user {
#        background-color: #E6F3FF;
#    }

#    .stChatMessage.assistant {
#        background-color: #F0F0F0;
#    }
#    </style>
# """, unsafe_allow_html=True)


# import os
# from dotenv import load_dotenv
# from langchain_openai import ChatOpenAI
# from langchain_community.tools.tavily_search import TavilySearchResults
# from langchain.agents import AgentExecutor, create_tool_calling_agent
# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain_core.messages import AIMessage, HumanMessage

# # Step-1(Api Call)
# load_dotenv()
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# # Step-2(Create Agent)
# @st.cache_resource
# def get_agent_executor():
#    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2, api_key=OPENAI_API_KEY)

#    tools = [
#        TavilySearchResults(
#            max_results=7,
#            name="web_search",
#            api_key=TAVILY_API_KEY,
#            description="Performs web searches"
#        )
#    ]

#    prompt_template = ChatPromptTemplate.from_messages([
#        ("system", "You are a research assistant..."),
#        MessagesPlaceholder("chat_history", optional=True),
#        ("human", "{input}"),
#        MessagesPlaceholder("agent_scratchpad"),
#    ])

#    agent = create_tool_calling_agent(llm, tools, prompt_template)

#    return AgentExecutor(
#        agent=agent,
#        tools=tools,
#        verbose=True,
#        handle_parsing_errors=True,
#        max_iterations=10,
#        return_intermediate_steps=True
#    )

# def should_use_tavily(user_query):
#     """
#     Simple logic to decide if Tavily API is needed.
#     You can make it more advanced with NLP/LLMs.
#     """
#     keywords = ["latest", "news", "current", "today", "trending", "update", "who won", "match", "live", "price", "stock", "weather"]
    
#     for word in keywords:
#         if word.lower() in user_query.lower():
#             return True
#     return False


# st.title("🧠 GyaniBaba-Your AI Agent")
# st.caption("Bharosa rakh Bhai ☺️, yeh GyaniBaba tujhe web se sahi info dhoondh ke, simple words mein samjha dega!❤️")

# # CHAT HISTORY
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []

# for message_obj in st.session_state.chat_history:
#     role = "user" if isinstance(message_obj, HumanMessage) else "assistant"
#     with st.chat_message(role):
#         st.markdown(message_obj.content)

# # USER INPUT
# user_query = st.chat_input("Ask a question...")


# if user_query:
#     st.session_state.chat_history.append(HumanMessage(content=user_query))

#     with st.chat_message("user"):
#         st.markdown(user_query)

#     with st.chat_message("assistant"):
#         with st.spinner("🧠 Thinking & Researching..."):
#             try:
#                 agent_executor = get_agent_executor()

#                 response = agent_executor.invoke({
#                     "input": user_query,
#                     "chat_history": st.session_state.chat_history[:-1]
#                 })

#                 answer = response["output"]
#                 st.session_state.chat_history.append(AIMessage(content=answer))
#                 st.markdown(answer)

#             except Exception as e:
#                 error_message = f"😕 Apologies, an error occurred: {str(e)}"
#                 st.error(error_message)
#                 print(f"Error during agent invocation: {e}")

# # venv\Scripts\python.exe -m streamlit run app.py -- for excution