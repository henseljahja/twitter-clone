import { UserAccountResponse } from "../../user-account/types/UserAccountResponse";
import { TweetStatisticsResponse } from "./TweetStatisticsResponse";

export type TweetResponse = {
  tweetId: number;
  text: string;
  source: string;
  createdDate: Date;
  userAccountId: number;
  userAccount: UserAccountResponse;
  tweetStatistics: TweetStatisticsResponse;
};
