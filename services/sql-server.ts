import sql from 'mssql'

const config = {
  server: process.env.SQLSERVER_HOST,
  database: process.env.SQLSERVER_DATABASE,
  user: process.env.SQLSERVER_USER,
  password: process.env.SQLSERVER_PASSWORD,
  options: {
    enableArithAbort: true,
    trustServerCertificate: true,
  },
  pool: {
    max: 10,
    min: 0,
    idleTimeoutMillis: 30000
  }
}

export async function connectSQLServer() {
  try {
    const pool = await sql.connect(config)
    console.log('✅ Conectado a SQL Server 2008')
    return pool
  } catch (error) {
    console.error('❌ Error conectando a SQL Server:', error)
    return null
  }
}