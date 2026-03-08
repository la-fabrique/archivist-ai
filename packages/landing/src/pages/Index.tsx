import Header from "@/components/landing/Header";
import HeroSection from "@/components/landing/HeroSection";
import PainPointsSection from "@/components/landing/PainPointsSection";
import SolutionSection from "@/components/landing/SolutionSection";
import IntegrationsSection from "@/components/landing/IntegrationsSection";
import TrustSection from "@/components/landing/TrustSection";
import UseCasesSection from "@/components/landing/UseCasesSection";
import FAQSection from "@/components/landing/FAQSection";
import WaitlistSection from "@/components/landing/WaitlistSection";
import Footer from "@/components/landing/Footer";

const Index = () => {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      <main>
        <HeroSection />
        <PainPointsSection />
        <SolutionSection />
        <IntegrationsSection />
        <TrustSection />
        <UseCasesSection />
        <FAQSection />
        <WaitlistSection />
      </main>
      <Footer />
    </div>
  );
};

export default Index;
