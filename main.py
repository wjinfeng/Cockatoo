import streamlit as st

from openai import OpenAI
from argparse import ArgumentParser
from cockatoo.agent import BaseAgent
from cockatoo.utils import set_single_bot_system

# 添加新角色的函数
def add_character():
    new_char_num = len(st.session_state.characters) + 1
    st.session_state.characters.append({
        "name": f"Character {new_char_num}",
        "prompt": ""
    })

def set_sidebar():
    with st.sidebar:
        st.title("🦜 Cockatoo")
        
        # set mode
        mode = st.radio(
            "Please select mode",
            ["Single Interactive Mode", "Multi Interactive Mode", "Visiting Mode"]
        )
        st.session_state.mode = mode 

        # set story
        story = st.text_area(
            "Story Setting",
            key="story_input",
            placeholder="Enter the story background..."
        )
        st.session_state.story = story

        # set characters
        if mode == "Single Interactive Mode":
            char_name = st.text_input(
                "Role Name", 
                key="char_name",
                placeholder="Enter character's name..."
            )
            char_prompt = st.text_area(
                "Role Setting", 
                placeholder="Enter character's personality and background..."
            )
            st.session_state.characters = [{
                "name": char_name,
                "prompt": char_prompt
            }]

        else:
            for i, char in enumerate(st.session_state.characters):
                col1, col2 = st.columns([1, 3])
                with col1:
                    char["name"] = st.text_input("Role Name", value=char["name"], key=f"name_{i}")
                with col2:
                    char["prompt"] = st.text_area("Role Setting", value=char["prompt"], 
                                                key=f"prompt_{i}",
                                                placeholder="Enter character's setting...")
            
            st.button("Add Character", on_click=add_character)


def display_single_chat(client, initial_message=None):
    if initial_message is not None:
        st.session_state.messages = initial_message
    
    # Display chat title
    st.title("💬 Chat with " + st.session_state.characters[0]["name"])
    
    # Display existing messages
    for msg in st.session_state.messages:
        if msg["role"] == "system":
            continue
        st.chat_message(msg["role"]).write(msg["content"])

    # Accept user input
    if prompt := st.chat_input("输入你的消息..."):
        # Display user message immediately
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        
        # Get AI response
        response, tokens = client.infer(st.session_state.messages)
        # Display AI response
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)



if __name__ == "__main__":
    parser = ArgumentParser()

    client = OpenAI(
        api_key="sk-Mj0YR9qDuAOyxBZ46Z9lGit8Eik4yLgchTXynJM8MlSy9dRV",
        base_url="https://api.moonshot.cn/v1"
    )

    set_sidebar()

    if st.session_state.mode == "Single Interactive Mode":
        # Initialize agent
        agent = BaseAgent(client, base_model="moonshot-v1-8k")
        system_prompt = set_single_bot_system(
            file_path="resource/single_bot_system.json",
            bot_name=st.session_state.characters[0]["name"],
            bot_prompt=st.session_state.characters[0]["prompt"],
            story=st.session_state.story
        )
        system = [{"role": "system", "content": system_prompt}]
        display_single_chat(agent, initial_message=system)
    elif st.session_state.mode == "Multi Interactive Mode":
        display_multi_chat(client)
    elif st.session_state.mode == "Visiting Mode":
        display_visiting_chat(client)
