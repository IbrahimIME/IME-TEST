import { Box, Collapse, Drawer, List, ListItemButton, ListItemText, ListSubheader, Toolbar, Tooltip } from "@mui/material";
import { Fragment, useState } from "react";
import { NavLink, useHistory } from "react-router-dom";

import i18n from "../i18n";
import { useTheme } from "../utils";
import { drawerWidth } from "./";
import { ExpandLessIcon, ExpandMoreIcon } from "./Icon";

function SideMenu(props) {
	const history = useHistory();
	const darkTheme = useTheme();

	const [bool, setBool] = useState(true);
	const [expandMenu, setExpandMenu] = useState([]);

	const expandSubMenu = (menu) => {
		let temp = expandMenu;

		if (expandMenu.find((option) => option === menu)) {
			for (var i = 0; i < temp.length; i++) {
				if (temp[i] === menu) {
					temp.splice(i, 1);
					setExpandMenu(temp);
				}
			}
		} else {
			temp.push(menu);
			setExpandMenu(temp);
		}

		setBool(!bool);
	};

	return (
		<Drawer
			sx={{
				width: drawerWidth,
				flexShrink: 0,
				"& .MuiDrawer-paper": {
					width: drawerWidth,
					boxSizing: "border-box",
				},
				"& a": { textDecoration: "none" },
			}}
			variant="persistent"
			anchor="left"
			open={props.openSideMenu}
		>
			<Toolbar variant="dense" sx={{ mt: "5px" }} />
			<Box sx={{ backgroundColor: darkTheme ? "#363640" : "#fffff", overflow: "auto", height: "100%" }}>
				<List sx={{ height: "100%" }}>
					{props.featureList &&
						props.featureList.map((feature, feature_index) => (
							<Fragment key={feature_index}>
								{feature.Read && (
									<Fragment>
										<ListSubheader
											key={feature.Feature_Trigram}
											variant="h6"
											sx={{
												backgroundColor: darkTheme ? "#363640" : "#ffffff",
												color: "#6c6e8f",
												fontSize: "1rem",
												height: "40px",
												textTransform: "uppercase",
											}}
										>
											{i18n.t(feature.Feature_Name, { ns: feature.App_Trigram })}
										</ListSubheader>
										{props.menuItems.length > 0 &&
											props.menuItems.map((item, index) => (
												<Fragment key={index}>
													{item.FeatureCategory === feature.Feature_Trigram && !item.Sub_Menu && (
														<NavLink
															to={`${props.path}/${feature.Feature_Trigram}/${item.Value}`}
															style={{ color: darkTheme ? "#bdbdbd" : "#020307" }}
															activeStyle={{ color: "#ffffff", backgroundColor: "#1e1e2d" }}
															onClick={() => setExpandMenu([])}
														>
															<ListItemButton
																sx={{
																	backgroundColor: "inherit",
																	color: "inherit",
																	height: "44px",
																	paddingLeft: "25px",
																	":hover": {
																		color: "#ffffff",
																		backgroundColor: darkTheme ? "#3e3e4d" : "#4e4e7d",
																	},
																}}
															>
																{i18n.t(item.Name, { ns: item.FeatureCategory })}
															</ListItemButton>
														</NavLink>
													)}
													{item.FeatureCategory === feature.Feature_Trigram && item.Sub_Menu && (
														<>
															<ListItemButton
																sx={{
																	color: darkTheme ? "#bdbdbd" : "#020307",
																	height: "44px",
																	paddingLeft: "25px",
																	":hover": {
																		color: "#ffffff",
																		backgroundColor: darkTheme ? "#3e3e4d" : "#4e4e7d",
																	},
																}}
																onClick={() => expandSubMenu(feature.Feature_Trigram + "/" + item.Name)}
															>
																<ListItemText>{i18n.t(item.Name, { ns: item.FeatureCategory })}</ListItemText>
																{(expandMenu.find((option) => option === feature.Feature_Trigram + "/" + item.Name)
																	? true
																	: false) ||
																history.location.pathname.includes(feature.Feature_Trigram + "/" + item.Name) ? (
																	<Tooltip title={i18n.t("show_less")}>
																		<ExpandLessIcon />
																	</Tooltip>
																) : (
																	<Tooltip title={i18n.t("show_more")}>
																		<ExpandMoreIcon />
																	</Tooltip>
																)}
															</ListItemButton>
															<Collapse
																in={
																	(expandMenu.find((option) => option === feature.Feature_Trigram + "/" + item.Name)
																		? true
																		: false) ||
																	history.location.pathname.includes(feature.Feature_Trigram + "/" + item.Name)
																}
															>
																<List component="div" disablePadding>
																	{item.Sub_Menu.map((sub_item, sub_item_index) => (
																		<NavLink
																			key={sub_item_index}
																			to={`${props.path}/${feature.Feature_Trigram}/${item.Name}/${sub_item.Name}`}
																			style={{ color: darkTheme ? "#bdbdbd" : "#020307" }}
																			activeStyle={{ color: "#ffffff", backgroundColor: "#1e1e2d" }}
																			onClick={() => setExpandMenu([])}
																		>
																			<ListItemButton
																				sx={{
																					backgroundColor: "inherit",
																					color: "inherit",
																					height: "44px",
																					paddingLeft: "40px",
																					":hover": {
																						color: "#ffffff",
																						backgroundColor: darkTheme ? "#3e3e4d" : "#4e4e7d",
																					},
																				}}
																			>
																				{i18n.t(sub_item.Name, { ns: item.FeatureCategory })}
																			</ListItemButton>
																		</NavLink>
																	))}
																</List>
															</Collapse>
														</>
													)}
												</Fragment>
											))}
									</Fragment>
								)}
							</Fragment>
						))}
				</List>
			</Box>
		</Drawer>
	);
}

export default SideMenu;
