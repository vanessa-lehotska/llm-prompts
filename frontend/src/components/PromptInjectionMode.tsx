import React, { useState, useEffect } from "react";
import Header from "./Header";
import LevelSelector from "./LevelSelector";
import PromptInput from "./PromptInput";
import ResponseBox from "./ResponseBox";
import ParticlesBackground from "./ParticlesBackground";
import Confetti from "./Confetti";

type Props = {
  onBack: () => void;
};

const STORAGE_KEY = "llm_security_lab_completed_levels";

export default function PromptInjectionMode({ onBack }: Props) {
  const [difficulty, setDifficulty] = useState(1);
  const [userInput, setUserInput] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);
  const [completedLevels, setCompletedLevels] = useState<Set<number>>(
    new Set()
  );
  const [showConfetti, setShowConfetti] = useState(false);

  // Load completed levels from localStorage on mount
  useEffect(() => {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
      try {
        const levels = JSON.parse(saved) as number[];
        setCompletedLevels(new Set(levels));
      } catch (e) {
        console.error("Failed to load completed levels:", e);
      }
    }
  }, []);

  // Save completed levels to localStorage whenever it changes
  useEffect(() => {
    if (completedLevels.size > 0) {
      localStorage.setItem(
        STORAGE_KEY,
        JSON.stringify(Array.from(completedLevels))
      );
    }
  }, [completedLevels]);

  async function send() {
    if (!userInput.trim()) return;
    setLoading(true);
    // Clear response when sending new message (but keep success message until then)
    setResponse("");
    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_message: userInput,
          difficulty,
          mode: "prompt_injection",
        }),
      });
      const data = await res.json();

      // Display AI response
      setResponse(data.response);

      // Check if user found the secret and should advance
      if (data.level_up && data.next_level) {
        // Mark current level as completed
        setCompletedLevels((prev) => new Set([...prev, difficulty]));

        // Show confetti animation
        setShowConfetti(true);

        // Wait for confetti to finish, then advance immediately
        // Keep success message visible until user sends new message
        setTimeout(() => {
          setDifficulty(data.next_level);
          setUserInput("");
          // Don't clear response - let user read the success message
          setShowConfetti(false);
        }, 1000); // Match confetti duration - 1 second
      }

      // Also mark level as completed if game is completed
      if (data.game_completed) {
        setCompletedLevels((prev) => new Set([...prev, difficulty]));
        setShowConfetti(true);

        setTimeout(() => {
          setShowConfetti(false);
        }, 1000);
      }
    } catch (e: any) {
      setResponse(`Error: ${String(e)}`);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-start p-6 relative overflow-hidden">
      <ParticlesBackground />
      <Confetti show={showConfetti} />

      {/* Back button */}
      <button
        onClick={onBack}
        className="absolute top-4 left-4 z-20 px-4 py-2 bg-slate-800/80 border border-slate-600 
                   text-slate-300 rounded hover:bg-slate-700 hover:border-blue-400 
                   hover:text-blue-400 transition-all duration-200"
      >
        ← Back to Home
      </button>

      <Header />
      <LevelSelector
        difficulty={difficulty}
        setDifficulty={(newLevel) => {
          setDifficulty(newLevel);
          setResponse(""); // Clear response when manually switching levels
          setUserInput("");
        }}
        completedLevels={completedLevels}
      />
      <PromptInput
        userInput={userInput}
        setUserInput={setUserInput}
        send={send}
        loading={loading}
      />
      <ResponseBox response={response} />
    </div>
  );
}
