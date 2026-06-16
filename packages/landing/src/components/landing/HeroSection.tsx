import { motion } from "framer-motion";
import { Github, Shield, Globe, CheckCircle, ExternalLink } from "lucide-react";
import { siteConfig } from "@/config/site";

const HeroSection = () => {
  return (
    <section className="relative pt-32 pb-20 md:pt-40 md:pb-28 overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-b from-primary/5 via-transparent to-transparent" />
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
            <Github className="w-4 h-4" />
            Open source · Apache 2.0 · Pour toujours
          </motion.div>

          <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-foreground leading-tight mb-6">
            Vos documents classés,{" "}
            <span className="text-gradient-primary">sans y penser</span>
          </h1>

          <p className="speakable text-lg md:text-xl text-muted-foreground max-w-2xl mx-auto mb-4">
            Dites à votre assistant IA de s'occuper de vos fichiers. Archivist lui donne l'expertise d'un archiviste professionnel — et range tout selon les règles du droit français.
          </p>

          <p className="text-base text-muted-foreground max-w-xl mx-auto mb-10">
            Sur votre ordinateur, dans le cloud, ou avec l'agent de votre choix.
            <br />
            Aucune nouvelle interface. Aucune formation.
          </p>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3, duration: 0.5 }}
            className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-12"
          >
            <a
              href={siteConfig.github}
              target="_blank"
              rel="noopener noreferrer"
              className="group inline-flex items-center gap-2 px-8 py-4 bg-foreground text-background font-semibold rounded-xl hover:bg-foreground/90 transition-all shadow-lg hover:shadow-xl hover:-translate-y-0.5"
            >
              <Github className="w-5 h-5" />
              Voir le code source
            </a>
            <a
              href={siteConfig.dekaUrl}
              target="_blank"
              rel="noopener noreferrer"
              data-gtm-event="cta_deka_hero"
              className="inline-flex items-center gap-2 px-6 py-4 text-sm font-medium text-muted-foreground hover:text-foreground border border-border rounded-xl hover:border-primary/30 transition-all"
            >
              Accompagnement & entreprise
              <ExternalLink className="w-4 h-4" />
            </a>
          </motion.div>

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
