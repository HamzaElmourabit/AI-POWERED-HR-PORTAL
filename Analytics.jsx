import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { 
  TrendingUp, 
  TrendingDown, 
  Users, 
  UserPlus, 
  AlertTriangle,
  Target,
  Calendar,
  Download,
  Brain,
  BarChart3
} from 'lucide-react'
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  AreaChart,
  Area
} from 'recharts'

const Analytics = () => {
  const [performanceData, setPerformanceData] = useState([])
  const [turnoverData, setTurnoverData] = useState([])
  const [recruitmentData, setRecruitmentData] = useState([])
  const [departmentPerformance, setDepartmentPerformance] = useState([])
  const [riskEmployees, setRiskEmployees] = useState([])

  useEffect(() => {
    // Simulation de données - à remplacer par des appels API réels
    setPerformanceData([
      { month: 'Jan', score: 7.8, satisfaction: 8.2 },
      { month: 'Fév', score: 8.1, satisfaction: 8.0 },
      { month: 'Mar', score: 7.9, satisfaction: 7.8 },
      { month: 'Avr', score: 8.3, satisfaction: 8.5 },
      { month: 'Mai', score: 8.2, satisfaction: 8.3 },
      { month: 'Jun', score: 8.5, satisfaction: 8.7 }
    ])

    setTurnoverData([
      { month: 'Jan', turnover: 2.1, prediction: 2.3 },
      { month: 'Fév', turnover: 1.8, prediction: 2.0 },
      { month: 'Mar', turnover: 2.5, prediction: 2.2 },
      { month: 'Avr', turnover: 1.9, prediction: 2.1 },
      { month: 'Mai', turnover: 2.2, prediction: 2.4 },
      { month: 'Jun', turnover: 1.7, prediction: 1.9 }
    ])

    setRecruitmentData([
      { month: 'Jan', applications: 45, hired: 8, success_rate: 17.8 },
      { month: 'Fév', applications: 52, hired: 12, success_rate: 23.1 },
      { month: 'Mar', applications: 38, hired: 6, success_rate: 15.8 },
      { month: 'Avr', applications: 61, hired: 15, success_rate: 24.6 },
      { month: 'Mai', applications: 48, hired: 9, success_rate: 18.8 },
      { month: 'Jun', applications: 55, hired: 13, success_rate: 23.6 }
    ])

    setDepartmentPerformance([
      { name: 'IT', performance: 8.7, satisfaction: 8.9, turnover_risk: 15, color: '#3B82F6' },
      { name: 'Marketing', performance: 8.2, satisfaction: 8.5, turnover_risk: 12, color: '#10B981' },
      { name: 'Ventes', performance: 7.9, satisfaction: 7.8, turnover_risk: 22, color: '#F59E0B' },
      { name: 'Finance', performance: 8.4, satisfaction: 8.1, turnover_risk: 8, color: '#8B5CF6' },
      { name: 'RH', performance: 8.6, satisfaction: 8.7, turnover_risk: 5, color: '#EF4444' }
    ])

    setRiskEmployees([
      {
        id: 1,
        name: 'Jean Dupont',
        department: 'Ventes',
        risk_score: 8.2,
        risk_level: 'Élevé',
        factors: ['Performance en baisse', 'Absence fréquente', 'Feedback négatif']
      },
      {
        id: 2,
        name: 'Marie Leroy',
        department: 'IT',
        risk_score: 7.1,
        risk_level: 'Moyen',
        factors: ['Surcharge de travail', 'Pas de promotion récente']
      },
      {
        id: 3,
        name: 'Paul Bernard',
        department: 'Marketing',
        risk_score: 6.8,
        risk_level: 'Moyen',
        factors: ['Changement de manager', 'Objectifs non atteints']
      }
    ])
  }, [])

  const getRiskColor = (level) => {
    switch (level) {
      case 'Élevé': return 'bg-red-100 text-red-800'
      case 'Moyen': return 'bg-yellow-100 text-yellow-800'
      case 'Faible': return 'bg-green-100 text-green-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getRiskIcon = (level) => {
    switch (level) {
      case 'Élevé': return <AlertTriangle className="h-3 w-3" />
      case 'Moyen': return <TrendingDown className="h-3 w-3" />
      case 'Faible': return <TrendingUp className="h-3 w-3" />
      default: return <BarChart3 className="h-3 w-3" />
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Analytics RH</h1>
          <p className="text-gray-600">Insights et prédictions alimentés par l'IA</p>
        </div>
        <div className="flex space-x-3">
          <Button variant="outline">
            <Download className="h-4 w-4 mr-2" />
            Exporter
          </Button>
          <Button>
            <Brain className="h-4 w-4 mr-2" />
            Rapport IA
          </Button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Performance Moyenne</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">8.3/10</div>
            <p className="text-xs text-muted-foreground">
              <span className="text-green-600">+0.4</span> vs mois dernier
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Taux de Turnover</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">1.9%</div>
            <p className="text-xs text-muted-foreground">
              <span className="text-green-600">-0.3%</span> vs mois dernier
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Taux de Réussite Recrutement</CardTitle>
            <UserPlus className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">23.6%</div>
            <p className="text-xs text-muted-foreground">
              <span className="text-green-600">+4.8%</span> vs mois dernier
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Employés à Risque</CardTitle>
            <AlertTriangle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">3</div>
            <p className="text-xs text-muted-foreground">
              Nécessitent une attention
            </p>
          </CardContent>
        </Card>
      </div>

      <Tabs defaultValue="performance" className="space-y-6">
        <TabsList>
          <TabsTrigger value="performance">Performance</TabsTrigger>
          <TabsTrigger value="turnover">Turnover</TabsTrigger>
          <TabsTrigger value="recruitment">Recrutement</TabsTrigger>
          <TabsTrigger value="predictions">Prédictions IA</TabsTrigger>
        </TabsList>

        {/* Performance Tab */}
        <TabsContent value="performance" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Évolution des Performances</CardTitle>
                <CardDescription>Score moyen et satisfaction sur 6 mois</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={performanceData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="month" />
                    <YAxis domain={[0, 10]} />
                    <Tooltip />
                    <Line type="monotone" dataKey="score" stroke="#3B82F6" strokeWidth={2} name="Performance" />
                    <Line type="monotone" dataKey="satisfaction" stroke="#10B981" strokeWidth={2} name="Satisfaction" />
                  </LineChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Performance par Département</CardTitle>
                <CardDescription>Comparaison des scores moyens</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={departmentPerformance}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis domain={[0, 10]} />
                    <Tooltip />
                    <Bar dataKey="performance" fill="#3B82F6" name="Performance" />
                    <Bar dataKey="satisfaction" fill="#10B981" name="Satisfaction" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Turnover Tab */}
        <TabsContent value="turnover" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Turnover vs Prédictions IA</CardTitle>
                <CardDescription>Taux réel vs prédictions de l'IA</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <AreaChart data={turnoverData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="month" />
                    <YAxis />
                    <Tooltip />
                    <Area type="monotone" dataKey="turnover" stackId="1" stroke="#EF4444" fill="#EF4444" fillOpacity={0.6} name="Turnover réel" />
                    <Area type="monotone" dataKey="prediction" stackId="2" stroke="#F59E0B" fill="#F59E0B" fillOpacity={0.4} name="Prédiction IA" />
                  </AreaChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Risque de Turnover par Département</CardTitle>
                <CardDescription>Pourcentage d'employés à risque</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={departmentPerformance}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, turnover_risk }) => `${name}: ${turnover_risk}%`}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="turnover_risk"
                    >
                      {departmentPerformance.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>

          {/* Risk Employees */}
          <Card>
            <CardHeader>
              <CardTitle>Employés à Risque de Turnover</CardTitle>
              <CardDescription>Identifiés par l'analyse IA</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {riskEmployees.map((employee) => (
                  <div key={employee.id} className="flex items-center justify-between p-4 border rounded-lg">
                    <div className="flex-1">
                      <div className="flex items-center space-x-3">
                        <div>
                          <h4 className="font-semibold">{employee.name}</h4>
                          <p className="text-sm text-gray-600">{employee.department}</p>
                        </div>
                        <Badge className={getRiskColor(employee.risk_level)}>
                          {getRiskIcon(employee.risk_level)}
                          <span className="ml-1">{employee.risk_level}</span>
                        </Badge>
                      </div>
                      <div className="mt-2">
                        <div className="text-sm text-gray-600">Facteurs de risque:</div>
                        <div className="flex flex-wrap gap-1 mt-1">
                          {employee.factors.map((factor, index) => (
                            <Badge key={index} variant="outline" className="text-xs">
                              {factor}
                            </Badge>
                          ))}
                        </div>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-lg font-semibold text-red-600">
                        {employee.risk_score}/10
                      </div>
                      <div className="text-xs text-gray-500">Score de risque</div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Recruitment Tab */}
        <TabsContent value="recruitment" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Métriques de Recrutement</CardTitle>
                <CardDescription>Candidatures et embauches sur 6 mois</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={recruitmentData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="month" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="applications" fill="#3B82F6" name="Candidatures" />
                    <Bar dataKey="hired" fill="#10B981" name="Embauches" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Taux de Réussite</CardTitle>
                <CardDescription>Pourcentage d'embauches par rapport aux candidatures</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={recruitmentData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="month" />
                    <YAxis />
                    <Tooltip />
                    <Line type="monotone" dataKey="success_rate" stroke="#8B5CF6" strokeWidth={3} name="Taux de réussite %" />
                  </LineChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* AI Predictions Tab */}
        <TabsContent value="predictions" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Prédictions de Performance</CardTitle>
                <CardDescription>Tendances prévues pour les 3 prochains mois</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
                  <div>
                    <div className="font-semibold text-green-800">Performance Globale</div>
                    <div className="text-sm text-green-600">Amélioration prévue</div>
                  </div>
                  <div className="text-2xl font-bold text-green-600">+0.3</div>
                </div>
                <div className="flex items-center justify-between p-3 bg-yellow-50 rounded-lg">
                  <div>
                    <div className="font-semibold text-yellow-800">Département Ventes</div>
                    <div className="text-sm text-yellow-600">Attention requise</div>
                  </div>
                  <div className="text-2xl font-bold text-yellow-600">-0.1</div>
                </div>
                <div className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
                  <div>
                    <div className="font-semibold text-blue-800">Satisfaction Employés</div>
                    <div className="text-sm text-blue-600">Stable</div>
                  </div>
                  <div className="text-2xl font-bold text-blue-600">8.5</div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Recommandations IA</CardTitle>
                <CardDescription>Actions suggérées basées sur l'analyse</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="border-l-4 border-red-500 pl-4">
                  <div className="font-semibold text-red-800">Priorité Élevée</div>
                  <div className="text-sm text-gray-600">
                    Organiser des entretiens individuels avec les 3 employés à risque de turnover
                  </div>
                </div>
                <div className="border-l-4 border-yellow-500 pl-4">
                  <div className="font-semibold text-yellow-800">Priorité Moyenne</div>
                  <div className="text-sm text-gray-600">
                    Mettre en place un plan de formation pour l'équipe Ventes
                  </div>
                </div>
                <div className="border-l-4 border-green-500 pl-4">
                  <div className="font-semibold text-green-800">Opportunité</div>
                  <div className="text-sm text-gray-600">
                    Capitaliser sur les bonnes performances de l'équipe IT pour le mentoring
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}

export default Analytics

