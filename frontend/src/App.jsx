import { useState } from "react";
import Landing   from "./pages/Landing";
import UserType  from "./pages/UserType";
import Quiz      from "./pages/Quiz";
import Results   from "./pages/Results";
import Careers   from "./pages/Careers";
import "./index.css";

export default function App() {
  const [screen,   setScreen]   = useState("landing");
  const [userType, setUserType] = useState(null);
  const [profile,  setProfile]  = useState(null);

  return (
    <div className="app">
      {screen === "landing" && (
        <Landing onBegin={() => setScreen("usertype")} />
      )}
      {screen === "usertype" && (
        <UserType onSelect={(type) => { setUserType(type); setScreen("quiz"); }} />
      )}
      {screen === "quiz" && (
        <Quiz
          userType={userType}
          onComplete={(p) => { setProfile(p); setScreen("results"); }}
        />
      )}
      {screen === "results" && (
        <Results
          profile={profile}
          onViewCareers={() => setScreen("careers")}
          onRetake={() => { setProfile(null); setUserType(null); setScreen("landing"); }}
        />
      )}
      {screen === "careers" && (
        <Careers
          profile={profile}
          onBack={() => setScreen("results")}
        />
      )}
    </div>
  );
}