import { motion } from "framer-motion";
import {
  FolderTree, FilePlus2, Inbox,
  BookOpen, Shield, Users, ClipboardList, Target, Lightbulb
} from "lucide-react";

const steps = [
  {
    icon: FolderTree,
    title: "Votre espace, créé en quelques secondes",
    description: "Votre assistant génère les bons dossiers selon votre profil — SASU, artisan, profession libérale. Une structure professionnelle, d'emblée."
  },
  {
    icon: FilePlus2,
    title: "Chaque document à sa place, au bon nom",
    description: "Votre assistant lit le document, comprend ce que c'est, le place dans le bon dossier et lui donne un nom clair. Même les PDF scannés."
  },
  {
    icon: Inbox,
    title: "Votre inbox vidée sans effort",
    description: "Un dossier entier traité en une passe. Votre assistant vous soumet un plan de classement avant de rien déplacer. Vous validez, il exécute."
  }
];

const benefits = [
  {
    icon: BookOpen,
    title: "Des règles professionnelles, pas de l'improvisation",
    description: "Archivist applique un corpus de règles conçues par des archivistes, adapté au droit fiscal français. Lisibles, auditables, pas une boîte noire."
  },
  {
    icon: Lightbulb,
    title: "Compatible avec votre assistant actuel",
    description: "Votre agent préféré — Claude, ChatGPT, Copilot ou un agent sur mesure — pilote Archivist. Vous ne changez pas d'outil."
  },
  {
    icon: Target,
    title: "Des noms de fichiers enfin lisibles",
    description: "Fini les « facture_jean_vf2_FINAL ». Chaque fichier porte une date, un émetteur, un objet — triable et compréhensible au premier coup d'œil."
  },
  {
    icon: ClipboardList,
    title: "Tout est traçable",
    description: "Chaque action est consignée. Votre assistant sait ce qu'il a fait, pourquoi, et peut vous l'expliquer."
  },
  {
    icon: Shield,
    title: "Rien ne disparaît",
    description: "Archivist range, ne supprime jamais. Zéro risque de perte, quel que soit le cas."
  },
  {
    icon: Users,
    title: "Vous gardez le contrôle",
    description: "Sur les cas clairs, l'agent agit. Sur les cas ambigus, il vous demande d'abord. Toujours."
  }
];

const SolutionSection = () => {
  return (
    <section id="solution" className="py-16 md:py-24">
      <div className="container-narrow">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="text-center mb-4"
        >
          <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4">
            Comment ça marche
          </h2>
          <p className="text-muted-foreground max-w-xl mx-auto">
            Vous parlez à votre assistant. Votre assistant parle à Archivist. Vos documents sont rangés.
          </p>
        </motion.div>

        <div className="flex flex-col md:flex-row items-stretch justify-center gap-4 md:gap-8 mb-16 mt-12">
          {steps.map((step, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.15, duration: 0.5 }}
              className="flex-1"
            >
              <div className="h-full p-8 bg-card rounded-2xl border border-border shadow-sm text-center flex flex-col items-center">
                <div className="w-14 h-14 mx-auto mb-4 rounded-2xl bg-primary/10 flex items-center justify-center">
                  <step.icon className="w-7 h-7 text-primary" />
                </div>
                <div className="w-6 h-6 rounded-full bg-primary/10 text-primary text-xs font-bold flex items-center justify-center mb-3">
                  {index + 1}
                </div>
                <h3 className="font-bold text-base text-foreground mb-3 leading-snug">{step.title}</h3>
                <p className="text-sm text-muted-foreground leading-relaxed">{step.description}</p>
              </div>
            </motion.div>
          ))}
        </div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="mb-8"
        >
          <h3 className="text-xl font-semibold text-center text-foreground mb-8">
            Ce qui rend Archivist différent
          </h3>
        </motion.div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {benefits.map((benefit, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1, duration: 0.5 }}
              className="flex items-start gap-4 p-5 bg-card rounded-xl border border-border hover:border-primary/30 hover:shadow-md transition-all"
            >
              <div className="w-10 h-10 rounded-lg bg-accent/10 flex items-center justify-center flex-shrink-0">
                <benefit.icon className="w-5 h-5 text-accent" />
              </div>
              <div>
                <h4 className="font-semibold text-foreground mb-1">{benefit.title}</h4>
                <p className="text-sm text-muted-foreground">{benefit.description}</p>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default SolutionSection;
