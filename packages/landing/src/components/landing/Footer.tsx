import { FileArchive, Github, Linkedin, Twitter } from "lucide-react";
import { siteConfig } from "@/config/site";

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
              <span className="font-semibold text-foreground">Archivist AI</span>
            </div>
            <p className="text-sm text-muted-foreground">
              Vos documents se rangent. Vous respirez.
            </p>
          </div>

          {/* Social links */}
          <div className="flex flex-col items-center gap-4">
            {siteConfig.email && (
              <a
                href={`mailto:${siteConfig.email}`}
                className="text-sm text-muted-foreground hover:text-foreground transition-colors"
              >
                {siteConfig.email}
              </a>
            )}
            <div className="flex items-center gap-4">
              <a
                href={siteConfig.github}
                target="_blank"
                rel="noopener noreferrer"
                className="w-9 h-9 rounded-lg bg-secondary flex items-center justify-center text-muted-foreground hover:text-foreground hover:bg-secondary/80 transition-colors"
                aria-label="GitHub — code source Apache 2.0"
              >
                <Github className="w-4 h-4" />
              </a>
              {siteConfig.linkedin && (
                <a
                  href={siteConfig.linkedin}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="w-9 h-9 rounded-lg bg-secondary flex items-center justify-center text-muted-foreground hover:text-foreground hover:bg-secondary/80 transition-colors"
                  aria-label="LinkedIn"
                >
                  <Linkedin className="w-4 h-4" />
                </a>
              )}
              {siteConfig.twitter && (
                <a
                  href={`https://twitter.com/${siteConfig.twitter}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="w-9 h-9 rounded-lg bg-secondary flex items-center justify-center text-muted-foreground hover:text-foreground hover:bg-secondary/80 transition-colors"
                  aria-label="Twitter / X"
                >
                  <Twitter className="w-4 h-4" />
                </a>
              )}
            </div>
          </div>

          {/* Legal */}
          <div className="text-center md:text-right">
            <p className="text-sm text-muted-foreground mb-2">
              © 2026 — Fait avec 🧠 et ❤️ en France
            </p>
            <a
              href={`${siteConfig.github}/blob/main/LICENCE.md`}
              target="_blank"
              rel="noopener noreferrer"
              className="text-xs text-muted-foreground hover:text-foreground transition-colors"
            >
              Licence Apache 2.0
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
