import sql from 'mssql'

const sqlConfig = {
  server: process.env.SQLSERVER_HOST,
  database: process.env.SQLSERVER_DATABASE,
  user: process.env.SQLSERVER_USER,
  password: process.env.SQLSERVER_PASSWORD,
  options: {
    enableArithAbort: true,
    trustServerCertificate: true,
    encrypt: false
  },
  pool: {
    max: 10,
    min: 0,
    idleTimeoutMillis: 30000
  }
}

export class SQLServerService {
  private static pool: sql.ConnectionPool | null = null

  static async connect() {
    if (!this.pool) {
      try {
        this.pool = await sql.connect(sqlConfig)
        console.log('✅ Conectado a SQL Server 2008')
      } catch (error) {
        console.error('❌ Error conectando a SQL Server:', error)
        throw error
      }
    }
    return this.pool
  }

  static async getCitas() {
    try {
      const pool = await this.connect()
      const result = await pool.request()
        .query('SELECT TOP 10 * FROM dbo.DCitas ORDER BY Fecha DESC')
      return result.recordset
    } catch (error) {
      console.error('❌ Error obteniendo citas:', error)
      return []
    }
  }

  static async getPacientes() {
    try {
      const pool = await this.connect()
      const result = await pool.request()
        .query('SELECT TOP 10 * FROM dbo.Pacientes ORDER BY Nombre')
      return result.recordset
    } catch (error) {
      console.error('❌ Error obteniendo pacientes:', error)
      return []
    }
  }
}