import { Box, Paper, Stack, Typography } from "@mui/material";
import { Component } from "react";
import { Beforeunload } from "react-beforeunload";
import { Helmet } from "react-helmet-async";
import { Prompt } from "react-router-dom";

import { LoadingSpinner, MuiButton, MuiTextField, SnackBar } from "../../../components/common";
import { CancelIcon, EditIcon, SaveIcon } from "../../../components/Icon";
import { SystemSetting } from "../../../endpoints/BAS_SYS";
import i18n from "../../../i18n";
import { ActivityLogging, Api } from "../../../utils";
import auth from "../../Login/auth";

class EmailServer extends Component {
	state = {
		EmailServer: {
			HOST: "",
			PORT: "",
			USER: "",
			PASSWORD: "",
		},
		editing: false,
		isLoadingEmailServer: true,
		isSavingEmailServer: false,
		edited: false,
		inputError: {
			HOST: false,
			PORT: false,
			USER: false,
			PASSWORD: false,
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

	onChangeEmailServer = (e) => {
		this.setState({ ...this.state, edited: true, EmailServer: { ...this.state.EmailServer, [e.target.name]: e.target.value } });
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
				HOST: this.state.EmailServer.HOST === "" ? true : false,
				PORT: this.state.EmailServer.PORT === "" ? true : false,
				USER: this.state.EmailServer.USER === "" ? true : false,
				PASSWORD: this.state.EmailServer.PASSWORD === "" ? true : false,
			},
		}));
	};

	saveEmailServer = async () => {
		if (!this.state.inputError.HOST && !this.state.inputError.PORT && !this.state.inputError.USER && !this.state.inputError.PASSWORD) {
			this.setState({ ...this.state, isSavingEmailServer: true });

			await Api.put({
				url: SystemSetting.update_mail_server(),
				body: this.state.EmailServer,
			}).then((result) => {
				if (!result.success) {
					console.log(result);
					return;
				}

				ActivityLogging("Update Email Server", "BAS_SYS");

				this.showSnackbarMessage("success", i18n.t("email_server_updated", { ns: "BAS_SYS" }));
				this.setState({ ...this.state, edited: false, isSavingEmailServer: false });
				this.switchMode();
			});
		}
	};

	retrieveAllData = () => {
		Api.get({ url: SystemSetting.get_mail_server() }).then((result) => {
			if (result.error) {
				console.log(result);
				this.setState({ ...this.state, isLoadingEmailServer: false });
				this.showSnackbarMessage("error", result.error);
				return;
			}

			this.setState({ ...this.state, EmailServer: result, isLoadingEmailServer: false });
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
					<title>{i18n.t("email_server", { ns: "BAS_SYS" })}</title>
				</Helmet>
				<Paper>
					<Stack direction="row" justifyContent="space-between" sx={{ pt: 2, px: 2 }}>
						<Typography variant="h6">{i18n.t("email_server", { ns: "BAS_SYS" })}</Typography>
						<Stack direction="row" spacing={1}>
							{!this.state.editing && (
								<MuiButton tooltip={i18n.t("edit")} variant="contained" onClick={this.switchMode} content={<EditIcon />} />
							)}
							{this.state.editing && (
								<Stack direction="row" spacing={1}>
									<MuiButton
										tooltip={i18n.t("cancel")}
										variant="outlined"
										disabled={this.state.isSavingEmailServer}
										onClick={this.handleCancel}
										content={<CancelIcon />}
									/>
									<MuiButton
										loading={this.state.isSavingEmailServer}
										tooltip={this.state.isSavingEmailServer ? i18n.t("saving") : i18n.t("save")}
										variant="contained"
										onClick={async () => {
											await this.handleValidate();
											this.saveEmailServer();
										}}
										content={<SaveIcon />}
									/>
								</Stack>
							)}
						</Stack>
					</Stack>
					<Box sx={{ p: 2 }}>
						{this.state.isLoadingEmailServer && <LoadingSpinner className="text-center" />}
						{!this.state.isLoadingEmailServer && (
							<div className="row">
								<div className="col-lg-6">
									<div className="row">
										<div className="col-form-label col-4 d-flex align-items-center justify-content-end text-end">
											{i18n.t("smtp_host", { ns: "BAS_SYS" })} <font className="red-asterisk">*</font>
										</div>
										{!this.state.editing && (
											<div className="col-form-label col-8">
												{this.state.EmailServer.HOST ? this.state.EmailServer.HOST : ""}
											</div>
										)}
										{this.state.editing && (
											<div className="col-form-label col-8">
												<MuiTextField
													name="HOST"
													value={this.state.EmailServer.HOST}
													error={this.state.inputError.HOST}
													onChange={this.onChangeEmailServer}
												/>
											</div>
										)}
									</div>
									<div className="row">
										<div className="col-form-label col-4 d-flex align-items-center justify-content-end text-end">
											{i18n.t("smtp_port", { ns: "BAS_SYS" })} <font className="red-asterisk">*</font>
										</div>
										{!this.state.editing && (
											<div className="col-form-label col-8">
												{this.state.EmailServer.PORT ? this.state.EmailServer.PORT : ""}
											</div>
										)}
										{this.state.editing && (
											<div className="col-form-label col-8">
												<MuiTextField
													name="PORT"
													value={this.state.EmailServer.PORT}
													error={this.state.inputError.PORT}
													onChange={this.onChangeEmailServer}
												/>
											</div>
										)}
									</div>
								</div>
								<div className="col-lg-6">
									<div className="row">
										<div className="col-form-label col-4 d-flex align-items-center justify-content-end text-end">
											{i18n.t("smtp_username", { ns: "BAS_SYS" })} <font className="red-asterisk">*</font>
										</div>
										{!this.state.editing && (
											<div className="col-form-label col-8">
												{this.state.EmailServer.USER ? this.state.EmailServer.USER : ""}
											</div>
										)}
										{this.state.editing && (
											<div className="col-form-label col-8">
												<MuiTextField
													name="USER"
													value={this.state.EmailServer.USER}
													error={this.state.inputError.USER}
													onChange={this.onChangeEmailServer}
												/>
											</div>
										)}
									</div>
									<div className="row">
										<div className="col-form-label col-4 d-flex align-items-center justify-content-end text-end">
											{i18n.t("smtp_password", { ns: "BAS_SYS" })} <font className="red-asterisk">*</font>
										</div>
										{!this.state.editing && (
											<div className="col-form-label col-8">
												{this.state.EmailServer.PASSWORD ? this.state.EmailServer.PASSWORD.replace(/./g, "*") : ""}
											</div>
										)}
										{this.state.editing && (
											<div className="col-form-label col-8">
												<MuiTextField
													name="PASSWORD"
													type="password"
													value={this.state.EmailServer.PASSWORD}
													error={this.state.inputError.PASSWORD}
													onChange={this.onChangeEmailServer}
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

export default EmailServer;
