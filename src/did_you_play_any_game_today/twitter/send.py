import json
import typing

from .auth import auth
from .type import ResponseData


class SendTextTweetResponse(typing.TypedDict):
    edit_history_tweet_ids: typing.List[str]
    id: str
    text: str


def send_text_tweet(text: str) -> ResponseData[SendTextTweetResponse]:
    # Be sure to add replace the text of the with the text you wish to Tweet.
    # You can also add parameters to post polls, quote Tweets, Tweet with reply
    # settings, and Tweet to Super Followers in addition to other features.
    payload = {"text": text}

    with auth() as session:
        # Making the request
        response = session.post(
            "https://api.twitter.com/2/tweets",
            json=payload,
        )

        if response.status_code != 201:
            raise Exception(
                "Request returned an error: {} {}".format(
                    response.status_code,
                    response.text
                )
            )

        print("Response code: {}".format(response.status_code))

        # Saving the response as JSON
        json_response = response.json()
        print(json.dumps(json_response, indent=4, sort_keys=True))
    return ResponseData(**json_response)
