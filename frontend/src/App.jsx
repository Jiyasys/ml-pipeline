import { useState } from "react";
import Landing from "./pages/Landing";
import UserType from "./pages/UserType";
import Quiz from "./pages/Quiz";
import Results from "./pages/Results";
import "./index.css";

export default function App() {
  const [screen, setScreen] = useState("landing");
  const [userType, setUserType] = useState(null);
  const [profile, setProfile] = useState(null);

  return (
    <div className="app">
      {screen === "landing" && (
        <Landing onBegin={() => setScreen("usertype")} />
      )}
      {screen === "usertype" && (
        <UserType
          onSelect={(type) => {
            setUserType(type);
            setScreen("quiz");
          }}
        />
      )}
      {screen === "quiz" && (
        <Quiz
          userType={userType}
          onComplete={(profileData) => {
            setProfile(profileData);
            setScreen("results");
          }}
        />
      )}
      {screen === "results" && (
        <Results
          profile={profile}
          onRetake={() => {
            setProfile(null);
            setUserType(null);
            setScreen("landing");
          }}
        />
      )}
    </div>
  );
}