import argparse
import json

from environs import Env

from dialogflow import create_intent


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
