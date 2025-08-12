import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { 
  Users, 
  UserPlus, 
  TrendingUp, 
  AlertTriangle,
  Calendar,
  MessageCircle,
  BarChart3,
  Clock
} from 'lucide-react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'

const Dashboard = () => {
  const [stats, setStats] = useState({
    totalEmployees: 0,
    activeJobs: 0,
    pendingApplications: 0,
    avgPerformance: 0
  })

  const [departmentData, setDepartmentData] = useState([])
  const [performanceData, setPerformanceData] = useState([])

  useEffect(() => {
    // Simulation de données - à remplacer par des appels API réels
    setStats({
      totalEmployees: 247,
      activeJobs: 12,
      pendingApplications: 34,
      avgPerformance: 8.2
    })

    setDepartmentData([
      { name: 'IT', employees: 45, color: '#3B82F6' },
      { name: 'Marketing', employees: 32, color: '#10B981' },
      { name: 'Ventes', employees: 28, color: '#F59E0B' },
      { name: 'RH', employees: 15, color: '#EF4444' },
      { name: 'Finance', employees: 22, color: '#8B5CF6' },
    ])

    setPerformanceData([
      { month: 'Jan', score: 7.8 },
      { month: 'Fév', score: 8.1 },
      { month: 'Mar', score: 7.9 },
      { month: 'Avr', score: 8.3 },
      { month: 'Mai', score: 8.2 },
      { month: 'Jun', score: 8.5 },
    ])
  }, [])

  const recentActivities = [
    {
      id: 1,
      type: 'new_employee',
      message: 'Marie Dubois a rejoint l\'équipe Marketing',
      time: '2 heures',
      icon: Users
    },
    {
      id: 2,
      type: 'application',
      message: '5 nouvelles candidatures pour le poste de Développeur',
      time: '4 heures',
      icon: UserPlus
    },
    {
      id: 3,
      type: 'performance',
      message: 'Évaluation de performance complétée pour l\'équipe IT',
      time: '1 jour',
      icon: TrendingUp
    },
    {
      id: 4,
      type: 'alert',
      message: 'Risque de turnover détecté pour 3 employés',
      time: '2 jours',
      icon: AlertTriangle
    }
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Tableau de bord</h1>
          <p className="text-gray-600">Vue d'ensemble de votre organisation</p>
        </div>
        <div className="flex space-x-3">
          <Button variant="outline">
            <Calendar className="h-4 w-4 mr-2" />
            Exporter rapport
          </Button>
          <Button>
            <MessageCircle className="h-4 w-4 mr-2" />
            Assistant IA
          </Button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Employés</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.totalEmployees}</div>
            <p className="text-xs text-muted-foreground">
              +12% par rapport au mois dernier
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Postes Ouverts</CardTitle>
            <UserPlus className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.activeJobs}</div>
            <p className="text-xs text-muted-foreground">
              3 nouveaux cette semaine
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Candidatures</CardTitle>
            <BarChart3 className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.pendingApplications}</div>
            <p className="text-xs text-muted-foreground">
              En attente de traitement
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Performance Moy.</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.avgPerformance}/10</div>
            <p className="text-xs text-muted-foreground">
              +0.3 ce trimestre
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Department Distribution */}
        <Card>
          <CardHeader>
            <CardTitle>Répartition par Département</CardTitle>
            <CardDescription>
              Distribution des employés par département
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={departmentData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, value }) => `${name}: ${value}`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="employees"
                >
                  {departmentData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Performance Trend */}
        <Card>
          <CardHeader>
            <CardTitle>Évolution des Performances</CardTitle>
            <CardDescription>
              Score moyen de performance sur 6 mois
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={performanceData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis domain={[0, 10]} />
                <Tooltip />
                <Bar dataKey="score" fill="#3B82F6" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Recent Activities */}
      <Card>
        <CardHeader>
          <CardTitle>Activités Récentes</CardTitle>
          <CardDescription>
            Dernières actions et événements dans le système
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {recentActivities.map((activity) => {
              const Icon = activity.icon
              return (
                <div key={activity.id} className="flex items-center space-x-4">
                  <div className="flex-shrink-0">
                    <div className="h-8 w-8 rounded-full bg-blue-100 flex items-center justify-center">
                      <Icon className="h-4 w-4 text-blue-600" />
                    </div>
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900">
                      {activity.message}
                    </p>
                  </div>
                  <div className="flex-shrink-0 text-sm text-gray-500">
                    <Clock className="h-3 w-3 inline mr-1" />
                    Il y a {activity.time}
                  </div>
                </div>
              )
            })}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default Dashboard

