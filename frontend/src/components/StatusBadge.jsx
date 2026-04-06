import { motion } from 'framer-motion';

const StatusBadge = ({ status }) => {
  const getStatusConfig = (status) => {
    switch (status.toLowerCase()) {
      case 'active':
        return { bg: 'bg-emerald-500/20', border: 'border-emerald-500/50', text: 'text-emerald-400', icon: '●' };
      case 'pending':
        return { bg: 'bg-amber-500/20', border: 'border-amber-500/50', text: 'text-amber-400', icon: '○' };
      case 'suspended':
        return { bg: 'bg-red-500/20', border: 'border-red-500/50', text: 'text-red-400', icon: '✕' };
      default:
        return { bg: 'bg-gray-500/20', border: 'border-gray-500/50', text: 'text-gray-400', icon: '?' };
    }
  };

  const config = getStatusConfig(status);

  return (
    <motion.span
      className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold border-2 ${config.border} ${config.bg} ${config.text} backdrop-blur-sm`}
      whileHover={{ scale: 1.05 }}
    >
      <span className="mr-1 font-mono">{config.icon}</span>
      {status}
    </motion.span>
  );
};

export default StatusBadge;

