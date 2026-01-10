import React, { useState } from 'react'
import Header from './Header'
import LevelSelector from './LevelSelector'
import PromptInput from './PromptInput'
import ResponseBox from './ResponseBox'
import ParticlesBackground from './ParticlesBackground'

type Props = {
  onBack: () => void
}

export default function PromptInjectionMode({ onBack }: Props) {
  const [difficulty, setDifficulty] = useState(1)
  const [userInput, setUserInput] = useState('')
  const [response, setResponse] = useState('')
  const [loading, setLoading] = useState(false)

  async function send() {
    if (!userInput.trim()) return
    setLoading(true)
    setResponse('')
    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          user_message: userInput, 
          difficulty,
          mode: 'prompt_injection'
        }),
      })
      const data = await res.json()
      
      // Display AI response
      setResponse(data.response)
      
      // Check if user found the secret and should advance
      if (data.level_up && data.next_level) {
        setTimeout(() => {
          setDifficulty(data.next_level)
          setUserInput('')
          // Show level up message briefly
          setResponse(prev => prev + '\n\nAdvancing to next level...')
        }, 2000) // Wait 2 seconds to let user read the success message
      }
      
      if (data.game_completed) {
        setTimeout(() => {
          setResponse(prev => prev + '\n\nGame completed! You are a prompt breaking master!')
        }, 2000)
      }
      
    } catch (e: any) {
      setResponse(`Error: ${String(e)}`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-start p-6 relative overflow-hidden">
      <ParticlesBackground />

      {/* Back button */}
      <button
        onClick={onBack}
        className="absolute top-4 left-4 z-20 px-4 py-2 bg-slate-800/80 border border-slate-600 
                   text-slate-300 rounded hover:bg-slate-700 hover:border-blue-400 
                   hover:text-blue-400 transition-all duration-200"
      >
        ← Back to Home
      </button>

      <Header />
      <LevelSelector difficulty={difficulty} setDifficulty={setDifficulty} />
      <PromptInput
        userInput={userInput}
        setUserInput={setUserInput}
        send={send}
        loading={loading}
      />
      <ResponseBox response={response} />
    </div>
  )
}
