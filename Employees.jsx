import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { 
  Search, 
  Plus, 
  Filter, 
  MoreHorizontal,
  Mail,
  Phone,
  Calendar,
  TrendingUp,
  AlertTriangle,
  User
} from 'lucide-react'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'

const Employees = () => {
  const [employees, setEmployees] = useState([])
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedDepartment, setSelectedDepartment] = useState('all')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Simulation de données - à remplacer par des appels API réels
    setTimeout(() => {
      setEmployees([
        {
          id: 1,
          employee_id: 'EMP001',
          first_name: 'Marie',
          last_name: 'Dubois',
          email: 'marie.dubois@entreprise.com',
          phone: '+33 1 23 45 67 89',
          position: 'Développeuse Senior',
          department: 'IT',
          hire_date: '2022-03-15',
          performance_score: 8.5,
          status: 'active',
          avatar: null
        },
        {
          id: 2,
          employee_id: 'EMP002',
          first_name: 'Pierre',
          last_name: 'Martin',
          email: 'pierre.martin@entreprise.com',
          phone: '+33 1 23 45 67 90',
          position: 'Chef de Projet',
          department: 'IT',
          hire_date: '2021-09-01',
          performance_score: 9.2,
          status: 'active',
          avatar: null
        },
        {
          id: 3,
          employee_id: 'EMP003',
          first_name: 'Sophie',
          last_name: 'Bernard',
          email: 'sophie.bernard@entreprise.com',
          phone: '+33 1 23 45 67 91',
          position: 'Responsable Marketing',
          department: 'Marketing',
          hire_date: '2020-11-20',
          performance_score: 8.8,
          status: 'active',
          avatar: null
        },
        {
          id: 4,
          employee_id: 'EMP004',
          first_name: 'Thomas',
          last_name: 'Leroy',
          email: 'thomas.leroy@entreprise.com',
          phone: '+33 1 23 45 67 92',
          position: 'Analyste Financier',
          department: 'Finance',
          hire_date: '2023-01-10',
          performance_score: 7.5,
          status: 'active',
          avatar: null
        },
        {
          id: 5,
          employee_id: 'EMP005',
          first_name: 'Julie',
          last_name: 'Moreau',
          email: 'julie.moreau@entreprise.com',
          phone: '+33 1 23 45 67 93',
          position: 'Consultante RH',
          department: 'RH',
          hire_date: '2022-07-05',
          performance_score: 8.1,
          status: 'active',
          avatar: null
        }
      ])
      setLoading(false)
    }, 1000)
  }, [])

  const departments = ['all', 'IT', 'Marketing', 'Finance', 'RH', 'Ventes']

  const filteredEmployees = employees.filter(employee => {
    const matchesSearch = 
      employee.first_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      employee.last_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      employee.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
      employee.position.toLowerCase().includes(searchTerm.toLowerCase())
    
    const matchesDepartment = selectedDepartment === 'all' || employee.department === selectedDepartment

    return matchesSearch && matchesDepartment
  })

  const getPerformanceColor = (score) => {
    if (score >= 8.5) return 'bg-green-100 text-green-800'
    if (score >= 7.5) return 'bg-yellow-100 text-yellow-800'
    return 'bg-red-100 text-red-800'
  }

  const getPerformanceIcon = (score) => {
    if (score >= 8.5) return <TrendingUp className="h-3 w-3" />
    if (score >= 7.5) return <TrendingUp className="h-3 w-3" />
    return <AlertTriangle className="h-3 w-3" />
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Employés</h1>
          <p className="text-gray-600">Gérez votre équipe et suivez les performances</p>
        </div>
        <Button>
          <Plus className="h-4 w-4 mr-2" />
          Nouvel employé
        </Button>
      </div>

      {/* Filters */}
      <Card>
        <CardContent className="pt-6">
          <div className="flex flex-col sm:flex-row gap-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
                <Input
                  placeholder="Rechercher un employé..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
              </div>
            </div>
            <div className="flex gap-2">
              <select
                value={selectedDepartment}
                onChange={(e) => setSelectedDepartment(e.target.value)}
                className="px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                {departments.map(dept => (
                  <option key={dept} value={dept}>
                    {dept === 'all' ? 'Tous les départements' : dept}
                  </option>
                ))}
              </select>
              <Button variant="outline">
                <Filter className="h-4 w-4 mr-2" />
                Filtres
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Employee List */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredEmployees.map((employee) => (
          <Card key={employee.id} className="hover:shadow-lg transition-shadow">
            <CardHeader className="pb-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className="h-10 w-10 rounded-full bg-blue-100 flex items-center justify-center">
                    <User className="h-5 w-5 text-blue-600" />
                  </div>
                  <div>
                    <CardTitle className="text-lg">
                      {employee.first_name} {employee.last_name}
                    </CardTitle>
                    <CardDescription>{employee.position}</CardDescription>
                  </div>
                </div>
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="ghost" size="sm">
                      <MoreHorizontal className="h-4 w-4" />
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end">
                    <DropdownMenuItem>Voir le profil</DropdownMenuItem>
                    <DropdownMenuItem>Modifier</DropdownMenuItem>
                    <DropdownMenuItem>Évaluation</DropdownMenuItem>
                    <DropdownMenuItem>Analyse IA</DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </div>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="flex items-center justify-between">
                <Badge variant="secondary">{employee.department}</Badge>
                <Badge className={getPerformanceColor(employee.performance_score)}>
                  {getPerformanceIcon(employee.performance_score)}
                  <span className="ml-1">{employee.performance_score}/10</span>
                </Badge>
              </div>
              
              <div className="space-y-2 text-sm text-gray-600">
                <div className="flex items-center space-x-2">
                  <Mail className="h-3 w-3" />
                  <span className="truncate">{employee.email}</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Phone className="h-3 w-3" />
                  <span>{employee.phone}</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Calendar className="h-3 w-3" />
                  <span>Embauché le {new Date(employee.hire_date).toLocaleDateString('fr-FR')}</span>
                </div>
              </div>

              <div className="pt-2 border-t">
                <div className="flex justify-between text-xs text-gray-500">
                  <span>ID: {employee.employee_id}</span>
                  <span className="capitalize">{employee.status}</span>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {filteredEmployees.length === 0 && (
        <Card>
          <CardContent className="text-center py-12">
            <User className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Aucun employé trouvé
            </h3>
            <p className="text-gray-600">
              Essayez de modifier vos critères de recherche ou ajoutez un nouvel employé.
            </p>
          </CardContent>
        </Card>
      )}
    </div>
  )
}

export default Employees

