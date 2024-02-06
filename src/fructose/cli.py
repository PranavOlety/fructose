import click
import openai
from openai.types.chat import ChatCompletionMessageParam, ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam
import os
import json

@click.group()
@click.version_option()
def cli():
    pass


@click.command()
def cook():
    client = openai.Client(
        api_key=os.environ['OPENAI_API_KEY']
    )

    messages = [
        ChatCompletionSystemMessageParam(
            role="system",
            content="""
You are a helpful assistant for "fructose" - a Python tool for strongly-typed LLM function calling.

"fructose" wraps python functions with an @ai decorator and uses the docstring, function parameters & arguments, and the return type to guide the LLM.

Here's an example of fructose code in action:

```python
# This examples demonstrates how to use Fructose to simulate an RPG "turn" where a player is attacked.

from fructose import Fructose
from dataclasses import dataclass

# Create a new instance of the Fructose app
ai = Fructose()

# Define a dataclass to represent a player
@dataclass
class Player:
  hp: int
  def_: int
  name: str
  mana: int

# decorate your function to call an LLM. Your ways to guide the LLM are through the docstring,
# functions parameters & arguments and the return type.
# If your function requires explicit randomness, you can specify the uses parameter.
@ai(uses=["random"])
def receive_attack(player_state: Player, dmg: int, crit_chance: float) -> Player:
  \"\"\"
  Simulates a player receiving an attack. If crit, then double the dmg amount. Crit is randomly rolled during this turn based on crit_chance. Subtracts def_ from final dmg.
  \"\"\"

def main():
    state = receive_attack({"hp": 100, "def_": 10, "name": "Jack Sparrow", "mana": 55}, 12, 0.3)
    print(state)

if __name__ == "__main__":
    main()
```

fructose-wrapped functions don't have a return statement, as the return value is generated by the LLM.

There can be multiple functions in a single file, and each function can have its own set of parameters and return types.

You are able to generate Python code that uses fructose.

Your task is to write relevant fructose Python code, based on a user's intended functionality.

Instead of hard-coded values, prefer generating random data using a fructose-wrapped function.

Response with JSON in the following format:

```json
{
    "code": <the generated Python code>
}
```
""".strip()
        ),
        ChatCompletionUserMessageParam(
            role="user",
            content="I want to create a hangman game"
        )
    ]

    chat_completion = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=messages,
        response_format={
            "type":"json_object",
        },
    )

    # print(chat_completion.choices[0].message.content)

    # save the content to test.py in this directory

    with open("fructose.py", "w") as f:
        f.write(json.loads(chat_completion.choices[0].message.content)["code"])
        f.close()


cli.add_command(cook)

if __name__ == "__main__":
    cli()
