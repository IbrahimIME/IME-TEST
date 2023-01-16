import { Formio } from "formiojs";
import React, { Component } from "react";

import { Form } from "../endpoints/BAS_CMM";
import i18n from "../i18n";
import { Api } from "../utils";

class Demo extends Component {
	state = {
		Form_ID: 9,
		Form: null,
		isLoadingForm: true,
	};

	async componentDidMount() {
		await Api.get({
			url: Form.read_single_form(this.state.Form_ID),
			headers: { "access-token": "formio" },
		}).then((result) => {
			if (result.error) {
				console.log(result);
				this.setState({ ...this.state, isLoadingForm: false });
				return;
			}

			this.setState({ ...this.state, Form: result, isLoadingForm: false });
		});

		if (!this.state.isLoadingForm) {
			Formio.createForm(document.getElementById("formio"), JSON.parse(this.state.Form.Form_Body), { i18next: i18n.createInstance() }).then(
				(form) => {
					form.on("change", this.onFillInForm);
				}
			);
		}
	}

	render() {
		return (
			<div className="d-flex flex-column flex-root h-100 p-4">
				<div id="formio"></div>
			</div>
		);
	}
}

export default Demo;
