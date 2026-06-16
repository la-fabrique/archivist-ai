import { motion } from "framer-motion";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";

const faqs = [
  {
    question: "C'est quoi le référentiel ?",
    answer: "Un corpus de règles d'archivage professionnel — plan de classement, conventions de nommage, durées de conservation légales — adapté au droit fiscal français (TVA, URSSAF, CFE…). Ces règles sont lisibles, documentées, co-construites avec des experts. Votre agent IA les applique fidèlement."
  },
  {
    question: "Le code est-il open source ?",
    answer: "Oui. Archivist et son référentiel sont publiés sous licence Apache 2.0 sur GitHub. Vous pouvez lire le code, contribuer, et l'héberger vous-même. Une offre avec support dédié et accompagnement est prévue pour les organisations qui préfèrent déléguer."
  },
  {
    question: "Comment mon agent IA utilise Archivist ?",
    answer: "Archivist est conçu pour être appelé comme un outil par un agent IA. Votre LLM — Claude, ChatGPT, Copilot ou autre — appelle Archivist pour créer une arborescence, classer un document, ou traiter un dossier entier, sans que vous ayez à ouvrir un terminal."
  },
  {
    question: "Est-ce que mes fichiers quittent mon ordinateur ?",
    answer: "Non. Archivist tourne localement sur votre machine ou votre serveur. Vos fichiers ne sont jamais envoyés à un service externe. Seul le contenu textuel extrait d'un document peut transiter vers le LLM pour la classification."
  },
  {
    question: "Est-ce que l'agent peut se tromper ?",
    answer: "Oui — et c'est pour ça qu'Archivist intègre une validation humaine. Pour les classements évidents, il agit. Pour les cas ambigus, il vous soumet une proposition avant d'agir. Aucune suppression n'est jamais possible."
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
