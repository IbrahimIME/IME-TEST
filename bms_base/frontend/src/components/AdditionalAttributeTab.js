import { Checkbox, FormControl, FormControlLabel, FormGroup, FormHelperText, Radio, RadioGroup } from "@mui/material";
import { Fragment } from "react";

import i18n from "../i18n";
import { AutoComplete, LoadingSpinner, MuiDatePicker, MuiSwitch, MuiTextField, TabPanel } from "./common";

function AdditionalAttributeTab(props) {
	return (
		<TabPanel value={props.state.tabValue} index={props.tabIndex}>
			<div className="row">
				{props.state.isLoadingAdditionalAttribute && <LoadingSpinner className="text-center w-100" />}
				{!props.state.isLoadingAdditionalAttribute && props.state.AdditionalAttribute.error && (
					<div className="text-center w-100">{props.state.AdditionalAttribute.error}</div>
				)}
				{!props.state.isLoadingAdditionalAttribute &&
					!props.state.AdditionalAttribute.error &&
					props.state.AdditionalAttribute.map((attribute, index) => (
						<Fragment key={index}>
							{(!attribute.Sensitive ||
								(attribute.Sensitive && props.editing && (attribute.Create || attribute.Update)) ||
								(attribute.Sensitive && !props.editing && attribute.Read)) && (
								<div className="col-lg-6">
									<div className="row">
										<div className="col-form-label col-4 d-flex align-items-center justify-content-end text-end">
											{attribute.Name} {attribute.Mandatory && <font className="red-asterisk">*</font>}
										</div>
										<div className="col-form-label col-8">
											{!props.editing &&
												(attribute.Attribute_Master_Value ? attribute.Attribute_Master_Value : attribute.Attribute_Value)}
											{props.editing && attribute.Input_Type === "freeinput" && (
												<>
													{attribute.Data_Type === "string" && (
														<MuiTextField
															inputProps={{ maxLength: attribute.Length }}
															name={attribute.Name}
															value={attribute.Attribute_Value ? attribute.Attribute_Value : ""}
															error={props.state.inputError.AdditionalAttribute[index]}
															onChange={(e) =>
																props.onChangeAdditional(e.target.name, "freeinput", e.target.value, index)
															}
														/>
													)}
													{attribute.Data_Type === "boolean" && (
														<MuiSwitch
															name={attribute.Name}
															checked={
																attribute.Attribute_Value
																	? attribute.Attribute_Value || attribute.Attribute_Value === "true"
																		? true
																		: false
																	: false
															}
															onChange={(e) =>
																props.onChangeAdditional(
																	attribute.Name,
																	"freeinput",
																	e.target.checked ? true : false,
																	index
																)
															}
														/>
													)}
													{(attribute.Data_Type === "integer" || attribute.Data_Type === "real") && (
														<MuiTextField
															inputProps={{
																step:
																	attribute.Data_Type === "integer" ? 1 : attribute.Data_Type === "real" ? 0.01 : 0,
																pattern:
																	attribute.Data_Type === "integer"
																		? "/^[-+]?[1-9]d*$/"
																		: attribute.Data_Type === "real"
																		? "[+-]?([0-9]*[.])?[0-9]+"
																		: "",
															}}
															name={attribute.Name}
															type="number"
															value={attribute.Attribute_Value ? attribute.Attribute_Value : ""}
															error={props.state.inputError.AdditionalAttribute[index]}
															onChange={(e) =>
																props.onChangeAdditional(attribute.Name, "freeinput", e.target.value, index)
															}
														/>
													)}
													{attribute.Data_Type === "date" && (
														<MuiDatePicker
															name={attribute.Name}
															value={attribute.Attribute_Value ? attribute.Attribute_Value : ""}
															onChange={(e) =>
																props.onChangeAdditional(
																	attribute.Name,
																	"freeinput",
																	Date.parse(e)
																		? e.getFullYear() + "-" + (e.getMonth() + 1) + "-" + e.getDate()
																		: e,
																	index
																)
															}
														/>
													)}
												</>
											)}
											{props.editing && attribute.Input_Type === "dropdown" && (
												<AutoComplete
													options={props.state.AdditionalOptions[attribute.Name]}
													value={attribute.Attribute_Value_ID !== null ? parseInt(attribute.Attribute_Value_ID) : null}
													onChange={(event, newValue) => {
														props.onChangeAdditional(
															attribute.Name,
															"dropdown",
															newValue !== null ? newValue.ID : null,
															index
														);
													}}
													optionValue="ID"
													name={attribute.Name}
													label={attribute.Name}
													error={props.state.inputError.AdditionalAttribute[index]}
													required={attribute.Mandatory}
												/>
											)}
											{props.editing && attribute.Input_Type === "radio" && (
												<FormControl error={props.state.inputError.AdditionalAttribute[index]}>
													<RadioGroup
														row
														name={attribute.Name}
														value={attribute.Attribute_Value_ID ? attribute.Attribute_Value_ID : null}
														onChange={(e) => props.onChangeAdditional(e.target.name, "radio", e.target.value, index)}
													>
														{!props.state.AdditionalOptions[attribute.Name].error &&
															props.state.AdditionalOptions[attribute.Name].map((value, index) => (
																<FormControlLabel
																	value={value.ID}
																	control={<Radio />}
																	label={value.Label}
																	key={index}
																/>
															))}
														{props.state.AdditionalOptions[attribute.Name].error && (
															<div>{i18n.t("no_value", { ns: "BAS_CMM" })}</div>
														)}
													</RadioGroup>
													{props.state.inputError.AdditionalAttribute[index] && (
														<FormHelperText>{i18n.t("select_one", { ns: "BAS_CMM" })}</FormHelperText>
													)}
												</FormControl>
											)}
											{props.editing && attribute.Input_Type === "checkbox" && (
												<FormControl>
													<FormGroup error={props.state.inputError.AdditionalAttribute[index] ? "true" : "false"}>
														{!props.state.AdditionalOptions[attribute.Name].error &&
															props.state.AdditionalOptions[attribute.Name].map((value) => (
																<FormControlLabel
																	control={
																		<Checkbox
																			checked={
																				attribute.Attribute_Value_ID
																					? attribute.Attribute_Value_ID.includes(String(value.ID))
																					: false
																			}
																			name={attribute.Name}
																			onChange={(e) =>
																				props.onChangeAdditional(
																					e.target.name,
																					"checkbox",
																					e.target.value,
																					index
																				)
																			}
																		/>
																	}
																	label={value.Label}
																	value={value.ID}
																	key={value.ID}
																/>
															))}
														{props.state.AdditionalOptions[attribute.Name].error && (
															<div>{i18n.t("no_value", { ns: "BAS_CMM" })}</div>
														)}
													</FormGroup>
													{props.state.inputError.AdditionalAttribute[index] && (
														<FormHelperText>{i18n.t("choose_at_least_one", { ns: "BAS_CMM" })}</FormHelperText>
													)}
												</FormControl>
											)}
										</div>
									</div>
								</div>
							)}
						</Fragment>
					))}
			</div>
		</TabPanel>
	);
}

export default AdditionalAttributeTab;
