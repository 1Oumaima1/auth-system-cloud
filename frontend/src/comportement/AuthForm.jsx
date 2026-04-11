import axios from "axios";
import { motion } from "framer-motion";
import {
  ArrowLeftRight,
  Loader2,
  Lock,
  Mail,
  User,
  UserCircle,
} from "lucide-react";
import { useState } from "react";

import GlassCard from "../components/GlassCard";
import GradientButton from "../components/GradientButton";
import InputField from "../components/InputField";
import OAuthButton from "../components/OAuthButton";

const AuthForm = ({ type = "login", onToggle }) => {
  const [formData, setFormData] = useState(
    type === "login"
      ? { email: "", password: "" }
      : { nom: "", prenom: "", email: "", password: "" }
  );

  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [successMsg, setSuccessMsg] = useState("");

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setError("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError("");

    try {
      const endpoint = type === "login" ? "/auth/login" : "/auth/signup";
      const res = await axios.post(
        `http://127.0.0.1:8000${endpoint}`,
        formData
      );

      if (type === "login") {
        const { access_token, role } = res.data;
        localStorage.setItem("token", access_token);
        localStorage.setItem("role", role);
        window.location.href = role === "admin" ? "/admin" : "/user";
      } else {
        setSuccessMsg(res.data.msg || "Compte créé avec succès !");
      }
    } catch (err) {
      setError(err.response?.data?.detail || "Une erreur est survenue");
    } finally {
      setIsLoading(false);
    }
  };

  // LOADING OVERLAY
  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-50 to-purple-50 p-8">
        <motion.div
          className="text-center"
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.9 }}
        >
          <div className="w-24 h-24 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin mb-6 mx-auto shadow-xl"></div>
          <div className="bg-white/90 backdrop-blur-xl p-8 rounded-2xl shadow-2xl max-w-md mx-auto">
            <h2 className="text-2xl font-bold text-indigo-600 mb-2">Connexion...</h2>
            <p className="text-slate-500">Nous vérifions vos identifiants</p>
          </div>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-8 bg-gradient-to-br from-indigo-50 to-purple-50">
      <motion.div
        className="w-full max-w-md"
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
      >
        {/* HEADER */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-extrabold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
            {type === "login" ? "Bon retour" : "Créer un compte"}
          </h1>
          <p className="text-slate-500 mt-2">
            {type === "login"
              ? "Connectez-vous pour continuer"
              : "Rejoignez notre plateforme cloud"}
          </p>
        </div>

        <GlassCard className="bg-white/90 p-8 space-y-6 shadow-xl">
          {/* ERROR */}
          {error && (
            <div className="p-3 rounded-xl bg-red-100 text-red-700 text-center text-sm">
              {error}
            </div>
          )}

          {/* SUCCESS */}
          {successMsg && (
            <div className="p-3 rounded-xl bg-green-100 text-green-700 text-center text-sm">
              {successMsg}
            </div>
          )}

          {/* FORM */}
          <form onSubmit={handleSubmit} className="space-y-4">
            {type === "signup" && (
              <>
                <InputField
                  name="nom"
                  placeholder="Nom"
                  icon={User}
                  onChange={handleChange}
                />
                <InputField
                  name="prenom"
                  placeholder="Prénom"
                  icon={UserCircle}
                  onChange={handleChange}
                />
              </>
            )}

            <InputField
              name="email"
              type="email"
              placeholder="Email"
              icon={Mail}
              onChange={handleChange}
            />

            <InputField
              name="password"
              type="password"
              placeholder="Mot de passe"
              icon={Lock}
              onChange={handleChange}
            />

            <GradientButton type="submit" disabled={isLoading}>
              {isLoading ? (
                <Loader2 className="animate-spin mx-auto" />
              ) : type === "login" ? (
                "Se connecter"
              ) : (
                "Créer"
              )}
            </GradientButton>
          </form>

          {/* FORGOT PASSWORD */}
          {type === "login" && (
            <button
              className="text-sm text-slate-500 hover:text-indigo-600 text-center w-full"
              onClick={async () => {
                await axios.post(
                  "http://127.0.0.1:8000/auth/forgot-password",
                  { email: formData.email }
                );
                setError("Lien envoyé si email existe.");
              }}
            >
              Mot de passe oublié ?
            </button>
          )}

          {/* OAUTH */}
          {type === "login" && (
            <div className="pt-4">
              <div className="flex justify-center gap-6">
                <OAuthButton provider="google" />
                <OAuthButton provider="facebook" />
              </div>

              <p className="text-center text-xs text-gray-400 mt-3">ou</p>
            </div>
          )}

          {/* SWITCH BUTTON */}
          <div className="pt-6">
            <button
              onClick={onToggle}
              className="mx-auto flex justify-center items-center gap-2 px-6 py-3 rounded-xl text-indigo-600 border border-indigo-200 hover:bg-indigo-50 shadow-sm hover:shadow-md transition"
            >
              {type === "login"
                ? "Créer un compte"
                : "Se connecter"}
              <ArrowLeftRight size={16} />
            </button>
          </div>
        </GlassCard>
      </motion.div>
    </div>
  );
};

export default AuthForm;

