import { Box, Stack, Typography } from "@mui/material";
import { useEffect } from "react";

import { MuiButton } from "./components/common";
import { HomeIcon } from "./components/Icon";
import i18n from "./i18n";
import { useTheme } from "./utils";

function PageNotFound(props) {
	const darkTheme = useTheme();

	useEffect(() => {
		props.getFeatureList("");
	}, [props]);

	return (
		<Box sx={{ display: "flex", alignItems: "center", justifyContent: "center", minWidth: "100%", height: "80vh" }}>
			<Stack direction="column" justifyContent="center" alignItems="center" spacing={3}>
				<img src="assets/media/logos/logo-light.png" alt="" style={{ maxHeight: "150px" }} />
				<Typography variant="h4" sx={{ color: darkTheme ? "#ffffff" : "#000000" }}>
					{i18n.t("page_not_found")}
				</Typography>
				<MuiButton
					variant="contained"
					size="large"
					startIcon={<HomeIcon />}
					onClick={() => {
						props.history.push("/home");
					}}
					content={i18n.t("back_to_home")}
				/>
			</Stack>
		</Box>
	);
}

export default PageNotFound;
