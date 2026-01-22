import { motion } from "framer-motion";
import { useState } from "react";
import { User, Building, Building2, Calculator, MoreHorizontal } from "lucide-react";

const useCases = [
  {
    id: "freelance",
    icon: User,
    title: "Indépendants & Freelances",
    description: "Fini le stress des justificatifs manquants. Votre comptable reçoit tout, bien classé, sans relance.",
    quote: '"Je ne cherche plus jamais mes factures"'
  },
  {
    id: "tpe",
    icon: Building,
    title: "TPE & PME (2-50 personnes)",
    description: "Une méthode de classement que TOUTE l'équipe comprend. Fini les \"demande à Marie, c'est elle qui sait\".",
    quote: "Économisez 2 à 6 heures par mois en recherche de documents"
  },
  {
    id: "accountant",
    icon: Calculator,
    title: "Experts-Comptables",
    description: "Réconciliation automatique relevé bancaire ↔ justificatifs. Relances automatiques aux clients.",
    quote: "Module dédié en développement",
    comingSoon: true
  }
];

const UseCasesSection = () => {
  const [activeTab, setActiveTab] = useState("freelance");
  const activeCase = useCases.find(uc => uc.id === activeTab) || useCases[0];
  
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
            Conçu pour votre quotidien
          </h2>
        </motion.div>
        
        {/* Tabs */}
        <div className="flex flex-wrap justify-center gap-2 mb-10">
          {useCases.map((useCase) => (
            <button
              key={useCase.id}
              onClick={() => setActiveTab(useCase.id)}
              className={`flex items-center gap-2 px-5 py-3 rounded-xl text-sm font-medium transition-all ${
                activeTab === useCase.id
                  ? "bg-primary text-primary-foreground shadow-md"
                  : "bg-card text-muted-foreground hover:text-foreground border border-border hover:border-primary/30"
              }`}
            >
              <useCase.icon className="w-4 h-4" />
              <span className="hidden sm:inline">{useCase.title}</span>
              <span className="sm:hidden">{useCase.title.split(" ")[0]}</span>
              {useCase.comingSoon && (
                <span className="text-xs px-2 py-0.5 bg-warning/20 text-warning rounded-full">
                  Soon
                </span>
              )}
            </button>
          ))}
        </div>
        
        {/* Content */}
        <motion.div
          key={activeTab}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
          className="max-w-2xl mx-auto"
        >
          <div className="bg-card rounded-2xl border border-border p-8 md:p-10 text-center">
            <div className="w-16 h-16 mx-auto mb-6 rounded-2xl bg-primary/10 flex items-center justify-center">
              <activeCase.icon className="w-8 h-8 text-primary" />
            </div>
            <h3 className="text-xl font-bold text-foreground mb-4">{activeCase.title}</h3>
            <p className="text-muted-foreground mb-6">{activeCase.description}</p>
            <p className="text-sm italic text-accent font-medium">{activeCase.quote}</p>
          </div>
        </motion.div>
      </div>
    </section>
  );
};

export default UseCasesSection;
