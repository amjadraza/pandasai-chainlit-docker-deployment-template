"""Python file to serve as the frontend"""
import sys
import os
import pandas as pd
import io
sys.path.append(os.path.abspath('.'))

from demo_app._utils import generate_pandasai_response

import chainlit as cl

from chainlit.types import AskFileResponse


def process_file(file: AskFileResponse):
    import tempfile

    with tempfile.NamedTemporaryFile() as tempfile:
        tempfile.write(file.content)
        df = pd.read_csv(tempfile.name)

    print(df.head(5))

    return df

@cl.on_chat_start
async def on_chat_start():
    files = await cl.AskFileMessage(
        content="Please upload a CSV file", accept=["text/csv"]
    ).send()
    file = files[0]
    csv_file = io.BytesIO(file.content)
    df = pd.read_csv(csv_file, encoding="latin1")
    cl.user_session.set('data', df)
    await cl.Message(
        content="The first 5 rows of the file are:\n" + str(df.head())
    ).send()


@cl.on_message
async def main(message: str):
    # Your custom logic goes here...

    # Use PandasAI to Run the Query on Uploaded CSV file
    answer = generate_pandasai_response(df=cl.user_session.get('data'),
                                        prompt=message,
                                        model_option="OpenAI",
                                        is_conversational_answer=True,
                                        is_verbose=True)

    # Send a response back to the user
    await cl.Message(
        content=answer,
    ).send()