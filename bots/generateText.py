# https://docs.aitextgen.io/

from aitextgen import aitextgen

# Without any parameters, aitextgen() will download, cache, and load the 124M GPT-2 "small" model
ai = aitextgen(model="EleutherAI/gpt-neo-125M")

# ai.generate()
# ai.generate(n=3, max_length=100)
# ai.generate(n=3, prompt="I believe in unicorns because", max_length=100)

prompt = """Oink, I do be a pug."""
ai.generate(prompt=prompt)
print("----------- high temp -------------")
ai.generate(prompt=prompt, temperature=0.9)


