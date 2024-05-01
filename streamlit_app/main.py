import streamlit as st
import yaml
from llm_bot import llama_bot

# Read config yaml file
with open('./streamlit_app/config.yml', 'r') as file:
    config = yaml.safe_load(file)

title = config['streamlit']['title']
avatar = {
    'user': None,
    'assistant': config['streamlit']['avatar']
}

# Set page config
st.set_page_config(
    page_title=config['streamlit']['tab_title'],
    page_icon=config['streamlit']['page_icon'],
)

# Set sidebar
st.sidebar.title("About")
st.sidebar.info(config['streamlit']['about'])

# Set logo
st.image(config['streamlit']['logo'], width=50)

# Set page title
st.title(title)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": config['streamlit']['assistant_intro_message']
    })

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=avatar[message["role"]]):
        st.markdown(message["content"], unsafe_allow_html=True)

# React to user input
if prompt := st.chat_input("Send a message"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get bot response
    api_url = config['llama']['api_url']
    headers = {"Authorization": f"Bearer {config['llama']['api_key']}"}
    personality_prompt = config['llama']['personality_prompt']
    response = llama_bot(prompt, api_url, headers, personality_prompt)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Display assistant response in chat message container
    with st.chat_message("assistant", avatar=config['streamlit']['avatar']):
        st.markdown(response, unsafe_allow_html=True)
