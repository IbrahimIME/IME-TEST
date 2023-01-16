import {
	Avatar,
	Box,
	Divider,
	Drawer,
	IconButton,
	List,
	ListItem,
	ListItemButton,
	ListItemText,
	Stack,
	Tooltip,
	Typography,
	Zoom,
} from "@mui/material";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { Auth } from "../../endpoints";
import { AccessControl } from "../../endpoints/BAS_CMM";
import i18n from "../../i18n";
import { Api, Cookies, useTheme, useThemeUpdate } from "../../utils";
import { LoadingSpinner, MuiButton } from "../common";
import { ChevronLeftIcon, ChevronRightIcon, CloseIcon, DarkModeIcon, LightModeIcon, LogoutIcon, MailIcon, PhoneIcon } from "../Icon";

function UserPanel(props) {
	const darkTheme = useTheme();
	const toggleTheme = useThemeUpdate();

	const style = {
		ListItem: { px: 1, py: 0 },
		ListItemText: {
			span: {
				height: "20px",
				lineHeight: "20px",
				whiteSpace: "nowrap",
				textOverflow: "ellipsis",
				overflow: "hidden",
				width: "200px",
			},
		},
	};
	const [orgList, setOrgList] = useState([]);
	const [isLoadingOrgList, setIsLoadingOrgList] = useState(true);

	const updateUITheme = () => {
		Api.patch({ url: Auth.change_ui_theme() }).then((result) => {
			if (result.error) console.log(result);
		});
	};

	useEffect(() => {
		async function fetchData() {
			await Api.get({ url: AccessControl.get_org_list(Cookies.get("User_ID")) }).then((result) => {
				if (result.error) {
					console.log(result);
					setIsLoadingOrgList(false);
					return;
				}

				setOrgList(result);
				setIsLoadingOrgList(false);
			});
		}

		fetchData();

		return () => {
			setOrgList([]);
			setIsLoadingOrgList(true);
		};
	}, []);

	return (
		<Drawer anchor="right" open={props.show} onClose={props.handleOpenUserPanel} sx={{ zIndex: (theme) => theme.zIndex.drawer + 2 }}>
			<div id="user_panel" style={{ padding: "1rem 2rem" }}>
				<Stack direction="row" alignItems="center" justifyContent="space-between">
					<Typography variant="h6">
						{i18n.t("welcome")}, {Cookies.get("User_First_Name")} {Cookies.get("User_Last_Name")}
					</Typography>
					<IconButton onClick={props.handleOpenUserPanel}>
						<CloseIcon />
					</IconButton>
				</Stack>
				<div className="pr-5 me-n5">
					<Stack direction="row" spacing={2} className="d-flex align-items-center mt-3">
						<Tooltip title={i18n.t("view_profile")} TransitionComponent={Zoom} arrow>
							<Link to="/profile" onClick={props.handleOpenUserPanel}>
								<Avatar
									alt="profile-image"
									src={
										props.UserProfile.adm_usr_master && props.UserProfile.adm_usr_master.Profile_Image
											? props.UserProfile.adm_usr_master.Profile_Image
											: "assets/media/users/default_profile.png"
									}
									sx={{ width: 100, height: 100 }}
									className="profile-image"
								/>
							</Link>
						</Tooltip>
						<Stack direction="column" spacing={1} className="w-100">
							<List>
								<ListItem sx={style.ListItem}>
									<Tooltip title={Cookies.get("User_Email")} TransitionComponent={Zoom} arrow>
										<ListItemText sx={style.ListItemText}>
											<MailIcon sx={{ mr: 1 }} />
											{Cookies.get("User_Email")}
										</ListItemText>
									</Tooltip>
								</ListItem>
								<ListItem sx={style.ListItem}>
									<Tooltip title={Cookies.get("Mobile_No")} TransitionComponent={Zoom} arrow>
										<ListItemText sx={style.ListItemText}>
											<PhoneIcon sx={{ mr: 1 }} />
											{Cookies.get("Mobile_No")}
										</ListItemText>
									</Tooltip>
								</ListItem>
							</List>
							<Stack direction="row" className="justify-content-between">
								<MuiButton
									tooltip={i18n.t("logout")}
									variant="contained"
									onClick={props.handleLogout}
									content={<LogoutIcon />}
									spanStyle={{ width: "50%" }}
									buttonStyle={{ width: "100%", ":hover": { color: "#ffffff", backgroundColor: "#ff0000" } }}
								/>
								<MuiButton
									tooltip={darkTheme ? "Light Mode" : "Dark Mode"}
									mode="icon"
									content={darkTheme ? <LightModeIcon /> : <DarkModeIcon />}
									onClick={() => {
										toggleTheme();
										updateUITheme();
									}}
								/>
							</Stack>
						</Stack>
					</Stack>
					<Divider sx={{ border: 1, mt: 2, mb: 1 }} />
					{isLoadingOrgList && <LoadingSpinner className="text-center" />}
					{!isLoadingOrgList && orgList.error && <div className="text-center">{orgList.error}</div>}
					{!isLoadingOrgList && !orgList.error && orgList && (
						<Box>
							<List>
								{orgList.map((company, index) => (
									<ListItemButton
										key={index}
										className={company.Org_ID === Cookies.get("Org_ID") ? "rounded px-3 org selected" : "rounded px-3 org"}
										sx={{
											border:
												company.Org_ID === Cookies.get("Org_ID")
													? darkTheme
														? "1px solid #f3f3f3"
														: "1px solid #e0e0e0"
													: "",
											padding: "0 5px",
										}}
										onClick={() => {
											props.switchOrg(company.Org_ID, company.Org_Code, company.Role_ID);
											props.handleOpenUserPanel();
										}}
									>
										{company.Org_ID === Cookies.get("Org_ID") ? <ChevronRightIcon /> : ""}
										<ListItemText
											primary={`${company.Org_Name}`}
											secondary={`(${company.Role_Name})`}
											primaryTypographyProps={{
												style: {
													fontSize: company.Org_ID === Cookies.get("Org_ID") ? "1.1rem" : "1rem",
													fontWeight: company.Org_ID === Cookies.get("Org_ID") ? "bold" : "normal",
												},
											}}
											secondaryTypographyProps={{
												style: { fontSize: "13px", fontStyle: "italic" },
											}}
											sx={{ textAlign: "center" }}
										/>
										{company.Org_ID === Cookies.get("Org_ID") ? <ChevronLeftIcon /> : ""}
									</ListItemButton>
								))}
							</List>
						</Box>
					)}
					<Divider sx={{ border: 1, mt: 1, mb: 2 }} />
				</div>
			</div>
		</Drawer>
	);
}

export default UserPanel;
