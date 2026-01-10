import { useState, useEffect } from "react";

type Props = {
  difficulty: number;
  setDifficulty: (level: number) => void;
};

type Level = {
  id: number;
  secret: string;
  has_system_prompt: boolean;
  info: string;
};

export default function LevelSelector({ difficulty, setDifficulty }: Props) {
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
              levels.map((level) => (
                <button
                  key={level.id}
                  onClick={() => {
                    setDifficulty(level.id);
                    setIsOpen(false);
                  }}
                  className={`w-full text-left px-4 py-2 transition-colors duration-150
                             hover:bg-blue-400/20 hover:text-purple-400
                             ${
                               difficulty === level.id
                                 ? "bg-blue-400/10 text-blue-400 font-bold"
                                 : "text-slate-300"
                             }`}
                >
                  Level {level.id}
                </button>
              ))
            )}
          </div>
        </>
      )}
    </div>
  );
}
