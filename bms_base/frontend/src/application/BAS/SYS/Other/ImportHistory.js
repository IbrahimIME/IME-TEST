import {
	Box,
	Dialog,
	DialogActions,
	DialogContent,
	DialogTitle,
	Paper,
	Stack,
	Table,
	TableBody,
	TableCell,
	TableContainer,
	TableHead,
	TableRow,
	Typography,
} from "@mui/material";
import DataGrid, { Column, Pager, Paging, SearchPanel } from "devextreme-react/data-grid";
import { Workbook } from "exceljs";
import { saveAs } from "file-saver";
import { useEffect, useState } from "react";
import { Component } from "react";
import { Helmet } from "react-helmet-async";
import { Switch } from "react-router-dom";

import { LoadingSpinner, MuiButton, SnackBar } from "../../../../components/common";
import { CloseIcon, DownloadIcon, ExportIcon } from "../../../../components/Icon";
import { User } from "../../../../endpoints/BAS_PNO";
import { ImportHistory } from "../../../../endpoints/BAS_SYS";
import i18n from "../../../../i18n";
import { ProtectedRoute } from "../../../../protected.route";
import { Api, Format } from "../../../../utils";
import auth from "../../../Login/auth";

class ImportHistory1 extends Component {
	state = {
		ImportHistory: {},
		isLoadingImportHistory: true,
		snackbar: { open: false, type: "info", message: "" },
	};

	showSnackbarMessage = (type, message) => {
		this.setState({ ...this.state, snackbar: { ...this.state.snackbar, open: true, type, message } });
	};

	handleCloseSnackbar = () => {
		this.setState({ ...this.state, snackbar: { ...this.state.snackbar, open: false } });
	};

	retrieveAllData = () => {
		Api.get({ url: ImportHistory.get_all_history() }).then((result) => {
			if (result.error) {
				console.log(result);
				this.setState({ ...this.state, isLoadingImportHistory: false });
				this.showSnackbarMessage("error", result.error);
				return;
			}

			this.setState({ ...this.state, ImportHistory: result, isLoadingImportHistory: false });
		});
	};

	componentDidMount() {
		auth.refresh_token();
		this.retrieveAllData();
	}

	render() {
		return (
			<>
				<SnackBar snackbar={this.state.snackbar} handleCloseSnackbar={this.handleCloseSnackbar} />
				<Switch>
					<ProtectedRoute exact path={`${this.props.match.path}/:ID`} component={SingleHistory} />
					<ProtectedRoute exact path={`${this.props.match.path}/`} component={History} state={this.state} />
				</Switch>
			</>
		);
	}
}

function History(props) {
	const [openDialog, setOpenDialog] = useState(false);
	const [history, setHistory] = useState({});

	const handleOpenDialog = () => {
		setOpenDialog(true);
	};
	const handleCloseDialog = () => {
		setOpenDialog(false);
		setHistory({});
	};

	const renderTime = (cellInfo) => {
		if (cellInfo.value) return Format.datetime_stamp(cellInfo.value);
	};

	const renderFile = (cellInfo) => {
		if (cellInfo.value) {
			return (
				<a href={cellInfo.value} target="_blank" rel="noreferrer">
					<MuiButton tooltip={i18n.t("download", { ns: "DCM_DAM" })} mode="icon" content={<DownloadIcon />} />
				</a>
			);
		}
	};

	const renderResult = (cellInfo) => {
		return i18n.t("click_to_view_details", { ns: "BAS_SYS" });
	};

	const onRowClick = (e) => {
		setHistory(e.data);
		handleOpenDialog();
	};

	return (
		<>
			<Helmet>
				<title>{i18n.t("import_history", { ns: "BAS_SYS" })}</title>
			</Helmet>
			<Paper sx={{ p: 2 }}>
				<Stack direction="row" justifyContent="space-between" sx={{ mb: 2 }}>
					<Typography variant="h6">{i18n.t("import_history", { ns: "BAS_SYS" })}</Typography>
					<Stack direction="row" spacing={1}></Stack>
				</Stack>
				<SingleHistory openDialog={openDialog} handleCloseDialog={handleCloseDialog} history={history} />
				{props.state.isLoadingImportHistory && <LoadingSpinner className="text-center" />}
				{!props.state.isLoadingImportHistory && (
					<DataGrid
						dataSource={props.state.ImportHistory}
						showBorders={true}
						columnAutoWidth={true}
						hoverStateEnabled={true}
						onRowClick={onRowClick}
					>
						<Paging enabled={true} defaultPageSize={20} />
						<Column dataField="Import_Date_Time" cellRender={renderTime} sortIndex={0} sortOrder="desc" />
						<Column dataField="Import_By" />
						<Column dataField="Object" />
						<Column dataField="File_Path" caption="File" cellRender={renderFile} />
						<Column dataField="Result" cellRender={renderResult} />
						<SearchPanel visible={true} />
						<Pager visible={true} />
						<Pager showPageSizeSelector={true} showNavigationButtons={true} showInfo={true} infoText="Page {0} of {1} ({2} items)" />
					</DataGrid>
				)}
			</Paper>
		</>
	);
}

function SingleHistory(props) {
	const [user, setUser] = useState({});

	const closeDialog = () => {
		setUser({});
		props.handleCloseDialog();
	};

	const exportResult = () => {
		const workbook = new Workbook();
		const worksheet = workbook.addWorksheet("Main sheet");

		worksheet.addRow(["Object", props.history.Object]);
		worksheet.addRow(["Import Date Time", Format.datetime_stamp(props.history.Import_Date_Time)]);
		worksheet.addRow(["Import By", user.adm_usr_master.User_First_Name + " " + user.adm_usr_master.User_Last_Name]);
		worksheet.addRow();

		worksheet.addRow(["Row", "Result", "Exception", "Traceback"]);
		for (const row of JSON.parse(props.history.Result)) {
			worksheet.addRow([row.Row, row.Result, row.Exception ? row.Exception : "", row.Traceback ? row.Traceback : ""]);
		}

		worksheet.getCell("A5").font = { bold: true };
		worksheet.getCell("B5").font = { bold: true };

		var date = new Date(props.history.Import_Date_Time);
		var filename =
			date.getFullYear().toString() +
			(date.getMonth() + 1).toString() +
			date.getDate().toString() +
			date.getHours().toString() +
			date.getMinutes().toString() +
			date.getSeconds().toString() +
			"_" +
			props.history.Object +
			"_Import_Result.xlsx";

		workbook.xlsx.writeBuffer().then(function (buffer) {
			saveAs(new Blob([buffer], { type: "application/octet-stream" }), filename);
		});
	};

	useEffect(() => {
		if (props.history.Import_By) {
			Api.get({ url: User.read_single_user(props.history.Import_By) }).then((result) => {
				setUser(result);
			});
		}
	}, [props.history]);

	return (
		<Dialog open={props.openDialog} fullWidth={true} maxWidth="md">
			<DialogTitle>{props.history.Object}</DialogTitle>
			<DialogContent>
				<Stack direction="column" spacing={2}>
					{JSON.stringify(user) !== "{}" && (
						<Box>
							<div className="row">
								<div className="col-form-label col-4">Import Date Time</div>
								<div className="col-form-label col-8">{Format.datetime_stamp(props.history.Import_Date_Time)}</div>
							</div>
							<div className="row">
								<div className="col-form-label col-4">Import By</div>
								<div className="col-form-label col-8">
									{user.adm_usr_master?.User_First_Name + " " + user.adm_usr_master?.User_Last_Name}
								</div>
							</div>
							<div className="row">
								<div className="col-form-label col-4 d-flex align-items-center">File</div>
								<div className="col-form-label col-8">
									<a href={props.history.File_Path} target="_blank" rel="noreferrer">
										<MuiButton tooltip={i18n.t("download", { ns: "DCM_DAM" })} mode="icon" content={<DownloadIcon />} />
									</a>
								</div>
							</div>
						</Box>
					)}
					<TableContainer component={Paper} sx={{ maxHeight: "60vh" }}>
						<Table stickyHeader size="small">
							<TableHead>
								<TableRow>
									<TableCell>{i18n.t("row")}</TableCell>
									<TableCell>{i18n.t("result")}</TableCell>
									<TableCell>{i18n.t("exception")}</TableCell>
									<TableCell>{i18n.t("traceback")}</TableCell>
								</TableRow>
							</TableHead>
							<TableBody>
								{JSON.stringify(props.history) !== "{}" &&
									props.history.Result !== "[]" &&
									JSON.parse(props.history.Result).map((row, index) => (
										<TableRow key={index}>
											<TableCell>{row.Row}</TableCell>
											<TableCell>{row.Result}</TableCell>
											<TableCell>{row.Exception}</TableCell>
											<TableCell>{row.Traceback}</TableCell>
										</TableRow>
									))}
							</TableBody>
						</Table>
					</TableContainer>
				</Stack>
			</DialogContent>
			<DialogActions>
				<MuiButton tooltip={i18n.t("export_result")} variant="outlined" onClick={exportResult} content={<ExportIcon />} />
				<MuiButton tooltip={i18n.t("done")} variant="outlined" onClick={closeDialog} content={<CloseIcon />} />
			</DialogActions>
		</Dialog>
	);
}

export default ImportHistory1;
