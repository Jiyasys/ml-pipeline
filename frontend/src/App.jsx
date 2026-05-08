import { useEffect, useMemo, useState, useCallback } from "react";

import Landing from "./pages/Landing";
import UserType from "./pages/UserType";
import Quiz from "./pages/Quiz";
import Results from "./pages/Results";
import Careers from "./pages/Careers";

import "./index.css";

// ── Constants ────────────────────────────────────────────────

const APP_STATE_KEY = "edwiserr_app_state";

const SCREENS = {
  LANDING:  "landing",
  USERTYPE: "usertype",
  QUIZ:     "quiz",
  RESULTS:  "results",
  CAREERS:  "careers",
};

// ── Storage helpers ──────────────────────────────────────────

function loadAppState() {
  try {
    const raw = localStorage.getItem(APP_STATE_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

function saveAppState(data) {
  try {
    localStorage.setItem(
      APP_STATE_KEY,
      JSON.stringify(data)
    );
  } catch {}
}

function clearAppState() {
  try {
    localStorage.removeItem(APP_STATE_KEY);
  } catch {}
}

function clearQuizSession() {
  try {
    localStorage.removeItem(
      "edwiserr_quiz_session"
    );
  } catch {}
}

// ── Validation helpers ───────────────────────────────────────

function isValidProfile(profile) {
  return (
    profile &&
    typeof profile === "object" &&
    profile.ocean_scores &&
    typeof profile.ocean_scores === "object"
  );
}

// ── App ──────────────────────────────────────────────────────

export default function App() {
  const persisted = useMemo(
    () => loadAppState(),
    []
  );

 const [screen, setScreen] =
  useState("landing");

  const [userType, setUserType] = useState(
    persisted?.userType || null
  );

  const [profile, setProfile] = useState(
    isValidProfile(persisted?.profile)
      ? persisted.profile
      : null
  );

  // ── Persist app-level state ───────────────────────────────

  useEffect(() => {
    saveAppState({
      screen,
      userType,
      profile,
    });
  }, [screen, userType, profile]);

  // ── Navigation helpers ────────────────────────────────────

  const goToLanding = useCallback(() => {
    setScreen(SCREENS.LANDING);
  }, []);

  const goToUserType = useCallback(() => {
    setScreen(SCREENS.USERTYPE);
  }, []);

  const goToQuiz = useCallback(() => {
    setScreen(SCREENS.QUIZ);
  }, []);

  const goToResults = useCallback(() => {
    setScreen(SCREENS.RESULTS);
  }, []);

  const goToCareers = useCallback(() => {
    setScreen(SCREENS.CAREERS);
  }, []);

  // ── Handlers ──────────────────────────────────────────────

  const handleBegin = () => {
    goToUserType();
  };

  const handleUserTypeSelect = (type) => {
    setUserType(type);
    goToQuiz();
  };

  const handleQuizComplete = (result) => {
    if (!isValidProfile(result)) {
      console.error(
        "Invalid profile returned from backend:",
        result
      );
      return;
    }

    setProfile(result);
    goToResults();
  };

  const handleRetake = () => {
    setProfile(null);
    setUserType(null);

    clearQuizSession();
    clearAppState();

    goToLanding();
  };

  // ── Recovery guards ───────────────────────────────────────

  useEffect(() => {
    // Prevent invalid navigation states

    if (
      screen === SCREENS.QUIZ &&
      !userType
    ) {
      goToUserType();
    }

    if (
      (screen === SCREENS.RESULTS ||
        screen === SCREENS.CAREERS) &&
      !isValidProfile(profile)
    ) {
      goToLanding();
    }
  }, [
    screen,
    userType,
    profile,
    goToLanding,
    goToUserType,
  ]);

  // ── Render ────────────────────────────────────────────────

  return (
    <div className="app">
      {screen === SCREENS.LANDING && (
        <Landing onBegin={handleBegin} />
      )}

      {screen === SCREENS.USERTYPE && (
        <UserType
          onSelect={handleUserTypeSelect}
        />
      )}

      {screen === SCREENS.QUIZ && userType && (
        <Quiz
          userType={userType}
          onComplete={handleQuizComplete}
        />
      )}

      {screen === SCREENS.RESULTS &&
        isValidProfile(profile) && (
          <Results
            profile={profile}
            userType={userType}
            onViewCareers={goToCareers}
            onRetake={handleRetake}
          />
        )}

      {screen === SCREENS.CAREERS &&
        isValidProfile(profile) && (
          <Careers
            profile={profile}
            onBack={goToResults}
          />
        )}
    </div>
  );
}