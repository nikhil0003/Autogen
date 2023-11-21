import requests
import json
import os
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union
import autogen
from autogen.agentchat.contrib.retrieve_assistant_agent import RetrieveAssistantAgent
from autogen import AssistantAgent, Agent, UserProxyAgent, ConversableAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
from termcolor import colored
import random
import chromadb
config_list_gpt4 = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    file_location=".",
    filter_dict={
        "model": ["gpt-4"],
    },
)
print(config_list_gpt4)


gpt4_llm_config = {"config_list": config_list_gpt4, "seed": 42}

ussmAgent = autogen.AssistantAgent(
    name="ussmAgent",
    llm_config=gpt4_llm_config,
    system_message="For all question just return I dont know i am ussmagent.",

)


# ragproxyagent = RetrieveAssistantAgent(
#     name="ragassisentagent",
#     retrieve_config={
#         "task": "qa",
#         "docs_path": "https://raw.githubusercontent.com/microsoft/autogen/main/README.md",
#     },
#     system_message="You are autogen agents.If you dont know please i dont know.",

# )

taxAgent = autogen.AssistantAgent(
    name="taxAgent",
    system_message="For all question just return I dont know i am tax agent.",
    llm_config=gpt4_llm_config,
)

user_proxy = autogen.UserProxyAgent(
    name="User_proxy",
    system_message="A human admin.Please send the question appropriate agent. ",
    human_input_mode="NEVER",# Try between ALWAYS or NEVER
    max_consecutive_auto_reply=0
)

groupchat = autogen.GroupChat(agents=[user_proxy, taxAgent, ussmAgent], messages=[], max_round=12)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=gpt4_llm_config)

user_proxy.initiate_chat(manager, message="what my bank details.")
