import { Masonry } from "@mui/lab";
import {
	Box,
	Card,
	CardActions,
	CardContent,
	Dialog,
	DialogActions,
	DialogContent,
	DialogTitle,
	FormControl,
	Grid,
	InputLabel,
	MenuItem,
	Popover,
	Select,
	Stack,
	Typography,
} from "@mui/material";
import { Component } from "react";
import { Helmet } from "react-helmet-async";

import { MuiButton, MuiTextField, SnackBar } from "../../components/common";
import { ConfirmIcon, SettingsIcon } from "../../components/Icon";
import { Auth } from "../../endpoints";
import i18n from "../../i18n";
import { Api, Cookies, ThemeContext } from "../../utils";
import auth from "../Login/auth";

class Home extends Component {
	state = {
		openDialog: false,
		new_password: "",
		confirm_password: "",
		settingsOpen: false,
		anchorEl: null,
		columns: 3,
		spacing: 2,
		snackbar: { open: false, type: "info", message: "" },
	};

	showSnackbarMessage = (type, message) => {
		this.setState({ ...this.state, snackbar: { ...this.state.snackbar, open: true, type, message } });
	};

	handleCloseSnackbar = () => {
		this.setState({ ...this.state, snackbar: { ...this.state.snackbar, open: false } });
	};

	handleOpenSettings = (e) => {
		this.setState({ ...this.state, settingsOpen: true, anchorEl: e.currentTarget });
	};

	handleCloseSettings = () => {
		this.setState({ ...this.state, settingsOpen: false });
	};

	handleOnChangeColumn = (e) => {
		this.setState({ ...this.state, columns: parseInt(e.target.value) });
	};

	handleOnChangeSpacing = (e) => {
		this.setState({ ...this.state, spacing: parseInt(e.target.value) });
	};

	closeDialog = () => {
		this.setState({ ...this.state, openDialog: false });
	};

	onChangePassword = (e) => {
		this.setState({ ...this.state, [e.target.name]: e.target.value });
	};

	handleKeyDown = (e) => {
		if (e.key === "Enter") this.handleResetPassword();
	};

	handleResetPassword = async () => {
		if (this.state.new_password !== "" && this.state.confirm_password !== "" && this.state.new_password === this.state.confirm_password) {
			var data = {
				User_ID: Cookies.get("User_ID"),
				User_Email: Cookies.get("User_Email"),
				New_Password: this.state.new_password,
			};

			await Api.patch({
				url: Auth.reset_password(),
				body: data,
			}).then((result) => {
				if (!result.success) {
					console.log(result);
					return false;
				}

				this.closeDialog();
				this.showSnackbarMessage("success", "Password updated");
			});
		} else {
			this.showSnackbarMessage(
				"warning",
				this.state.new_password === "" || this.state.confirm_password === ""
					? "Kindly fill in your new password"
					: this.state.new_password !== this.state.confirm_password
					? "Confirm Password is different"
					: ""
			);
		}
	};

	componentDidMount() {
		auth.refresh_token();

		if (this.props.location.resetPassword) this.setState({ ...this.state, openDialog: true });

		this.props.updateHeaderTitle("home");
		this.props.setPath(this.props.match.path);
		this.props.getFeatureList("");
		this.props.getMenuItems();
	}

	render() {
		return (
			<ThemeContext.Consumer>
				{(darkTheme) => (
					<>
						<Helmet>
							<title>{i18n.t("home")}</title>
						</Helmet>
						<ResetPasswordDialog
							state={this.state}
							onChangePassword={this.onChangePassword}
							handleKeyDown={this.handleKeyDown}
							handleResetPassword={this.handleResetPassword}
						/>
						<SnackBar snackbar={this.state.snackbar} handleCloseSnackbar={this.handleCloseSnackbar} />
						<Stack direction="column" spacing={1} sx={{ flexGrow: 1 }}>
							<Box className="d-flex justify-content-between">
								<Typography variant="h6" sx={{ color: darkTheme ? "#ffffff" : "#000000" }}>
									{i18n.t("home")}
								</Typography>
								<MuiButton mode="icon" onClick={this.handleOpenSettings} content={<SettingsIcon />} />
								<Popover
									open={this.state.settingsOpen}
									onClose={this.handleCloseSettings}
									anchorEl={this.state.anchorEl}
									anchorOrigin={{ vertical: "bottom", horizontal: "right" }}
									transformOrigin={{ vertical: "top", horizontal: "right" }}
									className="me-5"
								>
									<Box sx={{ p: 2, minWidth: "200px", maxWidth: "75%" }}>
										<Stack direction="column" spacing={2}>
											<Grid container alignItems="center">
												<Grid item xs={4} textAlign="right">
													{i18n.t("columns")}
												</Grid>
												<Grid item xs={1} textAlign="center">
													:
												</Grid>
												<Grid item xs={7}>
													<FormControl fullWidth size="small">
														<InputLabel id="column-select-label">{i18n.t("columns")}</InputLabel>
														<Select
															labelId="column-select-label"
															value={this.state.columns}
															label={i18n.t("columns")}
															onChange={this.handleOnChangeColumn}
														>
															<MenuItem value={1}>1</MenuItem>
															<MenuItem value={2}>2</MenuItem>
															<MenuItem value={3}>3</MenuItem>
															<MenuItem value={4}>4</MenuItem>
														</Select>
													</FormControl>
												</Grid>
											</Grid>
											<Grid container alignItems="center">
												<Grid item xs={4} textAlign="right">
													{i18n.t("spacing")}
												</Grid>
												<Grid item xs={1} textAlign="center">
													:
												</Grid>
												<Grid item xs={7}>
													<FormControl fullWidth size="small">
														<InputLabel id="spacing-select-label">{i18n.t("spacing")}</InputLabel>
														<Select
															labelId="spacing-select-label"
															value={this.state.spacing}
															label={i18n.t("spacing")}
															onChange={this.handleOnChangeSpacing}
														>
															<MenuItem value="1">1</MenuItem>
															<MenuItem value="2">2</MenuItem>
															<MenuItem value="3">3</MenuItem>
															<MenuItem value="4">4</MenuItem>
														</Select>
													</FormControl>
												</Grid>
											</Grid>
										</Stack>
									</Box>
								</Popover>
							</Box>
							<Box>
								<Masonry columns={this.state.columns} spacing={this.state.spacing}>
									<></>
									{/* <Card>
										<CardContent>Card 1</CardContent>
										<CardActions>
											<MuiButton content="Learn More" />
										</CardActions>
									</Card>
									<Card>
										<CardContent>Card 2</CardContent>
										<CardActions>
											<MuiButton content="Learn More" />
										</CardActions>
									</Card>
									<Card>
										<CardContent>Card 3</CardContent>
										<CardActions>
											<MuiButton content="Learn More" />
										</CardActions>
									</Card> */}
								</Masonry>
							</Box>
						</Stack>
					</>
				)}
			</ThemeContext.Consumer>
		);
	}
}

function ResetPasswordDialog(props) {
	return (
		<Dialog open={props.state.openDialog}>
			<DialogTitle>{i18n.t("reset_password")}</DialogTitle>
			<DialogContent>
				<div className="row">
					<div className="col-form-label col-4">New Password</div>
					<div className="col-form-label col-8">
						<MuiTextField
							name="new_password"
							type="password"
							value={props.state.new_password}
							onKeyDown={props.handleKeyDown}
							onChange={props.onChangePassword}
						/>
					</div>
				</div>
				<div className="row">
					<div className="col-form-label col-4">Confirm Password</div>
					<div className="col-form-label col-8">
						<MuiTextField
							name="confirm_password"
							type="password"
							value={props.state.confirm_password}
							onKeyDown={props.handleKeyDown}
							onChange={props.onChangePassword}
						/>
					</div>
				</div>
			</DialogContent>
			<DialogActions>
				<MuiButton
					tooltip={i18n.t("confirm")}
					variant="contained"
					disabled={props.state.new_password === "" || props.state.confirm_password === ""}
					onClick={props.handleResetPassword}
					content={<ConfirmIcon />}
				/>
			</DialogActions>
		</Dialog>
	);
}

export default Home;
