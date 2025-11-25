import './globals.css'

export const metadata = {
  title: 'Rubio García Dental',
  description: 'Sistema de gestión dental',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="es">
      <body className="font-sans">
        {children}
      </body>
    </html>
  )
}