import { motion } from 'framer-motion';
import Login from './Login';

const Signup = () => {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.3 }}
    >
      <Login />
    </motion.div>
  );
};

export default Signup;

