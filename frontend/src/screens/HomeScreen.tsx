import { motion } from "framer-motion";
import injectionIcon from "../assets/images/injection.png";
import ParticlesBackground from "../components/ParticlesBackground";

type Props = {
  onSelectMode: () => void;
};

export default function HomeScreen({ onSelectMode }: Props) {
  return (
    <div className="min-h-screen flex items-center justify-center p-6 relative overflow-hidden bg-slate-950">
      <ParticlesBackground />

      <motion.div
        className="relative z-10 w-full max-w-5xl rounded-2xl border border-slate-800 bg-slate-900/75 backdrop-blur-md shadow-[0_0_50px_rgba(34,211,238,0.08)] overflow-hidden"
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.45 }}
      >
        <div className="absolute inset-0 pointer-events-none bg-[radial-gradient(circle_at_top_left,rgba(34,211,238,0.08),transparent_35%),radial-gradient(circle_at_bottom_right,rgba(59,130,246,0.10),transparent_35%)]" />

        <div className="grid md:grid-cols-[1.25fr_0.75fr] relative">
          <div className="p-8 md:p-12 border-b md:border-b-0 md:border-r border-slate-800">
            <motion.h1
              className="text-5xl md:text-6xl font-bold text-slate-100 leading-none mb-6"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.4 }}
            >
              Break the Prompt
            </motion.h1>

            <motion.div
              className="max-w-2xl space-y-4 text-[15px] md:text-base leading-7 font-mono"
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.45, delay: 0.2 }}
            >
              <p className="text-slate-400">
                Each level hides a secret inside the model. Your objective is to
                extract it.
              </p>

              <p className="text-slate-400">
                As you progress, the defenses become stricter, less predictable,
                and harder to bypass.
              </p>

              <p className="text-emerald-400">
                Just you vs LLM.
              </p>
            </motion.div>
          </div>

          <div className="p-8 md:p-10 flex flex-col justify-center items-center text-center bg-slate-950/40">
            <motion.div
              className="w-16 h-16 rounded-2xl border border-cyan-500/30 bg-slate-900/80 flex items-center justify-center mb-6 shadow-[0_0_25px_rgba(34,211,238,0.12)]"
              initial={{ opacity: 0, scale: 0.92 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.35, delay: 0.2 }}
            >
              <img
                src={injectionIcon}
                alt="Break the Prompt"
                className="h-9 w-9 object-contain opacity-90"
                style={{ filter: "brightness(0) invert(1)" }}
              />
            </motion.div>

            <motion.h2
              className="text-xl font-semibold text-slate-100 mb-3"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.35, delay: 0.3 }}
            >
              Start the challenge
            </motion.h2>


            <motion.button
              onClick={onSelectMode}
              className="w-full max-w-xs rounded-lg border border-cyan-400/70 bg-cyan-400/10 px-6 py-3 text-cyan-300 font-medium tracking-wide transition-all duration-200 hover:bg-cyan-400 hover:text-slate-950 hover:shadow-[0_0_20px_rgba(34,211,238,0.25)]"
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.35, delay: 0.4 }}
            >
              Enter
            </motion.button>
          </div>
        </div>
      </motion.div>
    </div>
  );
}