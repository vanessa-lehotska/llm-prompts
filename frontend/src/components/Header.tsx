import { motion } from 'framer-motion'

export default function Header() {
  return (
    <motion.h1
      className="text-4xl font-bold mb-4 z-10 text-neon"
      animate={{ opacity: [0.5, 1, 0.5] }}
      transition={{ duration: 3, repeat: Infinity }}
    >
      PROMPTBREAK
    </motion.h1>
  )
}
