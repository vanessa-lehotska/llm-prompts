import { motion } from 'framer-motion'
import injectionIcon from '../assets/images/injection.png'
import testingIcon from '../assets/images/automated_test.png'
import ParticlesBackground from '../components/ParticlesBackground'

type Props = {
  onSelectMode: (mode: 'prompt_injection' | 'promptfoo') => void
}

export default function HomeScreen({ onSelectMode }: Props) {
  const modes = [
    {
      id: 'prompt_injection' as const,
      title: 'Prompt Attacks',
      description: 'Try to break the system with prompts',
      icon: injectionIcon,
      color: 'blue',
      levels: 6
    },
    {
      id: 'promptfoo' as const,
      title: 'Automated Testing',
      description: 'Let AI generate attacks',
      icon: testingIcon,
      color: 'red',
      levels: 'AI Attacks'
    }
  ]

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-6 relative overflow-hidden">
      <ParticlesBackground />

      {/* Header */}
      <motion.h1
        className="text-6xl font-bold mb-12 z-10"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.4 }}
      >
        LLM Security
      </motion.h1>

      {/* Mode Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl w-full z-10">
        {modes.map((mode, index) => (
          <motion.button
            key={mode.id}
            onClick={() => onSelectMode(mode.id)}
            className="bg-slate-800/80 backdrop-blur-sm border border-slate-700 rounded-lg p-6 
                       hover:border-blue-400 transition-all duration-200 text-left
                       hover:bg-slate-800"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.3 }}
          >
            <div className="flex justify-center items-center mb-4 h-16">
              {mode.icon ? (
                <img 
                  src={mode.icon} 
                  alt={mode.title}
                  className="h-12 w-12 object-contain opacity-70"
                  style={{ filter: 'brightness(0) invert(1)' }}
                />
              ) : (
                <div className="h-12 w-12 bg-slate-700 rounded flex items-center justify-center text-slate-500 text-xs">
                  Icon
                </div>
              )}
            </div>
            <h2 className="text-lg font-bold text-slate-100 mb-2">
              {mode.title}
            </h2>
            <p className="text-slate-500 text-sm mb-4">
              {mode.description}
            </p>
            <div className="text-blue-400 text-sm">
              Start →
            </div>
          </motion.button>
        ))}
      </div>
    </div>
  )
}
