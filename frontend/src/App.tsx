import { useState } from 'react'
import HomeScreen from './screens/HomeScreen'
import PromptInjectionScreen from './screens/PromptInjectionScreen'

export default function App() {
  const [started, setStarted] = useState(false)

  if (!started) {
    return <HomeScreen onSelectMode={() => setStarted(true)} />
  }

  return <PromptInjectionScreen onBack={() => setStarted(false)} />
}
