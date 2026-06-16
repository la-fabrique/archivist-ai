import { motion } from "framer-motion";
import { Monitor, Cloud, Bot } from "lucide-react";

const deploymentModes = [
  {
    icon: Monitor,
    tag: "Sur votre ordinateur",
    title: "Vos fichiers ne quittent jamais votre machine",
    description: "Archivist tourne en local. Aucun document n'est envoyé à un serveur externe. Idéal si vous gérez vos fichiers sur votre poste ou un serveur interne.",
    badge: "Disponible"
  },
  {
    icon: Cloud,
    tag: "Dans le cloud",
    title: "Accessible depuis n'importe où",
    description: "Hébergez Archivist sur un serveur ou une infrastructure cloud. Votre assistant IA y accède à distance, et votre classement se met à jour partout.",
    badge: "Disponible"
  },
  {
    icon: Bot,
    tag: "Avec votre agent préféré",
    title: "Claude, ChatGPT, Copilot — ou votre propre agent",
    description: "Archivist s'intègre à l'assistant IA de votre choix. Vous ne changez pas d'outil : vous donnez à votre agent actuel la capacité de gérer vos documents.",
    badge: "Tous agents"
  }
];

const IntegrationsSection = () => {
  return (
    <section id="deploiement" className="py-16 md:py-24 bg-secondary/30">
      <div className="container-narrow">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="text-center mb-4"
        >
          <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4">
            Trois façons de déployer Archivist
          </h2>
          <p className="text-muted-foreground max-w-xl mx-auto">
            Sur votre poste, sur un serveur, ou dans le cloud — Archivist s'adapte à votre organisation, pas l'inverse.
          </p>
        </motion.div>

        <div className="grid md:grid-cols-3 gap-6 mt-12">
          {deploymentModes.map((mode, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.15, duration: 0.5 }}
              className="flex flex-col p-7 bg-card rounded-2xl border border-border hover:border-primary/30 hover:shadow-md transition-all"
            >
              <div className="flex items-start justify-between mb-4">
                <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center">
                  <mode.icon className="w-6 h-6 text-primary" />
                </div>
                <span className="text-xs font-medium px-2.5 py-1 bg-accent/10 text-accent rounded-full">
                  {mode.badge}
                </span>
              </div>
              <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-2">
                {mode.tag}
              </p>
              <h3 className="font-bold text-foreground mb-3 leading-snug">{mode.title}</h3>
              <p className="text-sm text-muted-foreground leading-relaxed flex-1">{mode.description}</p>
            </motion.div>
          ))}
        </div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.5, duration: 0.5 }}
          className="text-center max-w-xl mx-auto mt-10"
        >
          <p className="text-lg font-semibold text-foreground mb-2">
            Vous choisissez. Archivist s'adapte.
          </p>
          <p className="text-muted-foreground">
            Pas de migration, pas de nouveau stockage à adopter. Archivist se branche sur ce que vous avez déjà.
          </p>
        </motion.div>
      </div>
    </section>
  );
};

export default IntegrationsSection;
