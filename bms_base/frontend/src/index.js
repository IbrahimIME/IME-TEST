import "bootstrap/dist/css/bootstrap.min.css";
import "react-app-polyfill/ie9";
import "react-app-polyfill/stable";
import "react-csv-importer/dist/index.css";
import "formiojs/dist/formio.full.min.css";

import { useEffect, useState } from "react";
import ReactDOM from "react-dom";
import { Helmet, HelmetProvider } from "react-helmet-async";
import { QueryClient, QueryClientProvider } from "react-query";
import { BrowserRouter, Route, Switch } from "react-router-dom";

import App from "./App";
import auth from "./application/Login/auth";
import Login from "./application/Login/Login";
import { SnackBar } from "./components/common";
import Demo from "./demo/demo";
import i18n from "./i18n";
import { Cookies, useTheme } from "./utils";

const queryClient = new QueryClient();

function Index() {
	const darkTheme = useTheme();
	const [isLoggedIn, setIsLoggedIn] = useState(false);
	const [openSideMenu, setOpenSideMenu] = useState(false);
	const [snackbar, setSnackbar] = useState({ open: false, type: "info", message: "" });

	const handleSetIsLoggedIn = () => {
		setIsLoggedIn(true);
	};

	const handleOpenSideMenu = () => {
		setOpenSideMenu(true);
	};

	const handleCloseSideMenu = () => {
		setOpenSideMenu(false);
	};

	const showSnackbarMessage = (type, message) => {
		setSnackbar({ ...snackbar, open: true, type, message });
	};

	const handleCloseSnackbar = () => {
		setSnackbar({ ...snackbar, open: false });
	};

	useEffect(() => {
		async function checkToken() {
			if (Cookies.get("token")) {
				await auth.authorize();

				if (auth.isAuthorized()) handleSetIsLoggedIn();
				else if (auth.isExpired() && window.location.pathname !== "/imebms") {
					setSnackbar((prevSnackbar) => ({ ...prevSnackbar, open: true, type: "warning", message: i18n.t("session_expired") }));
					window.location.pathname = "/imebms";
				} else {
					window.location.pathname = "/imebms";
				}
			} else if (window.location.pathname !== "/imebms" && window.location.pathname !== "/imebms/") {
				window.location.pathname = "/imebms";
			}
		}

		console.log("Your current browser language:", navigator.language);
		console.log("Your browser languages:", navigator.languages);
		console.log("Your User Agent:", navigator.userAgent);

		checkToken();
	}, []);

	return (
		<HelmetProvider>
			<Helmet>
				<title>IMEBMS</title>
			</Helmet>
			<BrowserRouter basename={"/imebms"}>
				<QueryClientProvider client={queryClient}>
					<SnackBar snackbar={snackbar} handleCloseSnackbar={handleCloseSnackbar} />
					<Switch>
						<Route
							exact
							path={`/`}
							render={(props) => (
								<Login {...props} handleSetIsLoggedIn={handleSetIsLoggedIn} showSnackbarMessage={showSnackbarMessage} />
							)}
						/>
						<Route exact path={`/vendor_registration`} render={(props) => <Demo {...props} />} />
						<Route
							path="*"
							render={(props) => (
								<App
									{...props}
									darkTheme={darkTheme}
									isLoggedIn={isLoggedIn}
									openSideMenu={openSideMenu}
									handleOpenSideMenu={handleOpenSideMenu}
									handleCloseSideMenu={handleCloseSideMenu}
									showSnackbarMessage={showSnackbarMessage}
								/>
							)}
						/>
					</Switch>
				</QueryClientProvider>
			</BrowserRouter>
		</HelmetProvider>
	);
}

const rootElement = document.getElementById("root");
ReactDOM.render(<Index />, rootElement);
