import { motion } from 'framer-motion';

const StatsCard = ({ title, value, icon: Icon, change = 0 }) => {
  return (
    <motion.div
      className="glass-card p-8 flex items-center space-x-6 group cursor-pointer hover:border-purple-200 transition-all duration-300"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      whileHover={{ scale: 1.05, y: -10 }}
    >
      <motion.div 
        className="w-16 h-16 bg-purple-50 rounded-2xl flex items-center justify-center border border-purple-100 group-hover:border-purple-300 transition-all duration-300"
        whileHover={{ scale: 1.1, rotate: 5 }}
      >
        <Icon className="w-8 h-8 text-purple-600" />
      </motion.div>
      <div className="flex-1 min-w-0">
        <p className="text-slate-500 text-sm font-medium uppercase tracking-wider">{title}</p>
        <p className="text-3xl font-bold text-slate-900 mt-1">{value}</p>
        <p className={`text-sm font-semibold mt-2 ${change >= 0 ? 'text-emerald-400' : 'text-red-400'}`}>
          {change >= 0 ? '↑' : '↓'} {Math.abs(change)}% par rapport au mois dernier
        </p>
      </div>
    </motion.div>
  );
};

export default StatsCard;
