import i18n from "i18next";
import LanguageDetector from "i18next-browser-languagedetector";
import HttpApi from "i18next-http-backend";
import { initReactI18next } from "react-i18next";

i18n.use(LanguageDetector)
	.use(HttpApi)
	.use(initReactI18next)
	.init({
		ns: [
			"common",
			"Login",
			"BAS",
			"BAS_PNO",
			"BAS_MAS",
			"BAS_CMM",
			"BAS_SYS",
			"DCM",
			"DCM_DAM",
			"SND",
			"SND_QTN",
			"SND_SOR",
			"SND_DOR",
			"SND_INV",
			"SND_PFI",
			"SND_DNO",
			"SND_CNO",
			"FIN",
			"FIN_DNO",
			"FIN_CMT",
		],
		supportedLngs: ["en", "zh", "hi"],
		detection: {
			order: ["navigator", "cookie", "localStorage", "querystring", "sessionStorage", "htmlTag", "path", "subdomain"],
			caches: ["cookie", "localStorage"],
		},
		fallbackLng: "en",
		backend: {
			loadPath: "assets/locales/{{lng}}/{{ns}}.json",
		},
		// react: { useSuspense: false },
	});

export default i18n;
