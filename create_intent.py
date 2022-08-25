import argparse
import json

from environs import Env
from google.cloud import dialogflow


def create_intent(
    project_id: str,
    display_name: str,
    training_phrases_parts: list[str],
    message_texts: list[str]
) -> dialogflow.Intent:

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)

    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(
            text=training_phrases_part
        )
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message]
    )

    intents_client.create_intent(
        request={
            'parent': parent, 
            'intent': intent
        }
    )


def main():
    env = Env()
    env.read_env()
    project_id = env('PROJECT_ID')

    parser = argparse.ArgumentParser()
    parser.add_argument('--path', default='questions.json')
    args = parser.parse_args()

    with open(args.path, 'r', encoding='utf8') as file:
        themes: dict = json.load(file)
    
    for theme_name, theme_data in themes.items():
        create_intent(
            project_id,
            theme_name,
            theme_data['questions'],
            [theme_data['answer']]
        )


if __name__ == '__main__':
    main()
