from pprint import pprint as pp

import chainlit as cl
from chainlit.input_widget import Select, Slider

from vertexai.generative_models import FunctionDeclaration, GenerativeModel, Part, Tool

import config as c
import api as t

PROJECT_ID = c.PROJECT_ID


get_inventry_func = FunctionDeclaration(
    name="get_inventry",
    description="Retrieve inventory information corresponding to the request",
    parameters={
        "type": "object",
        "properties": {
            "store_name": {
                "type": "string",
                "description": "store name",
            },
            "product_name": {
                "type": "string",
                "description": "product name",
            },
        },
        "required": ["store_name", "product_name"]
    },
)

model = GenerativeModel(
            t.default_model,
            # generation_config={"temparature":0},
            tools=[Tool(function_declarations=[get_inventry_func])],
        )

@cl.set_chat_profiles
async def _set_chat_profile():
    profiles = []
    return profiles

@cl.on_chat_start
async def _on_chat_start():

    content = "在庫情報を聞いてください"
    await cl.Message(content=content).send()

@cl.on_settings_update
async def setup_runnable(settings):
    profile = cl.user_session.get("chat_profile")
    return profile

@cl.on_message
async def _on_message(message: cl.Message):

    chat = model.start_chat()

    print(message.content)
    prompt = f"""
    {message.content}
    """

    response = chat.send_message(prompt)
    response = response.candidates[0].content.parts[0]
    i = t.InventoryRequest(**response.function_call.args)

    content = "見つからないので、再度、入力してね"
    try:

        if response.function_call.name == "get_inventry":
            pp("get_inventry")
            inventry = t.get_inventory(i)
            pp(inventry)
            content = inventry

    except Exception as e:
        content = str(e)
    finally:
        res = cl.Message(content=content)
        await res.send()

