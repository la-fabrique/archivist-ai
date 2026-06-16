import { motion } from "framer-motion";
import { Github, ExternalLink, Lock, BookOpen, Users } from "lucide-react";
import { siteConfig } from "@/config/site";

const openSourcePoints = [
  {
    icon: Lock,
    text: "Licence Apache 2.0 — libre d'utilisation, même commerciale"
  },
  {
    icon: BookOpen,
    text: "Référentiel ouvert — les règles sont lisibles, pas une boîte noire"
  },
  {
    icon: Github,
    text: "Code source public — auditable, forkable, auto-hébergeable"
  },
  {
    icon: Users,
    text: "Pour toujours — pas de bait-and-switch, pas de relicensing"
  }
];

const WaitlistSection = () => {
  return (
    <section id="open-source" className="py-16 md:py-24 bg-gradient-to-b from-secondary/30 to-primary/5">
      <div className="container-narrow">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="text-center mb-12"
        >
          <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4">
            Open source. Pour toujours.
          </h2>
          <p className="text-muted-foreground max-w-xl mx-auto">
            La CLI Archivist et son référentiel sont et resteront open source. Vous pouvez les utiliser, les modifier, les héberger — sans demander la permission.
          </p>
        </motion.div>

        <div className="grid lg:grid-cols-2 gap-12 items-center max-w-4xl mx-auto">
          {/* Open source points */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1, duration: 0.5 }}
            className="space-y-4"
          >
            {openSourcePoints.map((point, index) => (
              <div
                key={index}
                className="flex items-start gap-4 p-4 bg-card rounded-xl border border-border"
              >
                <div className="w-8 h-8 rounded-lg bg-accent/10 flex items-center justify-center flex-shrink-0">
                  <point.icon className="w-4 h-4 text-accent" />
                </div>
                <p className="text-sm text-foreground">{point.text}</p>
              </div>
            ))}

            <a
              href={siteConfig.github}
              target="_blank"
              rel="noopener noreferrer"
              className="mt-2 w-full flex items-center justify-center gap-2 px-6 py-3 bg-foreground text-background font-semibold rounded-xl hover:bg-foreground/90 transition-all shadow"
            >
              <Github className="w-5 h-5" />
              Accéder au dépôt GitHub
            </a>
          </motion.div>

          {/* Deka CTA */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2, duration: 0.5 }}
          >
            <div className="bg-card rounded-2xl border border-border p-8 shadow-lg text-center">
              <div className="w-14 h-14 mx-auto mb-5 rounded-2xl bg-primary/10 flex items-center justify-center">
                <Users className="w-7 h-7 text-primary" />
              </div>
              <h3 className="text-xl font-bold text-foreground mb-3">
                Besoin d'accompagnement ?
              </h3>
              <p className="text-muted-foreground text-sm mb-6 leading-relaxed">
                Intégration dans votre agent, support entreprise, déploiement cloud, formation — pour les équipes qui préfèrent déléguer.
              </p>
              <a
                href={siteConfig.dekaUrl}
                target="_blank"
                rel="noopener noreferrer"
                data-gtm-event="cta_deka_main"
                className="inline-flex items-center gap-2 px-6 py-3 bg-primary text-primary-foreground font-semibold rounded-xl hover:bg-primary/90 transition-all shadow hover:shadow-md"
              >
                En savoir plus
                <ExternalLink className="w-4 h-4" />
              </a>
              <p className="text-xs text-muted-foreground mt-4">
                Contactez-nous pour discuter de votre projet
              </p>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
};

export default WaitlistSection;
