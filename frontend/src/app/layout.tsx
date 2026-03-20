import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Legal Demand Planner",
  description: "Análise de demanda para benefícios e direitos",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="pt-BR">
      <body className="bg-gray-50 text-gray-900 min-h-screen">{children}</body>
    </html>
  );
}
