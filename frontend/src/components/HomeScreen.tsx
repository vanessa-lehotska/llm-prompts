import { motion } from 'framer-motion'
import injectionIcon from '../assets/images/injection.png'
import jailbreakingIcon from '../assets/images/jailbreak.png'
import testingIcon from '../assets/images/automated_test.png'
import ParticlesBackground from './ParticlesBackground'

type Props = {
  onSelectMode: (mode: 'prompt_injection' | 'jailbreaking' | 'automated_testing') => void
}

export default function HomeScreen({ onSelectMode }: Props) {
  const modes = [
    {
      id: 'prompt_injection' as const,
      title: 'Prompt Injection Challenge',
      description: 'Test prompt injection attacks on LLM applications. Find the secret in each level using various techniques.',
      icon: injectionIcon,
      color: 'blue',
      levels: 5
    },
    {
      id: 'jailbreaking' as const,
      title: 'Jailbreaking Arena',
      description: 'Test bypassing of model safety guardrails. Convince the model to do something it shouldn\'t.',
      icon: jailbreakingIcon,
      color: 'purple',
      levels: 4
    },
    {
      id: 'automated_testing' as const,
      title: 'Automated Testing Lab',
      description: 'Automated testing of LLM applications against an attack library. Find out how resistant your system prompt is.',
      icon: testingIcon,
      color: 'cyan',
      levels: 'Library'
    }
  ]

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-6 relative overflow-hidden">
      <ParticlesBackground />

      {/* Header */}
      <motion.h1
        className="text-5xl font-bold mb-2 z-10 bg-gradient-to-r from-blue-400 via-purple-400 to-cyan-400 bg-clip-text text-transparent"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        LLM Security Lab
      </motion.h1>
      
      <motion.p
        className="text-slate-400 mb-12 text-lg z-10"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.6, delay: 0.2 }}
      >
        Experimental platform for testing the security of large language models
      </motion.p>

      {/* Mode Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-6xl w-full z-10">
        {modes.map((mode, index) => (
          <motion.button
            key={mode.id}
            onClick={() => onSelectMode(mode.id)}
            className="bg-slate-800/80 backdrop-blur-sm border-2 border-slate-700 rounded-lg p-6 
                       hover:border-blue-400 hover:shadow-[0_0_20px_rgba(59,130,246,0.3)]
                       transition-all duration-300 text-left group
                       hover:scale-105 hover:bg-slate-800"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.3 + index * 0.1 }}
          >
            <div className="flex justify-center items-center mb-4 h-16 group-hover:scale-110 transition-transform duration-300">
              {mode.icon ? (
                <img 
                  src={mode.icon} 
                  alt={mode.title}
                  className="h-12 w-12 object-contain opacity-70 group-hover:opacity-100 transition-opacity"
                  style={{ filter: 'brightness(0) invert(1)' }}
                />
              ) : (
                <div className="h-12 w-12 bg-slate-700 rounded flex items-center justify-center text-slate-500 text-xs">
                  Icon
                </div>
              )}
            </div>
            <h2 className="text-xl font-bold text-slate-100 mb-2 group-hover:text-blue-400 transition-colors">
              {mode.title}
            </h2>
            <p className="text-slate-400 text-sm mb-4 leading-relaxed">
              {mode.description}
            </p>
            <div className="flex items-center justify-between">
              <span className="text-xs text-slate-500">
                {typeof mode.levels === 'number' ? `${mode.levels} levels` : mode.levels}
              </span>
              <span className="text-blue-400 group-hover:text-purple-400 transition-colors">
                Start →
              </span>
            </div>
          </motion.button>
        ))}
      </div>

      {/* Footer */}
      <motion.p
        className="text-slate-500 text-sm mt-12 z-10"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.6, delay: 0.8 }}
      >
        Select a mode and start testing LLM security
      </motion.p>
    </div>
  )
}
