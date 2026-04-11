import React, { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import GlassCard from '../components/GlassCard';
import InputField from '../components/InputField';
import GradientButton from '../components/GradientButton';

const API_BASE = 'http://127.0.0.1:8000/auth';

const ResetPassword = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const token = searchParams.get('token');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!token) {
      setMessage('Token manquant. Vérifiez votre email.');
    }
  }, [token]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      setMessage('Les mots de passe ne correspondent pas.');
      return;
    }
    if (password.length < 8) {
      setMessage('Mot de passe trop court (min 8 chars).');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/auth/reset-password`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          token,
          password,
          confirm_password: confirmPassword
        }),
      });

      const data = await response.json();
      if (response.ok) {
        setMessage('Mot de passe réinitialisé ! Redirection login...');
        setTimeout(() => navigate('/login'), 2000);
      } else {
        setMessage(data.error || 'Erreur reset.');
      }
    } catch (err) {
      setMessage('Erreur réseau.');
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-600 via-blue-600 to-indigo-800 flex items-center justify-center p-4">
      <GlassCard className="w-full max-w-md">
        <h2 className="text-2xl font-bold text-center text-white mb-8">Nouveau mot de passe</h2>
        {message && (
          <div className={`p-3 rounded-lg mb-4 text-sm ${
            message.includes('réinitialisé') ? 'bg-green-500 text-white' : 'bg-red-500 text-white'
          }`}>
            {message}
          </div>
        )}
        {token ? (
          <form onSubmit={handleSubmit} className="space-y-4">
            <InputField
              label="Nouveau mot de passe"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <InputField
              label="Confirmer"
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
            />
            <GradientButton type="submit" disabled={loading} className="w-full">
              {loading ? 'Réinitialisation...' : 'Réinitialiser'}
            </GradientButton>
          </form>
        ) : (
          <p className="text-center text-white/80">Redirection...</p>
        )}
      </GlassCard>
    </div>
  );
};

export default ResetPassword;

