from ollama import chat

import json


def get_model_response(text, annotation_classes):


    prompt = build_prompt(text, annotation_classes)
    response = chat('cqwen', messages =[{'role':'user','content': prompt}], think = False)
    list_tags = response['message']['content']
    list_tags = json.loads(list_tags)
    return list_tags




def build_prompt(text, annotation_classes):
    classes_str = ", ".join(annotation_classes)

    prompt = f"Список классов - {classes_str}: {text}"
    print(f"Готовый промпт{prompt}")
    return prompt