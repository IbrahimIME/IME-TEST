import { Box, Paper, Stack, Tab, Tabs, Tooltip, Zoom } from "@mui/material";
import { Country, State } from "country-state-city";
import { Column, ColumnChooser, DataGrid, FilterRow, GroupPanel, Grouping, Pager, Paging, SearchPanel, Sorting } from "devextreme-react/data-grid";
import { Component } from "react";
import { Beforeunload } from "react-beforeunload";
import { Helmet } from "react-helmet-async";
import { Prompt } from "react-router-dom";

import { AutoComplete, LoadingSpinner, MuiButton, MuiPhoneNumber, MuiTextField, SnackBar, TabPanel } from "../components/common";
import { CancelIcon, DeleteIcon, EditIcon, QuestionMarkIcon, SaveIcon } from "../components/Icon";
import { User } from "../endpoints/BAS_PNO";
import { Camunda } from "../endpoints/DCM_DAM";
import i18n from "../i18n";
import { ActivityLogging, Api, Cookies, ObjectLogging } from "../utils";
import auth from "./Login/auth";

class Profile extends Component {
	state = {
		editing: false,
		User_ID: Cookies.get("User_ID"),
		isLoadingUser: true,
		isLoadingRoles: true,
		User: {},
		Profile_Image_Preview: "",
		Roles: [],
		Countries: Country.getAllCountries(),
		States: [],
		edited: false,
		isSaving: false,
		inputError: {
			User_First_Name: false,
			User_Last_Name: false,
			Preferred_Name: false,
			User_Email: false,
			Mobile_No: false,
			User_Name: false,
			User_Password: false,
		},
		refreshProfile: false,
		tabValue: 0,
		snackbar: { open: false, type: "info", message: "" },
	};

	showSnackbarMessage = (type, message) => {
		this.setState({ ...this.state, snackbar: { ...this.state.snackbar, open: true, type, message } });
	};

	handleCloseSnackbar = () => {
		this.setState({ ...this.state, snackbar: { ...this.state.snackbar, open: false } });
	};

	switchMode = () => {
		this.setState({ ...this.state, edited: false, editing: !this.state.editing, refreshProfile: !this.state.refreshProfile });
	};

	handleCancel = async () => {
		await Api.get({ url: User.read_single_user(this.state.User_ID) }).then((result) => {
			if (result.error) {
				console.log(result);
				return;
			}

			this.setState({ ...this.state, User: result, isLoadingUser: false });
		});

		this.switchMode();
	};

	handleChangeTab = (event, newTabValue) => {
		this.setState({ ...this.state, tabValue: newTabValue });
	};

	imageHandler = (e) => {
		if (e.target.files) {
			// 5MB
			if (e.target.files[0].size < 5000000) {
				const reader = new FileReader();

				reader.onload = () => {
					if (reader.readyState === 2) this.setState({ ...this.state, edited: true, Profile_Image_Preview: reader.result });
				};
				reader.readAsDataURL(e.target.files[0]);
			} else this.showSnackbarMessage("warning", i18n.t("max_image_size_alert_msg"));
		}
	};

	removeImage = () => {
		this.setState({ ...this.state, User: { ...this.state.User, adm_usr_master: { ...this.state.User.adm_usr_master, Profile_Image: null } } });
	};

	cancelImage = () => {
		this.setState({ ...this.state, edited: true, Profile_Image_Preview: null });
	};

	onChangeCountry = (e) => {
		this.setState({
			...this.state,
			edited: true,
			User: { ...this.state.User, adm_usr_master: { ...this.state.User.adm_usr_master, Country: e.target.value, State: null } },
			States: State.getStatesOfCountry(e.target.value),
		});
	};

	onChangeProfile = (e) => {
		this.setState({
			...this.state,
			edited: true,
			User: { ...this.state.User, adm_usr_master: { ...this.state.User.adm_usr_master, [e.target.name]: e.target.value } },
		});
	};

	onChangeMobileNo = (value) => {
		this.setState({
			...this.state,
			edited: true,
			User: { ...this.state.User, adm_usr_master: { ...this.state.User.adm_usr_master, Mobile_No: value } },
		});
	};

	onChangeAccount = (e) => {
		this.setState({ ...this.state, edited: true, User: { ...this.state.User, [e.target.name]: e.target.value } });
	};

	handleValidate = () => {
		this.setState((prevState) => ({
			...prevState,
			inputError: {
				...prevState.inputError,
				User_First_Name: this.state.User.adm_usr_master.User_First_Name === "" ? true : false,
				User_Last_Name: this.state.User.adm_usr_master.User_Last_Name === "" ? true : false,
				Preferred_Name: this.state.User.adm_usr_master.Preferred_Name === "" ? true : false,
				Mobile_No: this.state.User.adm_usr_master.Mobile_No === "" ? true : false,
				User_Password: this.state.User.User_Password === "" ? true : false,
			},
		}));
	};

	saveProfile = async () => {
		if (
			this.state.inputError.User_First_Name ||
			this.state.inputError.User_Last_Name ||
			this.state.inputError.Preferred_Name ||
			this.state.inputError.Mobile_No ||
			this.state.inputError.User_Password
		) {
			this.showSnackbarMessage("error", i18n.t("fill_in_all_required_fields"));
			return;
		}

		if (this.state.Profile_Image_Preview) {
			this.setState((prevState) => ({
				...prevState,
				User: {
					...prevState.User,
					adm_usr_master: { ...prevState.User.adm_usr_master, Profile_Image: this.state.Profile_Image_Preview },
				},
			}));
		}

		this.setState({ ...this.state, isSaving: true });
		await Api.put({ url: User.update_user(Cookies.get("User_ID")), body: this.state.User }).then(async (result) => {
			if (!result.success) {
				console.log(result);
				this.showSnackbarMessage("error", result.error);
				this.setState({ ...this.state, isSaving: false });
				return;
			}

			let camunda_user = {
				User_Name: this.state.User.User_Name,
				User_First_Name: this.state.User.adm_usr_master.User_First_Name,
				User_Last_Name: this.state.User.adm_usr_master.User_Last_Name,
				User_Email: this.state.User.adm_usr_master.User_Email,
				User_Password: this.state.User.User_Password,
			};

			// Update Camunda
			Api.put({
				url: Camunda.update_user(this.state.User.User_Name),
				body: camunda_user,
			}).then((result) => {
				if (!result.success) console.log(result);
			});

			ActivityLogging("Update Profile");
			await Api.get({ url: User.refresh_token() }).then((result) => {
				if (!result.success) {
					console.log(result);
					this.showSnackbarMessage("error", result.error);
					return;
				}

				Cookies.set("token", result.token);
			});

			this.setState({ ...this.state, edited: false, isSaving: false });
			ObjectLogging("Update", "User", this.state.User.ID, "Updated User");
			this.showSnackbarMessage("success", i18n.t("profile_updated"));
			this.refreshUserProfile();
			this.switchMode();
		});
	};

	refreshUserProfile = () => {
		this.setState({ ...this.state, refreshProfile: !this.state.refreshProfile });
	};

	retrieveAllData = () => {
		Api.get({ url: User.read_single_user(this.state.User_ID) }).then((result) => {
			if (result.error) {
				console.log(result);
				return;
			}

			this.setState({
				...this.state,
				User: result,
				isLoadingUser: false,
				States: State.getStatesOfCountry(result.adm_usr_master.Country),
			});
		});

		Api.get({ url: User.read_all_roles(this.state.User_ID) }).then((result) => {
			if (result.error) {
				console.log(result);
				return;
			}

			this.setState({ ...this.state, Roles: result, isLoadingRoles: false });
		});
	};

	async componentDidMount() {
		auth.refresh_token();

		this.props.updateHeaderTitle("profile");
		this.props.setPath(this.props.match.path);
		this.props.getFeatureList("");
		this.props.getMenuItems();

		this.retrieveAllData();
	}

	componentDidUpdate(prevProps, prevState) {
		if (prevState.refreshProfile !== this.state.refreshProfile) {
			auth.refresh_token();
			this.setState({ ...this.state, isLoadingUser: true, isLoadingRoles: true });
			this.retrieveAllData();
		}
	}

	render() {
		return (
			<>
				<Helmet>
					<title>{i18n.t("profile")}</title>
				</Helmet>
				<Prompt when={this.state.edited} message={i18n.t("unsaved_changes")} />
				{this.state.edited && <Beforeunload onBeforeunload={(event) => event.preventDefault()} />}
				<SnackBar snackbar={this.state.snackbar} handleCloseSnackbar={this.handleCloseSnackbar} />
				<Paper>
					<Stack direction="row" justifyContent="space-between" sx={{ pt: 2, px: 2 }}>
						<Tabs value={this.state.tabValue} onChange={this.handleChangeTab} variant="scrollable" scrollButtons="auto">
							<Tab label={i18n.t("profile")} />
							<Tab label={i18n.t("account")} />
							<Tab label={i18n.t("roles", { ns: "BAS_PNO" })} />
						</Tabs>
						<Stack direction="row" spacing={1}>
							{!this.state.editing && (
								<MuiButton tooltip={i18n.t("edit")} variant="contained" onClick={this.switchMode} content={<EditIcon />} />
							)}
							{this.state.editing && (
								<>
									<MuiButton tooltip={i18n.t("cancel")} variant="outlined" onClick={this.handleCancel} content={<CancelIcon />} />
									<MuiButton
										tooltip={i18n.t("save")}
										variant="contained"
										onClick={async () => {
											await this.handleValidate();
											this.saveProfile();
										}}
										content={<SaveIcon />}
									/>
								</>
							)}
						</Stack>
					</Stack>
					<Box sx={{ p: 2 }}>
						<ProfileTab
							tabIndex={0}
							state={this.state}
							imageHandler={this.imageHandler}
							removeImage={this.removeImage}
							cancelImage={this.cancelImage}
							onChangeCountry={this.onChangeCountry}
							onChangeMobileNo={this.onChangeMobileNo}
							onChangeProfile={this.onChangeProfile}
						/>
						<AccountTab tabIndex={1} state={this.state} onChangeAccount={this.onChangeAccount} />
						<RoleTab tabIndex={2} state={this.state} />
					</Box>
				</Paper>
			</>
		);
	}
}

function ProfileTab(props) {
	const marital_status_options = [
		{ Label: i18n.t("single", { ns: "BAS_PNO" }), Value: "single" },
		{ Label: i18n.t("married", { ns: "BAS_PNO" }), Value: "married" },
		{ Label: i18n.t("divorced", { ns: "BAS_PNO" }), Value: "divorced" },
		{ Label: i18n.t("widowed", { ns: "BAS_PNO" }), Value: "widowed" },
	];

	return (
		<TabPanel value={props.state.tabValue} index={props.tabIndex}>
			{props.state.isLoadingUser && <LoadingSpinner className="text-center" />}
			{!props.state.isLoadingUser && (
				<>
					<div className="row">
						<div className="col-lg-6">
							<div className="row">
								<div className="col-form-label col-4 d-flex align-items-center justify-content-end text-end">
									{i18n.t("profile_image")}
								</div>
								<div className="col-form-label col-8">
									<div
										className={
											props.state.Profile_Image_Preview
												? "image-input image-input-outline image-input-changed"
												: props.state.User.adm_usr_master.Profile_Image
												? "image-input image-input-outline"
												: "image-input image-input-outline image-input-empty"
										}
									>
										<div
											className="image-input-wrapper"
											style={
												props.state.Profile_Image_Preview
													? {
															backgroundImage: "url(" + props.state.Profile_Image_Preview + ")",
															backgroundSize: "contain",
															backgroundPosition: "center",
													  }
													: {
															backgroundImage: "url(" + props.state.User.adm_usr_master.Profile_Image + ")",
															backgroundSize: "contain",
															backgroundPosition: "center",
													  }
											}
										></div>
										{props.state.editing && (
											<>
												<Tooltip
													title={
														props.state.User.adm_usr_master.Profile_Image || props.state.Profile_Image_Preview
															? i18n.t("change_profile_image", { ns: "BAS_PNO" })
															: i18n.t("select_profile_image", { ns: "BAS_PNO" })
													}
													TransitionComponent={Zoom}
													arrow
												>
													<label
														className="btn btn-xs btn-icon btn-circle btn-white btn-hover-text-primary btn-shadow"
														data-action="change"
													>
														<EditIcon sx={{ fontSize: "16px" }} />
														<input type="file" name="profile_avatar" accept="image/*" onChange={props.imageHandler} />
														<input type="hidden" name="profile_avatar_remove" />
													</label>
												</Tooltip>
												<Tooltip
													title={i18n.t(
														props.state.Profile_Image_Preview
															? "cancel"
															: props.state.User.adm_usr_master.Profile_Image
															? "remove"
															: ""
													)}
													TransitionComponent={Zoom}
													arrow
												>
													<label
														className="btn btn-xs btn-icon btn-circle btn-white btn-hover-text-primary btn-shadow"
														data-action={
															props.state.Profile_Image_Preview
																? "cancel"
																: props.state.User.adm_usr_master.Profile_Image
																? "remove"
																: ""
														}
														onClick={() => {
															props.state.Profile_Image_Preview
																? props.cancelImage()
																: props.state.User.adm_usr_master.Profile_Image
																? props.removeImage()
																: console.log();
														}}
													>
														{props.state.Profile_Image_Preview ? (
															<CancelIcon sx={{ fontSize: "16px" }} />
														) : props.state.User.adm_usr_master.Profile_Image ? (
															<DeleteIcon sx={{ fontSize: "16px" }} />
														) : (
															<QuestionMarkIcon />
														)}
													</label>
												</Tooltip>
											</>
										)}
									</div>
								</div>
							</div>
							<div className="row">
								<div className="col-form-label col-4 d-flex align-items-center justify-content-end text-end">
									{i18n.t("first_name", { ns: "BAS_PNO" })}
								</div>
								{!props.state.editing && (
									<div className="col-form-label col-8">
										{props.state.User.adm_usr_master && props.state.User.adm_usr_master.User_First_Name
											? props.state.User.adm_usr_master.User_First_Name
											: ""}
									</div>
								)}
								{props.state.editing && (
									<div className="col-form-label col-8">
										<MuiTextField
											inputProps={{ maxLength: "20" }}
											name="User_First_Name"
											value={
												props.state.User.adm_usr_master && props.state.User.adm_usr_master.User_First_Name
													? props.state.User.adm_usr_master.User_First_Name
													: ""
											}
											error={props.state.inputError.User_First_Name}
											onChange={props.onChangeProfile}
										/>
									</div>
								)}
							</div>
							<div className="row">
								<div className="col-form-label col-4 d-flex align-items-center justify-content-end text-end">
									{i18n.t("last_name", { ns: "BAS_PNO" })}
								</div>
								{!props.state.editing && (
									<div className="col-form-label col-8">
										{props.state.User.adm_usr_master && props.state.User.adm_usr_master.User_Last_Name
											? props.state.User.adm_usr_master.User_Last_Name
											: ""}
									</div>
								)}
								{props.state.editing && (
									<div className="col-form-label col-8">
										<MuiTextField
											inputProps={{ maxLength: "20" }}
											name="User_Last_Name"
											value={
												props.state.User.adm_usr_master && props.state.User.adm_usr_master.User_Last_Name
													? props.state.User.adm_usr_master.User_Last_Name
													: ""
											}
											error={props.state.inputError.User_Last_Name}
											onChange={props.onChangeProfile}
										/>
									</div>
								)}
							</div>
							<div className="row">
								<div className="col-form-label col-4 d-flex align-items-center justify-content-end text-end">
									{i18n.t("preferred_name", { ns: "BAS_PNO" })}
								</div>
								{!props.state.editing && (
									<div className="col-form-label col-8">
										{props.state.User.adm_usr_master && props.state.User.adm_usr_master.Preferred_Name
											? props.state.User.adm_usr_master.Preferred_Name
											: ""}
									</div>
								)}
								{props.state.editing && (
									<div className="col-form-label col-8">
										<MuiTextField
											inputProps={{ maxLength: "20" }}
											name="Preferred_Name"
											value={
												props.state.User.adm_usr_master && props.state.User.adm_usr_master.Preferred_Name
													? props.state.User.adm_usr_master.Preferred_Name
													: ""
											}
											error={props.state.inputError.Preferred_Name}
											onChange={props.onChangeProfile}
										/>
									</div>
								)}
							</div>
							<div className="row">
								<div className="col-form-label col-4 d-flex align-items-center justify-content-end text-end">
									{i18n.t("employee_id", { ns: "BAS_PNO" })}
								</div>
								<div className="col-form-label col-8">
									{props.state.User.adm_usr_master ? props.state.User.adm_usr_master.Employee_ID : ""}
								</div>
							</div>
							<div className="row">
								<div className="col-form-label col-4 d-flex align-items-center justify-content-end text-end">
									{i18n.t("email", { ns: "BAS_PNO" })}
								</div>
								<div className="col-form-label col-8">
									{props.state.User.adm_usr_master && props.state.User.adm_usr_master.User_Email
										? props.state.User.adm_usr_master.User_Email
										: ""}
								</div>
							</div>
							<div className="row">
								<div className="col-form-label col-4 d-flex align-items-center justify-content-end text-end">
									{i18n.t("mobile_no", { ns: "BAS_PNO" })}
								</div>
								{!props.state.editing && (
									<div className="col-form-label col-8">
										{props.state.User.adm_usr_master && props.state.User.adm_usr_master.Mobile_No
											? props.state.User.adm_usr_master.Mobile_No
											: ""}
									</div>
								)}
								{props.state.editing && (
									<div className="col-form-label col-8">
										<MuiPhoneNumber
											value={props.state.User.adm_usr_master?.Mobile_No ? props.state.User.adm_usr_master.Mobile_No : ""}
											onChange={props.onChangeMobileNo}
										/>
									</div>
								)}
							</div>
							<div className="row">
								<div className="col-form-label col-4 d-flex align-items-center justify-content-end text-end">
									{i18n.t("join_date", { ns: "BAS_PNO" })}
								</div>
								<div className="col-form-label col-8">
									{props.state.User.adm_usr_master && props.state.User.adm_usr_master.Join_Date
										? props.state.User.adm_usr_master.Join_Date
										: ""}
								</div>
							</div>
							<div className="row">
								<div className="col-form-label col-4 d-flex align-items-center justify-content-end text-end">
									{i18n.t("confirm_date", { ns: "BAS_PNO" })}
								</div>
								<div className="col-form-label col-8">
									{props.state.User.adm_usr_master && props.state.User.adm_usr_master.Confirm_Date
										? props.state.User.adm_usr_master.Confirm_Date
										: ""}
								</div>
							</div>
							<div className="row">
								<div className="col-form-label col-4 d-flex align-items-center justify-content-end text-end">
									{i18n.t("confirm_status", { ns: "BAS_PNO" })}
								</div>
								<div className="col-form-label col-8">
									{props.state.User.adm_usr_master && props.state.User.adm_usr_master.Confirm_Status
										? props.state.User.adm_usr_master.Confirm_Status
											? i18n.t("yes")
											: i18n.t("no")
										: ""}
								</div>
							</div>
						</div>
						<div className="col-lg-6">
							<div className="row">
								<div className="col-form-label col-4 d-flex align-items-center justify-content-end text-end">
									{i18n.t("marital_status", { ns: "BAS_PNO" })}
								</div>
								<div className="col-form-label col-8">
									{!props.state.editing &&
										(props.state.User.adm_usr_master
											? props.state.User.adm_usr_master.Marital_Status.charAt(0).toUpperCase() +
											  props.state.User.adm_usr_master.Marital_Status.slice(1)
											: "")}
									{props.state.editing && (
										<AutoComplete
											options={marital_status_options}
											value={props.state.User.adm_usr_master.Marital_Status}
											onChange={props.onChangeProfile}
											label={i18n.t("marital_status", { ns: "BAS_PNO" })}
											name="Marital_Status"
										/>
									)}
								</div>
							</div>
							<div className="row">
								<div className="col-form-label col-4 d-flex align-items-center justify-content-end text-end">
									{i18n.t("address_1")}
								</div>
								{!props.state.editing && (
									<div className="col-form-label col-8">
										{props.state.User.adm_usr_master ? props.state.User.adm_usr_master.User_Add1 : ""}
									</div>
								)}
								{props.state.editing && (
									<div className="col-form-label col-8">
										<MuiTextField
											inputProps={{ maxLength: "100" }}
											name="User_Add1"
											value={props.state.User.adm_usr_master.User_Add1 ? props.state.User.adm_usr_master.User_Add1 : ""}
											onChange={props.onChangeProfile}
										/>
									</div>
								)}
							</div>
							<div className="row">
								<div className="col-form-label col-4 d-flex align-items-center justify-content-end text-end">
									{i18n.t("address_2")}
								</div>
								{!props.state.editing && (
									<div className="col-form-label col-8">
										{props.state.User.adm_usr_master ? props.state.User.adm_usr_master.User_Add2 : ""}
									</div>
								)}
								{props.state.editing && (
									<div className="col-form-label col-8">
										<MuiTextField
											inputProps={{ maxLength: "100" }}
											name="User_Add2"
											value={props.state.User.adm_usr_master.User_Add2 ? props.state.User.adm_usr_master.User_Add2 : ""}
											onChange={props.onChangeProfile}
										/>
									</div>
								)}
							</div>
							<div className="row">
								<div className="col-form-label col-4 d-flex align-items-center justify-content-end text-end">{i18n.t("area")}</div>
								{!props.state.editing && (
									<div className="col-form-label col-8">
										{props.state.User.adm_usr_master ? props.state.User.adm_usr_master.Area : ""}
									</div>
								)}
								{props.state.editing && (
									<div className="col-form-label col-8">
										<MuiTextField
											inputProps={{ maxLength: "50" }}
											name="Area"
											value={props.state.User.adm_usr_master.Area ? props.state.User.adm_usr_master.Area : ""}
											onChange={props.onChangeProfile}
										/>
									</div>
								)}
							</div>
							<div className="row">
								<div className="col-form-label col-4 d-flex align-items-center justify-content-end text-end">{i18n.t("city")}</div>
								{!props.state.editing && (
									<div className="col-form-label col-8">
										{props.state.User.adm_usr_master ? props.state.User.adm_usr_master.City : ""}
									</div>
								)}
								{props.state.editing && (
									<div className="col-form-label col-8">
										<MuiTextField
											inputProps={{ maxLength: "100" }}
											name="City"
											value={props.state.User.adm_usr_master.City ? props.state.User.adm_usr_master.City : ""}
											onChange={props.onChangeProfile}
										/>
									</div>
								)}
							</div>
							<div className="row">
								<div className="col-form-label col-4 d-flex align-items-center justify-content-end text-end">
									{i18n.t("postcode")}
								</div>
								{!props.state.editing && (
									<div className="col-form-label col-8">
										{props.state.User.adm_usr_master ? props.state.User.adm_usr_master.Postcode : ""}
									</div>
								)}
								{props.state.editing && (
									<div className="col-form-label col-8">
										<MuiTextField
											inputProps={{ maxLength: "10" }}
											name="Postcode"
											value={props.state.User.adm_usr_master.Postcode ? props.state.User.adm_usr_master.Postcode : ""}
											onChange={props.onChangeProfile}
										/>
									</div>
								)}
							</div>
							<div className="row">
								<div className="col-form-label col-4 d-flex align-items-center justify-content-end text-end">{i18n.t("country")}</div>
								{!props.state.editing && (
									<div className="col-form-label col-8">
										{props.state.User.adm_usr_master
											? Country.getCountryByCode(props.state.User.adm_usr_master.Country).name
											: ""}
									</div>
								)}
								{props.state.editing && (
									<div className="col-form-label col-8">
										<AutoComplete
											options={props.state.Countries}
											value={props.state.User.adm_usr_master.Country}
											onChange={props.onChangeCountry}
											optionLabel="name"
											optionValue="isoCode"
											name="Country"
											label={i18n.t("country")}
										/>
									</div>
								)}
							</div>
							<div className="row">
								<div className="col-form-label col-4 d-flex align-items-center justify-content-end text-end">{i18n.t("state")}</div>
								{!props.state.editing && (
									<div className="col-form-label col-8">
										{props.state.User.adm_usr_master ? props.state.User.adm_usr_master.State : ""}
									</div>
								)}
								{props.state.editing && (
									<div className="col-form-label col-8">
										<AutoComplete
											options={props.state.States}
											value={props.state.User.adm_usr_master.State}
											onChange={props.onChangeProfile}
											optionLabel="name"
											optionValue="name"
											name="State"
											label={i18n.t("state")}
										/>
									</div>
								)}
							</div>
							<div className="row">
								<div className="col-form-label col-4 d-flex align-items-center justify-content-end text-end">
									{i18n.t("user_status", { ns: "BAS_PNO" })}
								</div>
								<div className="col-form-label col-8">
									{props.state.User.adm_usr_master && props.state.User.adm_usr_master.User_Status
										? props.state.User.adm_usr_master.User_Status
										: ""}
								</div>
							</div>
						</div>
					</div>
				</>
			)}
		</TabPanel>
	);
}

function AccountTab(props) {
	return (
		<TabPanel value={props.state.tabValue} index={props.tabIndex}>
			{props.state.isLoadingUser && <LoadingSpinner className="text-center" />}
			{!props.state.isLoadingUser && (
				<div className="row">
					<div className="col-lg-6">
						<div className="row">
							<div className="col-form-label col-4 d-flex align-items-center justify-content-end text-end">Username</div>
							<div className="col-form-label col-8">{props.state.User.User_Name}</div>
						</div>
						<div className="row">
							<div className="col-form-label col-4 d-flex align-items-center justify-content-end text-end">Password</div>
							{!props.state.editing && <div className="col-form-label col-8">{props.state.User.User_Password.replace(/./g, "*")}</div>}
							{props.state.editing && (
								<div className="col-form-label col-8">
									<MuiTextField
										type="password"
										name="User_Password"
										value={props.state.User.User_Password}
										error={props.state.inputError.User_Password}
										onChange={props.onChangeAccount}
									/>
								</div>
							)}
						</div>
					</div>
				</div>
			)}
		</TabPanel>
	);
}

function RoleTab(props) {
	return (
		<TabPanel value={props.state.tabValue} index={props.tabIndex}>
			{props.state.isLoadingRoles && <LoadingSpinner className="text-center" />}
			{!props.state.isLoadingRoles && props.state.Roles && (
				<DataGrid
					dataSource={props.state.Roles}
					showBorders={true}
					allowColumnReordering={true}
					allowColumnResizing={true}
					columnAutoWidth={true}
					// columnHidingEnabled={true}
				>
					<Sorting mode="multiple" />
					<Paging enabled={true} defaultPageSize={20} />
					<Column dataField="Role_ID" caption={i18n.t("role_id", { ns: "BAS_PNO" })} />
					<Column dataField="adm_role_master.Role_Name" caption={i18n.t("role_name", { ns: "BAS_PNO" })} />
					<Column dataField="adm_role_master.Role_Description" caption={i18n.t("role_description", { ns: "BAS_PNO" })} />
					<Column dataField="Org_ID" caption={i18n.t("company_id", { ns: "BAS_PNO" })} visible={false} defaultSortOrder="asc" />
					<Column dataField="adm_org_master.Org_Name" caption={i18n.t("company", { ns: "BAS" })} />
					<ColumnChooser enabled={true} mode="select" />
					{props.state.Roles.length > 0 && <FilterRow visible={true} />}
					<SearchPanel visible={true} />
					<GroupPanel visible={true} />
					<Grouping autoExpandAll={true} contextMenuEnabled={true} />
					<Pager
						visible={true}
						showPageSizeSelector={true}
						showNavigationButtons={true}
						showInfo={true}
						infoText="Page {0} of {1} ({2} items)"
					/>
				</DataGrid>
			)}
		</TabPanel>
	);
}

export default Profile;
