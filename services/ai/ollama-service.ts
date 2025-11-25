const OLLAMA_HOST = process.env.LLM_HOST

export async function askAI(prompt: string) {
  try {
    const response = await fetch(`${OLLAMA_HOST}/api/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: 'llama2',
        prompt: prompt,
        stream: false
      })
    })
    return await response.json()
  } catch (error) {
    console.error('❌ Error con Ollama:', error)
    return null
  }
}