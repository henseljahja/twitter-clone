import React from "react";

export function ProfileNav() {
  return (
    <div id="nav-header">
      <div id="box-nav" className="box-Tweets">
        <p id="nav">Tweets</p>
      </div>

      <div id="box-nav" className="box-replies">
        <p id="nav">Tweets & replies</p>
      </div>

      <div id="box-nav" className="box-Media">
        <p id="nav">Media</p>
      </div>

      <div id="box-nav" className="box-Likes">
        <p id="nav">Likes</p>
      </div>
    </div>
  );
}
