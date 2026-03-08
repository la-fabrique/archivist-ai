import { FileArchive, Linkedin, Twitter } from "lucide-react";

const Footer = () => {
  return (
    <footer className="py-12 border-t border-border">
      <div className="container-narrow">
        <div className="flex flex-col md:flex-row items-center justify-between gap-8">
          {/* Logo and tagline */}
          <div className="text-center md:text-left">
            <div className="flex items-center justify-center md:justify-start gap-2 mb-2">
              <div className="w-8 h-8 rounded-lg bg-primary flex items-center justify-center">
                <FileArchive className="w-4 h-4 text-primary-foreground" />
              </div>
              <span className="font-semibold text-foreground">Archiviste IA</span>
            </div>
            <p className="text-sm text-muted-foreground">
              Vos documents se rangent. Vous respirez.
            </p>
          </div>
          
          {/* Contact */}
          <div className="flex flex-col items-center gap-4">
            <a
              href="mailto:contact@archiviste-ia.com"
              className="text-sm text-muted-foreground hover:text-foreground transition-colors"
            >
              📧 contact@archiviste-ia.com
            </a>
            <div className="flex items-center gap-4">
              <a
                href="#"
                className="w-9 h-9 rounded-lg bg-secondary flex items-center justify-center text-muted-foreground hover:text-foreground hover:bg-secondary/80 transition-colors"
                aria-label="LinkedIn"
              >
                <Linkedin className="w-4 h-4" />
              </a>
              <a
                href="#"
                className="w-9 h-9 rounded-lg bg-secondary flex items-center justify-center text-muted-foreground hover:text-foreground hover:bg-secondary/80 transition-colors"
                aria-label="Twitter"
              >
                <Twitter className="w-4 h-4" />
              </a>
            </div>
          </div>
          
          {/* Legal */}
          <div className="text-center md:text-right">
            <p className="text-sm text-muted-foreground mb-2">
              © 2026 — Fait avec 🧠 en France
            </p>
            <div className="flex items-center justify-center md:justify-end gap-4 text-xs text-muted-foreground">
              <a href="#" className="hover:text-foreground transition-colors">
                Mentions légales
              </a>
              <span>|</span>
              <a href="#" className="hover:text-foreground transition-colors">
                Politique de confidentialité
              </a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
