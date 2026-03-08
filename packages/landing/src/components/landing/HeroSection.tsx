import { motion } from "framer-motion";
import { Rocket, Shield, Globe, CheckCircle } from "lucide-react";

const HeroSection = () => {
  return (
    <section className="relative pt-32 pb-20 md:pt-40 md:pb-28 overflow-hidden">
      {/* Background gradient */}
      <div className="absolute inset-0 bg-gradient-to-b from-primary/5 via-transparent to-transparent" />
      
      {/* Floating shapes */}
      <div className="absolute top-20 left-10 w-72 h-72 bg-primary/10 rounded-full blur-3xl" />
      <div className="absolute bottom-20 right-10 w-96 h-96 bg-accent/10 rounded-full blur-3xl" />
      
      <div className="container-narrow relative">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center max-w-4xl mx-auto"
        >
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.1, duration: 0.5 }}
            className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-accent/10 text-accent text-sm font-medium mb-6"
          >
            <span className="w-2 h-2 rounded-full bg-accent animate-pulse" />
            Bientôt disponible
          </motion.div>
          
          <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-foreground leading-tight mb-6">
            Un archiviste pour{" "}
            <span className="text-gradient-primary">tous vos fichiers</span>
          </h1>
          
          <p className="text-lg md:text-xl text-muted-foreground max-w-2xl mx-auto mb-4">
            Google Drive, Office 365, serveur local... Un seul assistant pour tout organiser.
          </p>
          
          <p className="text-base text-muted-foreground max-w-xl mx-auto mb-10">
            Connecté à vos outils existants. Zéro nouvelle interface à apprendre.
            <br />
            Demandez simplement : <span className="italic">"Trouve-moi la facture de Jean"</span> — et voilà.
          </p>
          
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3, duration: 0.5 }}
            className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-12"
          >
            <a
              href="#waitlist"
              className="group inline-flex items-center gap-2 px-8 py-4 bg-warning text-warning-foreground font-semibold rounded-xl hover:bg-warning/90 transition-all shadow-lg hover:shadow-xl hover:-translate-y-0.5"
            >
              <Rocket className="w-5 h-5" />
              Rejoindre la liste d'attente
            </a>
            <span className="text-sm text-muted-foreground">
              Accès prioritaire + tarif early adopter
            </span>
          </motion.div>
          
          {/* Trust badges */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5, duration: 0.5 }}
            className="flex flex-wrap items-center justify-center gap-6 text-sm text-muted-foreground"
          >
            <div className="flex items-center gap-2">
              <Shield className="w-4 h-4 text-accent" />
              <span>Données souveraines</span>
            </div>
            <div className="flex items-center gap-2">
              <Globe className="w-4 h-4 text-primary" />
              <span>Hébergé en Europe</span>
            </div>
            <div className="flex items-center gap-2">
              <CheckCircle className="w-4 h-4 text-accent" />
              <span>Compatible RGPD</span>
            </div>
          </motion.div>
        </motion.div>
      </div>
    </section>
  );
};

export default HeroSection;
