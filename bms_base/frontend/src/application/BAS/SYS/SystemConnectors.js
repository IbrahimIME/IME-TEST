import { Box, Paper, Stack, Typography } from "@mui/material";
import { Component } from "react";
import { Beforeunload } from "react-beforeunload";
import { Helmet } from "react-helmet-async";
import { Prompt } from "react-router-dom";

import { LoadingSpinner, MuiButton, MuiTextField, SnackBar } from "../../../components/common";
import { CancelIcon, EditIcon, SaveIcon } from "../../../components/Icon";
import { SystemSetting } from "../../../endpoints/BAS_SYS";
import i18n from "../../../i18n";
import { ActivityLogging, Api, Cookies } from "../../../utils";
import auth from "../../Login/auth";

class SystemConnectors extends Component {
	state = {
		WorkflowServer: {},
		SQLAServer: {},
		isLoadingWorkflowServer: true,
		isLoadingSQLAServer: true,
		testingWorkflow: false,
		testingSQLA: false,
		workflowediting: false,
		sqlaediting: false,
		editedWorkflow: false,
		editedSQLA: false,
		isSavingWorkflow: false,
		isSavingSQLA: false,
		inputError: {
			CAMUNDA_SERVER_IP: false,
			PORT: false,
			SQLA_HOST: false,
			SQLA_PORT: false,
			SQLA_WEB_PORT: false,
		},
		snackbar: { open: false, type: "info", message: "" },
	};

	showSnackbarMessage = (type, message) => {
		this.setState({ ...this.state, snackbar: { ...this.state.snackbar, open: true, type, message } });
	};

	handleCloseSnackbar = () => {
		this.setState({ ...this.state.snackbar, snackbar: { ...this.state.snackbar, open: false } });
	};

	testWorkflow = async () => {
		this.setState({ ...this.state, testingWorkflow: true });

		let url = "http://" + this.state.WorkflowServer.CAMUNDA_SERVER_IP + ":" + this.state.WorkflowServer.PORT;

		await Api.post({
			url: SystemSetting.test_workflow_server(),
			body: { url: url },
		}).then((result) => {
			if (!result.version) {
				console.log(result);
				ActivityLogging("Test Workflow Server Connection FAILED", "BAS_SYS");
				this.showSnackbarMessage("error", i18n.t("connection_failed", { ns: "BAS_SYS" }));
				return;
			}

			ActivityLogging("Test Workflow Server Connection SUCCESS", "BAS_SYS");
			this.showSnackbarMessage("success", i18n.t("connection_success", { ns: "BAS_SYS" }));
		});

		this.setState({ ...this.state, testingWorkflow: false });
	};

	testSQLA = async () => {
		this.setState({ ...this.state, testingSQLA: true });

		let url = "http://" + this.state.SQLAServer.SQLA_HOST + ":" + this.state.SQLAServer.SQLA_PORT;

		await Api.post({
			url: SystemSetting.test_sqla_server(),
			body: {
				web_port: this.state.SQLAServer.SQLA_WEB_PORT,
				url: url,
				Org_ID: Cookies.get("Org_ID"),
			},
		}).then((result) => {
			if (!result.success) {
				console.log(result);
				ActivityLogging("Test SQLA Server Connection FAILED", "BAS_SYS");
				this.showSnackbarMessage("error", i18n.t("connection_failed", { ns: "BAS_SYS" }));
				return;
			}

			ActivityLogging("Test SQLA Server Connection SUCCESS", "BAS_SYS");
			this.showSnackbarMessage("success", i18n.t("connection_success", { ns: "BAS_SYS" }));
		});

		this.setState({ ...this.state, testingSQLA: false });
	};

	switchWorkflowMode = () => {
		this.setState({ ...this.state, editedWorkflow: false, workflowediting: !this.state.workflowediting });
	};

	switchSQLAMode = () => {
		this.setState({ ...this.state, editedSQLA: false, sqlaediting: !this.state.sqlaediting });
	};

	handleCancelWorkflow = () => {
		this.switchWorkflowMode();

		Api.get({ url: SystemSetting.get_workflow_server() }).then((result) => {
			if (result.error) {
				console.log(result);
				this.setState({ ...this.state, editedWorkflow: false, isLoadingWorkflowServer: false });
				return;
			}

			this.setState({ ...this.state, editedWorkflow: false, WorkflowServer: result, isLoadingWorkflowServer: false });
		});
	};

	handleCancelSQLA = () => {
		this.switchSQLAMode();

		Api.get({ url: SystemSetting.get_sqla_server() }).then((result) => {
			if (result.error) {
				console.log(result);
				this.setState({ ...this.state, editedSQLA: false, isLoadingSQLAServer: false });
				return;
			}

			this.setState({ ...this.state, editedSQLA: false, SQLAServer: result, isLoadingSQLAServer: false });
		});
	};

	onChangeWorkflow = (e) => {
		this.setState({ ...this.state, editedWorkflow: true, WorkflowServer: { ...this.state.WorkflowServer, [e.target.name]: e.target.value } });
	};

	onChangeSQLA = (e) => {
		this.setState({ ...this.state, editedSQLA: true, SQLAServer: { ...this.state.SQLAServer, [e.target.name]: e.target.value } });
	};

	saveWorkflow = () => {
		Api.put({
			url: SystemSetting.update_workflow_server(),
			body: this.state.WorkflowServer,
		}).then((result) => {
			if (!result.success) {
				this.showSnackbarMessage("error", i18n.t("contact_system_admin"));
				return;
			}

			ActivityLogging("Update Workflow Server", "BAS_SYS");

			this.switchWorkflowMode();
			this.setState({ ...this.state, editedWorkflow: false });
			this.showSnackbarMessage("success", i18n.t("workflow_server_updated", { ns: "BAS_SYS" }));
		});
	};

	saveSQLA = () => {
		Api.put({
			url: SystemSetting.update_sqla_server(),
			body: this.state.SQLAServer,
		}).then((result) => {
			if (!result.success) {
				this.showSnackbarMessage("error", i18n.t("contact_system_admin"));
				return;
			}

			ActivityLogging("Update SQLA Server", "BAS_SYS");

			this.switchSQLAMode();
			this.setState({ ...this.state, editedSQLA: false });
			this.showSnackbarMessage("success", i18n.t("sqla_server_updated", { ns: "BAS_SYS" }));
		});
	};

	retrieveAllData = () => {
		Api.get({ url: SystemSetting.get_workflow_server() }).then((result) => {
			if (result.error) {
				console.log(result);
				this.setState({ ...this.state, isLoadingWorkflowServer: false });
				this.showSnackbarMessage("error", result.error);
				return;
			}

			this.setState({ ...this.state, WorkflowServer: result, isLoadingWorkflowServer: false });
		});

		Api.get({ url: SystemSetting.get_sqla_server() }).then((result) => {
			if (result.error) {
				console.log(result);
				this.setState({ ...this.state, isLoadingSQLAServer: false });
				this.showSnackbarMessage("error", result.error);
				return;
			}

			this.setState({ ...this.state, SQLAServer: result, isLoadingSQLAServer: false });
		});
	};

	componentDidMount() {
		auth.refresh_token();

		this.retrieveAllData();
	}

	render() {
		return (
			<>
				<Prompt when={this.state.editedWorkflow || this.state.editedSQLA} message={i18n.t("unsaved_changes")} />
				{(this.state.editedWorkflow || this.state.editedSQLA) && <Beforeunload onBeforeunload={(event) => event.preventDefault()} />}
				<SnackBar snackbar={this.state.snackbar} handleCloseSnackbar={this.handleCloseSnackbar} />
				<Helmet>
					<title>{i18n.t("system_connectors", { ns: "BAS_SYS" })}</title>
				</Helmet>
				<Stack direction="column" spacing={2}>
					<Workflow
						state={this.state}
						onChangeWorkflow={this.onChangeWorkflow}
						switchWorkflowMode={this.switchWorkflowMode}
						handleCancelWorkflow={this.handleCancelWorkflow}
						saveWorkflow={this.saveWorkflow}
						testWorkflow={this.testWorkflow}
						showSnackbarMessage={this.showSnackbarMessage}
					/>
					<SQLA
						state={this.state}
						onChangeSQLA={this.onChangeSQLA}
						switchSQLAMode={this.switchSQLAMode}
						handleCancelSQLA={this.handleCancelSQLA}
						saveSQLA={this.saveSQLA}
						testSQLA={this.testSQLA}
						showSnackbarMessage={this.showSnackbarMessage}
					/>
				</Stack>
			</>
		);
	}
}

function Workflow(props) {
	return (
		<Paper>
			<Stack direction="row" justifyContent="space-between" sx={{ pt: 2, px: 2 }}>
				<Typography variant="h6">{i18n.t("workflow_server", { ns: "BAS_SYS" })}</Typography>
				<Stack direction="row" spacing={1}>
					{!props.state.workflowediting && (
						<MuiButton
							tooltip={i18n.t("edit")}
							variant="contained"
							disabled={props.state.isSavingWorkflow}
							onClick={props.switchWorkflowMode}
							content={<EditIcon />}
						/>
					)}
					{props.state.workflowediting && (
						<>
							<MuiButton
								tooltip={i18n.t("cancel")}
								variant="outlined"
								disabled={props.state.isSavingWorkflow}
								onClick={props.handleCancelWorkflow}
								content={<CancelIcon />}
							/>
							<MuiButton
								loading={props.state.isSavingWorkflow}
								tooltip={props.state.isSavingWorkflow ? i18n.t("saving") : i18n.t("save")}
								variant="contained"
								onClick={props.saveWorkflow}
								content={<SaveIcon />}
							/>
						</>
					)}
				</Stack>
			</Stack>
			{props.state.isLoadingWorkflowServer && <LoadingSpinner className="text-center" />}
			{!props.state.isLoadingWorkflowServer && (
				<Box sx={{ p: 2 }}>
					<Stack direction="column" spacing={2}>
						<div className="row">
							<div className="col-lg-6">
								<div className="row">
									<div className="col-form-label col-4 d-flex align-items-center justify-content-end text-end">
										{i18n.t("camunda_server_ip", { ns: "BAS_SYS" })} <font className="red-asterisk">*</font>
									</div>
									{!props.state.workflowediting && (
										<div className="col-form-label col-8">
											{props.state.WorkflowServer.CAMUNDA_SERVER_IP ? props.state.WorkflowServer.CAMUNDA_SERVER_IP : ""}
										</div>
									)}
									{props.state.workflowediting && (
										<div className="col-form-label col-8">
											<MuiTextField
												name="CAMUNDA_SERVER_IP"
												placeholder="xxx.xxx.xxx.xxx"
												value={props.state.WorkflowServer.CAMUNDA_SERVER_IP}
												error={props.state.inputError.CAMUNDA_SERVER_IP}
												onChange={props.onChangeWorkflow}
												// inputComponent={ServerIPMask}
											/>
										</div>
									)}
								</div>
								<div className="row">
									<div className="col-form-label col-4 d-flex align-items-center justify-content-end text-end">
										{i18n.t("port", { ns: "BAS_SYS" })} <font className="red-asterisk">*</font>
									</div>
									{!props.state.workflowediting && (
										<div className="col-form-label col-8">
											{props.state.WorkflowServer.PORT ? props.state.WorkflowServer.PORT : ""}
										</div>
									)}
									{props.state.workflowediting && (
										<div className="col-form-label col-8">
											<MuiTextField
												inputProps={{ step: "1" }}
												name="PORT"
												type="number"
												value={props.state.WorkflowServer.PORT}
												error={props.state.inputError.PORT}
												onChange={props.onChangeWorkflow}
											/>
										</div>
									)}
								</div>
							</div>
						</div>
						<MuiButton
							tooltip=""
							loading={props.state.testingWorkflow}
							variant="outlined"
							disabled={props.state.testingSQLA}
							onClick={props.testWorkflow}
							content={i18n.t("test_connection", { ns: "BAS_SYS" })}
						/>
					</Stack>
				</Box>
			)}
		</Paper>
	);
}

function SQLA(props) {
	return (
		<Paper>
			<Stack direction="row" justifyContent="space-between" sx={{ pt: 2, px: 2 }}>
				<Typography variant="h6">{i18n.t("sqla_server", { ns: "BAS_SYS" })}</Typography>
				<Stack direction="row" spacing={1}>
					{!props.state.sqlaediting && (
						<MuiButton
							tooltip={i18n.t("edit")}
							variant="contained"
							disabled={props.state.isSavingSQLA}
							onClick={props.switchSQLAMode}
							content={<EditIcon />}
						/>
					)}
					{props.state.sqlaediting && (
						<>
							<MuiButton
								tooltip={i18n.t("cancel")}
								variant="outlined"
								disabled={props.state.isSavingSQLA}
								onClick={props.handleCancelSQLA}
								content={<CancelIcon />}
							/>
							<MuiButton
								loading={props.state.isSavingSQLA}
								tooltip={props.state.isSavingSQLA ? i18n.t("saving") : i18n.t("save")}
								variant="contained"
								onClick={props.saveSQLA}
								content={<SaveIcon />}
							/>
						</>
					)}
				</Stack>
			</Stack>
			{props.state.isLoadingSQLAServer && <LoadingSpinner className="text-center" />}
			{!props.state.isLoadingSQLAServer && (
				<Box sx={{ p: 2 }}>
					<Stack direction="column" spacing={2}>
						<div className="row">
							<div className="col-lg-6">
								<div className="row">
									<div className="col-form-label col-4 d-flex align-items-center justify-content-end text-end">
										{i18n.t("sqla_host", { ns: "BAS_SYS" })} <font className="red-asterisk">*</font>
									</div>
									{!props.state.sqlaediting && (
										<div className="col-form-label col-8">
											{props.state.SQLAServer.SQLA_HOST ? props.state.SQLAServer.SQLA_HOST : ""}
										</div>
									)}
									{props.state.sqlaediting && (
										<div className="col-form-label col-8">
											<MuiTextField
												name="SQLA_HOST"
												placeholder="xxx.xxx.xxx.xxx"
												value={props.state.SQLAServer.SQLA_HOST}
												error={props.state.inputError.SQLA_HOST}
												onChange={props.onChangeSQLA}
												// inputComponent={ServerIPMask}
											/>
										</div>
									)}
								</div>
								<div className="row">
									<div className="col-form-label col-4 d-flex align-items-center justify-content-end text-end">
										{i18n.t("sqla_port", { ns: "BAS_SYS" })} <font className="red-asterisk">*</font>
									</div>
									{!props.state.sqlaediting && (
										<div className="col-form-label col-8">
											{props.state.SQLAServer.SQLA_PORT ? props.state.SQLAServer.SQLA_PORT : ""}
										</div>
									)}
									{props.state.sqlaediting && (
										<div className="col-form-label col-8">
											<MuiTextField
												inputProps={{ step: "1" }}
												name="SQLA_PORT"
												type="number"
												value={props.state.SQLAServer.SQLA_PORT}
												error={props.state.inputError.SQLA_PORT}
												onChange={props.onChangeSQLA}
											/>
										</div>
									)}
								</div>
							</div>
							<div className="col-lg-6">
								<div className="row">
									<div className="col-form-label col-4 d-flex align-items-center justify-content-end text-end">
										{i18n.t("sqla_web_port", { ns: "BAS_SYS" })} <font className="red-asterisk">*</font>
									</div>
									{!props.state.sqlaediting && (
										<div className="col-form-label col-8">
											{props.state.SQLAServer.SQLA_WEB_PORT ? props.state.SQLAServer.SQLA_WEB_PORT : ""}
										</div>
									)}
									{props.state.sqlaediting && (
										<div className="col-form-label col-8">
											<MuiTextField
												inputProps={{ step: "1" }}
												name="SQLA_WEB_PORT"
												type="number"
												value={props.state.SQLAServer.SQLA_WEB_PORT}
												error={props.state.inputError.SQLA_WEB_PORT}
												onChange={props.onChangeSQLA}
											/>
										</div>
									)}
								</div>
							</div>
						</div>
						<MuiButton
							tooltip=""
							loading={props.state.testingSQLA}
							variant="outlined"
							disabled={props.state.testingWorkflow}
							onClick={props.testSQLA}
							content={i18n.t("test_connection", { ns: "BAS_SYS" })}
						/>
					</Stack>
				</Box>
			)}
		</Paper>
	);
}

export default SystemConnectors;
