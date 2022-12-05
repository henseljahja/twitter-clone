import { useTweets } from "../../tweet/api/GetTweets";
import Tweet from "../../tweet/component/Tweet";
import React from "react";
import { ClipLoader } from "react-spinners";

export function Tweets() {
  const username = "hensel";
  const tweetsQuery = useTweets({ username });
  console.log(tweetsQuery.data);
  return (
    <>
      {tweetsQuery.isLoading ? (
        <ClipLoader color="#36d7b7" />
      ) : (
        tweetsQuery.data?.map((tweet) => <Tweet tweetResponse={tweet} />)
      )}
    </>
  );
}
