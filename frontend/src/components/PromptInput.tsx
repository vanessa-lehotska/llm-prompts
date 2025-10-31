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
        className="w-full max-w-xl bg-slate-800 text-slate-100 border border-blue-400 p-4 rounded mb-4 z-10 resize-none 
                   focus:outline-none focus:ring-2 focus:ring-purple-400 focus:border-purple-400
                   placeholder-slate-400"
        rows={4}
        placeholder="Enter your prompt to break the AI..."
        value={userInput}
        onChange={(e) => setUserInput(e.target.value)}
      />
      <button
        className="px-6 py-2 border border-blue-400 text-blue-400 rounded 
                   hover:bg-blue-400 hover:text-slate-900 
                   disabled:opacity-50 disabled:cursor-not-allowed
                   transition-all duration-200 z-10 font-medium"
        onClick={send}
        disabled={loading}
      >
        {loading ? 'Sending...' : 'Send'}
      </button>
    </>
  )
}
