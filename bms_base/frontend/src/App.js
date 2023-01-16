import { Box } from "@mui/material";
import { Component, Suspense } from "react";
import { Route, Switch } from "react-router-dom";

import Administration from "./application/BAS/Administration";
import DocumentManagement from "./application/DCM/DocumentManagement";
import Home from "./application/Home";
import Profile from "./application/Profile";
import { Header, Main, MainContainer, SideMenu } from "./components";
import { LoadingSpinner } from "./components/common";
import { AccessControl } from "./endpoints/BAS_CMM";
import { User } from "./endpoints/BAS_PNO";
import i18n from "./i18n";
import PageNotFound from "./page_not_found";
import { ProtectedRoute } from "./protected.route";
import { Api, Cookies, ThemeProvider } from "./utils";

// import SalesDistribution from "./application/SND/SalesDistribution";

class App extends Component {
	state = {
		headerTitle: "",
		path: "",
		UserProfile: {},
		updateUserProfile: false,
		featureList: [],
		menuItems: {},
	};

	updateHeaderTitle = (title, ns = "common") => {
		this.setState((prevState) => ({ ...prevState, headerTitle: i18n.t(title, { ns: ns }) }));
	};

	setPath = (path) => {
		this.setState((prevState) => ({ ...prevState, path }));
	};

	getFeatureList = async (App_Trigram) => {
		await Api.get({ url: AccessControl.get_all_features_access(Cookies.get("Role_ID")) }).then((result) => {
			if (result.error) {
				console.log(result);
				return;
			}

			let feature_list_array = [];

			for (const feature of result) {
				if (feature.App_Trigram === App_Trigram) {
					feature_list_array.push({
						App_Trigram: App_Trigram,
						Feature_ID: feature.Feature_ID,
						Feature_Name: feature.Feature_Name,
						Feature_Trigram: feature.Feature_Trigram,
						Create: feature.Create,
						Read: feature.Read,
						Update: feature.Update,
						Delete: feature.Delete,
						Approve: feature.Approve,
					});
				}
			}

			this.setState({ ...this.state, featureList: feature_list_array });
		});
	};

	getMenuItems = async () => {
		await Api.get({ url: AccessControl.get_menu_item() }).then((result) => {
			if (result.error) {
				console.log(result);
				return;
			}

			this.setState({ ...this.state, menuItems: result });
		});
	};

	setUpdateUserProfile = () => {
		this.setState({ ...this.state, updateUserProfile: !this.state.updateUserProfile });
	};

	getUserProfile = async () => {
		await Api.get({ url: User.read_single_user(Cookies.get("User_ID")) }).then((result) => {
			if (result.error) {
				console.log(result);
				return;
			}

			this.setState({ ...this.state, UserProfile: result, isLoadingUserProfile: false });
			Cookies.set("User_ID", result.adm_usr_master.User_ID);
			Cookies.set("User_First_Name", result.adm_usr_master.User_First_Name);
			Cookies.set("User_Last_Name", result.adm_usr_master.User_Last_Name);
			Cookies.set("Preferred_Name", result.adm_usr_master.Preferred_Name);
			Cookies.set("Mobile_No", result.adm_usr_master.Mobile_No);
		});
	};

	async componentDidMount() {
		if (window.innerWidth >= 992) this.props.handleOpenSideMenu();

		if (Cookies.get("User_ID") && Cookies.get("token")) {
			await Api.get({ url: User.read_single_user(Cookies.get("User_ID")) }).then((result) => {
				if (result.error) {
					console.log(result);
					return;
				}

				this.setState({ ...this.state, UserProfile: result, isLoadingUserProfile: false });
			});
		}
	}

	componentDidUpdate(prevProps, prevState) {
		if (prevProps.isLoggedIn !== this.props.isLoggedIn || prevState.updateUserProfile !== this.state.updateUserProfile) this.getUserProfile();
	}

	render() {
		return (
			<ThemeProvider>
				{this.props.isLoggedIn && (
					<Box sx={{ display: "flex", flexGrow: 1, overflow: "auto", height: "100%" }}>
						<Header
							openSideMenu={this.props.openSideMenu}
							handleOpenSideMenu={this.props.handleOpenSideMenu}
							handleCloseSideMenu={this.props.handleCloseSideMenu}
							history={this.props.history}
							headerTitle={this.state.headerTitle}
							UserProfile={this.state.UserProfile}
							showSnackbarMessage={this.props.showSnackbarMessage}
						/>
						<SideMenu
							openSideMenu={this.props.openSideMenu}
							handleCloseSideMenu={this.props.handleCloseSideMenu}
							path={this.state.path}
							featureList={this.state.featureList}
							menuItems={this.state.menuItems}
						/>
						<Main open={this.props.openSideMenu}>
							<MainContainer darktheme={this.props.darkTheme}>
								<Suspense fallback={<LoadingSpinner size={40} text={false} />}>
									<Switch>
										<ProtectedRoute
											path={`/home`}
											component={Home}
											setPath={this.setPath}
											updateHeaderTitle={this.updateHeaderTitle}
											getFeatureList={this.getFeatureList}
											getMenuItems={this.getMenuItems}
											showSnackbarMessage={this.props.showSnackbarMessage}
										/>
										<ProtectedRoute
											path={`/profile`}
											component={Profile}
											setUpdateUserProfile={this.setUpdateUserProfile}
											setPath={this.setPath}
											updateHeaderTitle={this.updateHeaderTitle}
											getFeatureList={this.getFeatureList}
											getMenuItems={this.getMenuItems}
											showSnackbarMessage={this.props.showSnackbarMessage}
										/>
										<ProtectedRoute
											path={`/BAS`}
											component={Administration}
											setPath={this.setPath}
											updateHeaderTitle={this.updateHeaderTitle}
											getFeatureList={this.getFeatureList}
											getMenuItems={this.getMenuItems}
											showSnackbarMessage={this.props.showSnackbarMessage}
										/>
										<ProtectedRoute
											path={`/DCM`}
											component={DocumentManagement}
											setPath={this.setPath}
											updateHeaderTitle={this.updateHeaderTitle}
											getFeatureList={this.getFeatureList}
											getMenuItems={this.getMenuItems}
											showSnackbarMessage={this.props.showSnackbarMessage}
										/>
										{/* <ProtectedRoute
											path={`/SND`}
											component={SalesDistribution}
											setPath={this.setPath}
											updateHeaderTitle={this.updateHeaderTitle}
											getFeatureList={this.getFeatureList}
											getMenuItems={this.getMenuItems}
											showSnackbarMessage={this.props.showSnackbarMessage}
										/> */}
										{/* <ProtectedRoute
											path={`/FIN`}
											component={Finance_Accounting}
											setPath={this.setPath}
											updateHeaderTitle={this.updateHeaderTitle}
											getFeatureList={this.getFeatureList}
											getMenuItems={this.getMenuItems}
											showSnackbarMessage={this.props.showSnackbarMessage}
										/> */}
										<Route path="*" render={(props) => <PageNotFound {...props} getFeatureList={this.getFeatureList} />} />
									</Switch>
								</Suspense>
							</MainContainer>
						</Main>
					</Box>
				)}
			</ThemeProvider>
		);
	}
}

export default App;
