import { motion } from 'framer-motion';

const GradientButton = ({ children, className = '', whileHover = { scale: 1.05 }, ...props }) => {
  return (
    <motion.button
      className={`gradient-btn ${className}`}
      whileHover={whileHover}
      whileTap={{ scale: 0.95 }}
      transition={{ duration: 0.2 }}
      {...props}
    >
      {children}
    </motion.button>
  );
};

export default GradientButton;

