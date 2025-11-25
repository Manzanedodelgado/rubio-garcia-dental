export class SQLServerService {
  static async getCitas() {
    try {
      // Simulamos datos - luego conectaremos via API
      const citas = [
        {
          id: 1,
          nombre: 'Maria Gonzalez',
          fecha: '2024-11-25',
          hora: '10:00',
          doctor: 'Dr. Mario Rubio',
          tratamiento: 'Limpieza dental'
        },
        {
          id: 2, 
          nombre: 'Juan Martinez',
          fecha: '2024-11-25',
          hora: '11:30',
          doctor: 'Dra. Virginia Tresgallo', 
          tratamiento: 'Ortodoncia'
        }
      ]
      return citas
    } catch (error) {
      console.error('Error obteniendo citas:', error)
      return []
    }
  }

  static async getPacientes() {
    try {
      // Simulamos datos
      const pacientes = [
        {
          id: 1,
          nombre: 'Maria Gonzalez',
          telefono: '+34 612 345 678',
          email: 'maria@email.com'
        },
        {
          id: 2,
          nombre: 'Juan Martinez', 
          telefono: '+34 623 456 789',
          email: 'juan@email.com'
        }
      ]
      return pacientes
    } catch (error) {
      console.error('Error obteniendo pacientes:', error)
      return []
    }
  }
}