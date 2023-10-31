import json
import typing

from .auth import auth
from .type import ResponseData


class MeResponse(typing.TypedDict):
    created_at: str
    id: str
    name: str
    profile_image_url: str
    username: str


def me() -> ResponseData[MeResponse]:
    with auth() as session:
        # Making the request
        fields = ','.join([
            'created_at',
            'profile_image_url'
        ])
        response = session.get(
            "https://api.twitter.com/2/users/me",
            params={
                'user.fields': fields,
            }
        )

        if not response.ok:
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
    return json_response
