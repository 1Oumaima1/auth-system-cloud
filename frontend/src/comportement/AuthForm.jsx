import axios from 'axios';
import { motion } from 'framer-motion';
import { ArrowLeftRight, Loader2, Mail, Lock, User, UserCircle } from 'lucide-react';
import { useState } from 'react';
import GlassCard from '../components/GlassCard';
import GradientButton from '../components/GradientButton';
import InputField from '../components/InputField';

const AuthForm = ({ type = 'login', onToggle }) => {
  const [formData, setFormData] = useState(
    type === 'login'
      ? { email: '', password: '' }
      : { nom: '', prenom: '', email: '', password: '' }
  );
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      const endpoint = type === 'login' ? '/auth/login' : '/auth/signup';
      const res = await axios.post(`http://127.0.0.1:8000${endpoint}`, formData);
      
      if (type === 'login') {
        const { access_token, role } = res.data;
        localStorage.setItem('token', access_token);
        localStorage.setItem('role', role);
        window.location.href = role === 'admin' ? '/admin' : '/user';
      } else {
        onToggle(); // Bascule vers login après inscription réussie
      }
    } catch (err) {
      setError(err.response?.data?.detail || "Une erreur est survenue");
    } finally {
      setIsLoading(false);
    }
  };

  const fields = type === 'login' 
    ? [
        { name: 'email', type: 'email', placeholder: 'Adresse e-mail', icon: Mail },
        { name: 'password', type: 'password', placeholder: 'Mot de passe', icon: Lock },
      ]
    : [
        { name: 'nom', type: 'text', placeholder: 'Nom', icon: User },
        { name: 'prenom', type: 'text', placeholder: 'Prénom', icon: UserCircle },
        { name: 'email', type: 'email', placeholder: 'Adresse e-mail', icon: Mail },
        { name: 'password', type: 'password', placeholder: 'Mot de passe', icon: Lock },
      ];

  return (
    <div className="w-full max-w-md mx-auto space-y-8">
      <motion.div 
        className="text-center"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h1 className="text-4xl font-extrabold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent mb-3">
          {type === 'login' ? 'Bon retour' : 'Créer un compte'}
        </h1>
        <p className="text-slate-500 font-medium">
          {type === 'login' ? 'Connectez-vous pour continuer' : 'Rejoignez notre plateforme cloud dès aujourd’hui'}
        </p>
      </motion.div>

      <GlassCard className="bg-white/90 border-white/50 shadow-xl">
        {error && (
          <motion.div 
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className="mb-6 p-3 rounded-lg bg-red-500/10 border border-red-500/50 text-red-200 text-sm text-center"
          >
            {error}
          </motion.div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5">
          {fields.map((field, idx) => (
            <motion.div 
              key={field.name}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: idx * 0.1 }}
            >
              <InputField
                {...field}
                value={formData[field.name]}
                onChange={handleChange}
              />
            </motion.div>
          ))}

          <GradientButton 
            type="submit" 
            disabled={isLoading} 
            className="w-full"
          >
            {isLoading ? (
              <Loader2 className="w-5 h-5 animate-spin mx-auto" />
            ) : (
              type === 'login' ? 'Se connecter' : 'Commencer'
            )}
          </GradientButton>
        </form>

        <div className="mt-8 flex flex-col items-center gap-4 text-sm">
          <span className="text-slate-500">
            {type === 'login' ? "Nouveau ici ?" : "Déjà membre ?"}
          </span>
          <button
            onClick={onToggle}
            className="text-indigo-600 hover:text-indigo-700 font-bold flex items-center gap-2 transition-colors px-4 py-2 rounded-lg hover:bg-indigo-50"
          >
            {type === 'login' ? 'Créer un compte' : 'Se connecter'}
            <ArrowLeftRight className="w-3 h-3" />
          </button>
        </div>
      </GlassCard>
    </div>
  );
};

export default AuthForm;