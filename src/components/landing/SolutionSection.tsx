import { motion } from "framer-motion";
import { 
  Download, Brain, FolderCheck, 
  Target, Search, Plug, Shield, Users, Lightbulb
} from "lucide-react";

const steps = [
  {
    icon: Download,
    title: "CAPTE",
    items: ["Emails", "Scans", "Téléchargements"]
  },
  {
    icon: Brain,
    title: "COMPREND",
    items: ["Lit le contenu", "Identifie le type"]
  },
  {
    icon: FolderCheck,
    title: "RANGE",
    items: ["Place au bon endroit", "Nomme correctement"]
  }
];

const benefits = [
  {
    icon: Target,
    title: "Nommage intelligent",
    description: "Fichiers triables ET compréhensibles"
  },
  {
    icon: Lightbulb,
    title: "Comprend VOTRE logique",
    description: "Facture client ≠ Facture achat"
  },
  {
    icon: Search,
    title: "Recherche naturelle",
    description: '"Trouve la facture de Jean en mars"'
  },
  {
    icon: Plug,
    title: "Zéro nouvelle interface",
    description: "Se branche sur VOS outils existants"
  },
  {
    icon: Shield,
    title: "Jamais de suppression",
    description: "Chaque action tracée, historique complet"
  },
  {
    icon: Users,
    title: "Human-in-the-loop",
    description: "Autonome sur le simple, vous consulte pour le risqué"
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
          className="text-center mb-12"
        >
          <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4">
            Votre archiviste virtuel, disponible 24/7
          </h2>
        </motion.div>
        
        {/* Workflow steps */}
        <div className="flex flex-col md:flex-row items-stretch justify-center gap-4 md:gap-8 mb-16">
          {steps.map((step, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.15, duration: 0.5 }}
              className="flex-1 flex flex-col items-center"
            >
              <div className="relative w-full max-w-xs">
                <div className="p-8 bg-card rounded-2xl border border-border shadow-sm text-center">
                  <div className="w-16 h-16 mx-auto mb-4 rounded-2xl bg-primary/10 flex items-center justify-center">
                    <step.icon className="w-8 h-8 text-primary" />
                  </div>
                  <h3 className="font-bold text-lg text-foreground mb-3">{step.title}</h3>
                  <ul className="space-y-1">
                    {step.items.map((item, i) => (
                      <li key={i} className="text-sm text-muted-foreground">{item}</li>
                    ))}
                  </ul>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
        
        {/* Benefits grid */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="mb-6"
        >
          <h3 className="text-xl font-semibold text-center text-foreground mb-8">
            Ce que ça change pour vous
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
