import './globals.css'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import Footer from '../components/structure/Footer'
import Header from '../components/structure/Header'
import { getServerSession } from 'next-auth';
import SessionProvider from '../components/SessionProvider';
const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Music Tracker',
  description: 'Graphs to better explain your tastes',
}

export default async function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const session  = await getServerSession()
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className='flex flex-col min-h-screen'>
          <Header />
          {children}
          <Footer />
        </div>

      </body>
    </html>
  )
}
