import logging
import random

from environs import Env
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from dialogflow import get_reply_by_intent

logger = logging.getLogger(__name__)


def reply(event, vk_api_method, project_id, language_code):
    is_fallback, fulfillment_text = get_reply_by_intent(
        project_id,
        event.user_id,
        event.text,
        language_code
    )
    if not is_fallback:
        vk_api_method.messages.send(
            user_id=event.user_id,
            random_id=random.randint(1, 1000),
            message=fulfillment_text
        )


def main():
    env = Env()
    env.read_env()
    vk_club_token = env('VK_CLUB_TOKEN')
    project_id = env('PROJECT_ID')
    language_code = env('LANGUAGE_CODE')

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logger.setLevel(logging.INFO)

    vk_session = vk_api.VkApi(token=vk_club_token)
    vk_api_method = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    logger.info('VK bot is running.')

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            reply(event, vk_api_method, project_id, language_code)


if __name__ == '__main__':
    main()
