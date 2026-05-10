import { useEffect, useMemo, useRef, useState, useCallback } from "react";

import Landing  from "./pages/Landing";
import UserType from "./pages/UserType";
import Quiz     from "./pages/Quiz";
import Results  from "./pages/Results";
import Careers  from "./pages/Careers";

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
    // Never persist screen — app always starts at Landing
    const { screen: _omit, ...rest } = data;
    localStorage.setItem(APP_STATE_KEY, JSON.stringify(rest));
  } catch {}
}

function clearAppState() {
  try {
    localStorage.removeItem(APP_STATE_KEY);
  } catch {}
}

function clearQuizSession() {
  try {
    localStorage.removeItem("edwiserr_quiz_session");
  } catch {}
}

// ── Validation ───────────────────────────────────────────────

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
  const persisted = useMemo(() => loadAppState(), []);

  // Screen always starts at LANDING — never restored from storage
  const [screen, setScreen] = useState(SCREENS.LANDING);

  const [userType, setUserType] = useState(
    persisted?.userType || null
  );

  const [profile, setProfile] = useState(
    isValidProfile(persisted?.profile) ? persisted.profile : null
  );

  // recommendations stored in both a ref AND state.
  // The ref is written FIRST (synchronously) so that when setScreen
  // triggers a re-render, Careers reads recsRef.current — which is
  // already populated — rather than waiting for the state flush.
  const recsRef = useRef(
    Array.isArray(persisted?.recommendations) ? persisted.recommendations : []
  );
  const [recommendations, setRecommendationsState] = useState(
    recsRef.current
  );

  const setRecommendations = useCallback((recs) => {
    const safe = Array.isArray(recs) ? recs : [];
    recsRef.current = safe;       // synchronous — available immediately
    setRecommendationsState(safe); // triggers re-render for persistence
  }, []);

  // ── Persist (never screen) ────────────────────────────────

  useEffect(() => {
    saveAppState({ userType, profile, recommendations });
  }, [userType, profile, recommendations]);

  // ── Navigation ────────────────────────────────────────────

  const goToLanding  = useCallback(() => setScreen(SCREENS.LANDING),  []);
  const goToUserType = useCallback(() => setScreen(SCREENS.USERTYPE), []);
  const goToQuiz     = useCallback(() => setScreen(SCREENS.QUIZ),     []);
  const goToResults  = useCallback(() => setScreen(SCREENS.RESULTS),  []);
  const goToCareers  = useCallback(() => setScreen(SCREENS.CAREERS),  []);

  // ── Handlers ─────────────────────────────────────────────

  const handleBegin = () => goToUserType();

  const handleUserTypeSelect = (type) => {
    setUserType(type);
    goToQuiz();
  };

  const handleQuizComplete = (result) => {
    if (!isValidProfile(result)) {
      console.error("Invalid profile returned from backend:", result);
      return;
    }
    setProfile(result);
    goToResults();
  };

  // Results calls this once careers are fetched.
  // Write to ref first, then navigate — Careers will read recsRef.current
  // on its very first render, so it never sees an empty array.
  const handleCareersReady = useCallback(
    (recs) => {
      setRecommendations(recs); // writes ref synchronously
      goToCareers();            // triggers re-render — ref is already set
    },
    [setRecommendations, goToCareers]
  );

  const handleRetake = () => {
    setProfile(null);
    setUserType(null);
    setRecommendations([]);
    clearQuizSession();
    clearAppState();
    goToLanding();
  };

  // ── Render ────────────────────────────────────────────────

  return (
    <div className="app">
      {screen === SCREENS.LANDING && (
        <Landing onBegin={handleBegin} />
      )}

      {screen === SCREENS.USERTYPE && (
        <UserType onSelect={handleUserTypeSelect} />
      )}

      {screen === SCREENS.QUIZ && userType && (
        <Quiz userType={userType} onComplete={handleQuizComplete} />
      )}

      {screen === SCREENS.RESULTS && isValidProfile(profile) && (
        <Results
          profile={profile}
          userType={userType}
          onCareersReady={handleCareersReady}
          onRetake={handleRetake}
        />
      )}

      {screen === SCREENS.CAREERS && isValidProfile(profile) && (
        <Careers
          // Pass recsRef.current directly — this is the synchronously
          // written value, guaranteed to be populated when Careers mounts
          recommendations={recsRef.current}
          onBack={goToResults}
        />
      )}
    </div>
  );
}