import React, { useState } from 'react'
import HomeScreen from './components/HomeScreen'
import PromptInjectionMode from './components/PromptInjectionMode'

type Mode = 'home' | 'prompt_injection' | 'jailbreaking' | 'automated_testing'

export default function App() {
  const [currentMode, setCurrentMode] = useState<Mode>('home')

  const handleModeSelect = (mode: 'prompt_injection' | 'jailbreaking' | 'automated_testing') => {
    setCurrentMode(mode)
  }

  const handleBackToHome = () => {
    setCurrentMode('home')
  }

  // Render based on current mode
  if (currentMode === 'home') {
    return <HomeScreen onSelectMode={handleModeSelect} />
  }

  if (currentMode === 'prompt_injection') {
    return <PromptInjectionMode onBack={handleBackToHome} />
  }

  // Placeholder for other modes (will be implemented in next phases)
  if (currentMode === 'jailbreaking') {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl text-slate-100 mb-4">Jailbreaking Arena</h1>
          <p className="text-slate-400 mb-4">Coming soon...</p>
          <button
            onClick={handleBackToHome}
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          >
            Back to Home
          </button>
        </div>
      </div>
    )
  }

  if (currentMode === 'automated_testing') {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl text-slate-100 mb-4">Automated Testing Lab</h1>
          <p className="text-slate-400 mb-4">Coming soon...</p>
          <button
            onClick={handleBackToHome}
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          >
            Back to Home
          </button>
        </div>
      </div>
    )
  }

  return null
}
