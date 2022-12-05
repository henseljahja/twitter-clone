import React, { useState } from "react";

import { CgMoreAlt } from "react-icons/cg";
import { SiGoogleanalytics } from "react-icons/si";
import { FiShare } from "react-icons/fi";
import { AiFillHeart, AiOutlineHeart, AiOutlineRetweet } from "react-icons/ai";
import { FaRegComment } from "react-icons/fa";
import { TweetResponse } from "../types/TweetResponse";

type propsType = {
  tweet: string;
  comment?: string;
  likeNumber: any;
};
const Tweet = (props: { tweetResponse: TweetResponse }) => {
  const [like, setLike] = useState(false);
  console.log("props");
  console.log(props.tweetResponse);
  const likeHandler = () => {
    if (!like) {
      setLike(true);
    } else if (like) {
      setLike(false);
    }
  };

  return (
    <div id="tweet-box">
      <div id="profile-tweet">
        <img
          src={props.tweetResponse.userAccount.profilePicture}
          alt="profile"
          id="image-profile"
        />
      </div>

      <div id="box-tweet">
        <div id="name-id">
          <span id="flex-tweet">
            <p id="tweet-name">
              {props.tweetResponse.userAccount.name}
              {/*Hensel*/}
            </p>
            <p id="tweet-id">
              @{props.tweetResponse.userAccount.username}
              {/*hensel*/}
            </p>
            <p id="tweet-date">{props.tweetResponse.createdDate.toString()}</p>
          </span>

          <span id="span-more">
            <CgMoreAlt />
          </span>
        </div>

        <div id="post-box">
          <p id="text-tweet"> {props.tweetResponse.text} </p>
        </div>

        <div id="nav-bottom-post">
          <div id="box-comment-number">
            <span className="comment" id="nav-icon-box">
              <FaRegComment />
            </span>
            <p id="comment-tweet">
              {props.tweetResponse.tweetStatistics.replyNumber}
            </p>
          </div>
          <div id="box-comment-number">
            <span className="retweet" id="nav-icon-box">
              <AiOutlineRetweet />
            </span>
            <p id="comment-tweet">
              {props.tweetResponse.tweetStatistics.retweetNumber}
            </p>
          </div>
          <div id="box-like-number">
            <span onClick={likeHandler} className="like" id="nav-icon-box">
              {like ? <AiFillHeart id="red-heart" /> : <AiOutlineHeart />}
            </span>
            <span id="like-number">
              {props.tweetResponse.tweetStatistics.likeNumber}
            </span>
          </div>
          <span className="share" id="nav-icon-box">
            <FiShare />
          </span>
          <span className="analytic" id="nav-icon-box">
            <SiGoogleanalytics />
          </span>
        </div>
      </div>
    </div>
  );
};

export default Tweet;
