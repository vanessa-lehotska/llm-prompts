type Props = {
  userInput: string
  setUserInput: (val: string) => void
  send: () => void
  loading: boolean
}

export default function PromptInput({ userInput, setUserInput, send, loading }: Props) {
  return (
    <>
      <textarea
        className="w-full max-w-xl bg-black text-neon border border-neon p-4 rounded mb-4 z-10 resize-none focus:outline-none focus:ring-2 focus:ring-neon"
        rows={4}
        placeholder="Zadaj svoj prompt..."
        value={userInput}
        onChange={(e) => setUserInput(e.target.value)}
      />
      <button
        className="px-6 py-2 border border-neon rounded hover:bg-neon hover:text-black transition-colors z-10"
        onClick={send}
        disabled={loading}
      >
        {loading ? 'Sending...' : 'Send'}
      </button>
    </>
  )
}
