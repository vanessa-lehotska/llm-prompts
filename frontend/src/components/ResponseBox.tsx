import { motion } from "framer-motion";

type Props = {
  response: string;
};

export default function ResponseBox({ response }: Props) {
  return (
    <motion.pre
      className="mt-6 max-w-xl w-full text-left text-sm bg-slate-800 border border-cyan-400 p-4 rounded 
                 whitespace-pre-wrap z-10 text-slate-100 shadow-[0_0_15px_rgba(6,182,212,0.2)]"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: response ? 1 : 0, y: response ? 0 : 20 }}
      transition={{ duration: 0.5 }}
    >
      {response}
    </motion.pre>
  );
}
