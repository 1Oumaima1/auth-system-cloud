import axios from 'axios';
import { motion } from 'framer-motion';
import { Activity, DollarSign, Users } from 'lucide-react';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import ActivityChart from '../components/ActivityChart';
import Sidebar from '../components/Sidebar';
import StatsCard from '../components/StatsCard';

const UserDashboard = () => {
  const navigate = useNavigate();
  const [message, setMessage] = useState('');

  useEffect(() => {
    const token = localStorage.getItem('token');
    const role = localStorage.getItem('role');

    if (!token || role !== 'user') {
      navigate('/login');
      return;
    }

    axios.get('http://127.0.0.1:8000/user/data', {
      headers: { Authorization: `Bearer ${token}` }
    })
    .then(res => setMessage('Bienvenue User!'))
    .catch(err => setMessage('Erreur lors de la récupération des données utilisateur'));
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    navigate('/login');
  };

  return (
    <motion.div
      className="min-h-screen bg-slate-50 p-6 lg:p-12"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.4 }}
    >
      <Sidebar isAdmin={false} onLogout={handleLogout} />
      
      <motion.main 
        className="lg:ml-72 mt-20 lg:mt-0 max-w-7xl mx-auto space-y-8"
        initial={{ opacity: 0, x: 30 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
      >
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-indigo-400 to-purple-500 bg-clip-text text-transparent mb-2">
              Bon retour
            </h1>
            <p className="text-slate-600 text-lg font-medium">{message}</p>
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <StatsCard 
            title="Activité Totale" 
            value="24" 
            icon={Activity}
            change={12.5}
          />
          <StatsCard 
            title="Abonnés" 
            value="1.2K" 
            icon={Users}
            change={8.3}
          />
          <StatsCard 
            title="Revenu" 
            value="$4.2K" 
            icon={DollarSign}
            change={-2.1}
          />
        </div>

        {/* Chart & Recent Activity */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <ActivityChart />
          <div className="space-y-4">
            <h3 className="text-2xl font-bold flex items-center text-slate-900">
              Activité Récente
              <span className="ml-2 px-3 py-1 bg-indigo-500/20 text-indigo-400 rounded-full text-sm font-semibold">
                En direct
              </span>
            </h3>
            <div className="space-y-4">
              {['Tâche #123 terminée', 'Nouvel abonné', 'Paiement reçu', 'Profil mis à jour'].map((activity, idx) => (
                <motion.div
                  key={activity}
                  className="glass-card p-6 flex items-center space-x-4 hover:border-purple-200 transition-colors"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3, delay: idx * 0.1 }}
                >
                  <div className="w-2 h-2 bg-purple-500 rounded-full" />
                  <span className="text-slate-800 font-medium">{activity}</span>
                  <span className="ml-auto text-xs text-slate-400">Il y a 2 min</span>
                </motion.div>
              ))}
            </div>
          </div>
        </div>
      </motion.main>
    </motion.div>
  );
};

export default UserDashboard;
