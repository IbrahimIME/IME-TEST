import { Box, Paper, Stack, Typography } from "@mui/material";
import DataGrid, { Column, Editing, FilterRow, GroupPanel, Grouping, Pager, Paging, SearchPanel, Sorting } from "devextreme-react/data-grid";
import React, { Component } from "react";
import { Beforeunload } from "react-beforeunload";
import { Helmet } from "react-helmet-async";
import { Prompt } from "react-router-dom";

import { LoadingSpinner, SnackBar } from "../../../../components/common";
import { SystemSetting } from "../../../../endpoints/BAS_SYS";
import i18n from "../../../../i18n";
import { ActivityLogging, Api } from "../../../../utils";
import auth from "../../../Login/auth";

class SQLA extends Component {
	state = {
		edited: false,
		editing: false,
		SQLAOrg: [],
		isLoadingSQLAOrg: true,
		isSaving: false,
		snackbar: { open: false, type: "info", message: "" },
	};

	showSnackbarMessage = (type, message) => {
		this.setState({ ...this.state, snackbar: { ...this.state.snackbar, open: true, type, message } });
	};

	handleCloseSnackbar = () => {
		this.setState({ ...this.state.snackbar, snackbar: { ...this.state.snackbar, open: false } });
	};

	onRowUpdating = async (e) => {
		let updated_mapping = {
			Org_ID: e.oldData.Org_ID,
			UserName: e.newData.UserName ? e.newData.UserName : e.oldData.UserName,
			Password: e.newData.Password ? e.newData.Password : e.oldData.Password,
			Database: e.newData.Database ? e.newData.Database : e.oldData.Database,
			Path: e.newData.Path ? e.newData.Path : e.oldData.Path,
		};

		Api.put({
			url: SystemSetting.update_sqla_org_mapping(),
			body: updated_mapping,
		}).then((result) => {
			if (!result.success) {
				console.log(result);
				return;
			}

			ActivityLogging("Update SQLA Mapping " + e.oldData.Org_ID, "BAS_SYS");

			this.setState({ ...this.state, edited: false });
			this.showSnackbarMessage("success", i18n.t("updated"));
		});
	};

	onEditingStart = (e) => {
		this.setState({ ...this.state, edited: true });
	};

	retrieveAllData = () => {
		Api.get({ url: SystemSetting.get_sqla_org_mapping() }).then((result) => {
			if (result.error) {
				console.log(result);
				this.showSnackbarMessage("error", result.error);
				return;
			}

			console.log(result);
			this.setState({ ...this.state, SQLAOrg: result, isLoadingSQLAOrg: false });
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
					<title>{i18n.t("sqla_org_mapping", { ns: "BAS_SYS" })}</title>
				</Helmet>
				<Paper>
					<Stack direction="row" justifyContent="space-between" sx={{ pt: 2, px: 2 }}>
						<Typography variant="h6">{i18n.t("sqla_org_mapping", { ns: "BAS_SYS" })}</Typography>
					</Stack>
					<Box sx={{ p: 2 }}>
						{this.state.isLoadingSQLAOrg && <LoadingSpinner className="text-center" />}
						{!this.state.isLoadingSQLAOrg && (
							<DataGrid
								dataSource={this.state.SQLAOrg}
								showBorders={true}
								allowColumnReordering={true}
								allowColumnResizing={true}
								columnAutoWidth={true}
								// columnHidingEnabled={true}
								hoverStateEnabled={true}
								onEditingStart={this.onEditingStart}
								onRowUpdating={this.onRowUpdating}
							>
								<Sorting mode="multiple" />
								<Paging enabled={true} defaultPageSize={20} />
								<Editing mode="batch" useIcons={true} allowUpdating={true} allowAdding={false} allowDeleting={false} />
								<Column dataField="adm_org_master.Org_Name" caption={i18n.t("company", { ns: "BAS_SYS" })} allowEditing={false} />
								<Column dataField="UserName" caption={i18n.t("username", { ns: "BAS_SYS" })} />
								<Column dataField="Password" caption={i18n.t("password", { ns: "BAS_SYS" })} />
								<Column dataField="Database" caption={i18n.t("database_name", { ns: "BAS_SYS" })} />
								<Column dataField="Path" caption={i18n.t("path", { ns: "BAS_SYS" })} />
								{this.state.SQLAOrg.length > 0 && <FilterRow visible={true} />}
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
					</Box>
				</Paper>
			</>
		);
	}
}

export default SQLA;
