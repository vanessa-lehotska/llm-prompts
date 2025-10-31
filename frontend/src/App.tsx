import React, { useState } from 'react'
import Header from './components/Header'
import LevelSelector from './components/LevelSelector'
import PromptInput from './components/PromptInput'
import ResponseBox from './components/ResponseBox'

export default function App() {
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
        body: JSON.stringify({ user_message: userInput, difficulty }),
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
          setResponse(prev => prev + '\n\n🚀 Advancing to next level...')
        }, 2000) // Wait 2 seconds to let user read the success message
      }
      
      if (data.game_completed) {
        setTimeout(() => {
          setResponse(prev => prev + '\n\n🎊 Game completed! You are a prompt breaking master!')
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
      {/* Floating particles background */}
      <div className="particles">
        <div className="particle" style={{ top: '15%', left: '10%' }}></div>
        <div className="particle" style={{ top: '25%', left: '80%' }}></div>
        <div className="particle" style={{ top: '45%', left: '15%' }}></div>
        <div className="particle" style={{ top: '65%', left: '70%' }}></div>
        <div className="particle" style={{ top: '80%', left: '25%' }}></div>
        <div className="particle" style={{ top: '35%', left: '90%' }}></div>
        <div className="particle" style={{ top: '75%', left: '85%' }}></div>
        <div className="particle" style={{ top: '55%', left: '5%' }}></div>
      </div>

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
