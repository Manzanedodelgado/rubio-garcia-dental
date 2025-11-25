const OLLAMA_HOST = process.env.LLM_HOST || 'http://192.168.1.34:11434'

export class AIService {
  static async generateResponse(prompt: string, context?: string) {
    try {
      const fullPrompt = context ? 
        `Eres un asistente de la clínica dental Rubio García. ${context}\n\nPregunta: ${prompt}` :
        `Eres un asistente de la clínica dental Rubio García. Responde amablemente a: ${prompt}`

      const response = await fetch(`${OLLAMA_HOST}/api/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model: 'llama2',
          prompt: fullPrompt,
          stream: false,
          options: {
            temperature: 0.7,
            top_p: 0.9
          }
        })
      })

      if (!response.ok) throw new Error('Error en respuesta Ollama')
      const data = await response.json()
      return data.response
    } catch (error) {
      console.error('❌ Error con Ollama AI:', error)
      return 'Lo siento, el servicio de IA no está disponible en este momento.'
    }
  }

  static async detectUrgency(message: string) {
    const urgentKeywords = ['dolor', 'urgente', 'emergencia', 'sangrado', 'hinchazón']
    const hasUrgency = urgentKeywords.some(keyword => 
      message.toLowerCase().includes(keyword)
    )
    
    return {
      isUrgent: hasUrgency,
      level: hasUrgency ? 'high' : 'low',
      detectedKeywords: urgentKeywords.filter(keyword => 
        message.toLowerCase().includes(keyword)
      )
    }
  }
}