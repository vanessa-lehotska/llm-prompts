import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import LevelSelector from "../components/LevelSelector";
import PromptInput from "../components/PromptInput";
import ResponseBox from "../components/ResponseBox";
import ParticlesBackground from "../components/ParticlesBackground";
import Confetti from "../components/Confetti";

type Props = {
  onBack: () => void;
};

const STORAGE_KEY = "llm_security_lab_completed_levels";

export default function PromptInjectionScreen({ onBack }: Props) {
  const [difficulty, setDifficulty] = useState(1);
  const [userInput, setUserInput] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);
  const [completedLevels, setCompletedLevels] = useState<Set<number>>(
    new Set()
  );
  const [showConfetti, setShowConfetti] = useState(false);

  useEffect(() => {
    const saved = localStorage.getItem(STORAGE_KEY);

    if (!saved) {
      return;
    }

    try {
      const levels = JSON.parse(saved) as number[];
      setCompletedLevels(new Set(levels));
    } catch (error) {
      console.error("Failed to load completed levels:", error);
    }
  }, []);

  useEffect(() => {
    if (completedLevels.size === 0) {
      return;
    }

    localStorage.setItem(
      STORAGE_KEY,
      JSON.stringify(Array.from(completedLevels))
    );
  }, [completedLevels]);

  async function send() {
    if (!userInput.trim()) {
      return;
    }

    setLoading(true);
    setResponse("");

    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_message: userInput,
          difficulty,
        }),
      });

      const data = await res.json();
      setResponse(data.response);

      if (data.level_up && data.next_level) {
        setCompletedLevels((prev) => new Set([...prev, difficulty]));
        setShowConfetti(true);

        setTimeout(() => {
          setDifficulty(data.next_level);
          setUserInput("");
          setShowConfetti(false);
        }, 1000);
      }

      if (data.game_completed) {
        setCompletedLevels((prev) => new Set([...prev, difficulty]));
        setShowConfetti(true);

        setTimeout(() => {
          setShowConfetti(false);
        }, 1000);
      }
    } catch (error) {
      setResponse(`Error: ${String(error)}`);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-6 relative overflow-hidden bg-slate-950">
      <ParticlesBackground />
      <Confetti show={showConfetti} />

      <button
        onClick={onBack}
        className="absolute top-5 left-5 z-30 rounded-lg border border-slate-700 bg-slate-900/80 px-4 py-2 text-sm text-slate-300 transition-all duration-200 hover:border-cyan-400 hover:text-cyan-300 hover:bg-slate-900"
      >
        ← Back
      </button>

      <motion.div
        className="relative z-10 w-full max-w-5xl rounded-2xl border border-slate-800 bg-slate-900/75 backdrop-blur-md shadow-[0_0_50px_rgba(34,211,238,0.08)] overflow-hidden"
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.45 }}
      >
        <div className="absolute inset-0 pointer-events-none bg-[radial-gradient(circle_at_top_left,rgba(34,211,238,0.08),transparent_35%),radial-gradient(circle_at_bottom_right,rgba(59,130,246,0.10),transparent_35%)]" />

        <div className="grid md:grid-cols-[1.05fr_0.95fr] relative">
          <div className="p-8 md:p-12 border-b md:border-b-0 md:border-r border-slate-800">
            <motion.h1
              className="text-4xl md:text-5xl font-bold text-slate-100 leading-none mb-5 font-mono tracking-tight"
              initial={{ opacity: 0 }}
              animate={{
                opacity: [1, 0.9, 1],
                textShadow: [
                  "0 0 0px rgba(34,211,238,0)",
                  "0 0 14px rgba(34,211,238,0.14)",
                  "0 0 0px rgba(34,211,238,0)",
                ],
              }}
              transition={{
                duration: 4,
                repeat: Infinity,
                repeatDelay: 1.5,
                times: [0, 0.12, 1],
              }}
            >
              Break the Prompt
            </motion.h1>

            <motion.p
              className="max-w-2xl text-[15px] md:text-base leading-7 font-mono text-slate-400 mb-8"
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.45, delay: 0.15 }}
            >
              Unlock new levels by outsmarting the AI with your prompt. If you think you know the secret word, just type it into the input box.
            </motion.p>

            <motion.div
              className="space-y-5"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.45, delay: 0.2 }}
            >
              <div>
                <p className="text-xs uppercase tracking-[0.28em] text-cyan-400/90 mb-3 font-mono">
                  Level
                </p>
                <LevelSelector
                  difficulty={difficulty}
                  setDifficulty={(newLevel) => {
                    setDifficulty(newLevel);
                    setResponse("");
                    setUserInput("");
                  }}
                  completedLevels={completedLevels}
                />
              </div>

              <div>
                <p className="text-xs uppercase tracking-[0.28em] text-cyan-400/90 mb-3 font-mono">
                  Prompt
                </p>
                <PromptInput
                  userInput={userInput}
                  setUserInput={setUserInput}
                  send={send}
                  loading={loading}
                />
              </div>
            </motion.div>
          </div>

          <div className="p-8 md:p-10 flex flex-col bg-slate-950/40 min-h-[420px]">
            <motion.div
              className="mb-4"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.35, delay: 0.25 }}
            >
              <p className="text-xs uppercase tracking-[0.28em] text-cyan-400/90 mb-3 font-mono">
                Model response
              </p>
              <p className="text-sm text-slate-500 leading-6">
                The output appears here after each attempt.
              </p>
            </motion.div>

            <div className="flex-1 flex">
              <ResponseBox response={response} />
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  );
}