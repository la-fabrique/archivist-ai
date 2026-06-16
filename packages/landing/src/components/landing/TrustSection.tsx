import { motion } from "framer-motion";
import { Shield, Globe, Lock, ClipboardList, Ban, Eye } from "lucide-react";

const badges = [
  { icon: Shield, label: "RGPD Compliant" },
  { icon: Globe, label: "Hébergé en Europe" },
  { icon: Eye, label: "Open Source Apache 2.0" },
  { icon: ClipboardList, label: "Audit trail" },
  { icon: Ban, label: "Zéro partage externe" },
  { icon: Shield, label: "Souveraineté" }
];

const guarantees = [
  {
    icon: Lock,
    title: "100% Local",
    description: "Vos documents ne quittent JAMAIS vos systèmes"
  },
  {
    icon: ClipboardList,
    title: "Traçabilité totale",
    description: "Chaque action de l'archiviste est loggée"
  },
  {
    icon: Ban,
    title: "Zéro suppression",
    description: "L'archiviste range, ne supprime jamais"
  },
  {
    icon: Eye,
    title: "Transparence",
    description: "Prévisualisez chaque classement avant validation"
  }
];

const TrustSection = () => {
  return (
    <section className="py-16 md:py-24">
      <div className="container-narrow">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="text-center mb-10"
        >
          <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4">
            Vos documents sont en sécurité
          </h2>
        </motion.div>
        
        {/* Badges */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.2, duration: 0.5 }}
          className="flex flex-wrap items-center justify-center gap-2 mb-12"
        >
          {badges.map((badge, index) => (
            <div
              key={index}
              className="flex items-center gap-2 px-4 py-2 bg-accent/10 rounded-full text-sm font-medium text-accent"
            >
              <badge.icon className="w-4 h-4" />
              <span>{badge.label}</span>
            </div>
          ))}
        </motion.div>
        
        {/* Guarantees */}
        <div className="grid md:grid-cols-2 gap-6 max-w-3xl mx-auto">
          {guarantees.map((guarantee, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1, duration: 0.5 }}
              className="flex items-start gap-4 p-6 bg-card rounded-xl border border-border"
            >
              <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center flex-shrink-0">
                <guarantee.icon className="w-5 h-5 text-primary" />
              </div>
              <div>
                <h4 className="font-semibold text-foreground mb-1">{guarantee.title}</h4>
                <p className="text-sm text-muted-foreground">{guarantee.description}</p>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default TrustSection;
