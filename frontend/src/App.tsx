import React, { useState } from 'react'
import './app.css'

export default function App() {
  const [userInput, setUserInput] = useState('')
  const [response, setResponse] = useState('')
  const [loading, setLoading] = useState(false)
  const [difficulty, setDifficulty] = useState<number>(1)

  async function send() {
    setLoading(true)
    setResponse('')
    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_message: userInput,
          difficulty: difficulty,
        }),
      })
      const text = await res.text()
      try {
        const json = JSON.parse(text)
        const body = (json && typeof json === 'object' && 'response' in json)
          ? (json as any).response
          : JSON.stringify(json, null, 2)
        setResponse(body || `HTTP ${res.status}`)
      } catch {
        setResponse(text || `HTTP ${res.status}`)
      }
    } catch (e: any) {
      setResponse(String(e))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <h2>Prompt Game</h2>
      <div>
        <label>Level</label>
        <select
          className="fullwidth"
          value={difficulty}
          onChange={(e) => setDifficulty(Number(e.target.value))}
        >
          <option value={1}>Level 1</option>
          <option value={2}>Level 2</option>
          <option value={3}>Level 3</option>
          <option value={4}>Level 4</option>
          <option value={5}>Level 5</option>
          <option value={6}>Level 6</option>
          <option value={7}>Level 7</option>
        </select>
      </div>
      <label className="mt12" style={{ display: 'block' }}>Your prompt</label>
      <textarea className="textarea" rows={4} value={userInput} onChange={(e) => setUserInput(e.target.value)} />
      <button className="mt12" disabled={loading} onClick={send}>{loading ? 'Sending...' : 'Send'}</button>
      <div className="mt16">
        <strong>Response</strong>
        <pre className="response">{response}</pre>
      </div>
    </div>
  )
}


