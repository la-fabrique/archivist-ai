import { motion } from "framer-motion";
import { FileArchive } from "lucide-react";

const Header = () => {
  return (
    <motion.header
      initial={{ y: -20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="fixed top-0 left-0 right-0 z-50 glass-effect"
    >
      <div className="container-narrow">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center gap-2">
            <div className="w-9 h-9 rounded-lg bg-primary flex items-center justify-center">
              <FileArchive className="w-5 h-5 text-primary-foreground" />
            </div>
            <span className="font-semibold text-lg text-foreground">Archiviste IA</span>
          </div>
          
          <nav className="hidden md:flex items-center gap-8">
            <a href="#solution" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
              Solution
            </a>
            <a href="#integrations" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
              Intégrations
            </a>
            <a href="#faq" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
              FAQ
            </a>
          </nav>
          
          <a
            href="#waitlist"
            className="px-4 py-2 text-sm font-medium bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors"
          >
            Rejoindre
          </a>
        </div>
      </div>
    </motion.header>
  );
};

export default Header;
