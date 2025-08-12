import { useState, useEffect, useRef } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { 
  Send, 
  Bot, 
  User, 
  Sparkles,
  Clock,
  Users,
  FileText,
  Calendar,
  HelpCircle,
  Lightbulb,
  MessageCircle
} from 'lucide-react'

const Chatbot = () => {
  const [messages, setMessages] = useState([])
  const [inputMessage, setInputMessage] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const [quickActions, setQuickActions] = useState([])
  const messagesEndRef = useRef(null)

  useEffect(() => {
    // Message de bienvenue
    setMessages([
      {
        id: 1,
        type: 'bot',
        content: 'Bonjour ! Je suis votre assistant RH intelligent. Comment puis-je vous aider aujourd\'hui ?',
        timestamp: new Date(),
        suggestions: [
          'Rechercher un employé',
          'Voir les postes ouverts',
          'Demander un congé',
          'Consulter les politiques RH'
        ]
      }
    ])

    // Actions rapides
    setQuickActions([
      {
        id: 'search_employee',
        title: 'Rechercher un employé',
        description: 'Trouver les coordonnées d\'un collègue',
        icon: Users
      },
      {
        id: 'job_postings',
        title: 'Postes ouverts',
        description: 'Voir les opportunités de carrière',
        icon: FileText
      },
      {
        id: 'leave_request',
        title: 'Demande de congé',
        description: 'Soumettre une demande d\'absence',
        icon: Calendar
      },
      {
        id: 'hr_policies',
        title: 'Politiques RH',
        description: 'Consulter les règlements internes',
        icon: HelpCircle
      }
    ])
  }, [])

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputMessage,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInputMessage('')
    setIsTyping(true)

    // Simulation d'une réponse IA
    setTimeout(() => {
      const botResponse = generateBotResponse(inputMessage)
      setMessages(prev => [...prev, botResponse])
      setIsTyping(false)
    }, 1500)
  }

  const generateBotResponse = (userInput) => {
    const input = userInput.toLowerCase()
    let response = ''
    let suggestions = []

    if (input.includes('employé') || input.includes('collègue') || input.includes('contact')) {
      response = 'Je peux vous aider à trouver les informations de contact d\'un employé. Pouvez-vous me donner le nom de la personne que vous recherchez ?'
      suggestions = ['Marie Dubois', 'Pierre Martin', 'Sophie Bernard']
    } else if (input.includes('congé') || input.includes('vacances') || input.includes('absence')) {
      response = 'Pour demander un congé, vous pouvez utiliser le formulaire en ligne ou me donner les détails de votre demande. De quel type de congé s\'agit-il et pour quelles dates ?'
      suggestions = ['Congés payés', 'Congé maladie', 'Congé parental']
    } else if (input.includes('poste') || input.includes('emploi') || input.includes('recrutement')) {
      response = 'Nous avons actuellement 12 postes ouverts dans différents départements. Quel type de poste vous intéresse ?'
      suggestions = ['Développeur', 'Marketing', 'Finance', 'Voir tous les postes']
    } else if (input.includes('politique') || input.includes('règlement') || input.includes('procédure')) {
      response = 'Je peux vous renseigner sur nos politiques RH. Quelle information spécifique recherchez-vous ?'
      suggestions = ['Télétravail', 'Congés', 'Formation', 'Évaluation']
    } else if (input.includes('formation') || input.includes('développement')) {
      response = 'Nous proposons de nombreuses formations pour le développement professionnel. Quel domaine vous intéresse ?'
      suggestions = ['Formations techniques', 'Management', 'Soft skills']
    } else {
      response = 'Je comprends votre question. Voici quelques informations qui pourraient vous aider. N\'hésitez pas à être plus spécifique pour que je puisse mieux vous assister.'
      suggestions = ['Reformuler la question', 'Parler à un humain', 'Voir la FAQ']
    }

    return {
      id: Date.now(),
      type: 'bot',
      content: response,
      timestamp: new Date(),
      suggestions
    }
  }

  const handleQuickAction = (action) => {
    let message = ''
    switch (action.id) {
      case 'search_employee':
        message = 'Je recherche un employé'
        break
      case 'job_postings':
        message = 'Quels sont les postes ouverts ?'
        break
      case 'leave_request':
        message = 'Je voudrais demander un congé'
        break
      case 'hr_policies':
        message = 'Où puis-je consulter les politiques RH ?'
        break
      default:
        message = action.title
    }
    setInputMessage(message)
  }

  const handleSuggestionClick = (suggestion) => {
    setInputMessage(suggestion)
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Assistant IA</h1>
          <p className="text-gray-600">Votre assistant RH intelligent disponible 24h/24</p>
        </div>
        <div className="flex items-center space-x-2">
          <Badge variant="secondary" className="bg-green-100 text-green-800">
            <div className="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
            En ligne
          </Badge>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Quick Actions */}
        <div className="lg:col-span-1 space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Actions rapides</CardTitle>
              <CardDescription>Cliquez pour commencer</CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              {quickActions.map((action) => {
                const Icon = action.icon
                return (
                  <Button
                    key={action.id}
                    variant="outline"
                    className="w-full justify-start h-auto p-3"
                    onClick={() => handleQuickAction(action)}
                  >
                    <div className="flex items-start space-x-3">
                      <Icon className="h-5 w-5 mt-0.5 text-blue-600" />
                      <div className="text-left">
                        <div className="font-medium text-sm">{action.title}</div>
                        <div className="text-xs text-gray-500">{action.description}</div>
                      </div>
                    </div>
                  </Button>
                )
              })}
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Conseils</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="flex items-start space-x-2">
                <Lightbulb className="h-4 w-4 text-yellow-500 mt-0.5" />
                <div className="text-sm text-gray-600">
                  Posez des questions précises pour obtenir de meilleures réponses
                </div>
              </div>
              <div className="flex items-start space-x-2">
                <Sparkles className="h-4 w-4 text-purple-500 mt-0.5" />
                <div className="text-sm text-gray-600">
                  L'IA peut analyser les CV et recommander des candidats
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Chat Interface */}
        <div className="lg:col-span-3">
          <Card className="h-[600px] flex flex-col">
            <CardHeader className="border-b">
              <div className="flex items-center space-x-3">
                <div className="h-10 w-10 rounded-full bg-blue-100 flex items-center justify-center">
                  <Bot className="h-5 w-5 text-blue-600" />
                </div>
                <div>
                  <CardTitle className="text-lg">Assistant RH IA</CardTitle>
                  <CardDescription>Alimenté par l'intelligence artificielle</CardDescription>
                </div>
              </div>
            </CardHeader>

            {/* Messages */}
            <CardContent className="flex-1 overflow-y-auto p-4 space-y-4">
              {messages.map((message) => (
                <div key={message.id} className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
                  <div className={`flex space-x-3 max-w-[80%] ${message.type === 'user' ? 'flex-row-reverse space-x-reverse' : ''}`}>
                    <div className={`h-8 w-8 rounded-full flex items-center justify-center flex-shrink-0 ${
                      message.type === 'user' ? 'bg-blue-600' : 'bg-gray-100'
                    }`}>
                      {message.type === 'user' ? (
                        <User className="h-4 w-4 text-white" />
                      ) : (
                        <Bot className="h-4 w-4 text-gray-600" />
                      )}
                    </div>
                    <div className="space-y-2">
                      <div className={`rounded-lg p-3 ${
                        message.type === 'user' 
                          ? 'bg-blue-600 text-white' 
                          : 'bg-gray-100 text-gray-900'
                      }`}>
                        {message.content}
                      </div>
                      <div className={`text-xs text-gray-500 ${message.type === 'user' ? 'text-right' : ''}`}>
                        <Clock className="h-3 w-3 inline mr-1" />
                        {message.timestamp.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })}
                      </div>
                      {message.suggestions && message.suggestions.length > 0 && (
                        <div className="flex flex-wrap gap-2">
                          {message.suggestions.map((suggestion, index) => (
                            <Button
                              key={index}
                              variant="outline"
                              size="sm"
                              className="text-xs"
                              onClick={() => handleSuggestionClick(suggestion)}
                            >
                              {suggestion}
                            </Button>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ))}

              {isTyping && (
                <div className="flex justify-start">
                  <div className="flex space-x-3 max-w-[80%]">
                    <div className="h-8 w-8 rounded-full bg-gray-100 flex items-center justify-center">
                      <Bot className="h-4 w-4 text-gray-600" />
                    </div>
                    <div className="bg-gray-100 rounded-lg p-3">
                      <div className="flex space-x-1">
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                      </div>
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </CardContent>

            {/* Input */}
            <div className="border-t p-4">
              <div className="flex space-x-2">
                <Input
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Tapez votre message..."
                  className="flex-1"
                />
                <Button onClick={handleSendMessage} disabled={!inputMessage.trim()}>
                  <Send className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  )
}

export default Chatbot

