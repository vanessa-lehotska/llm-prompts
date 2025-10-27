import { motion } from 'framer-motion'

type Props = {
  response: string
}

export default function ResponseBox({ response }: Props) {
  return (
    <motion.pre
      className="mt-6 max-w-xl w-full text-left text-sm bg-black border border-neon p-4 rounded whitespace-pre-wrap z-10"
      initial={{ opacity: 0 }}
      animate={{ opacity: response ? 1 : 0 }}
      transition={{ duration: 0.5 }}
    >
      {response || 'Response will appear here...'}
    </motion.pre>
  )
}
