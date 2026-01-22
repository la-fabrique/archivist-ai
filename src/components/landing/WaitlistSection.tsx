import { motion } from "framer-motion";
import { useState } from "react";
import { Rocket, Check, Gift, Megaphone, Lock } from "lucide-react";

const incentives = [
  { icon: Check, text: "Accès prioritaire — Soyez les premiers à tester" },
  { icon: Gift, text: "Tarif early adopter — Prix de lancement réservé aux inscrits" },
  { icon: Gift, text: "3 mois offerts — Pour les 100 premiers inscrits" },
  { icon: Megaphone, text: "Influencez le produit — Vos retours façonnent l'archiviste" }
];

const roles = [
  { value: "freelance", label: "Indépendant / Freelance" },
  { value: "tpe", label: "Dirigeant TPE (2-10 personnes)" },
  { value: "pme", label: "Dirigeant PME (10-50 personnes)" },
  { value: "accountant", label: "Expert-comptable" },
  { value: "other", label: "Autre" }
];

const WaitlistSection = () => {
  const [email, setEmail] = useState("");
  const [role, setRole] = useState("");
  const [isSubmitted, setIsSubmitted] = useState(false);
  
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitted(true);
  };
  
  return (
    <section id="waitlist" className="py-16 md:py-24 bg-gradient-to-b from-secondary/30 to-primary/5">
      <div className="container-narrow">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="text-center mb-12"
        >
          <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4">
            Soyez parmi les premiers à retrouver la sérénité documentaire
          </h2>
          <p className="text-muted-foreground max-w-xl mx-auto">
            Inscrivez-vous pour un accès prioritaire au lancement et bénéficiez du tarif early adopter.
          </p>
        </motion.div>
        
        <div className="grid lg:grid-cols-2 gap-12 items-start max-w-4xl mx-auto">
          {/* Form */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2, duration: 0.5 }}
          >
            {!isSubmitted ? (
              <form onSubmit={handleSubmit} className="bg-card rounded-2xl border border-border p-8 shadow-lg">
                <div className="mb-6">
                  <label htmlFor="email" className="block text-sm font-medium text-foreground mb-2">
                    📧 Votre email professionnel
                  </label>
                  <input
                    type="email"
                    id="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="vous@entreprise.com"
                    required
                    className="w-full px-4 py-3 rounded-lg border border-input bg-background text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary transition-colors"
                  />
                </div>
                
                <div className="mb-8">
                  <label className="block text-sm font-medium text-foreground mb-3">
                    👤 Vous êtes :
                  </label>
                  <div className="space-y-2">
                    {roles.map((roleOption) => (
                      <label
                        key={roleOption.value}
                        className={`flex items-center gap-3 p-3 rounded-lg border cursor-pointer transition-all ${
                          role === roleOption.value
                            ? "border-primary bg-primary/5"
                            : "border-border hover:border-primary/30"
                        }`}
                      >
                        <input
                          type="radio"
                          name="role"
                          value={roleOption.value}
                          checked={role === roleOption.value}
                          onChange={(e) => setRole(e.target.value)}
                          className="sr-only"
                        />
                        <div className={`w-4 h-4 rounded-full border-2 flex items-center justify-center ${
                          role === roleOption.value ? "border-primary" : "border-muted-foreground"
                        }`}>
                          {role === roleOption.value && (
                            <div className="w-2 h-2 rounded-full bg-primary" />
                          )}
                        </div>
                        <span className="text-sm text-foreground">{roleOption.label}</span>
                      </label>
                    ))}
                  </div>
                </div>
                
                <button
                  type="submit"
                  className="w-full flex items-center justify-center gap-2 px-6 py-4 bg-warning text-warning-foreground font-semibold rounded-xl hover:bg-warning/90 transition-all shadow-lg hover:shadow-xl"
                >
                  <Rocket className="w-5 h-5" />
                  REJOINDRE LA LISTE D'ATTENTE
                </button>
                
                <p className="flex items-center justify-center gap-2 text-xs text-muted-foreground mt-4">
                  <Lock className="w-3 h-3" />
                  Pas de spam. Juste les infos de lancement.
                </p>
              </form>
            ) : (
              <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="bg-card rounded-2xl border border-accent p-8 text-center"
              >
                <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-accent/10 flex items-center justify-center">
                  <Check className="w-8 h-8 text-accent" />
                </div>
                <h3 className="text-xl font-bold text-foreground mb-2">Vous êtes inscrit ! 🎉</h3>
                <p className="text-muted-foreground">
                  Nous vous contacterons dès le lancement de l'archiviste.
                </p>
              </motion.div>
            )}
          </motion.div>
          
          {/* Incentives */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.3, duration: 0.5 }}
            className="space-y-4"
          >
            {incentives.map((incentive, index) => (
              <div
                key={index}
                className="flex items-start gap-4 p-4 bg-card rounded-xl border border-border"
              >
                <div className="w-8 h-8 rounded-lg bg-accent/10 flex items-center justify-center flex-shrink-0">
                  <incentive.icon className="w-4 h-4 text-accent" />
                </div>
                <p className="text-sm text-foreground">{incentive.text}</p>
              </div>
            ))}
          </motion.div>
        </div>
      </div>
    </section>
  );
};

export default WaitlistSection;
