# Sirius Games

Un proyecto Next.js moderno con TypeScript, React y Tailwind CSS.

## 🚀 Tecnologías

- **Next.js 16** - Framework React con App Router
- **TypeScript** - Tipado estático para JavaScript
- **React 19** - Biblioteca para interfaces de usuario
- **Tailwind CSS** - Framework CSS utility-first
- **ESLint** - Linter para código JavaScript/TypeScript

## 📁 Estructura del Proyecto

```
sirius-games/
├── src/
│   ├── app/                 # App Router de Next.js
│   │   ├── globals.css      # Estilos globales
│   │   ├── layout.tsx       # Layout principal
│   │   └── page.tsx         # Página de inicio
│   ├── components/          # Componentes reutilizables
│   │   └── Button.tsx       # Componente de botón
│   ├── lib/                 # Utilidades y helpers
│   │   └── utils.ts         # Función para clases CSS
│   └── types/               # Definiciones de tipos TypeScript
├── public/                  # Archivos estáticos
├── tailwind.config.ts       # Configuración de Tailwind
├── tsconfig.json           # Configuración de TypeScript
└── next.config.ts          # Configuración de Next.js
```

## 🛠️ Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/14-David-06/sirius-games.git
cd sirius-games
```

2. Instala las dependencias:
```bash
npm install
```

3. Ejecuta el servidor de desarrollo:
```bash
npm run dev
```

4. Abre [http://localhost:3000](http://localhost:3000) en tu navegador.

## 📜 Scripts Disponibles

- `npm run dev` - Inicia el servidor de desarrollo
- `npm run build` - Construye la aplicación para producción
- `npm run start` - Inicia el servidor de producción
- `npm run lint` - Ejecuta ESLint para revisar el código

## 🎨 Personalización

### Tailwind CSS
El proyecto está configurado con Tailwind CSS. Puedes personalizar los colores, fuentes y otros estilos editando `tailwind.config.ts`.

### Componentes
Los componentes están en `src/components/`. El proyecto incluye un componente `Button` de ejemplo que muestra cómo usar Tailwind CSS con TypeScript.

### Estilos Globales
Los estilos globales están en `src/app/globals.css` e incluyen variables CSS para modo oscuro.

## 🌙 Modo Oscuro

El proyecto incluye soporte para modo oscuro usando las clases `dark:` de Tailwind CSS y las preferencias del sistema.

## 📚 Recursos

- [Documentación de Next.js](https://nextjs.org/docs)
- [Documentación de TypeScript](https://www.typescriptlang.org/docs)
- [Documentación de Tailwind CSS](https://tailwindcss.com/docs)
- [Documentación de React](https://react.dev)

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.
