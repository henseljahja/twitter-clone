import { useQuery } from "react-query";
import { axios } from "../../../common/axios";
import { ExtractFnReturnType, QueryConfig } from "../../../common/react-query";
import { TweetResponse } from "../types/TweetResponse";

export const getTweets = ({
  username,
}: {
  username: string;
}): Promise<TweetResponse[]> => {
  return axios.get(`/username/${username}/tweet`);
};

type QueryFnType = typeof getTweets;

type UseTweetsOptions = {
  username: string;
  config?: QueryConfig<QueryFnType>;
};

export const useTweets = ({ username, config }: UseTweetsOptions) => {
  return useQuery<ExtractFnReturnType<QueryFnType>>({
    ...config,
    queryKey: ["tweets", username],
    queryFn: () => getTweets({ username }),
  });
};
