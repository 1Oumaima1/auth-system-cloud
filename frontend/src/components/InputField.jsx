const InputField = ({ icon: Icon, placeholder, type = 'text', className = '', ...props }) => {
  return (
    <div className="relative group">
      {Icon && (
        <div className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-indigo-500 transition-colors duration-300">
          <Icon size={20} />
        </div>
      )}
      <input
        type={type}
        className={`input-field ${Icon ? 'pl-12' : ''} ${className}`}
        placeholder={placeholder}
        {...props}
      />
    </div>
  );
};

export default InputField;
