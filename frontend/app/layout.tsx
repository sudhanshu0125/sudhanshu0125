import './globals.css';
import { ReactNode } from 'react';

export const metadata = {
  title: 'InfluencersPlace Lead Agent',
  description: 'Automated lead discovery dashboard',
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
