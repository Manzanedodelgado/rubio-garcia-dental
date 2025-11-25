const WHATSAPP_BASE_URL = process.env.WHATSAPP_BAILEYS_HOST || 'http://192.168.1.34:3001'

export class WhatsAppService {
  static async sendMessage(phone: string, message: string) {
    try {
      const response = await fetch(`${WHATSAPP_BASE_URL}/send`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          phone: phone.replace('+', ''), 
          message 
        })
      })
      
      if (!response.ok) throw new Error('Error en respuesta HTTP')
      return await response.json()
    } catch (error) {
      console.error('❌ Error enviando WhatsApp:', error)
      return { success: false, error: 'Servicio no disponible' }
    }
  }

  static async getStatus() {
    try {
      const response = await fetch(`${WHATSAPP_BASE_URL}/status`)
      return await response.json()
    } catch (error) {
      console.error('❌ Error obteniendo estado WhatsApp:', error)
      return { status: 'offline', message: 'Servicio no disponible' }
    }
  }

  static async sendAppointmentReminder(phone: string, appointmentData: any) {
    const message = `Recordatorio de cita:\n📅 Fecha: ${appointmentData.fecha}\n⏰ Hora: ${appointmentData.hora}\n👨‍⚕️ Doctor: ${appointmentData.doctor}\n📍 Clínica Rubio García Dental`
    return await this.sendMessage(phone, message)
  }
}