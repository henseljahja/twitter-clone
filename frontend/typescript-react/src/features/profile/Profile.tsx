import { Header } from "./Header";
import { ProfileNav } from "./ProfileNav";
import { Tweets } from "./tweets/Tweets";
import React from "react";
import "./Profile.css";

export function Profile() {
  return (
    <div id="container-main">
      <Header />
      <ProfileNav />

      <div id="line"></div>

      <Tweets />
    </div>
  );
}
