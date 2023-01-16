import React, { Component } from "react";

import { ProtectedRoute } from "../../../../protected.route";
import Authentication from "./Authentication";
import Camunda from "./Camunda";
import ImportHistory1 from "./ImportHistory";
import SQLA from "./SQLA";

class Other extends Component {
	render() {
		return (
			<>
				<ProtectedRoute path={`${this.props.match.path}/authentication`} component={Authentication} />
				<ProtectedRoute path={`${this.props.match.path}/camunda`} component={Camunda} />
				<ProtectedRoute path={`${this.props.match.path}/sqla`} component={SQLA} />
				<ProtectedRoute path={`${this.props.match.path}/import_history`} component={ImportHistory1} />
			</>
		);
	}
}

export default Other;
