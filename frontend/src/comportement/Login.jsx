import { motion, AnimatePresence } from 'framer-motion';
import { useState } from 'react';
import AuthForm from './AuthForm';

const Login = () => {
  const [view, setView] = useState('login');

  return (
    <main className="min-h-screen flex items-center justify-center p-6">
      <AnimatePresence mode="wait">
        <motion.div
          key={view}
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 1.05 }}
          transition={{ duration: 0.3, ease: "easeOut" }}
          className="w-full"
        >
          <AuthForm 
            type={view} 
            onToggle={() => setView(view === 'login' ? 'signup' : 'login')} 
          />
        </motion.div>
      </AnimatePresence>
    </main>
  );
};

export default Login;