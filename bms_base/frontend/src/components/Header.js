import { AppBar, Avatar, Badge, IconButton, Stack, Toolbar, Tooltip, Typography, Zoom } from "@mui/material";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import auth from "../application/Login/auth";
import { Company } from "../endpoints/BAS_PNO";
import i18n from "../i18n";
import { Api, Cookies, useTheme } from "../utils";
import { MuiButton } from "./common";
import Application from "./header/application";
import Notification from "./header/notification";
import Search from "./header/search";
import UserPanel from "./header/user_panel";
import { AppsIcon, ChevronLeftIcon, HomeIcon, MenuIcon, NotificationsActiveIcon, NotificationsNoneIcon, SearchIcon } from "./Icon";

const logo = "assets/media/logos/logo-light.png";

const logoStyles = {
	maxHeight: 40,
	marginRight: 16,
};

const headerIconStyle = { fontSize: 25 };

function Header(props) {
	const notifications = [
		{
			message: "TESTING TESTING TESTING TESTING TESTING TESTING TESTING TESTING TESTING TESTING",
			url: "",
		},
		{ message: "Go to Companies", url: "/BAS/BAS_PNO/companies" },
		{ message: "Go to People", url: "/BAS/BAS_PNO/people" },
		{ message: "Go to Item Master", url: "/BAS/BAS_MAS/item/master" },
		{ message: "Go to Customers", url: "/BAS/BAS_MAS/customers" },
		{ message: "Go to Suppliers", url: "/BAS/BAS_MAS/suppliers" },
		{ message: "Notification 1", url: "" },
		{ message: "Notification 2", url: "" },
		{ message: "Notification 3", url: "" },
		{ message: "Notification 4", url: "" },
		{ message: "Notification 5", url: "" },
		{ message: "Notification 6", url: "" },
		{ message: "Notification 7", url: "" },
		{ message: "Notification 8", url: "" },
		{ message: "Notification 9", url: "" },
		{ message: "Notification 10", url: "" },
	];

	const darkTheme = useTheme();

	const [orgID, setOrgID] = useState(Cookies.get("Org_ID"));
	const [anchorEl, setAnchorEl] = useState(null);
	const [showSearch, setShowSearch] = useState(false);
	const [showNotification, setShowNotification] = useState(false);
	const [showApplication, setShowApplication] = useState(false);
	const [showUserPanel, setShowUserPanel] = useState(false);

	const handleClosePopover = () => {
		setAnchorEl(null);
		setShowSearch(false);
		setShowNotification(false);
		setShowApplication(false);
	};

	const handleOpenPopover = (e, open) => {
		setAnchorEl(e.currentTarget);
		setShowSearch(open === "search" ? true : false);
		setShowNotification(open === "notification" ? true : false);
		setShowApplication(open === "application" ? true : false);
	};

	const handleOpenUserPanel = () => {
		setShowSearch(false);
		setShowNotification(false);
		setShowApplication(false);
		setShowUserPanel((prevShowUserPanel) => !prevShowUserPanel);
	};

	const handleLogout = async () => {
		await auth.logout();
		props.history.push("/");
		props.showSnackbarMessage("success", i18n.t("logout_successful"));
	};

	const switchOrg = (Org_ID, Org_Code, Role_ID) => {
		Cookies.set("Org_ID", Org_ID);
		Cookies.set("Org_Code", Org_Code);
		Cookies.set("Role_ID", Role_ID);
		setOrgID(Org_ID);
		props.history.push("/");
	};

	useEffect(() => {
		Api.get({ url: Company.read_single_org(orgID) }).then((result) => {
			if (result.error) {
				console.log(result);
				return;
			}

			Cookies.set("PrimaryColor", result.Org_Color_Primary);
			Cookies.set("SecondaryColor", result.Org_Color_Secondary);
		});
	}, [orgID]);

	return (
		<AppBar position="fixed" color="inherit" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
			<Toolbar variant="dense">
				<Tooltip title={props.openSideMenu ? i18n.t("hide_menu") : i18n.t("show_menu")} TransitionComponent={Zoom} arrow>
					<IconButton
						color="inherit"
						aria-label="open drawer"
						onClick={props.openSideMenu ? props.handleCloseSideMenu : props.handleOpenSideMenu}
						edge="start"
						sx={{ mr: 2 }}
					>
						{props.openSideMenu ? <ChevronLeftIcon /> : <MenuIcon />}
					</IconButton>
				</Tooltip>
				<Link to="/home" className="brand-logo d-xs-none d-md-block">
					<img src={logo} style={logoStyles} alt="" />
				</Link>
				<Typography variant="h6" component="h6" noWrap sx={{ flexGrow: 1 }}>
					{props.headerTitle}
				</Typography>
				<Tooltip title={i18n.t("home")} TransitionComponent={Zoom}>
					<Link to="/home" className="topbar-item">
						<IconButton sx={{ color: "#adadad", ":hover": { color: darkTheme ? "#ffffff" : "#000000" } }}>
							<HomeIcon sx={headerIconStyle} />
						</IconButton>
					</Link>
				</Tooltip>
				<Tooltip title={i18n.t("search")} TransitionComponent={Zoom}>
					<div className="topbar-item" onClick={(e) => handleOpenPopover(e, "search")}>
						<IconButton
							sx={{
								color: showSearch ? (darkTheme ? "#ffffff" : "#000000") : "#adadad",
								":hover": { color: darkTheme ? "#ffffff" : "#000000" },
							}}
						>
							<SearchIcon sx={headerIconStyle} />
						</IconButton>
					</div>
				</Tooltip>
				<Search show={showSearch} anchorEl={anchorEl} handleClosePopover={handleClosePopover} />
				<Tooltip title={i18n.t("notifications")} TransitionComponent={Zoom}>
					<div className="topbar-item" onClick={(e) => handleOpenPopover(e, "notification")}>
						<IconButton
							sx={{
								color: showNotification ? (darkTheme ? "#ffffff" : "#000000") : "#adadad",
								":hover": { color: darkTheme ? "#ffffff" : "#000000" },
							}}
						>
							<Badge color="primary" variant="dot" invisible={notifications.length === 0}>
								{notifications.length === 0 && <NotificationsNoneIcon sx={headerIconStyle} />}
								{notifications.length > 0 && <NotificationsActiveIcon sx={headerIconStyle} />}
							</Badge>
						</IconButton>
					</div>
				</Tooltip>
				<Notification
					show={showNotification}
					anchorEl={anchorEl}
					history={props.history}
					notifications={notifications}
					handleClosePopover={handleClosePopover}
				/>
				<Tooltip title={i18n.t("applications")} TransitionComponent={Zoom}>
					<div className="topbar-item" onClick={(e) => handleOpenPopover(e, "application")}>
						<IconButton
							sx={{
								color: showApplication ? (darkTheme ? "#ffffff" : "#000000") : "#adadad",
								":hover": { color: darkTheme ? "#ffffff" : "#000000" },
							}}
						>
							<AppsIcon sx={headerIconStyle} />
						</IconButton>
					</div>
				</Tooltip>
				<Application show={showApplication} anchorEl={anchorEl} history={props.history} handleClosePopover={handleClosePopover} />
				<div className="user-panel topbar-item">
					<MuiButton
						onClick={handleOpenUserPanel}
						buttonStyle={{
							fontSize: "1rem",
							lineHeight: 1.5,
							padding: "6px!important",
							textTransform: "none",
							color: darkTheme ? "#adadad" : "#6c757d",
							":hover": { color: darkTheme ? "#ffffff" : "#000000", backgroundColor: darkTheme ? "default" : "#f5f5f5" },
						}}
						content={
							<>
								<Stack
									direction="column"
									spacing={0}
									className="fw-normal d-none d-md-flex me-3"
									sx={{ color: showUserPanel ? (darkTheme ? "#ffffff" : "#000000") : "inherit" }}
								>
									<span>{Cookies.get("Preferred_Name")}</span>
									<span>{Cookies.get("Org_Code")}</span>
								</Stack>
								<Avatar
									alt="profile-image"
									src={
										props.UserProfile.adm_usr_master?.Profile_Image
											? props.UserProfile.adm_usr_master.Profile_Image
											: "assets/media/users/default_profile.png"
									}
									sx={{ width: 35, height: 35 }}
								/>
							</>
						}
					/>
				</div>
			</Toolbar>
			<UserPanel
				show={showUserPanel}
				handleOpenUserPanel={handleOpenUserPanel}
				UserProfile={props.UserProfile}
				switchOrg={switchOrg}
				handleLogout={handleLogout}
			/>
		</AppBar>
	);
}

export default Header;
