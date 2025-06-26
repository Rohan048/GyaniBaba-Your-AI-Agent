import streamlit as st
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage

# --- Streamlit UI Setup ---
st.set_page_config(page_title="GyaniBaba.ai", page_icon="🤖", layout="wide")

# Custom CSS
st.markdown("""
    <style>
        .stChatMessage {
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 10px;
        }
        .stChatMessage.user {
            background-color: #E6F3FF;
        }
        .stChatMessage.assistant {
            background-color: #F0F0F0;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("🧠 GyaniBaba-Your AI Agent")
st.caption("Bharosa rakh Bhai ☺️, yeh GyaniBaba tujhe web se sahi info dhoondh ke, simple words mein samjha dega!❤️")
st.markdown("<script>window.scrollTo(0, document.body.scrollHeight);</script>", unsafe_allow_html=True)


# --- Load API Keys ---
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# --- Check if Tavily is Needed ---
def should_use_tavily(user_query):
    keywords = ["latest", "news", "current", "today", "trending", "update", "who won", "match", "live", "price", "stock", "weather"]
    return any(word in user_query.lower() for word in keywords)

# --- Get Agent Based on Tool Use ---
def get_agent_executor(use_tavily):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2, api_key=OPENAI_API_KEY)

    tools = []
    if use_tavily:
        tools = [
            TavilySearchResults(
                max_results=7,
                name="web_search",
                api_key=TAVILY_API_KEY,
                description="Performs web searches"
            )
        ]

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful research assistant. Answer using markdown and be informative."),
        MessagesPlaceholder("chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ])

    agent = create_tool_calling_agent(llm, tools, prompt_template)

    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=10,
        return_intermediate_steps=True
    )

# --- Chat History State ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


for msg in st.session_state.chat_history:
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(msg.content)

# --- User Input ---
user_query = st.chat_input("Ask a question...")

if user_query:
    st.session_state.chat_history.append(HumanMessage(content=user_query))
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        with st.spinner("🧠 Thinking & Researching..."):
            try:
                use_tavily = should_use_tavily(user_query)
                agent_executor = get_agent_executor(use_tavily)

                response = agent_executor.invoke({
                    "input": user_query,
                    "chat_history": st.session_state.chat_history[:-1]
                })

                answer = response["output"]
                st.session_state.chat_history.append(AIMessage(content=answer))
                st.markdown(answer)

            except Exception as e:
                st.error(f"😕 Apologies, an error occurred: {str(e)}")
                print(f"Error: {e}")

if user_query is None:
    st.info("💬 Type your question below to begin!")
