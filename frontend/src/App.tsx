import React, { useState } from 'react'
import HomeScreen from './screens/HomeScreen'
import PromptInjectionMode from './screens/PromptInjectionMode'
import PromptfooMode from './screens/PromptfooMode'

type Mode = 'home' | 'prompt_injection' | 'promptfoo'

export default function App() {
  const [currentMode, setCurrentMode] = useState<Mode>('home')

  const handleModeSelect = (mode: 'prompt_injection' | 'promptfoo') => {
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

  if (currentMode === 'promptfoo') {
    return <PromptfooMode onBack={handleBackToHome} />
  }

  return null
}
