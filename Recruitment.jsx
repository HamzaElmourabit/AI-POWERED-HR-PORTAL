import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { 
  Search, 
  Plus, 
  Filter, 
  MoreHorizontal,
  MapPin,
  Calendar,
  DollarSign,
  Users,
  FileText,
  Star,
  Brain,
  Clock,
  CheckCircle,
  XCircle
} from 'lucide-react'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'

const Recruitment = () => {
  const [jobPostings, setJobPostings] = useState([])
  const [candidates, setCandidates] = useState([])
  const [applications, setApplications] = useState([])
  const [searchTerm, setSearchTerm] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Simulation de données - à remplacer par des appels API réels
    setTimeout(() => {
      setJobPostings([
        {
          id: 1,
          title: 'Développeur Full Stack Senior',
          department: 'IT',
          location: 'Paris',
          employment_type: 'CDI',
          salary_min: 55000,
          salary_max: 75000,
          posted_date: '2024-01-15',
          status: 'active',
          applications_count: 12
        },
        {
          id: 2,
          title: 'Chef de Projet Marketing Digital',
          department: 'Marketing',
          location: 'Lyon',
          employment_type: 'CDI',
          salary_min: 45000,
          salary_max: 60000,
          posted_date: '2024-01-20',
          status: 'active',
          applications_count: 8
        },
        {
          id: 3,
          title: 'Analyste Financier Junior',
          department: 'Finance',
          location: 'Remote',
          employment_type: 'CDI',
          salary_min: 35000,
          salary_max: 45000,
          posted_date: '2024-01-25',
          status: 'active',
          applications_count: 15
        }
      ])

      setCandidates([
        {
          id: 1,
          first_name: 'Alice',
          last_name: 'Johnson',
          email: 'alice.johnson@email.com',
          phone: '+33 6 12 34 56 78',
          experience_years: 5,
          ai_score: 8.7,
          skills: ['React', 'Node.js', 'Python', 'AWS'],
          created_at: '2024-01-28'
        },
        {
          id: 2,
          first_name: 'Bob',
          last_name: 'Smith',
          email: 'bob.smith@email.com',
          phone: '+33 6 12 34 56 79',
          experience_years: 3,
          ai_score: 7.2,
          skills: ['Marketing Digital', 'SEO', 'Google Ads', 'Analytics'],
          created_at: '2024-01-29'
        },
        {
          id: 3,
          first_name: 'Claire',
          last_name: 'Wilson',
          email: 'claire.wilson@email.com',
          phone: '+33 6 12 34 56 80',
          experience_years: 2,
          ai_score: 9.1,
          skills: ['Finance', 'Excel', 'Power BI', 'SQL'],
          created_at: '2024-01-30'
        }
      ])

      setApplications([
        {
          id: 1,
          candidate_id: 1,
          job_posting_id: 1,
          status: 'interview',
          ai_match_score: 8.5,
          application_date: '2024-01-28',
          candidate_name: 'Alice Johnson',
          job_title: 'Développeur Full Stack Senior'
        },
        {
          id: 2,
          candidate_id: 2,
          job_posting_id: 2,
          status: 'screening',
          ai_match_score: 7.8,
          application_date: '2024-01-29',
          candidate_name: 'Bob Smith',
          job_title: 'Chef de Projet Marketing Digital'
        },
        {
          id: 3,
          candidate_id: 3,
          job_posting_id: 3,
          status: 'submitted',
          ai_match_score: 9.2,
          application_date: '2024-01-30',
          candidate_name: 'Claire Wilson',
          job_title: 'Analyste Financier Junior'
        }
      ])

      setLoading(false)
    }, 1000)
  }, [])

  const getStatusColor = (status) => {
    switch (status) {
      case 'active': return 'bg-green-100 text-green-800'
      case 'closed': return 'bg-gray-100 text-gray-800'
      case 'draft': return 'bg-yellow-100 text-yellow-800'
      case 'submitted': return 'bg-blue-100 text-blue-800'
      case 'screening': return 'bg-yellow-100 text-yellow-800'
      case 'interview': return 'bg-purple-100 text-purple-800'
      case 'hired': return 'bg-green-100 text-green-800'
      case 'rejected': return 'bg-red-100 text-red-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getStatusIcon = (status) => {
    switch (status) {
      case 'hired': return <CheckCircle className="h-3 w-3" />
      case 'rejected': return <XCircle className="h-3 w-3" />
      case 'interview': return <Users className="h-3 w-3" />
      default: return <Clock className="h-3 w-3" />
    }
  }

  const getScoreColor = (score) => {
    if (score >= 8.5) return 'text-green-600'
    if (score >= 7.0) return 'text-yellow-600'
    return 'text-red-600'
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
          <h1 className="text-3xl font-bold text-gray-900">Recrutement</h1>
          <p className="text-gray-600">Gérez vos offres d'emploi et candidatures avec l'IA</p>
        </div>
        <Button>
          <Plus className="h-4 w-4 mr-2" />
          Nouvelle offre
        </Button>
      </div>

      <Tabs defaultValue="jobs" className="space-y-6">
        <TabsList>
          <TabsTrigger value="jobs">Offres d'emploi</TabsTrigger>
          <TabsTrigger value="candidates">Candidats</TabsTrigger>
          <TabsTrigger value="applications">Candidatures</TabsTrigger>
        </TabsList>

        {/* Job Postings Tab */}
        <TabsContent value="jobs" className="space-y-6">
          <Card>
            <CardContent className="pt-6">
              <div className="flex flex-col sm:flex-row gap-4">
                <div className="flex-1">
                  <div className="relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
                    <Input
                      placeholder="Rechercher une offre..."
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      className="pl-10"
                    />
                  </div>
                </div>
                <Button variant="outline">
                  <Filter className="h-4 w-4 mr-2" />
                  Filtres
                </Button>
              </div>
            </CardContent>
          </Card>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {jobPostings.map((job) => (
              <Card key={job.id} className="hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="space-y-1">
                      <CardTitle className="text-lg">{job.title}</CardTitle>
                      <CardDescription>{job.department}</CardDescription>
                    </div>
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button variant="ghost" size="sm">
                          <MoreHorizontal className="h-4 w-4" />
                        </Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent align="end">
                        <DropdownMenuItem>Voir les détails</DropdownMenuItem>
                        <DropdownMenuItem>Modifier</DropdownMenuItem>
                        <DropdownMenuItem>Optimiser avec IA</DropdownMenuItem>
                        <DropdownMenuItem>Fermer l'offre</DropdownMenuItem>
                      </DropdownMenuContent>
                    </DropdownMenu>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex items-center justify-between">
                    <Badge className={getStatusColor(job.status)}>
                      {job.status === 'active' ? 'Actif' : job.status}
                    </Badge>
                    <Badge variant="outline">
                      <Users className="h-3 w-3 mr-1" />
                      {job.applications_count} candidatures
                    </Badge>
                  </div>

                  <div className="space-y-2 text-sm text-gray-600">
                    <div className="flex items-center space-x-2">
                      <MapPin className="h-3 w-3" />
                      <span>{job.location}</span>
                      <span>•</span>
                      <span>{job.employment_type}</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <DollarSign className="h-3 w-3" />
                      <span>{job.salary_min.toLocaleString()}€ - {job.salary_max.toLocaleString()}€</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Calendar className="h-3 w-3" />
                      <span>Publié le {new Date(job.posted_date).toLocaleDateString('fr-FR')}</span>
                    </div>
                  </div>

                  <div className="flex space-x-2 pt-2">
                    <Button size="sm" variant="outline" className="flex-1">
                      <FileText className="h-3 w-3 mr-1" />
                      Voir
                    </Button>
                    <Button size="sm" className="flex-1">
                      <Brain className="h-3 w-3 mr-1" />
                      Analyse IA
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        {/* Candidates Tab */}
        <TabsContent value="candidates" className="space-y-6">
          <Card>
            <CardContent className="pt-6">
              <div className="flex flex-col sm:flex-row gap-4">
                <div className="flex-1">
                  <div className="relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
                    <Input
                      placeholder="Rechercher un candidat..."
                      className="pl-10"
                    />
                  </div>
                </div>
                <Button variant="outline">
                  <Filter className="h-4 w-4 mr-2" />
                  Filtres
                </Button>
              </div>
            </CardContent>
          </Card>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {candidates.map((candidate) => (
              <Card key={candidate.id} className="hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="space-y-1">
                      <CardTitle className="text-lg">
                        {candidate.first_name} {candidate.last_name}
                      </CardTitle>
                      <CardDescription>{candidate.experience_years} ans d'expérience</CardDescription>
                    </div>
                    <div className="text-right">
                      <div className="flex items-center space-x-1">
                        <Star className={`h-4 w-4 ${getScoreColor(candidate.ai_score)}`} />
                        <span className={`font-semibold ${getScoreColor(candidate.ai_score)}`}>
                          {candidate.ai_score}/10
                        </span>
                      </div>
                      <span className="text-xs text-gray-500">Score IA</span>
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-2 text-sm text-gray-600">
                    <div>{candidate.email}</div>
                    <div>{candidate.phone}</div>
                    <div className="text-xs">
                      Candidature le {new Date(candidate.created_at).toLocaleDateString('fr-FR')}
                    </div>
                  </div>

                  <div className="space-y-2">
                    <div className="text-sm font-medium">Compétences:</div>
                    <div className="flex flex-wrap gap-1">
                      {candidate.skills.slice(0, 3).map((skill, index) => (
                        <Badge key={index} variant="secondary" className="text-xs">
                          {skill}
                        </Badge>
                      ))}
                      {candidate.skills.length > 3 && (
                        <Badge variant="outline" className="text-xs">
                          +{candidate.skills.length - 3}
                        </Badge>
                      )}
                    </div>
                  </div>

                  <div className="flex space-x-2 pt-2">
                    <Button size="sm" variant="outline" className="flex-1">
                      Profil
                    </Button>
                    <Button size="sm" className="flex-1">
                      <Brain className="h-3 w-3 mr-1" />
                      Analyser
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        {/* Applications Tab */}
        <TabsContent value="applications" className="space-y-6">
          <Card>
            <CardContent className="pt-6">
              <div className="flex flex-col sm:flex-row gap-4">
                <div className="flex-1">
                  <div className="relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
                    <Input
                      placeholder="Rechercher une candidature..."
                      className="pl-10"
                    />
                  </div>
                </div>
                <Button variant="outline">
                  <Filter className="h-4 w-4 mr-2" />
                  Filtres
                </Button>
              </div>
            </CardContent>
          </Card>

          <div className="space-y-4">
            {applications.map((application) => (
              <Card key={application.id} className="hover:shadow-lg transition-shadow">
                <CardContent className="pt-6">
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <div className="flex items-center space-x-4">
                        <div>
                          <h3 className="font-semibold">{application.candidate_name}</h3>
                          <p className="text-sm text-gray-600">{application.job_title}</p>
                        </div>
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-4">
                      <div className="text-right">
                        <div className="flex items-center space-x-1">
                          <Star className={`h-4 w-4 ${getScoreColor(application.ai_match_score)}`} />
                          <span className={`font-semibold ${getScoreColor(application.ai_match_score)}`}>
                            {application.ai_match_score}/10
                          </span>
                        </div>
                        <span className="text-xs text-gray-500">Match IA</span>
                      </div>
                      
                      <Badge className={getStatusColor(application.status)}>
                        {getStatusIcon(application.status)}
                        <span className="ml-1 capitalize">{application.status}</span>
                      </Badge>
                      
                      <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                          <Button variant="ghost" size="sm">
                            <MoreHorizontal className="h-4 w-4" />
                          </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end">
                          <DropdownMenuItem>Voir le profil</DropdownMenuItem>
                          <DropdownMenuItem>Programmer entretien</DropdownMenuItem>
                          <DropdownMenuItem>Questions IA</DropdownMenuItem>
                          <DropdownMenuItem>Changer statut</DropdownMenuItem>
                        </DropdownMenuContent>
                      </DropdownMenu>
                    </div>
                  </div>
                  
                  <div className="mt-4 text-sm text-gray-500">
                    Candidature soumise le {new Date(application.application_date).toLocaleDateString('fr-FR')}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}

export default Recruitment

