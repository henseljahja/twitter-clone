from app.features.db.database import db
from app.features.user_account.follower.follower_association import Follower


class FollowerRepository:
    def is_follower(
        self,
        requester_user_account_id: int,
        target_user_account_id: int,
    ):
        is_follower = (
            db.session.query(Follower)
            .filter(
                Follower.c.follower_id == requester_user_account_id,
                Follower.c.followee_id == target_user_account_id,
            )
            .first()
        )
        if is_follower is None:
            return False
        return True
