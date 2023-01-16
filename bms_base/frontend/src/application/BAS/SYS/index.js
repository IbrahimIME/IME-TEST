import { Component } from "react";

import { ProtectedRoute } from "../../../protected.route";
import EmailServer from "./EmailServer";
import Logging from "./Logging";
import Other from "./Other";
import SystemConnectors from "./SystemConnectors";

class SYS extends Component {
	componentDidMount() {
		this.props.updateHeaderTitle("system_settings", "BAS_SYS");
	}

	render() {
		return (
			<>
				<ProtectedRoute path={`${this.props.match.path}/email_server`} component={EmailServer} />
				<ProtectedRoute path={`${this.props.match.path}/system_connectors`} component={SystemConnectors} />
				<ProtectedRoute path={`${this.props.match.path}/logging`} component={Logging} />
				<ProtectedRoute path={`${this.props.match.path}/other`} component={Other} />
			</>
		);
	}
}

export default SYS;
