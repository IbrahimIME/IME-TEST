import { Stack } from "@mui/material";
import { Fragment } from "react";
import { useQuery } from "react-query";
import { Redirect, Route, useHistory } from "react-router-dom";

import auth from "./application/Login/auth";
import { LoadingSpinner } from "./components/common";
import { AccessControl } from "./endpoints/BAS_CMM";
import i18n from "./i18n";
import { Api, Cookies } from "./utils";

export const ProtectedRoute = ({ component: Component, ...rest }) => {
	const { location } = useHistory();

	const Authorization = async () => {
		if (Cookies.get("token")) {
			await auth.authorize();

			if (auth.isExpired()) {
				auth.logout();
				rest.showSnackbarMessage("warning", i18n.t("session_expired"));
				return false;
			}
			return auth.isAuthorized();
		}

		return false;
	};

	const Allowed_App = async () => {
		if (location.pathname === "/" || location.pathname === "/home" || location.pathname === "/profile") return true;

		if (location.pathname !== "/" && location.pathname !== "/home" && location.pathname !== "/profile" && Cookies.get("Role_ID")) {
			const result = await Api.get({ url: AccessControl.get_all_features_access(Cookies.get("Role_ID")) });

			if (!result || result.error) return false;

			for (const row of result) {
				if (location.pathname === "/" + row.App_Trigram || location.pathname.includes(row.App_Trigram + "/" + row.Feature_Trigram)) {
					if (row.Read) return true;
				}
			}
		}

		return false;
	};

	const isAuth = useQuery("authorization", Authorization, { retry: 0 });
	const isAllowed = useQuery("access_control", Allowed_App, { retry: 0 });

	return (
		<Fragment>
			{(isAuth.status === "loading" || isAllowed.status === "loading") && (
				<Stack direction="column" alignItems="center" justifyContent="center" spacing={1} sx={{ height: "100%", flexGrow: 1 }}>
					<LoadingSpinner size={50} text={false} />
				</Stack>
			)}
			{(isAuth.status === "error" || isAllowed.status === "error") && (
				<Route
					{...rest}
					render={(props) => {
						return <Redirect to={{ pathname: "/", state: { from: props.location } }} />;
					}}
				/>
			)}
			{isAuth.status === "success" && isAllowed.status === "success" && (
				<Route
					{...rest}
					render={(props) => {
						if (isAuth.data && isAllowed.data) {
							return <Component {...props} {...rest} />;
						} else if (isAuth.data && !isAllowed.data) {
							window.location.pathname = "/imebms/home";
						} else if (!isAuth.data) {
							return <Redirect to={{ pathname: "/", state: { from: props.location } }} />;
						}
					}}
				/>
			)}
		</Fragment>
	);
};
