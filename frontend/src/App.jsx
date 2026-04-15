import { useState } from "react";
import { fetchQuestions, submitAnswers } from "./api";
import Quiz from "./Quiz";
import Results from "./Results";

const USER_TYPES = ["class_10", "class_12", "undergraduate", "professional"];
const INST_ID = "inst_001"; // change as needed

export default function App() {
  const [step, setStep] = useState("select"); // select | quiz | results
  const [userType, setUserType] = useState("");
  const [questions, setQuestions] = useState([]);
  const [results, setResults] = useState(null);

  async function handleStart(type) {
    setUserType(type);
    const data = await fetchQuestions(type, INST_ID);
    setQuestions(data.questions);
    setStep("quiz");
  }

  async function handleSubmit(answers) {
    const data = await submitAnswers(userType, INST_ID, answers);
    setResults(data);
    setStep("results");
  }

  if (step === "select") {
    return (
      <div style={styles.center}>
        <h1>Edwiserr</h1>
        <p>Select your profile to begin</p>
        <div style={styles.grid}>
          {USER_TYPES.map((t) => (
            <button key={t} style={styles.btn} onClick={() => handleStart(t)}>
              {t.replace("_", " ")}
            </button>
          ))}
        </div>
      </div>
    );
  }

  if (step === "quiz") {
    return <Quiz questions={questions} onSubmit={handleSubmit} />;
  }

  if (step === "results") {
    return <Results data={results} onRetake={() => setStep("select")} />;
  }
}

const styles = {
  center: { maxWidth: 480, margin: "80px auto", textAlign: "center", fontFamily: "sans-serif" },
  grid: { display: "flex", flexDirection: "column", gap: 12, marginTop: 24 },
  btn: { padding: "12px 24px", fontSize: 16, cursor: "pointer", borderRadius: 8, border: "1px solid #ccc" },
};