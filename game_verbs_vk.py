import logging
import random

import vk_api
from environs import Env
from google.cloud import dialogflow
from vk_api.longpoll import VkEventType, VkLongPoll

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


def detect_intent_text(project_id,
                       session_id,
                       message_to_dialogflow,
                       language_code='ru'):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(
        text=message_to_dialogflow,
        language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    serialized_answer = {
        'intention': response.query_result.intent.display_name,
        'confidence': response.query_result.intent_detection_confidence,
        'answer': response.query_result.fulfillment_text
    }
    if response.query_result.intent.is_fallback:
        return

    return serialized_answer


def echo_dialogflow(event, vk_api) -> None:
    message_to_dialogflow = event.text
    session_id = vk_api.messages.getChat.chat_id
    serialized_answer = detect_intent_text(
        project_id,
        session_id,
        message_to_dialogflow)

    if serialized_answer:
        vk_api.messages.send(
            user_id=event.user_id,
            message=serialized_answer['answer'],
            random_id=random.randint(1, 1000)
        )


if __name__ == '__main__':

    env = Env()
    env.read_env()

    project_id = env.str('DIALOGFLOW_PROJECT_ID')

    vk_community_token = env.str('VK_COMMUNITY_TOKEN')
    vk_session = vk_api.VkApi(token=vk_community_token)
    vk_api = vk_session.get_api()

    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo_dialogflow(event=event, vk_api=vk_api)
