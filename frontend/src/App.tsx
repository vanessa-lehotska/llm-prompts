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
      const text = await res.text()
      setResponse(text || `HTTP ${res.status}`)
    } catch (e: any) {
      setResponse(String(e))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-start p-6 bg-[#0a0a0a] relative overflow-hidden">
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
