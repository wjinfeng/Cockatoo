import json 

def load_json(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def set_single_bot_system(
        file_path: str,
        bot_name: str,
        bot_prompt: str,
        memory: str = "",
        story: str = ""
    ):
    system_prompt = load_json(file_path)
    prompts = []
    for key, value in system_prompt.items():
        if key == "main":
            prompts.append(value.format(bot_name=bot_name))
        if key == "content":
            prompts.append(value.format(bot_name=bot_name, bot_prompt=bot_prompt, story=story))
        if key == "memory":
            prompts.append(value.format(memory=memory))
    prompts = "\n".join(prompts)
    return prompts
