import websockets, asyncio
import openai
import os
import json
from dotenv import load_dotenv
import time
load_dotenv('.env')
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
openai.api_key = OPENAI_API_KEY
async def get_openai_response(prompt, model='gpt-3.5-turbo', max_tokens=1000, temperature = 0.4):
    response = openai.ChatCompletion.create(
        model = model,
        messages = [
            {'role':'user','content':prompt}
        ],
        max_tokens = max_tokens,
        temperature = temperature
    )
    return response['choices'][0]['message'].get('content', '')

async def get_openai_response_v2( prompt, model='gpt-3.5-turbo', max_tokens=1000, temperature = 0.4,):
    response = openai.ChatCompletion.create(
        model = model,
        messages = [
            {'role':'user','content':prompt}
        ],
        # max_tokens = max_tokens,
        temperature = temperature,
        stream = True
    )
    answer = ''
    for chunk in response:
        content = chunk["choices"][0].get("delta", {}).get("content",'')
        answer+=content
        yield json.dumps({"answer":answer})
        
async def handler(websocket):
    message = await websocket.recv()
    prompt = json.loads(message)['prompt']
    # print(prompt)
    async for response in get_openai_response_v2(prompt):
        await websocket.send(response)
        await asyncio.sleep(0.01)

async def main():
    async with websockets.serve(handler, "localhost", 8888):
        await asyncio.Future()  # run forever
if __name__ == "__main__":
    asyncio.run(main())