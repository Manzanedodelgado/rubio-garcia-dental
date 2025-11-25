const WHATSAPP_API = process.env.WHATSAPP_BAILEYS_HOST

export async function sendWhatsAppMessage(phone: string, message: string) {
  try {
    const response = await fetch(`${WHATSAPP_API}/send`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ phone, message })
    })
    return await response.json()
  } catch (error) {
    console.error('❌ Error enviando WhatsApp:', error)
    return null
  }
}