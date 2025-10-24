import Image from "next/image";
import { Button } from "@/components/Button";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
      <main className="container mx-auto px-4 py-16">
        <div className="text-center mb-12">
          <Image
            className="mx-auto mb-8 dark:invert"
            src="/next.svg"
            alt="Next.js logo"
            width={200}
            height={40}
            priority
          />
          <h1 className="text-4xl md:text-6xl font-bold text-gray-900 dark:text-white mb-6">
            Welcome to{" "}
            <span className="text-blue-600 dark:text-blue-400">Sirius Games</span>
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300 mb-8 max-w-2xl mx-auto">
            Tu proyecto Next.js con TypeScript, React y Tailwind CSS está listo para empezar.
          </p>
        </div>

        <div className="flex flex-col md:flex-row items-center justify-center gap-6 mb-12">
          <Button variant="primary" size="lg">
            Comenzar
          </Button>
          <Button variant="secondary" size="lg">
            Documentación
          </Button>
        </div>

        <div className="grid md:grid-cols-3 gap-8 max-w-4xl mx-auto">
          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-lg">
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">
              ⚡ Next.js 16
            </h3>
            <p className="text-gray-600 dark:text-gray-300">
              Framework React de producción con App Router y las últimas características.
            </p>
          </div>
          
          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-lg">
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">
              🔷 TypeScript
            </h3>
            <p className="text-gray-600 dark:text-gray-300">
              Tipado estático para un desarrollo más seguro y productivo.
            </p>
          </div>
          
          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-lg">
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">
              🎨 Tailwind CSS
            </h3>
            <p className="text-gray-600 dark:text-gray-300">
              Framework CSS utility-first para un diseño rápido y consistente.
            </p>
          </div>
        </div>

        <div className="text-center mt-12">
          <p className="text-gray-500 dark:text-gray-400">
            Edita{" "}
            <code className="bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded text-sm">
              src/app/page.tsx
            </code>{" "}
            para comenzar a desarrollar
          </p>
        </div>
      </main>
    </div>
  );
}
