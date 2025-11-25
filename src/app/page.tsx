'use client'

import { useState, useEffect } from 'react'
// import { WhatsAppService } from '../../services/whatsapp/whatsapp-api'
// import { AIService } from '../../services/ai/ollama-service'
// import { SyncService } from '../../services/sync/sync-service'

export default function Home() {
  const [servicesStatus, setServicesStatus] = useState({
    sqlServer: 'loading',
    // whatsapp: 'loading', 
    // ai: 'loading',
    // sync: 'loading'
  })
  const [citas, setCitas] = useState([])

  useEffect(() => {
    checkServices()
  }, [])

  const checkServices = async () => {
    // Verificar citas via API
    try {
      const response = await fetch('/api/citas')
      const citasData = await response.json()
      setCitas(citasData)
      setServicesStatus(prev => ({ ...prev, sqlServer: 'connected' }))
    } catch (error) {
      setServicesStatus(prev => ({ ...prev, sqlServer: 'error' }))
    }

    // Otros servicios comentados por ahora
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'connected': return 'bg-green-500'
      case 'loading': return 'bg-yellow-500' 
      case 'error': return 'bg-red-500'
      default: return 'bg-gray-500'
    }
  }

  const getStatusText = (status: string) => {
    switch (status) {
      case 'connected': return 'Conectado'
      case 'loading': return 'Conectando...'
      case 'error': return 'Error'
      default: return 'Desconocido'
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-navy-50 to-white p-8">
      <div className="max-w-6xl mx-auto">
        
        {/* Header */}
        <div className="text-center mb-8">
          <div className="w-20 h-20 bg-navy-600 rounded-2xl flex items-center justify-center mx-auto mb-4">
            <span className="text-white font-bold text-2xl">RG</span>
          </div>
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Rubio García Dental
          </h1>
          <p className="text-gray-600 text-lg">Sistema de Gestión Integral</p>
        </div>

        {/* Estado de Servicios */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          {Object.entries(servicesStatus).map(([service, status]) => (
            <div key={service} className="bg-white rounded-xl border border-gray-200 p-4 shadow-sm">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="font-semibold text-gray-900 capitalize">
                    {service === 'sqlServer' ? 'SQL Server' : 
                     service === 'whatsapp' ? 'WhatsApp' :
                     service === 'ai' ? 'IA' : 'Sincronización'}
                  </h3>
                  <p className="text-sm text-gray-500 mt-1">
                    {getStatusText(status)}
                  </p>
                </div>
                <div className={`w-3 h-3 rounded-full ${getStatusColor(status)} animate-pulse`}></div>
              </div>
            </div>
          ))}
        </div>

        {/* Citas del Día */}
        <div className="bg-white rounded-2xl border border-gray-200 p-6 shadow-sm mb-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            Últimas Citas ({citas.length})
          </h2>
          <div className="space-y-3">
            {citas.length > 0 ? (
              citas.map((cita: any, index: number) => (
                <div key={index} className="flex items-center justify-between p-3 border border-gray-100 rounded-lg">
                  <div>
                    <h4 className="font-medium text-gray-900">{cita.nombre}</h4>
                    <p className="text-sm text-gray-500">{cita.fecha} - {cita.hora}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-medium text-gray-900">{cita.doctor}</p>
                    <p className="text-xs text-gray-500">{cita.tratamiento}</p>
                  </div>
                </div>
              ))
            ) : (
              <div className="text-center py-8 text-gray-500">
                <p>No hay citas disponibles</p>
                <p className="text-sm mt-1">Conectando con base de datos...</p>
              </div>
            )}
          </div>
        </div>

        {/* Acciones Rápidas */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <button 
            onClick={checkServices}
            className="bg-navy-600 text-white py-3 rounded-xl font-semibold hover:bg-navy-700 transition-colors"
          >
            Actualizar
          </button>
          <button className="bg-green-600 text-white py-3 rounded-xl font-semibold hover:bg-green-700 transition-colors">
            Nueva Cita
          </button>
          <button className="bg-blue-600 text-white py-3 rounded-xl font-semibold hover:bg-blue-700 transition-colors">
            Nuevo Paciente
          </button>
          <button className="bg-orange-600 text-white py-3 rounded-xl font-semibold hover:bg-orange-700 transition-colors">
            Mensaje
          </button>
        </div>

      </div>
    </div>
  )
}