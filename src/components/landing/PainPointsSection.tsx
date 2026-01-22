import { motion } from "framer-motion";
import { FolderOpen, Clock, HelpCircle, Users, Phone, AlertTriangle } from "lucide-react";

const painPoints = [
  {
    icon: FolderOpen,
    emoji: "📂",
    title: '"scan001.pdf"',
    description: "Des fichiers aux noms incompréhensibles partout"
  },
  {
    icon: Clock,
    emoji: "⏰",
    title: "30 à 90 minutes par semaine",
    description: "Perdues à chercher des documents"
  },
  {
    icon: HelpCircle,
    emoji: "🤯",
    title: '"Où j\'ai mis cette facture ?"',
    description: "Le stress du document introuvable"
  },
  {
    icon: Users,
    emoji: "👥",
    title: '"Personne ne comprend mon classement"',
    description: "Méthodes personnelles non partageables"
  },
  {
    icon: Phone,
    emoji: "📞",
    title: '"Votre comptable a encore appelé"',
    description: "Justificatifs manquants, relances infinies"
  },
  {
    icon: AlertTriangle,
    emoji: "😰",
    title: '"Le contrôle fiscal est dans 2 jours"',
    description: "Panique des documents perdus"
  }
];

const PainPointsSection = () => {
  return (
    <section className="py-16 md:py-24 bg-secondary/30">
      <div className="container-narrow">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="text-center mb-12"
        >
          <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4">
            Vous reconnaissez-vous ?
          </h2>
        </motion.div>
        
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-12">
          {painPoints.map((point, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1, duration: 0.5 }}
              className="group p-6 bg-card rounded-2xl border border-border hover:border-destructive/30 hover:shadow-lg transition-all"
            >
              <span className="text-3xl mb-4 block">{point.emoji}</span>
              <h3 className="font-semibold text-foreground mb-2">{point.title}</h3>
              <p className="text-sm text-muted-foreground">{point.description}</p>
            </motion.div>
          ))}
        </div>
        
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.3, duration: 0.5 }}
          className="text-center max-w-2xl mx-auto"
        >
          <p className="text-xl md:text-2xl font-semibold text-foreground mb-2">
            Et si un archiviste professionnel s'occupait de tout ça pour vous ?
          </p>
          <p className="text-muted-foreground italic">
            Sans embaucher. Sans former. Sans y penser.
          </p>
        </motion.div>
      </div>
    </section>
  );
};

export default PainPointsSection;
