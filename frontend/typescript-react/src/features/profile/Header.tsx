import { BiArrowBack } from "react-icons/bi";
import { CgCalendarDates, CgMoreAlt } from "react-icons/cg";
import React, { useState } from "react";
import { useUserAccount } from "../user-account/api/GetUserAccount";

export function Header() {
  const [follow, setFollow] = useState(true);
  const followHandler = () => {
    if (follow) {
      setFollow(false);
    } else if (!follow) {
      setFollow(true);
    }
  };
  const username = "hensel";
  const userAccountQuery = useUserAccount({ username });
  return (
    <>
      {userAccountQuery.isLoading ? (
        <></>
      ) : (
        <>
          <div id="box-top">
            <span id="back-icon-box">
              <BiArrowBack id="back-icon" />
            </span>

            <div id="box-top-right">
              <p id="name-header">{userAccountQuery.data?.username}</p>
              <span id="tweets-number">22 Tweets</span>
            </div>
          </div>

          <div id="header-box">
            <div id="profile-image">
              <img
                id="profile-picture"
                src={userAccountQuery.data?.profilePicture}
                alt={"profile"}
              />
            </div>
          </div>

          <div id="edit-box">
            <span id="more-box">
              <CgMoreAlt id="more-header" />
            </span>
            <button
              className={!follow ? "following" : "Follow"}
              onClick={followHandler}
            >
              {follow ? "Follow" : "Following"}
            </button>
          </div>

          <div id="name-id-box">
            <p id="name-user">{userAccountQuery.data?.name}</p>
            <p id="id-user">@{userAccountQuery.data?.username}</p>
          </div>

          <div id="job-box">
            <p id="job">{userAccountQuery.data?.about}</p>
          </div>

          <div id="date-box">
            <CgCalendarDates id="date-icon" />
            <p id="date">
              Joined {userAccountQuery.data?.joinedDate.toString()}
            </p>
          </div>

          <div id="following-follow-box">
            <span id="number-follow">
              {userAccountQuery.data?.userAccountStatistics.followingCount}
            </span>
            <a
              href="src/components/main"
              id="follow-text"
              onClick={(e) => e.preventDefault()}
            >
              Following
            </a>

            <span id="number-follow" className="margin-left">
              {userAccountQuery.data?.userAccountStatistics.followerCount}
            </span>
            <a
              href="src/components/main"
              id="follow-text"
              onClick={(e) => e.preventDefault()}
            >
              Followers
            </a>
          </div>
        </>
      )}
    </>
  );
}
