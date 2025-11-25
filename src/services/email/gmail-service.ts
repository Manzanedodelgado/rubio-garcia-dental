export class GmailService {
  static async sendEmail(to: string, subject: string, body: string) {
    try {
      // Simulación - implementación real necesitaría OAuth2
      console.log(`📧 Email simulado enviado a: ${to}`)
      console.log(`📝 Asunto: ${subject}`)
      
      return { 
        success: true, 
        message: 'Email enviado (simulación)',
        details: { to, subject }
      }
    } catch (error) {
      console.error('❌ Error enviando email:', error)
      return { success: false, error: 'Error enviando email' }
    }
  }

  static async sendAppointmentConfirmation(to: string, appointmentData: any) {
    const subject = `Confirmación de Cita - Clínica Rubio García Dental`
    const body = `
      <h2>Confirmación de Cita</h2>
      <p>Estimado/a paciente,</p>
      <p>Su cita ha sido confirmada:</p>
      <ul>
        <li><strong>Fecha:</strong> ${appointmentData.fecha}</li>
        <li><strong>Hora:</strong> ${appointmentData.hora}</li>
        <li><strong>Doctor:</strong> ${appointmentData.doctor}</li>
        <li><strong>Tratamiento:</strong> ${appointmentData.tratamiento}</li>
      </ul>
      <p>📍 <strong>Dirección:</strong> Calle Mayor 19, 28921 Alcorcón, Madrid</p>
      <p>📞 <strong>Teléfono:</strong> 916 410 841 | 664 218 253</p>
    `

    return await this.sendEmail(to, subject, body)
  }
}