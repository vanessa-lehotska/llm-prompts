import { useState } from 'react'

type Props = {
  difficulty: number
  setDifficulty: (level: number) => void
}

export default function LevelSelector({ difficulty, setDifficulty }: Props) {
  const [isOpen, setIsOpen] = useState(false)

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
        <span className={`transition-transform duration-200 ${isOpen ? 'rotate-180' : ''}`}>
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
          <div className="absolute top-full mt-1 w-full bg-slate-800 border border-blue-400 rounded 
                          max-h-60 overflow-y-auto z-50
                          origin-top animate-[slideDown_0.2s_ease-out]
                          shadow-[0_0_20px_rgba(59,130,246,0.3)]">
            {Array.from({ length: 10 }, (_, i) => (
              <button
                key={i}
                onClick={() => {
                  setDifficulty(i + 1)
                  setIsOpen(false)
                }}
                className={`w-full text-left px-4 py-2 transition-colors duration-150
                           hover:bg-blue-400/20 hover:text-purple-400
                           ${difficulty === i + 1 ? 'bg-blue-400/10 text-blue-400 font-bold' : 'text-slate-300'}`}
              >
                Level {i + 1}
              </button>
            ))}
          </div>
        </>
      )}
    </div>
  )
}
