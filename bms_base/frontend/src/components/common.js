import { LoadingButton } from "@mui/lab";
import { Alert, Autocomplete, CircularProgress, IconButton, Snackbar, Switch, TextField, Tooltip, Zoom } from "@mui/material";
import { AdapterDateFns } from "@mui/x-date-pickers/AdapterDateFns";
import { DatePicker } from "@mui/x-date-pickers/DatePicker";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import MaterialUiPhoneNumber from "material-ui-phone-number";

import i18n from "../i18n";
import { QuestionMarkIcon } from "./Icon";

export function LoadingSpinner({ className = "", size = 16, text = true }) {
	return (
		<div className={className}>
			{text ? (
				<>
					<CircularProgress size={size} sx={{ marginRight: "5px" }} />
					{i18n.t("loading")}...
				</>
			) : (
				<CircularProgress size={size} />
			)}
		</div>
	);
}

export function MuiButton({
	loading = false,
	tooltip = null,
	variant,
	size = "medium",
	color = "primary",
	disabled = false,
	onClick,
	content = <QuestionMarkIcon />,
	mode,
	spanStyle = {},
	buttonStyle = {},
}) {
	return tooltip !== null ? (
		<Tooltip title={tooltip} TransitionComponent={Zoom} arrow>
			<span style={spanStyle}>
				{mode === "icon" ? (
					<IconButton disabled={disabled} onClick={onClick}>
						{content}
					</IconButton>
				) : (
					<LoadingButton
						loading={loading}
						variant={variant}
						size={size}
						color={color}
						disabled={disabled}
						onClick={onClick}
						sx={buttonStyle}
					>
						{content}
					</LoadingButton>
				)}
			</span>
		</Tooltip>
	) : (
		<>
			{mode === "icon" ? (
				<IconButton disabled={disabled} onClick={onClick}>
					{content}
				</IconButton>
			) : (
				<LoadingButton loading={loading} variant={variant} size={size} color={color} disabled={disabled} onClick={onClick} sx={buttonStyle}>
					{content}
				</LoadingButton>
			)}
		</>
	);
}

export function MuiTextField({
	required = false,
	hiddenLabel = true,
	fullWidth = true,
	variant = "filled",
	size = "small",
	inputProps = {},
	InputProps = {},
	className = "",
	type = "text",
	name = "",
	placeholder = "",
	value = "",
	error = false,
	onChange,
	onBlur = null,
	onKeyDown = null,
	sx = {},
}) {
	return (
		<TextField
			required={required}
			hiddenLabel={hiddenLabel}
			fullWidth={fullWidth}
			variant={variant}
			size={size}
			inputProps={inputProps}
			InputProps={InputProps}
			className={className}
			type={type}
			name={name}
			placeholder={placeholder}
			value={value}
			error={error}
			onChange={onChange}
			onBlur={onBlur}
			onKeyDown={onKeyDown}
			sx={sx}
		/>
	);
}

export function MuiTextArea({
	required = false,
	hiddenLabel = true,
	fullWidth = true,
	variant = "filled",
	size = "small",
	multiline = false,
	rows = null,
	minRows = null,
	maxRows = null,
	inputProps = {},
	type = "text",
	name = "",
	placeholder = "",
	value = "",
	error = false,
	onChange,
	sx = {},
}) {
	sx = { ...sx, padding: 0 };

	return (
		<TextField
			required={required}
			hiddenLabel={hiddenLabel}
			fullWidth={fullWidth}
			variant={variant}
			size={size}
			multiline={multiline}
			rows={rows}
			minRows={minRows}
			maxRows={maxRows}
			inputProps={inputProps}
			type={type}
			name={name}
			placeholder={placeholder}
			value={value}
			error={error}
			onChange={onChange}
			sx={sx}
		/>
	);
}

export function MuiSwitch({ checked = false, name = "", onChange, size = "small" }) {
	return <Switch checked={checked} name={name} onChange={onChange} size={size} />;
}

export function MuiDatePicker({ id, name, minDate = null, value, onChange, required = false }) {
	return (
		<LocalizationProvider dateAdapter={AdapterDateFns}>
			{minDate !== null ? (
				<DatePicker
					id={id}
					name={name}
					inputFormat="dd/MM/yyyy"
					minDate={minDate}
					value={value ? value : null}
					onChange={onChange}
					renderInput={(params) => (
						<TextField {...params} hiddenLabel variant="filled" size="small" sx={{ width: "100%" }} required={required} />
					)}
				/>
			) : (
				<DatePicker
					id={id}
					name={name}
					inputFormat="dd/MM/yyyy"
					value={value ? value : null}
					onChange={onChange}
					renderInput={(params) => (
						<TextField {...params} hiddenLabel variant="filled" size="small" sx={{ width: "100%" }} required={required} />
					)}
				/>
			)}
		</LocalizationProvider>
	);
}

export function MuiPhoneNumber({ size = "small", variant = "filled", defaultCountry = "my", value = "", error = false, onChange }) {
	return (
		<MaterialUiPhoneNumber
			fullWidth
			size={size}
			variant={variant}
			defaultCountry={defaultCountry}
			className="phone-input"
			value={value}
			error={error}
			onChange={onChange}
		/>
	);
}

export function SnackBar(props) {
	return (
		<Snackbar
			anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
			open={props.snackbar.open}
			autoHideDuration={1500}
			onClose={props.handleCloseSnackbar}
		>
			<Alert severity={props.snackbar.type} variant="filled" style={{ fontSize: "1.25rem" }}>
				{props.snackbar.message}
			</Alert>
		</Snackbar>
	);
}

export function TabPanel(props) {
	const { children, value, index, ...other } = props;

	return (
		<div role="tabpanel" hidden={value !== index} id={`simple-tabpanel-${index}`} aria-labelledby={`simple-tab-${index}`} {...other}>
			{children}
		</div>
	);
}

export function AutoComplete({
	options,
	value,
	onChange,
	optionLabel = "Label",
	optionValue = "Value",
	name,
	label,
	error = false,
	required = false,
	width = "100%",
	getOptionLabel = null,
}) {
	return options === undefined ? null : JSON.stringify(options) === JSON.stringify([]) ? (
		<Autocomplete
			options={options}
			value={null}
			renderInput={(params) => <TextField {...params} label={label} error={error} autoComplete="new-password" required={required} />}
			noOptionsText={i18n.t("no_option")}
			sx={{ width: width }}
			size="small"
		/>
	) : (typeof options === "object" && options.error) || typeof options[0] === "object" ? (
		<Autocomplete
			clearOnEscape
			options={options.error ? [{ Label: options.error, Value: "" }] : options}
			getOptionLabel={getOptionLabel !== null ? getOptionLabel : (option) => (option.Label ? option.Label || "" : option[optionLabel] || "")}
			isOptionEqualToValue={(option, value) => (value !== null ? option[optionValue] === value[optionValue] : null)}
			value={value !== null && !options.error ? options.find((option) => option[optionValue] === value) : null}
			onChange={
				onChange?.name && onChange.name.length > 0
					? onChange
					: (event, newValue) => {
							onChange({ target: { name: name, value: newValue !== null ? newValue[optionValue] : null } });
					  }
			}
			renderInput={(params) => <TextField {...params} label={label} error={error} autoComplete="new-password" required={required} />}
			noOptionsText={i18n.t("no_option")}
			sx={{ width: width }}
			size="small"
		/>
	) : typeof options[0] === "string" ? (
		<Autocomplete
			clearOnEscape
			options={options}
			value={value}
			onChange={
				onChange?.name && onChange.name.length > 0 ? onChange : (event, newValue) => onChange({ target: { name: name, value: newValue } })
			}
			renderInput={(params) => <TextField {...params} label={label} error={error} autoComplete="new-password" required={required} />}
			noOptionsText={i18n.t("no_option")}
			sx={{ width: width }}
			size="small"
		/>
	) : null;
}
