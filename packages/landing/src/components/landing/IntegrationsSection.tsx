import { motion } from "framer-motion";

const integrations = [
  { name: "Google Workspace", logo: "🔵" },
  { name: "Office 365", logo: "🟠" },
  { name: "Dropbox", logo: "🔷" },
  { name: "OneDrive", logo: "☁️" },
  { name: "Serveur Local", logo: "🖥️" },
  { name: "Votre Compta*", logo: "📊" }
];

const IntegrationsSection = () => {
  return (
    <section id="integrations" className="py-16 md:py-24 bg-secondary/30">
      <div className="container-narrow">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="text-center mb-10"
        >
          <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4">
            Se connecte à votre écosystème
          </h2>
        </motion.div>
        
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4 max-w-2xl mx-auto mb-8">
          {integrations.map((integration, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, scale: 0.9 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1, duration: 0.4 }}
              className="flex flex-col items-center gap-3 p-6 bg-card rounded-xl border border-border hover:border-primary/30 hover:shadow-md transition-all"
            >
              <span className="text-4xl">{integration.logo}</span>
              <span className="text-sm font-medium text-foreground text-center">{integration.name}</span>
            </motion.div>
          ))}
        </div>
        
        <motion.p
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ delay: 0.3, duration: 0.5 }}
          className="text-xs text-muted-foreground text-center mb-12"
        >
          *Intégrations comptables en développement
        </motion.p>
        
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.4, duration: 0.5 }}
          className="text-center max-w-xl mx-auto"
        >
          <p className="text-lg font-semibold text-foreground mb-2">
            Pas une nouvelle GED à apprendre.
          </p>
          <p className="text-muted-foreground">
            Un archiviste pour celle que vous avez déjà.
          </p>
        </motion.div>
      </div>
    </section>
  );
};

export default IntegrationsSection;
