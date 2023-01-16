import { Box, Paper, Stack, Typography } from "@mui/material";
import { Component } from "react";
import { Beforeunload } from "react-beforeunload";
import { Helmet } from "react-helmet-async";
import { Prompt } from "react-router-dom";

import { LoadingSpinner, MuiButton, MuiTextField, SnackBar } from "../../../../components/common";
import { CancelIcon, EditIcon, SaveIcon } from "../../../../components/Icon";
import { SystemSetting } from "../../../../endpoints/BAS_SYS";
import i18n from "../../../../i18n";
import { ActivityLogging, Api } from "../../../../utils";
import auth from "../../../Login/auth";

class Authentication extends Component {
	state = {
		edited: false,
		editing: false,
		Authentication: {},
		isLoadingAuthentication: true,
		isSaving: false,
		inputError: {
			TOKEN_EXPIRES_IN_MINUTES: false,
		},
		snackbar: { open: false, type: "info", message: "" },
	};

	showSnackbarMessage = (type, message) => {
		this.setState({ ...this.state, snackbar: { ...this.state.snackbar, open: true, type, message } });
	};

	handleCloseSnackbar = () => {
		this.setState({ ...this.state.snackbar, snackbar: { ...this.state.snackbar, open: false } });
	};

	switchMode = () => {
		this.setState({ ...this.state.snackbar, edited: false, editing: !this.state.editing });
	};

	onChangeAuthentication = (e) => {
		this.setState({ ...this.state, edited: true, Authentication: { ...this.state.Authentication, [e.target.name]: e.target.value } });
	};

	handleCancel = () => {
		this.switchMode();
		this.retrieveAllData();
	};

	handleValidate = () => {
		this.setState((prevState) => ({
			...prevState,
			inputError: {
				...prevState.inputError,
				TOKEN_EXPIRES_IN_MINUTES:
					this.state.Authentication.TOKEN_EXPIRES_IN_MINUTES === "" || this.state.Authentication.TOKEN_EXPIRES_IN_MINUTES === "0"
						? true
						: false,
			},
		}));
	};

	saveAuthentication = () => {
		if (!this.state.inputError.TOKEN_EXPIRES_IN_MINUTES) {
			Api.put({
				url: SystemSetting.update_authentication_setting(),
				body: this.state.Authentication,
			}).then((result) => {
				console.log(result);
				if (result.error) {
					console.log(result);
					this.showSnackbarMessage("error", result.error);
					return;
				}

				ActivityLogging("Update Authentication", "BAS_SYS");

				this.showSnackbarMessage("success", i18n.t("authentication_setting_updated", { ns: "BAS_SYS" }));
				this.setState({ ...this.state, edited: false, isSaving: false });
				this.switchMode();
			});
		}
	};

	retrieveAllData = () => {
		Api.get({ url: SystemSetting.get_authentication_setting() }).then((result) => {
			if (result.error) {
				console.log(result);
				this.showSnackbarMessage("error", result.error);
				return;
			}

			this.setState({ ...this.state, Authentication: result, isLoadingAuthentication: false });
		});
	};

	componentDidMount() {
		auth.refresh_token();
		this.retrieveAllData();
	}

	render() {
		return (
			<>
				<Prompt when={this.state.edited} message={i18n.t("unsaved_changes")} />
				{this.state.edited && <Beforeunload onBeforeunload={(event) => event.preventDefault()} />}
				<SnackBar snackbar={this.state.snackbar} handleCloseSnackbar={this.handleCloseSnackbar} />
				<Helmet>
					<title>{i18n.t("authentication", { ns: "BAS_SYS" })}</title>
				</Helmet>
				<Paper>
					<Stack direction="row" justifyContent="space-between" sx={{ pt: 2, px: 2 }}>
						<Typography variant="h6">{i18n.t("authentication", { ns: "BAS_SYS" })}</Typography>
						<Stack direction="row" spacing={1}>
							{!this.state.editing && (
								<MuiButton tooltip={i18n.t("edit")} variant="contained" onClick={this.switchMode} content={<EditIcon />} />
							)}
							{this.state.editing && (
								<Stack direction="row" spacing={1}>
									<MuiButton
										tooltip={i18n.t("cancel")}
										variant="outlined"
										disabled={this.state.isSaving}
										onClick={this.handleCancel}
										content={<CancelIcon />}
									/>
									<MuiButton
										loading={this.state.isSaving}
										tooltip={this.state.isSaving ? i18n.t("saving") : i18n.t("save")}
										variant="contained"
										onClick={async () => {
											await this.handleValidate();
											this.saveAuthentication();
										}}
										content={<SaveIcon />}
									/>
								</Stack>
							)}
						</Stack>
					</Stack>
					<Box sx={{ p: 2 }}>
						{this.state.isLoadingAuthentication && <LoadingSpinner className="text-center" />}
						{!this.state.isLoadingAuthentication && (
							<div className="row">
								<div className="col-lg-6">
									<div className="row">
										<div className="col-form-label col-4 d-flex align-items-center justify-content-end text-end">
											{i18n.t("user_token_expires_in_minutes", { ns: "BAS_SYS" })} <font className="red-asterisk">*</font>
										</div>
										{!this.state.editing && (
											<div className="col-form-label col-8">
												{this.state.Authentication.TOKEN_EXPIRES_IN_MINUTES
													? this.state.Authentication.TOKEN_EXPIRES_IN_MINUTES
													: ""}
											</div>
										)}
										{this.state.editing && (
											<div className="col-form-label col-8">
												<MuiTextField
													inputProps={{ step: "1", min: 1 }}
													name="TOKEN_EXPIRES_IN_MINUTES"
													type="number"
													value={this.state.Authentication.TOKEN_EXPIRES_IN_MINUTES}
													error={this.state.inputError.TOKEN_EXPIRES_IN_MINUTES}
													onChange={this.onChangeAuthentication}
												/>
											</div>
										)}
									</div>
								</div>
							</div>
						)}
					</Box>
				</Paper>
			</>
		);
	}
}

export default Authentication;
