import { ThemeProvider as MuiThemeProvider, createTheme } from "@mui/material/styles";
import React, { useContext, useState } from "react";

import Cookies from "./Cookies";

// const Colors = {
// 	primary: { light: "#42a5f5", main: "#1976d2", dark: "#1565c0" },
// 	secondary: { light: "#ba68c8", main: "#9c27b0", dark: "#7b1fa2" },
// 	error: { light: "#ef5350", main: "#d32f2f", dark: "#c62828" },
// 	warning: { light: "#ff9800", main: "#ed6c02", dark: "#e65100" },
// 	info: { light: "#03a9f4", main: "#0288d1", dark: "#01579b" },
// 	success: { light: "#4caf50", main: "#2e7d32", dark: "#1b5e20" },
// };

export const ThemeContext = React.createContext();
export const ThemeUpdateContext = React.createContext();

export function useTheme() {
	return useContext(ThemeContext);
}

export function useThemeUpdate() {
	return useContext(ThemeUpdateContext);
}

export function ThemeProvider({ children }) {
	const darkDataGridCss = `https://cdn3.devexpress.com/jslib/${process.env.REACT_APP_DEVEXTREME_VERSION}/css/dx.material.blue.dark.compact.css`;
	const lightDataGridCss = `https://cdn3.devexpress.com/jslib/${process.env.REACT_APP_DEVEXTREME_VERSION}/css/dx.material.blue.light.compact.css`;

	const [darkTheme, setDarkTheme] = useState(Cookies.get("theme") === "dark" ? true : false);

	function toggleTheme() {
		setDarkTheme((prevDarkTheme) => {
			Cookies.set("theme", !prevDarkTheme ? "dark" : "light");
			return !prevDarkTheme;
		});
	}

	const theme = createTheme({
		palette: {
			mode: darkTheme ? "dark" : "light",
			background: { paper: darkTheme ? "#363640" : "#ffffff" },
		},
	});

	return (
		<ThemeContext.Provider value={darkTheme}>
			<ThemeUpdateContext.Provider value={toggleTheme}>
				<link rel="stylesheet" type="text/css" href={darkTheme ? darkDataGridCss : lightDataGridCss} />
				<MuiThemeProvider theme={theme}>{children}</MuiThemeProvider>
			</ThemeUpdateContext.Provider>
		</ThemeContext.Provider>
	);
}
