import type { Metadata } from 'next';
import '../src/styles/globals.css';

export const metadata: Metadata = {
  title: 'Cute Love Proposal Website',
  description: 'A special Valentine\'s Day proposal website with interactive animations and heartfelt messages',
  viewport: {
    width: 'device-width',
    initialScale: 1,
    userScalable: false,
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
