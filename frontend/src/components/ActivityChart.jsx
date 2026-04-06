import { motion } from 'framer-motion';

const ActivityChart = () => {
  return (
    <motion.div
      className="glass-card p-8"
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
    >
      <div className="flex items-center mb-8">
        <div className="w-3 h-3 bg-purple-600 rounded-full mr-3" />
        <h3 className="text-xl font-bold text-slate-900">Aperçu de l'Activité</h3>
      </div>
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <span className="text-slate-500 font-medium">Janv</span>
          <div className="w-24 h-3 bg-slate-100 rounded-full overflow-hidden">
            <motion.div 
              className="h-full bg-gradient-to-r from-purple-500 to-indigo-500 rounded-full"
              initial={{ width: 0 }}
              animate={{ width: '80%' }}
              transition={{ duration: 1.5, delay: 0.5 }}
            />
          </div>
          <span className="text-slate-900 font-bold">1.2k</span>
        </div>
        <div className="flex items-center justify-between">
          <span className="text-gray-400">Févr</span>
          <div className="w-24 h-3 glass-card bg-white/5 rounded-full overflow-hidden">
            <motion.div 
              className="h-full bg-gradient-to-r from-indigo-500 to-purple-600 rounded-full"
              initial={{ width: 0 }}
              animate={{ width: '95%' }}
              transition={{ duration: 1.5, delay: 0.7 }}
            />
          </div>
          <span className="text-white font-semibold">1.8k</span>
        </div>
        <div className="flex items-center justify-between">
          <span className="text-gray-400">Mars</span>
          <div className="w-24 h-3 glass-card bg-white/5 rounded-full overflow-hidden">
            <motion.div 
              className="h-full bg-gradient-to-r from-indigo-500 to-purple-600 rounded-full"
              initial={{ width: 0 }}
              animate={{ width: '70%' }}
              transition={{ duration: 1.5, delay: 0.9 }}
            />
          </div>
          <span className="text-white font-semibold">1.1k</span>
        </div>
      </div>
    </motion.div>
  );
};

export default ActivityChart;
