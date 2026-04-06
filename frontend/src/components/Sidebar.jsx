import { motion } from 'framer-motion';
import { BarChart3, LogOut, Settings, Shield, User } from 'lucide-react';
import { useState } from 'react';

const Sidebar = ({ isAdmin = false, onLogout }) => {
  const [isOpen, setIsOpen] = useState(true);

  const menuItems = isAdmin 
    ? [
        { icon: Shield, label: 'Tableau de bord', path: '/admin' },
        { icon: Settings, label: 'Paramètres', path: '/admin/settings' },
      ]
    : [
        { icon: User, label: 'Profil', path: '/user' },
        { icon: BarChart3, label: 'Activité', path: '/user/activity' },
      ];

  return (
    <>
      <motion.div 
        className={`glass-card h-screen p-6 flex flex-col justify-between fixed lg:relative z-50 w-64 lg:w-72 transition-all duration-300 ${isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}`}
        initial={{ x: -300 }}
        animate={{ x: 0 }}
        transition={{ duration: 0.3 }}
      >
        <div>
          <div className="flex items-center mb-8">
            <motion.div 
              className="w-10 h-10 bg-gradient-to-r from-purple-500 to-indigo-600 rounded-xl flex items-center justify-center mr-3"
              whileHover={{ scale: 1.1 }}
            >
              {isAdmin ? <Shield className="w-5 h-5 text-white" /> : <User className="w-5 h-5 text-white" />}
            </motion.div>
            <h2 className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-indigo-600 bg-clip-text text-transparent">
              {isAdmin ? 'Panel Admin' : 'Tableau de bord'}
            </h2>
          </div>
          <nav className="space-y-4">
            {menuItems.map((item, idx) => (
              <motion.a
                key={item.label}
                href="#"
                className="flex items-center p-4 rounded-xl text-slate-700 hover:bg-purple-50 hover:text-purple-700 transition-all duration-200 flex font-medium"
                whileHover={{ x: 8 }}
                initial={{ x: 0 }}
                transition={{ delay: idx * 0.05 }}
              >
                <item.icon className="w-5 h-5 mr-4 text-purple-500" />
                {item.label}
              </motion.a>
            ))}
          </nav>
        </div>
        <motion.button
          onClick={onLogout}
          className="flex items-center p-4 rounded-xl text-slate-700 hover:bg-red-50 hover:text-red-600 transition-all duration-200 self-start font-medium"
          whileHover={{ x: 4 }}
        >
          <LogOut className="w-5 h-5 mr-4 text-red-500" />
          Déconnexion
        </motion.button>
      </motion.div>
      {!isOpen && (
        <motion.button
          className="lg:hidden fixed z-40 top-6 left-6 p-3 glass-card rounded-xl"
          onClick={() => setIsOpen(true)}
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </motion.button>
      )}
    </>
  );
};

export default Sidebar;
