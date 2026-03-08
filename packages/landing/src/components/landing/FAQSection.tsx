import { motion } from "framer-motion";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";

const faqs = [
  {
    question: "Est-ce que l'archiviste peut supprimer mes documents ?",
    answer: "Non, jamais. L'archiviste range et organise uniquement. Aucune suppression n'est possible. Chaque action est tracée dans un historique consultable."
  },
  {
    question: "Dois-je changer ma façon de travailler ?",
    answer: "Non ! L'archiviste s'adapte à VOTRE méthode existante. Il apprend votre logique de classement et l'applique automatiquement."
  },
  {
    question: "Mes données sont-elles en sécurité ?",
    answer: "Vos fichiers restent sur VOS systèmes (Google Drive, Office 365, etc.). L'archiviste ne stocke rien. Données hébergées en Europe, conformité RGPD."
  },
  {
    question: "Et si l'archiviste se trompe ?",
    answer: "Pour les cas simples, il agit en autonomie. Pour les cas complexes ou risqués, il vous demande validation AVANT d'agir. Vous gardez toujours le contrôle."
  },
  {
    question: "Combien de temps pour configurer ?",
    answer: "5 minutes. Connectez vos outils, l'archiviste apprend vos habitudes au fil du temps. Zéro configuration complexe."
  }
];

const FAQSection = () => {
  return (
    <section id="faq" className="py-16 md:py-24">
      <div className="container-narrow">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="text-center mb-10"
        >
          <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4">
            Questions fréquentes
          </h2>
        </motion.div>
        
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.2, duration: 0.5 }}
          className="max-w-2xl mx-auto"
        >
          <Accordion type="single" collapsible className="space-y-4">
            {faqs.map((faq, index) => (
              <AccordionItem
                key={index}
                value={`item-${index}`}
                className="bg-card rounded-xl border border-border px-6 data-[state=open]:border-primary/30"
              >
                <AccordionTrigger className="text-left font-medium text-foreground hover:no-underline py-5">
                  {faq.question}
                </AccordionTrigger>
                <AccordionContent className="text-muted-foreground pb-5">
                  {faq.answer}
                </AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        </motion.div>
      </div>
    </section>
  );
};

export default FAQSection;
