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

print(config_list_4v)

config_list_gpt4 = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    file_location=".",
    filter_dict={
        "model": ["gpt-4"],
    },
)
print(config_list_gpt4)


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

# Ask the question with an image
user_proxy.initiate_chat(image_agent, 
                         message="""extract text name and address from below image. 
<img https://upload.wikimedia.org/wikipedia/commons/c/cb/BankStatementChequing.png>.""")


