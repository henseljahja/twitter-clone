from sqlalchemy import select

from app.features.db.db_session import session
from app.features.user_account.follower.follower_association import Follower


class FollowerRepository:
    async def is_follower(
        self,
        requester_user_account_id: int,
        target_user_account_id: int,
    ):
        is_follower = (
            (
                await (
                    session.execute(
                        select(Follower).filter(
                            Follower.c.follower_id == requester_user_account_id,
                            Follower.c.followee_id == target_user_account_id,
                        )
                    )
                )
            )
            .scalars()
            .first()
        )

        if is_follower is None:
            return False
        return True
