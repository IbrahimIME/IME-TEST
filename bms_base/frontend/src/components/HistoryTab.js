import DataGrid, { Column, ColumnChooser, FilterRow, Pager, Paging, SearchPanel, Sorting } from "devextreme-react/data-grid";
import { Fragment } from "react";

import i18n from "../i18n";
import { Format } from "../utils";
import { LoadingSpinner, TabPanel } from "./common";

function HistoryTab(props) {
	const renderTime = (cellInfo) => {
		if (cellInfo.value) return Format.datetime_stamp(cellInfo.value);
	};

	const renderOperation = (cellInfo) => {
		return cellInfo.value === "I" || cellInfo.value.toUpperCase() === "CREATE"
			? "Create"
			: cellInfo.value === "U" || cellInfo.value.toUpperCase() === "UPDATE"
			? "Update"
			: "";
	};

	const renderChanges = (cellInfo) => {
		return (
			<div>
				{cellInfo.value && typeof cellInfo.value === "string" && cellInfo.value}
				{cellInfo.value &&
					typeof cellInfo.value === "object" &&
					Object.entries(cellInfo.value).map(([key, value]) => (
						<Fragment key={key}>
							<b>{key}</b> ( {value} )
							<br />
						</Fragment>
					))}
			</div>
		);
	};

	return (
		<TabPanel value={props.tabValue} index={props.tabIndex}>
			{props.isLoadingHistory && <LoadingSpinner className="text-center" />}
			{!props.isLoadingHistory && (
				<DataGrid
					dataSource={props.History}
					showBorders={true}
					allowColumnReordering={true}
					allowColumnResizing={true}
					columnAutoWidth={true}
					// columnHidingEnabled={true}
				>
					<Sorting mode="multiple" />
					<Paging enabled={true} defaultPageSize={20} />
					<Column
						dataField="Stamp"
						caption={i18n.t("time", { ns: "BAS_SYS" })}
						dataType="datetime"
						defaultSortOrder="desc"
						cellRender={renderTime}
					/>
					<Column dataField="Last_Edit_User" caption={i18n.t("user", { ns: "BAS_SYS" })} />
					<Column dataField="Op" caption={i18n.t("action", { ns: "BAS_SYS" })} cellRender={renderOperation} />
					<Column dataField="Changes" caption={i18n.t("changes", { ns: "BAS_SYS" })} cellRender={renderChanges} />
					<ColumnChooser enabled={true} mode="select" />
					{props.History.length > 0 && <FilterRow visible={true} />}
					<SearchPanel visible={true} />
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

export default HistoryTab;
