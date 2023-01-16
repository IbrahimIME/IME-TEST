import { Component } from "react";
import { Helmet } from "react-helmet-async";

import i18n from "../../i18n";
import { ProtectedRoute } from "../../protected.route";
import CMM from "./CMM";
import MAS from "./MAS";
import PNO from "./PNO";
import SYS from "./SYS";

class Administration extends Component {
	componentDidMount() {
		this.props.updateHeaderTitle("platform_administration", "BAS");
		this.props.setPath(this.props.match.path);
		this.props.getFeatureList("BAS");
		this.props.getMenuItems();
	}

	render() {
		return (
			<>
				<Helmet>
					<title>{i18n.t("administration", { ns: "BAS" })}</title>
				</Helmet>
				<ProtectedRoute path={`${this.props.match.path}/BAS_PNO`} component={PNO} updateHeaderTitle={this.props.updateHeaderTitle} />
				<ProtectedRoute path={`${this.props.match.path}/BAS_MAS`} component={MAS} updateHeaderTitle={this.props.updateHeaderTitle} />
				<ProtectedRoute path={`${this.props.match.path}/BAS_CMM`} component={CMM} updateHeaderTitle={this.props.updateHeaderTitle} />
				<ProtectedRoute path={`${this.props.match.path}/BAS_SYS`} component={SYS} updateHeaderTitle={this.props.updateHeaderTitle} />
			</>
		);
	}
}

export default Administration;
