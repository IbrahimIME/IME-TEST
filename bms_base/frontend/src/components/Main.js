import { Box } from "@mui/material";
import { styled } from "@mui/material/styles";

import { useTheme } from "../utils";

export const drawerWidth = 265;
export const drawerHeaderHeight = 50;

export const Main = styled("main")(({ theme, open }) => ({
	transition: theme.transitions.create("margin", {
		easing: theme.transitions.easing.sharp,
		duration: theme.transitions.duration.leavingScreen,
	}),
	marginLeft: `-${drawerWidth}px`,
	...(open && {
		transition: theme.transitions.create("margin", {
			easing: theme.transitions.easing.easeOut,
			duration: theme.transitions.duration.enteringScreen,
		}),
		marginLeft: 0,
	}),
	marginTop: drawerHeaderHeight,
	overflowX: "hidden",
	width: "100%",
}));

export const MainContainer = styled(Box)(({ theme }) => {
	const darkTheme = useTheme();

	return {
		backgroundColor: darkTheme ? "#262525" : "#f1f3f9",
		padding: theme.spacing(2),
		height: `calc(100vh - ${drawerHeaderHeight}px)`,
		width: "100%",
		overflow: "auto",
	};
});

export const DrawerHeader = styled("div")(({ theme }) => ({
	display: "flex",
	alignItems: "center",
	padding: theme.spacing(0, 1),
	minHeight: drawerHeaderHeight,
	justifyContent: "space-between",
}));
