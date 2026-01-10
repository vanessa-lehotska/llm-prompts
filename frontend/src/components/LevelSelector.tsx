import { useState, useEffect } from "react";

type Props = {
  difficulty: number;
  setDifficulty: (level: number) => void;
  completedLevels: Set<number>;
};

type Level = {
  id: number;
  secret: string;
  has_system_prompt: boolean;
  info: string;
};

export default function LevelSelector({
  difficulty,
  setDifficulty,
  completedLevels,
}: Props) {
  const [isOpen, setIsOpen] = useState(false);
  const [levels, setLevels] = useState<Level[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchLevels() {
      try {
        const res = await fetch("/api/levels");
        const data = await res.json();
        // Filter out placeholder levels
        const realLevels = data.levels.filter(
          (level: Level) =>
            level.secret !== "COMING_SOON" && level.secret !== ""
        );
        setLevels(realLevels);
      } catch (error) {
        console.error("Failed to fetch levels:", error);
        // Fallback to default levels if API fails
        setLevels([
          { id: 1, secret: "", has_system_prompt: true, info: "" },
          { id: 2, secret: "", has_system_prompt: true, info: "" },
          { id: 3, secret: "", has_system_prompt: true, info: "" },
          { id: 4, secret: "", has_system_prompt: true, info: "" },
        ]);
      } finally {
        setLoading(false);
      }
    }
    fetchLevels();
  }, []);

  return (
    <div className="relative mb-4">
      {/* Tlačidlo */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="bg-slate-800 border border-blue-400 text-blue-400 px-4 py-2 rounded 
                   hover:bg-blue-400/10 hover:border-purple-400 hover:text-purple-400
                   transition-all duration-200 flex items-center gap-2 min-w-[150px] justify-between"
      >
        <span>Level {difficulty}</span>
        <span
          className={`transition-transform duration-200 ${
            isOpen ? "rotate-180" : ""
          }`}
        >
          ▼
        </span>
      </button>

      {/* Dropdown menu */}
      {isOpen && (
        <>
          {/* Overlay */}
          <div
            className="fixed inset-0 z-40"
            onClick={() => setIsOpen(false)}
          />

          {/* Menu */}
          <div
            className="absolute top-full mt-1 w-full bg-slate-800 border border-blue-400 rounded 
                          max-h-60 overflow-y-auto z-50
                          origin-top animate-[slideDown_0.2s_ease-out]
                          shadow-[0_0_20px_rgba(59,130,246,0.3)]"
          >
            {loading ? (
              <div className="px-4 py-2 text-slate-400 text-sm">
                Loading levels...
              </div>
            ) : levels.length === 0 ? (
              <div className="px-4 py-2 text-slate-400 text-sm">
                No levels available
              </div>
            ) : (
              levels.map((level) => {
                const isCompleted = completedLevels.has(level.id);
                const isCurrent = difficulty === level.id;
                const isAvailable =
                  level.id === 1 ||
                  isCompleted ||
                  completedLevels.has(level.id - 1);
                const isLocked = !isAvailable && !isCurrent;

                return (
                  <button
                    key={level.id}
                    onClick={() => {
                      if (!isLocked) {
                        setDifficulty(level.id);
                        setIsOpen(false);
                      }
                    }}
                    disabled={isLocked}
                    className={`w-full text-left px-4 py-2 transition-colors duration-150
                               ${
                                 isLocked
                                   ? "opacity-50 cursor-not-allowed text-slate-500"
                                   : isCurrent
                                   ? "bg-blue-400/10 text-blue-400 font-bold hover:bg-blue-400/20"
                                   : isCompleted
                                   ? "text-green-400 hover:bg-green-400/20 hover:text-green-300"
                                   : "text-slate-300 hover:bg-blue-400/20 hover:text-purple-400"
                               }`}
                  >
                    <div className="flex items-center justify-between">
                      <span>Level {level.id}</span>
                      {isCompleted && (
                        <span className="text-green-400 text-xs">✓</span>
                      )}
                      {isLocked && (
                        <span className="text-slate-500 text-xs">🔒</span>
                      )}
                    </div>
                  </button>
                );
              })
            )}
          </div>
        </>
      )}
    </div>
  );
}
