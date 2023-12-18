import argparse
import json

from environs import Env
from google.cloud import dialogflow


def create_intent(project_id,
                  display_name,
                  training_phrases_parts,
                  message_texts):
    """Create an intent of the given intent type."""

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(
            text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    print("Intent created: {}".format(response))


def open_json_file(file_name):
    with open(file_name, 'r') as json_file:
        file_json = json_file.read()

    return json.loads(file_json)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Script create intents on DialogFlow.')
    parser.add_argument(
        'file_name',
        action='store',
        help='Json file name (traning questions and answer.')

    args = parser.parse_args()

    questions = open_json_file(args.file_name)

    env = Env()
    env.read_env()

    project_id = env.str('DIALOGFLOW_PROJECT_ID')

    for indent_title, indent_questions_answer in questions.items():
        for indent_questions, indent_answer in indent_questions_answer.items():
            create_intent(
                project_id=project_id,
                display_name=indent_title,
                training_phrases_parts=indent_questions,
                message_texts=(indent_answer,)
            )
