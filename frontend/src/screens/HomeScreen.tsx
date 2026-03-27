import { motion } from 'framer-motion'
import injectionIcon from '../assets/images/injection.png'
import ParticlesBackground from '../components/ParticlesBackground'

type Props = {
  onSelectMode: () => void
}

export default function HomeScreen({ onSelectMode }: Props) {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-6 relative overflow-hidden">
      <ParticlesBackground />

      {/* Header */}
      <motion.h1
        className="text-6xl font-bold mb-8 z-10"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.4 }}
      >
        LLM Security
      </motion.h1>

      {/* Intro Instructions (not a card) */}
      <motion.div
        className="mb-8 max-w-2xl w-full text-slate-200 text-center z-10"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
      >
        <h2 className="text-xl font-semibold mb-2 tracking-wider">Welcome, Hacker</h2>
        <p className="text-slate-300 text-base font-mono">
          Your mission: <span className="text-green-400">exploit</span> the AI.<br />
          Each level hides a secret. Use your prompt engineering skills to trick the system and extract it.<br />
          The game starts at Level 1. Outsmart the defenses, level up, and prove you can break the black box.<br />
          <span className="text-pink-400">No mercy. No hints. Just you vs. the LLM.</span>
        </p>
      </motion.div>

      {/* Prompt Attacks Card */}
      <div className="max-w-2xl w-full z-10">
        <motion.div
          className="bg-slate-900/80 border border-slate-700 rounded-lg p-8 flex flex-col items-center justify-center shadow-lg hover:border-blue-400 transition-all duration-200 hover:bg-slate-900"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.3 }}
        >
          <div className="flex justify-center items-center mb-4 h-16 w-full">
            <img 
              src={injectionIcon} 
              alt="Prompt Attacks"
              className="h-12 w-12 object-contain opacity-70"
              style={{ filter: 'brightness(0) invert(1)' }}
            />
          </div>
          <h2 className="text-lg font-bold text-slate-100 mb-2 text-center w-full">
            Prompt Attacks
          </h2>
          <p className="text-slate-500 text-sm mb-6 text-center w-full">
            Try to break the system with prompts
          </p>
          <button
            onClick={onSelectMode}
            className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-6 rounded shadow transition-all duration-150 text-base mt-2"
          >
            Click here to start
          </button>
        </motion.div>
      </div>
    </div>
  )
}
