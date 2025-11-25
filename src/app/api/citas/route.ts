import { NextResponse } from 'next/server'

export async function GET() {
  try {
    // Simulamos datos por ahora - luego conectaremos con SQL Server
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
    
    return NextResponse.json(citas)
  } catch (error) {
    return NextResponse.json(
      { error: 'Error obteniendo citas' },
      { status: 500 }
    )
  }
}