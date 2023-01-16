import {
	Box,
	Dialog,
	DialogActions,
	DialogContent,
	DialogTitle,
	Paper,
	Stack,
	Tab,
	Table,
	TableBody,
	TableCell,
	TableContainer,
	TableHead,
	TableRow,
	Tabs,
	Typography,
} from "@mui/material";
import { useEffect } from "react";
import { Component, useState } from "react";
import { Beforeunload } from "react-beforeunload";
import { Helmet } from "react-helmet-async";
import { Prompt } from "react-router-dom";

import { AutoComplete, LoadingSpinner, MuiButton, MuiDatePicker, SnackBar, TabPanel } from "../../../components/common";
import { CancelIcon, CloseIcon, EditIcon, SaveIcon } from "../../../components/Icon";
import { ActivityLog } from "../../../endpoints";
import { SystemSetting } from "../../../endpoints/BAS_SYS";
import i18n from "../../../i18n";
import { Api, Format } from "../../../utils";
import auth from "../../Login/auth";

class Logging extends Component {
	state = {
		Logging: {
			DB_LVL: "",
			BACKEND_LVL: "",
		},
		editing: false,
		isLoadingLogging: true,
		edited: false,
		isSaving: false,
		inputError: {
			DB_LVL: false,
			BACKEND_LVL: false,
		},
		openBackendDialog: false,
		openActivityDialog: false,
		snackbar: { open: false, type: "info", message: "" },
	};

	showSnackbarMessage = (type, message) => {
		this.setState({ ...this.state, snackbar: { ...this.state.snackbar, open: true, type, message } });
	};

	handleCloseSnackbar = () => {
		this.setState({ ...this.state, snackbar: { ...this.state.snackbar, open: false } });
	};

	switchMode = () => {
		this.setState({ ...this.state, edited: false, editing: !this.state.editing });
	};

	handleChangeLevel = (e) => {
		this.setState({ ...this.state, edited: true, Logging: { ...this.state.Logging, [e.target.name]: e.target.value } });
	};

	handleCancel = async () => {
		this.switchMode();
		this.retrieveAllData();
	};

	handleValidate = async () => {
		this.setState((prevState) => ({
			...prevState,
			inputError: {
				...prevState.inputError,
				DB_LVL: this.state.Logging.DB_LVL === "" || this.state.Logging.DB_LVL === null ? true : false,
				BACKEND_LVL: this.state.Logging.BACKEND_LVL === "" || this.state.Logging.BACKEND_LVL === null ? true : false,
			},
		}));
	};

	saveLogging = async () => {
		if (!this.state.inputError.DB_LVL && !this.state.inputError.BACKEND_LVL) {
			await Api.put({
				url: SystemSetting.update_log_setting(),
				body: this.state.Logging,
			}).then((result) => {
				if (!result.success) {
					console.log(result);
					return;
				}

				this.showSnackbarMessage("success", i18n.t("log_updated", { ns: "BAS_SYS" }));
				this.setState({ ...this.state, edited: false, isSaving: false });
				this.switchMode();
			});
		}
	};

	handleOpenBackendDialog = () => {
		this.setState({ ...this.state, openBackendDialog: true });
	};

	handleCloseBackendDialog = () => {
		this.setState({ ...this.state, openBackendDialog: false });
	};

	handleOpenActivityDialog = () => {
		this.setState({ ...this.state, openActivityDialog: true });
	};

	handleCloseActivityDialog = () => {
		this.setState({ ...this.state, openActivityDialog: false });
	};

	retrieveAllData = () => {
		Api.get({ url: SystemSetting.get_log_setting() }).then((result) => {
			if (result.error) {
				console.log(result);
				this.setState({ ...this.state, isLoadingLogging: false });
				this.showSnackbarMessage("error", result.error);
				return;
			}

			this.setState({ ...this.state, Logging: result, isLoadingLogging: false });
		});
	};

	componentDidMount() {
		auth.refresh_token();
		this.retrieveAllData();
	}

	render() {
		const DB_LVL = [
			{ Label: "LOG", Value: "NONE" },
			{ Label: "INFO", Value: "INFO" },
			{ Label: "NOTICE", Value: "NOTICE" },
			{ Label: "WARNING", Value: "WARNING" },
			{ Label: "ERROR", Value: "ERROR" },
		];

		const BACKEND_LVL = [
			{ Label: "NONE", Value: "NOTSET" },
			{ Label: "DEBUG", Value: "DEBUG" },
			{ Label: "INFO", Value: "INFO" },
			{ Label: "WARNING", Value: "WARNING" },
			{ Label: "ERROR", Value: "ERROR" },
			{ Label: "CRITICAL", Value: "CRITICAL" },
		];

		return (
			<>
				<Prompt when={this.state.edited} message={i18n.t("unsaved_changes")} />
				{this.state.edited && <Beforeunload onBeforeunload={(event) => event.preventDefault()} />}
				<SnackBar snackbar={this.state.snackbar} handleCloseSnackbar={this.handleCloseSnackbar} />
				<Helmet>
					<title>{i18n.t("log_setting", { ns: "BAS_SYS" })}</title>
				</Helmet>
				<Paper>
					<Stack direction="row" justifyContent="space-between" sx={{ pt: 2, px: 2 }}>
						<Typography variant="h6">{i18n.t("logging", { ns: "BAS_SYS" })}</Typography>
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
										onClick={this.saveLogging}
										content={<SaveIcon />}
									/>
								</Stack>
							)}
						</Stack>
					</Stack>
					<Box sx={{ p: 2 }}>
						{this.state.isLoadingLogging && <LoadingSpinner className="text-center" />}
						{!this.state.isLoadingLogging && (
							<Stack direction="column" spacing={2}>
								<div className="row">
									<div className="col-lg-6">
										<div className="row">
											<div className="col-form-label col-4 d-flex align-items-center justify-content-end text-end">
												{i18n.t("database", { ns: "BAS_SYS" })} <font className="red-asterisk">*</font>
											</div>
											<div className="col-form-label col-8">
												{!this.state.editing && this.state.Logging.DB_LVL ? this.state.Logging.DB_LVL : ""}
												{this.state.editing && (
													<AutoComplete
														options={DB_LVL}
														value={this.state.Logging.DB_LVL}
														onChange={this.handleChangeLevel}
														name="DB_LVL"
														label={i18n.t("database", { ns: "BAS_SYS" })}
														error={this.state.inputError.DB_LVL}
														required={true}
													/>
												)}
											</div>
										</div>
										<div className="row">
											<div className="col-form-label col-4 d-flex align-items-center justify-content-end text-end">
												{i18n.t("backend_endpoint", { ns: "BAS_SYS" })} <font className="red-asterisk">*</font>
											</div>
											<div className="col-form-label col-8">
												{!this.state.editing && this.state.Logging.BACKEND_LVL ? this.state.Logging.BACKEND_LVL : ""}
												{this.state.editing && (
													<AutoComplete
														options={BACKEND_LVL}
														value={this.state.Logging.BACKEND_LVL}
														onChange={this.handleChangeLevel}
														name="BACKEND_LVL"
														label={i18n.t("backend_endpoint", { ns: "BAS_SYS" })}
														error={this.state.inputError.BACKEND_LVL}
														required={true}
													/>
												)}
											</div>
										</div>
									</div>
								</div>

								<MuiButton
									tooltip=""
									variant="outlined"
									onClick={this.handleOpenBackendDialog}
									content={i18n.t("view_backend_logs", { ns: "BAS_SYS" })}
								/>
								<BackendLogDialog openDialog={this.state.openBackendDialog} handleCloseDialog={this.handleCloseBackendDialog} />

								<MuiButton
									tooltip=""
									variant="outlined"
									onClick={this.handleOpenActivityDialog}
									content={i18n.t("user_activity_logs", { ns: "BAS_SYS" })}
								/>
								<ActivityLogDialog openDialog={this.state.openActivityDialog} handleCloseDialog={this.handleCloseActivityDialog} />
							</Stack>
						)}
					</Box>
				</Paper>
			</>
		);
	}
}

function BackendLogDialog(props) {
	var today = new Date();
	today = today.getFullYear() + "-" + (today.getMonth() + 1) + "-" + today.getDate();

	const [tabValue, setTabValue] = useState(0);

	const handleChangeTab = (event, newTabValue) => {
		setTabValue(newTabValue);
	};

	const [loading, setLoading] = useState(true);
	const [logDate, setLogDate] = useState(today);
	const [mainLogs, setMainLogs] = useState("");
	const [adminLogs, setAdminLogs] = useState("");
	const [authLogs, setAuthLogs] = useState("");
	const [documentLogs, setDocumentLogs] = useState("");
	const [masterLogs, setMasterLogs] = useState("");
	const [systemLogs, setSystemLogs] = useState("");

	useEffect(() => {
		setLoading(true);
		let date = new Date(logDate);
		date = date.getFullYear() + "_" + Format.left_pad(date.getMonth() + 1, 2, "0") + "_" + Format.left_pad(date.getDate(), 2, "0");

		Api.get({ url: SystemSetting.read_logs(date) }).then((result) => {
			setLoading(false);
			setMainLogs(result.mainLogs);
			setAdminLogs(result.adminLogs);
			setAuthLogs(result.authLogs);
			setDocumentLogs(result.documentLogs);
			setMasterLogs(result.masterLogs);
			setSystemLogs(result.systemLogs);
		});
	}, [logDate]);

	return (
		<Dialog open={props.openDialog} fullWidth={true} maxWidth="md">
			<DialogTitle>{i18n.t("backend_logs", { ns: "BAS_SYS" })}</DialogTitle>
			<DialogContent>
				<div className="row">
					<div className="col-6">
						<div className="row">
							<div className="col-3 col-form-label">{i18n.t("date")}</div>
							<div className="col-9 col-form-label">
								<MuiDatePicker name="logDate" value={logDate} onChange={(e) => setLogDate(e)} />
							</div>
						</div>
					</div>
				</div>
				<Tabs value={tabValue} onChange={handleChangeTab} variant="scrollable" scrollButtons="auto">
					<Tab label={i18n.t("main", { ns: "BAS_SYS" })} />
					<Tab label={i18n.t("administration", { ns: "BAS_SYS" })} />
					<Tab label={i18n.t("auth", { ns: "BAS_SYS" })} />
					<Tab label={i18n.t("document_management", { ns: "BAS_SYS" })} />
					<Tab label={i18n.t("master_data", { ns: "BAS_SYS" })} />
					<Tab label={i18n.t("system_setting", { ns: "BAS_SYS" })} />
				</Tabs>
				<Box sx={{ p: 1, maxHeight: "50vh", overflow: "auto", whiteSpace: "pre-line" }}>
					{loading ? (
						<LoadingSpinner className="text-center" />
					) : (
						<>
							<TabPanel value={tabValue} index={0}>
								{mainLogs}
							</TabPanel>
							<TabPanel value={tabValue} index={1}>
								{adminLogs}
							</TabPanel>
							<TabPanel value={tabValue} index={2}>
								{authLogs}
							</TabPanel>
							<TabPanel value={tabValue} index={3}>
								{documentLogs}
							</TabPanel>
							<TabPanel value={tabValue} index={4}>
								{masterLogs}
							</TabPanel>
							<TabPanel value={tabValue} index={5}>
								{systemLogs}
							</TabPanel>
						</>
					)}
				</Box>
			</DialogContent>
			<DialogActions>
				<MuiButton tooltip={i18n.t("close")} variant="outlined" content={<CloseIcon />} onClick={props.handleCloseDialog} />
			</DialogActions>
		</Dialog>
	);
}

function ActivityLogDialog(props) {
	var today = new Date();
	today = today.getFullYear() + "-" + (today.getMonth() + 1) + "-" + today.getDate();

	const [loading, setLoading] = useState(true);
	const [logDate, setLogDate] = useState(today);
	const [logs, setLogs] = useState([]);

	useEffect(() => {
		setLoading(true);
		let date = new Date(logDate);
		date = date.getFullYear() + "_" + Format.left_pad(date.getMonth() + 1, 2, "0") + "_" + Format.left_pad(date.getDate(), 2, "0");

		Api.get({ url: ActivityLog.read_logs(date) }).then((result) => {
			setLoading(false);

			if (result.error) {
				console.log(result);
				setLogs(result);
				return;
			}

			setLogs(result);
		});
	}, [logDate]);

	return (
		<Dialog open={props.openDialog} fullWidth={true} maxWidth="lg">
			<DialogTitle>{i18n.t("user_activity_logs", { ns: "BAS_SYS" })}</DialogTitle>
			<DialogContent>
				<div className="row">
					<div className="col-6">
						<div className="row">
							<div className="col-3 col-form-label">{i18n.t("date")}</div>
							<div className="col-9 col-form-label">
								<MuiDatePicker name="logDate" value={logDate} onChange={(e) => setLogDate(e)} />
							</div>
						</div>
					</div>
				</div>
				<TableContainer component={Paper} sx={{ maxHeight: "70vh" }}>
					<Table stickyHeader size="small">
						<TableHead>
							<TableRow>
								<TableCell>Date/Time</TableCell>
								<TableCell>User ID</TableCell>
								<TableCell>Name</TableCell>
								<TableCell>Action</TableCell>
								<TableCell>App_Feature</TableCell>
								<TableCell className="d-none">Location</TableCell>
								<TableCell className="d-none">IP</TableCell>
							</TableRow>
						</TableHead>
						<TableBody>
							{(loading || logs.error) && (
								<TableRow>
									<TableCell colSpan={7} align="center">
										{loading ? <LoadingSpinner /> : logs.error}
									</TableCell>
								</TableRow>
							)}
							{!loading &&
								!logs.error &&
								logs.map((log, index) => {
									let date = new Date(log.Date_Time);
									let date_time =
										Format.left_pad(date.getDate(), 2, "0") +
										"/" +
										Format.left_pad(date.getMonth() + 1, 2, "0") +
										"/" +
										date.getFullYear() +
										" " +
										Format.left_pad(date.getHours(), 2, "0") +
										":" +
										Format.left_pad(date.getMinutes(), 2, "0") +
										":" +
										Format.left_pad(date.getSeconds(), 2, "0");

									return (
										<TableRow key={index}>
											<TableCell>{date_time}</TableCell>
											<TableCell>{log.User_ID}</TableCell>
											<TableCell>{log.Name}</TableCell>
											<TableCell>{log.Action}</TableCell>
											<TableCell>{log.App_Feature}</TableCell>
											<TableCell className="d-none">{log.State ? `${log.State}, ${log.Country}` : log.Country}</TableCell>
											<TableCell className="d-none">{log.IP}</TableCell>
										</TableRow>
									);
								})}
						</TableBody>
					</Table>
				</TableContainer>
			</DialogContent>
			<DialogActions>
				<MuiButton tooltip={i18n.t("close")} variant="outlined" content={<CloseIcon />} onClick={props.handleCloseDialog} />
			</DialogActions>
		</Dialog>
	);
}

export default Logging;
