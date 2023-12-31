import logging
import random

import vk_api
from environs import Env
from vk_api.longpoll import VkEventType, VkLongPoll

from detect_intent import detect_intent_text

logger = logging.getLogger('game verbs chat vk')


def get_response_from_dialogflow(project_id,
                                 event,
                                 vk_session_api) -> None:
    message_to_dialogflow = event.text
    session_id = vk_session_api.messages.getChat.chat_id

    try:
        serialized_answer = detect_intent_text(
            project_id,
            session_id,
            message_to_dialogflow)

    except response.exceptions.ConnectionError:
        logger.exception('Problem connection.')

    except Exception as err:
        logger.exception(err)

    if serialized_answer and not serialized_answer['is_fallback']:
        vk_session_api.messages.send(
            user_id=event.user_id,
            message=serialized_answer['fulfillment_text'],
            random_id=random.randint(1, 1000)
        )


def main():
    env = Env()
    env.read_env()

    logger.info('Start chat vk')

    project_id = env.str('DIALOGFLOW_PROJECT_ID')

    vk_community_token = env.str('VK_COMMUNITY_TOKEN')
    vk_session = vk_api.VkApi(token=vk_community_token)
    vk_session_api = vk_session.get_api()

    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            get_response_from_dialogflow(project_id,
                                         event=event,
                                         vk_session_api=vk_session_api)


if __name__ == '__main__':
    main()
