import streamlit as st
from agent.roi_chat_agent import agent
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import json
import logging
import uuid
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load system prompt
def load_system_prompt():
    try:
        with open('prompts/system_prompt.md', 'r') as file:
            return file.read().strip()
    except Exception as e:
        logger.error(f"Error loading system prompt: {str(e)}")
        return "You are an AI ROI calculation assistant specialized in helping businesses evaluate investments in AI and robotics solutions."

# Set page config
st.set_page_config(
    page_title="AIRE ROI AI Assistant",
    page_icon="💰",
    layout="wide"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())
if "language" not in st.session_state:
    st.session_state.language = "English"  # Set default to English

# Language-specific content
content = {
    "Estonian": {
        "title": "AIRE ROI AI Assistent",
        "welcome": "Tere tulemast AIRE ROI AI Assistent-i! See bot aitab teil hinnata AI ja robootika investeeringute tasuvust.",
        "capabilities": [
            "Arvutada investeeringu tasuvusnäitajaid (NPV, IRR, tasuvusaeg)",
            "Analüüsida majanduslikku efekti",
            "Pakkuda näiteid ja vihjeid",
            "Selgitada finantsmõisteid lihtsas keeles"
        ],
        "buttons": {
            "roi_calculation": "Kuidas arvutada investeeringu tasuvust?",
            "ai_costs": "Millised on tüüpilised AI investeeringu kulud?",
            "labor_savings": "Kuidas hinnata tööjõukulude kokkuhoidu?",
            "npv_explanation": "Mis on NPV ja kuidas seda arvutada?",
            "irr_calculation": "Kuidas arvutada IRR-i?",
            "payback_period": "Milline on optimaalne tasuvusaeg?"
        },
        "chat_placeholder": "Kuidas saan teid aidata?",
        "error_message": "Vabandust, tekkis viga. Palun proovige uuesti.",
        "refresh": "Värskenda vestlust",
        "aire_link": "Külasta AIRE kodulehte",
        "metrics": {
            "title": "Tasuvusnäitajate selgitused",
            "npv": {
                "title": "NPV (Net Present Value)",
                "points": [
                    "Näitab investeeringu praegust väärtust",
                    "Positiivne NPV tähendab kasumlikku investeeringut"
                ]
            },
            "irr": {
                "title": "IRR (Internal Rate of Return)",
                "points": [
                    "Näitab investeeringu tasuvusmäära",
                    "Mida kõrgem IRR, seda parem investeering"
                ]
            },
            "payback": {
                "title": "Tasuvusaeg",
                "points": [
                    "Aeg, mis kulub investeeringu tagasi teenimiseks",
                    "Lühem tasuvusaeg on parem"
                ]
            }
        },
        "inflation": {
            "title": "Kulude indekseerimine",
            "points": [
                "Tööjõukulud: 4-5% aastas",
                "Muud kulud: 2-2.5% aastas",
                "Brutokasum: võrdne kulude indekseerimisega või pisut kõrgem"
            ]
        }
    },
    "English": {
        "title": "AIRE ROI AI Assistant",
        "welcome": "Welcome to AIRE ROI AI Assistant! This bot helps you evaluate the return on investment for AI and robotics solutions.",
        "capabilities": [
            "Calculate investment return metrics (NPV, IRR, payback period)",
            "Analyze economic impact",
            "Provide examples and tips",
            "Explain financial concepts in simple terms"
        ],
        "buttons": {
            "roi_calculation": "How to calculate investment return?",
            "ai_costs": "What are typical AI investment costs?",
            "labor_savings": "How to estimate labor cost savings?",
            "npv_explanation": "What is NPV and how to calculate it?",
            "irr_calculation": "How to calculate IRR?",
            "payback_period": "What is the optimal payback period?"
        },
        "chat_placeholder": "How can I help you?",
        "error_message": "Sorry, an error occurred. Please try again.",
        "refresh": "Refresh Conversation",
        "aire_link": "Visit AIRE website",
        "metrics": {
            "title": "ROI Metrics Explained",
            "npv": {
                "title": "NPV (Net Present Value)",
                "points": [
                    "Shows the present value of the investment",
                    "Positive NPV indicates a profitable investment"
                ]
            },
            "irr": {
                "title": "IRR (Internal Rate of Return)",
                "points": [
                    "Shows the investment's rate of return",
                    "Higher IRR means better investment"
                ]
            },
            "payback": {
                "title": "Payback Period",
                "points": [
                    "Time needed to recover the investment",
                    "Shorter payback period is better"
                ]
            }
        },
        "inflation": {
            "title": "Cost Indexation",
            "points": [
                "Labor costs: 4-5% annually",
                "Other costs: 2-2.5% annually",
                "Gross profit: equal to or slightly higher than cost indexation"
            ]
        }
    }
}

# Title and description
st.title(content[st.session_state.language]["title"])
st.markdown(content[st.session_state.language]["welcome"])

# Display capabilities
st.markdown("**Bot can:**")
for capability in content[st.session_state.language]["capabilities"]:
    st.markdown(f"- {capability}")

# Create two rows of buttons with typical questions
col1, col2, col3 = st.columns(3)

with col1:
    if st.button(content[st.session_state.language]["buttons"]["roi_calculation"]):
        st.session_state.messages.append({"role": "user", "content": content[st.session_state.language]["buttons"]["roi_calculation"]})
        st.rerun()
with col2:
    if st.button(content[st.session_state.language]["buttons"]["ai_costs"]):
        st.session_state.messages.append({"role": "user", "content": content[st.session_state.language]["buttons"]["ai_costs"]})
        st.rerun()
with col3:
    if st.button(content[st.session_state.language]["buttons"]["labor_savings"]):
        st.session_state.messages.append({"role": "user", "content": content[st.session_state.language]["buttons"]["labor_savings"]})
        st.rerun()

col4, col5, col6 = st.columns(3)

with col4:
    if st.button(content[st.session_state.language]["buttons"]["npv_explanation"]):
        st.session_state.messages.append({"role": "user", "content": content[st.session_state.language]["buttons"]["npv_explanation"]})
        st.rerun()
with col5:
    if st.button(content[st.session_state.language]["buttons"]["irr_calculation"]):
        st.session_state.messages.append({"role": "user", "content": content[st.session_state.language]["buttons"]["irr_calculation"]})
        st.rerun()
with col6:
    if st.button(content[st.session_state.language]["buttons"]["payback_period"]):
        st.session_state.messages.append({"role": "user", "content": content[st.session_state.language]["buttons"]["payback_period"]})
        st.rerun()

# Add a separator
st.markdown("---")

# Chat interface
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Process any pending messages
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    # Get agent response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Convert messages to LangChain format
            messages = []
            for msg in st.session_state.messages:
                if msg["role"] == "user":
                    messages.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    messages.append(AIMessage(content=msg["content"]))
            
            # Add system message if not present
            if not any(isinstance(msg, SystemMessage) for msg in messages):
                messages = [SystemMessage(content=load_system_prompt())] + messages
            
            # Ensure the last message is from the user
            if not isinstance(messages[-1], HumanMessage):
                raise ValueError("Last message must be from user")
            
            # Run agent with config
            logger.info("Starting agent processing")
            response = agent.invoke(
                {"messages": messages},
                config={"configurable": {"thread_id": st.session_state.thread_id}}
            )
            
            # Process and display response
            if isinstance(response, dict) and "messages" in response:
                last_message = response["messages"][-1]
                if isinstance(last_message, AIMessage):
                    full_response = last_message.content
                else:
                    full_response = str(last_message)
            else:
                full_response = str(response)
            
            message_placeholder.markdown(full_response)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            logger.error(f"Error in agent processing: {str(e)}")
            st.error(f"Error: {str(e)}")
            st.session_state.messages.append({"role": "assistant", "content": content[st.session_state.language]["error_message"]})

# Chat input
if prompt := st.chat_input(content[st.session_state.language]["chat_placeholder"]):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# Sidebar with information
with st.sidebar:
    # Language selector
    st.header("Language / Keel")
    language = st.radio(
        "Select language / Vali keel",
        ["English", "Estonian"],
        index=0 if st.session_state.language == "English" else 1,
        key="language_selector"
    )
    if language != st.session_state.language:
        st.session_state.language = language
        st.rerun()
    
    # AIRE link
    st.markdown(f"[{content[st.session_state.language]['aire_link']}](https://aire-edih.eu/en/)")
    
    # Refresh button
    if st.button(content[st.session_state.language]["refresh"]):
        st.session_state.messages = []
        st.session_state.thread_id = str(uuid.uuid4())
        st.rerun()
    
    # ROI Metrics
    st.header(content[st.session_state.language]["metrics"]["title"])
    st.markdown(f"**{content[st.session_state.language]['metrics']['npv']['title']}**")
    for point in content[st.session_state.language]["metrics"]["npv"]["points"]:
        st.markdown(f"- {point}")
    
    st.markdown(f"**{content[st.session_state.language]['metrics']['irr']['title']}**")
    for point in content[st.session_state.language]["metrics"]["irr"]["points"]:
        st.markdown(f"- {point}")
    
    st.markdown(f"**{content[st.session_state.language]['metrics']['payback']['title']}**")
    for point in content[st.session_state.language]["metrics"]["payback"]["points"]:
        st.markdown(f"- {point}")
    
    # Cost Indexation
    st.header(content[st.session_state.language]["inflation"]["title"])
    for point in content[st.session_state.language]["inflation"]["points"]:
        st.markdown(f"- {point}")
    
    # References
    st.markdown("---")
    st.markdown("**Built with:**")
    st.markdown("- [Mistral AI](https://mistral.ai/)")
    st.markdown("- [LangChain](https://www.langchain.com/)")
    st.markdown("- [Streamlit](https://streamlit.io/)")
