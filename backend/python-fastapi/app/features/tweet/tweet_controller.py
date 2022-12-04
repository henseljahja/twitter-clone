from typing import Any

from fastapi import APIRouter, Depends
from starlette import status

from app.features.security.security_service import SecurityService
from app.features.tweet.tweet_schema import TweetRequest, TweetResponse
from app.features.tweet.tweet_service import TweetService
from app.features.user_account.user_account_schema import UserAccountResponse
from app.features.user_account.user_account_service import UserAccountService

tweet_service = TweetService()
tweet_controller = APIRouter()
security_service = SecurityService()
user_account_service = UserAccountService()


@tweet_controller.get(
    "/username/{username}/tweet",
    # response_model=list[TweetResponse],
    response_model_exclude_none=True,
)
def get_by_username(
    username: str,
    user_account: UserAccountResponse = Depends(security_service.get_current_user),
    # session: Session = Depends(get_db),
) -> Any:
    user_account_service.check_privilege_by_username(
        user_account=user_account, username=username
    )
    return tweet_service.get_tweets_by_username(username=username)


@tweet_controller.get(
    "/username/{username}/retweets",
    response_model=list[TweetResponse],
    response_model_exclude_none=True,
)
def get_retweet_by_username(
    username: str,
    user_account: UserAccountResponse = Depends(security_service.get_current_user),
) -> list[TweetResponse]:
    user_account_service.check_privilege_by_username(
        user_account=user_account, username=username
    )
    return tweet_service.get_retweets_by_username(username=username)


@tweet_controller.get(
    "/username/{username}/likes",
    response_model=list[TweetResponse],
    response_model_exclude_none=True,
)
def get_retweet_by_username(
    username: str,
    user_account: UserAccountResponse = Depends(security_service.get_current_user),
) -> list[TweetResponse]:
    user_account_service.check_privilege_by_username(
        user_account=user_account, username=username
    )

    return tweet_service.get_likes_by_username(username=username)


@tweet_controller.post(
    "/create",
    # response_model=TweetResponse,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
)
def create_tweet(
    tweet_request: TweetRequest,
    user_account: UserAccountResponse = Depends(security_service.get_current_user),
) -> Any:

    return tweet_service.create_tweet(
        user_account=user_account, tweet_request=tweet_request
    )


@tweet_controller.delete(
    "/delete/{tweet_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT
)
def delete_tweet(
    tweet_id: int,
    user_account: UserAccountResponse = Depends(security_service.get_current_user),
) -> None:
    return tweet_service.delete_tweet(user_account=user_account, tweet_id=tweet_id)
