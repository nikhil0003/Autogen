import requests
import json
import os
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union
import autogen
from autogen import AssistantAgent, Agent, UserProxyAgent, ConversableAgent
from termcolor import colored
import random
from autogen.agentchat.contrib.multimodal_conversable_agent import MultimodalConversableAgent

config_list_4v = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    file_location=".",
    filter_dict={
        "model": ["gpt-4-vision-preview"],
    },
)


config_list_gpt4 = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    file_location=".",
    filter_dict={
        "model": ["gpt-4"],
    },
)


gpt4_llm_config = {"config_list": config_list_gpt4, "seed": 42}

for config in config_list_4v:
    config.pop("api_type", None)

image_agent = MultimodalConversableAgent(
    name="image-explainer",
    max_consecutive_auto_reply=10,
    llm_config={"config_list": config_list_4v, "temperature": 0.5, "max_tokens": 300}
)


user_proxy = autogen.UserProxyAgent(
    name="User_proxy",
    system_message="A human admin.",
    human_input_mode="NEVER", # Try between ALWAYS or NEVER
    max_consecutive_auto_reply=0
)


wokmarketAgent = autogen.AssistantAgent(
    name="Workmarket Support Agent",
    llm_config=gpt4_llm_config,
    system_message="""You are a workmarket support agent. If you dont know answer reply to User_proxy with "I don't know answer.Please contact workmarket support team." """
)

# Ask the question with an image
user_proxy.initiate_chat(image_agent, 
                         message="""extract text below image and file the follwing fields 
                         name:____, accountNumber:______ 
<img https://upload.wikimedia.org/wikipedia/commons/c/cb/BankStatementChequing.png>.""")


