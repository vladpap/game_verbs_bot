from google.cloud import dialogflow


def detect_intent_text(logger,
                       project_id,
                       session_id,
                       message_to_dialogflow,
                       language_code='ru'):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(
        text=message_to_dialogflow,
        language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    try:
        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )
    except response.exceptions.ConnectionError:
        logger.exception('Problem connection.')

    except Exception as err:
        logger.exception(err)

    serialized_answer = {
        'intention': response.query_result.intent.display_name,
        'confidence': response.query_result.intent_detection_confidence,
        'answer': response.query_result.fulfillment_text
    }
    return serialized_answer


if __name__ == '__main__':
    pass
