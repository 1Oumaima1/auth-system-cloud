import axios from 'axios';
import { motion } from 'framer-motion';
import { Shield, TrendingUp, Users } from 'lucide-react';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Sidebar from '../components/Sidebar';
import StatsCard from '../components/StatsCard';

const AdminDashboard = () => {
  const navigate = useNavigate();
  const [message, setMessage] = useState('');

  useEffect(() => {
    const token = localStorage.getItem('token');
    const role = localStorage.getItem('role');

    if (!token || role !== 'admin') {
      navigate('/login');
      return;
    }

    axios.get('http://127.0.0.1:8000/admin/data', {
      headers: { Authorization: `Bearer ${token}` }
    })
    .then(res => setMessage('Bienvenue Admin!'))
    .catch(err => setMessage('Erreur lors de la récupération des données admin'));
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
      <Sidebar isAdmin={true} onLogout={handleLogout} />
      
      <motion.main 
        className="lg:ml-72 mt-20 lg:mt-0 max-w-7xl mx-auto space-y-8"
        initial={{ opacity: 0, x: 30 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
      >
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-indigo-400 to-purple-500 bg-clip-text text-transparent mb-2">
              Panneau de Contrôle Admin
            </h1>
            <p className="text-gray-400 text-lg">{message}</p>
          </div>
        </div>

        {/* Admin Stats */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
          <StatsCard title="Utilisateurs Totaux" value="1,247" icon={Users} change={15.2} />
          <StatsCard title="Admins Actifs" value="12" icon={Shield} change={3.8} />
          <StatsCard title="Croissance Plateforme" value="124%" icon={TrendingUp} change={28.7} />
        </div>

      </motion.main>
    </motion.div>
  );
};

export default AdminDashboard;
