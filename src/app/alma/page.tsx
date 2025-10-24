'use client';

import { useState, useRef, useEffect } from 'react';
import { ChatMessage, ChatInput, ChatHeader } from '@/components';

interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: Date;
}

export default function AlmaPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      content: '¡Hola! Soy ALMA, tu asistente de inteligencia artificial. ¿En qué puedo ayudarte hoy?',
      role: 'assistant',
      timestamp: new Date(),
    },
  ]);
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (content: string) => {
    const userMessage: Message = {
      id: Date.now().toString(),
      content,
      role: 'user',
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setIsTyping(true);

    // Simular respuesta de ALMA (aquí conectarías con tu API real)
    setTimeout(() => {
      const almaResponse: Message = {
        id: (Date.now() + 1).toString(),
        content: generateAlmaResponse(content),
        role: 'assistant',
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, almaResponse]);
      setIsTyping(false);
    }, 1000 + Math.random() * 2000);
  };

  const generateAlmaResponse = (userInput: string): string => {
    const responses = [
      `Entiendo tu consulta sobre "${userInput}". Como ALMA, puedo ayudarte a analizar este tema desde diferentes perspectivas.`,
      `Es una pregunta muy interesante. Basándome en mi conocimiento, puedo decirte que...`,
      `Me parece un tema fascinante. Permíteme compartir contigo algunos insights sobre "${userInput}".`,
      `Gracias por compartir eso conmigo. Como agente de IA, mi análisis sugiere que...`,
      `Excelente pregunta. Desde mi perspectiva como ALMA, considero que este es un punto muy relevante.`,
    ];

    const randomResponse = responses[Math.floor(Math.random() * responses.length)];
    
    return `${randomResponse} ¿Te gustaría que profundice en algún aspecto específico?`;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-indigo-100 dark:from-gray-900 dark:via-purple-900 dark:to-indigo-900">
      <div className="container mx-auto max-w-4xl h-screen flex flex-col">
        <ChatHeader />
        
        <div className="flex-1 overflow-hidden bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-t-3xl shadow-2xl">
          <div className="h-full flex flex-col">
            {/* Messages Area */}
            <div className="flex-1 overflow-y-auto p-6 space-y-4">
              {messages.map((message) => (
                <ChatMessage
                  key={message.id}
                  message={message}
                />
              ))}
              
              {isTyping && (
                <div className="flex items-start space-x-3">
                  <div className="w-8 h-8 bg-gradient-to-r from-purple-500 to-blue-500 rounded-full flex items-center justify-center text-white font-bold text-sm">
                    A
                  </div>
                  <div className="bg-gray-100 dark:bg-gray-700 rounded-2xl px-4 py-3 max-w-xs">
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                    </div>
                  </div>
                </div>
              )}
              
              <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div className="border-t border-gray-200 dark:border-gray-600 p-4">
              <ChatInput onSendMessage={handleSendMessage} disabled={isTyping} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}