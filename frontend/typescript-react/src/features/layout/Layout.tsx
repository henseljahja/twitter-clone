import NavBar from "../navbar/Navbar";
import { Profile } from "../profile/Profile";
import Right from "../right/Right";
import React from "react";
import "./Layout.css";

export function Layout() {
  return (
    <>
      <div id="container">
        <div id="nav-box">
          <NavBar />
        </div>
        <Profile />
        <Right />
      </div>
    </>
  );
}
