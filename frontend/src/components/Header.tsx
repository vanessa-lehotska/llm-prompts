import { motion } from 'framer-motion'

export default function Header() {
  return (
    <motion.h1
      className="text-4xl font-bold mb-4 z-10 bg-gradient-to-r from-blue-400 via-purple-400 to-cyan-400 bg-clip-text text-transparent"
      animate={{ opacity: [0.7, 1, 0.7] }}
      transition={{ duration: 3, repeat: Infinity }}
    >
      GenAI Security Hack
    </motion.h1>
  )
}
