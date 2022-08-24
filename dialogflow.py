from google.cloud import dialogflow


def reply_by_intent(project_id: str, session_id: str,
                    message: str, language_code: str) -> str:

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(
        text=message, language_code=language_code
    )
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={'session': session, 'query_input': query_input}
    )

    return response.query_result.fulfillment_text
