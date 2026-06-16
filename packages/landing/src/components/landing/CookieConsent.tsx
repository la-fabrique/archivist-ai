import { useState, useEffect } from "react";
import { siteConfig } from "@/config/site";

const STORAGE_KEY = "cookie-consent";

declare global {
  interface Window {
    dataLayer: Record<string, unknown>[];
  }
}

function loadGTM(id: string) {
  if (document.getElementById("gtm-script")) return;

  const script = document.createElement("script");
  script.id = "gtm-script";
  script.async = true;
  script.src = `https://www.googletagmanager.com/gtm.js?id=${id}`;
  document.head.appendChild(script);

  const noscript = document.createElement("noscript");
  noscript.innerHTML = `<iframe src="https://www.googletagmanager.com/ns.html?id=${id}" height="0" width="0" style="display:none;visibility:hidden"></iframe>`;
  document.body.insertBefore(noscript, document.body.firstChild);

  window.dataLayer = window.dataLayer || [];
  window.dataLayer.push({ "gtm.start": Date.now(), event: "gtm.js" });
}

export function CookieConsent() {
  const [visible, setVisible] = useState(() => {
    const stored = localStorage.getItem(STORAGE_KEY);
    return !stored;
  });

  useEffect(() => {
    if (localStorage.getItem(STORAGE_KEY) === "accepted") {
      loadGTM(siteConfig.gtmId);
    }
  }, []);

  function accept() {
    localStorage.setItem(STORAGE_KEY, "accepted");
    loadGTM(siteConfig.gtmId);
    setVisible(false);
  }

  function refuse() {
    localStorage.setItem(STORAGE_KEY, "refused");
    setVisible(false);
  }

  if (!visible) return null;

  return (
    <div className="fixed bottom-0 left-0 right-0 z-50 bg-white border-t border-gray-200 shadow-lg">
      <div className="max-w-5xl mx-auto px-6 py-4 flex flex-col sm:flex-row items-start sm:items-center gap-4">
        <p className="text-sm text-gray-600 flex-1">
          Ce site utilise des cookies de mesure d'audience pour comprendre comment vous utilisez la page.{" "}
          <br />
          <span className="text-gray-400">Conformément à la réglementation, votre consentement est requis.</span>
        </p>
        <div className="flex gap-3 shrink-0">
          <button
            onClick={refuse}
            className="px-4 py-2 text-sm text-gray-600 border border-gray-300 rounded-md hover:bg-gray-50 transition-colors"
          >
            Refuser
          </button>
          <button
            onClick={accept}
            className="px-4 py-2 text-sm text-white bg-gray-900 rounded-md hover:bg-gray-700 transition-colors"
          >
            Accepter
          </button>
        </div>
      </div>
    </div>
  );
}
