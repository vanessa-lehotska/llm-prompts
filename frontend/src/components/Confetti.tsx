import { motion } from "framer-motion";
import { useEffect, useState } from "react";

type Props = {
  show: boolean;
  onComplete?: () => void;
};

export default function Confetti({ show, onComplete }: Props) {
  const [particles, setParticles] = useState<
    Array<{ id: number; x: number; delay: number; color: string }>
  >([]);

  useEffect(() => {
    if (show) {
      // Generate confetti particles
      const colors = ["#3B82F6", "#8B5CF6", "#06B6D4", "#10B981", "#F59E0B"];
      const newParticles = Array.from({ length: 50 }, (_, i) => ({
        id: i,
        x: Math.random() * 100,
        delay: Math.random() * 0.5,
        color: colors[Math.floor(Math.random() * colors.length)],
      }));
      setParticles(newParticles);

      // Call onComplete after animation
      const timer = setTimeout(() => {
        if (onComplete) onComplete();
      }, 1000); // 1 second - faster animation

      return () => clearTimeout(timer);
    } else {
      setParticles([]);
    }
  }, [show, onComplete]);

  if (!show) return null;

  return (
    <div className="fixed inset-0 pointer-events-none z-50 overflow-hidden">
      {particles.map((particle) => (
        <motion.div
          key={particle.id}
          className="absolute w-2 h-2 rounded-full"
          style={{
            left: `${particle.x}%`,
            backgroundColor: particle.color,
            boxShadow: `0 0 6px ${particle.color}`,
          }}
          initial={{
            top: "-10%",
            opacity: 1,
            scale: 1,
            rotate: 0,
          }}
          animate={{
            top: "110%",
            opacity: [1, 1, 0],
            scale: [1, 1.2, 0.5],
            rotate: [0, 360, 720],
            x: [0, Math.random() * 200 - 100, Math.random() * 400 - 200],
          }}
          transition={{
            duration: 1,
            delay: particle.delay,
            ease: "easeOut",
          }}
        />
      ))}
    </div>
  );
}
