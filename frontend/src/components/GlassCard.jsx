import { motion } from 'framer-motion';

const GlassCard = ({ children, className = '', onClick, ...props }) => {
  return (
    <motion.div
      className={`glass-card p-8 ${className}`}
      whileHover={{ y: -4, scale: 1.02 }}
      transition={{ duration: 0.2 }}
      onClick={onClick}
      {...props}
    >
      {children}
    </motion.div>
  );
};

export default GlassCard;

