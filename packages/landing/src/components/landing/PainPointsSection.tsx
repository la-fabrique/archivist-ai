import { motion } from "framer-motion";

const painPoints = [
  {
    emoji: "📂",
    title: "Fichiers perdus",
    description: '"Je perds 30 min par jour à chercher des fichiers éparpillés."',
    bgColor: "bg-orange-50 dark:bg-orange-900/20"
  },
  {
    emoji: "⏰",
    title: "Temps gaspillé",
    description: '"30 à 90 minutes par semaine perdues en recherche de documents."',
    bgColor: "bg-amber-50 dark:bg-amber-900/20"
  },
  {
    emoji: "🤯",
    title: "Versions multiples",
    description: '"Est-ce la v2_final.pdf ou la v3_review.docx ?"',
    bgColor: "bg-red-50 dark:bg-red-900/20"
  },
  {
    emoji: "👥",
    title: "Chaos d'équipe",
    description: '"Mon équipe ne range jamais rien au bon endroit."',
    bgColor: "bg-blue-50 dark:bg-blue-900/20"
  },
  {
    emoji: "📞",
    title: "Relances comptables",
    description: '"Votre comptable a encore appelé pour les justificatifs manquants."',
    bgColor: "bg-purple-50 dark:bg-purple-900/20"
  },
  {
    emoji: "😰",
    title: "Panique fiscale",
    description: '"Le contrôle fiscal est dans 2 jours et je ne trouve rien."',
    bgColor: "bg-rose-50 dark:bg-rose-900/20"
  }
];

const PainPointsSection = () => {
  return (
    <section className="py-16 md:py-24 bg-secondary/30">
      <div className="container-narrow">
        <motion.h2
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="text-2xl md:text-3xl lg:text-4xl font-bold leading-tight tracking-tight text-center text-foreground mb-12"
        >
          Vous reconnaissez-vous ?
        </motion.h2>
        
        <div className="grid md:grid-cols-2 gap-4 mb-12">
          {painPoints.map((point, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.08, duration: 0.5 }}
              className="flex items-center gap-4 rounded-xl bg-card p-5 shadow-sm border border-border hover:border-destructive/30 hover:shadow-md transition-all"
            >
              <div className={`flex-shrink-0 flex items-center justify-center w-12 h-12 rounded-full ${point.bgColor} text-2xl`}>
                {point.emoji}
              </div>
              <div className="flex flex-col gap-1">
                <p className="text-foreground text-base font-bold leading-tight">{point.title}</p>
                <p className="text-muted-foreground text-sm font-normal leading-normal">
                  {point.description}
                </p>
              </div>
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
            Pendant ce temps, chaque semaine qui passe coûte des heures.
          </p>
          <p className="text-muted-foreground mb-6">
            30 à 90 minutes perdues à chercher des fichiers. Multipliées par 52 semaines. Multipliées par votre taux journalier.
          </p>
          <a
            href="#solution"
            className="inline-flex items-center gap-2 px-6 py-3 text-sm font-medium text-primary hover:text-primary/80 transition-colors"
          >
            Voir comment Archivist règle ça →
          </a>
        </motion.div>
      </div>
    </section>
  );
};

export default PainPointsSection;
