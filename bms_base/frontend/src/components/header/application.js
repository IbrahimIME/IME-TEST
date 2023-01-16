import { Box, Card, CardActionArea, Grid, Popover, Stack, Tooltip, Typography } from "@mui/material";
import { useEffect, useState } from "react";

import { AccessControl } from "../../endpoints/BAS_CMM";
import i18n from "../../i18n";
import { Api, Cookies, useTheme } from "../../utils";
import { LoadingSpinner } from "../common";
import { BASIcon, DCMIcon, FINIcon, HRMIcon, INVIcon, PURIcon, QuestionMarkIcon, SNDIcon, SNMIcon } from "../Icon";

function Application(props) {
	const darkTheme = useTheme();

	const cardStyle = {
		boxShadow: "none",
		":hover": {
			boxShadow: "0px 2px 1px -1px rgb(0 0 0 / 20%), 0px 1px 1px 0px rgb(0 0 0 / 14%), 0px 1px 3px 0px rgb(0 0 0 / 12%)",
		},
	};
	const appIconStyle = {
		fontSize: 40,
		color: darkTheme ? "#ffffff" : Cookies.get("PrimaryColor"),
	};

	const [apps, setApps] = useState([]);
	const [isLoadingApps, setIsLoadingApps] = useState(true);

	const renderAppIcon = (App_Trigram) => {
		switch (App_Trigram) {
			case "BAS":
				return <BASIcon sx={appIconStyle} />;
			case "DCM":
				return <DCMIcon sx={appIconStyle} />;
			case "SND":
				return <SNDIcon sx={appIconStyle} />;
			case "FIN":
				return <FINIcon sx={appIconStyle} />;
			case "PUR":
				return <PURIcon sx={appIconStyle} />;
			case "INV":
				return <INVIcon sx={appIconStyle} />;
			case "HRM":
				return <HRMIcon sx={appIconStyle} />;
			case "SNM":
				return <SNMIcon sx={appIconStyle} />;
			default:
				return <QuestionMarkIcon sx={appIconStyle} />;
		}
	};

	useEffect(() => {
		Api.get({ url: AccessControl.get_all_applications_access(Cookies.get("Role_ID")) }).then((result) => {
			if (result.error) {
				console.log(result);
				setIsLoadingApps(false);
				return;
			}

			setApps(result);
			setIsLoadingApps(false);
		});
	}, [props]);

	return (
		<Popover
			open={props.show}
			onClose={props.handleClosePopover}
			anchorEl={props.anchorEl}
			anchorOrigin={{ vertical: "bottom", horizontal: "right" }}
			transformOrigin={{ vertical: "top", horizontal: "right" }}
			className="mx-5 mt-4"
		>
			<Box sx={{ maxWidth: "400px" }}>
				<Box sx={{ backgroundColor: Cookies.get("PrimaryColor"), display: "flex", justifyContent: "center", py: 1 }}>
					<Typography variant="h6" sx={{ color: "white" }}>
						{i18n.t("applications")}
					</Typography>
				</Box>
				<Grid container alignItems="center" spacing={1} sx={{ p: 1 }}>
					{isLoadingApps && (
						<Grid
							item
							xs={12}
							sx={{ display: "flex", alignItem: "center", justifyContent: "center", margin: "3vh 0", minWidth: "200px" }}
						>
							<LoadingSpinner />
						</Grid>
					)}
					{!isLoadingApps && apps.error && (
						<Grid item xs={12} sx={{ maxWidth: "110px" }}>
							<Card sx={cardStyle}>
								<CardActionArea sx={{ padding: 1, backgroundColor: "#262525" }} onClick={() => props.history.push(`/home`)}>
									<Typography variant="body1" sx={{ width: "95%", overflow: "hidden", textOverflow: "ellipsis" }}>
										{apps.error}
									</Typography>
								</CardActionArea>
							</Card>
						</Grid>
					)}
					{!isLoadingApps &&
						!apps.error &&
						apps.map(
							(app, index) =>
								app.Read && (
									<Grid item xs={6} sm={4} sx={{ minWidth: "110px" }} key={index}>
										<Card sx={cardStyle}>
											<CardActionArea
												sx={{ padding: 1, backgroundColor: "inherit" }}
												onClick={() => {
													props.handleClosePopover();
													props.history.push(`/${app.App_Trigram}`);
												}}
											>
												<Stack
													direction="column"
													justifyContent="center"
													alignItems="center"
													spacing={2}
													sx={{ textAlign: "center" }}
												>
													{renderAppIcon(app.App_Trigram)}
													<Tooltip title={app.App_Name}>
														<Typography
															variant="body1"
															sx={{ width: "97%", overflow: "hidden", textOverflow: "ellipsis" }}
														>
															{app.App_Name}
														</Typography>
													</Tooltip>
												</Stack>
											</CardActionArea>
										</Card>
									</Grid>
								)
						)}
				</Grid>
			</Box>
		</Popover>
	);
}

export default Application;
