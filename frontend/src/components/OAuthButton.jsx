import { motion } from "framer-motion";
import { FaFacebookF } from "react-icons/fa";

const OAuthButton = ({ provider }) => {
  const isGoogle = provider === "google";

  return (
    <motion.button
      onClick={() =>
        (window.location.href = `http://127.0.0.1:8000/auth/${provider}`)
      }
      whileHover={{ scale: 1.1 }}
      whileTap={{ scale: 0.9 }}
      className={`w-14 h-14 flex items-center justify-center rounded-full shadow-md transition-all
        ${isGoogle ? "bg-white border" : "bg-blue-600 text-white"}
      `}
    >
      {isGoogle ? (
        <img
          src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg"
          alt="google"
          className="w-6 h-6"
        />
      ) : (
        <FaFacebookF className="text-lg" />
      )}
    </motion.button>
  );
};

export default OAuthButton;