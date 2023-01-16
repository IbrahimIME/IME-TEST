import {
	Accordion,
	AccordionDetails,
	AccordionSummary,
	Box,
	Checkbox,
	Dialog,
	DialogActions,
	DialogContent,
	DialogTitle,
	Link,
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
import React, { Component, useEffect, useState } from "react";
import { Beforeunload } from "react-beforeunload";
import { Helmet } from "react-helmet-async";
import { Prompt } from "react-router-dom";

import { LoadingSpinner, MuiButton, MuiTextField, SnackBar } from "../../../../components/common";
import { AddIcon, CancelIcon, CloseIcon, ConfirmIcon, DeleteIcon, EditIcon, ExpandMoreIcon, SaveIcon, SyncIcon } from "../../../../components/Icon";
import { CamundaAdmin } from "../../../../endpoints/DCM_DAM";
import i18n from "../../../../i18n";
import { ActivityLogging, Api } from "../../../../utils";

class Camunda extends Component {
	state = {
		edited: false,
		editing: false,
		Groups: [],
		Users: [],
		isLoadingGroups: true,
		isLoadingUsers: true,
		updateGroups: false,
		updateUsers: false,
		isSaving: false,
		snackbar: { open: false, type: "info", message: "" },
	};

	showSnackbarMessage = (type, message) => {
		this.setState({ ...this.state, snackbar: { ...this.state.snackbar, open: true, type, message } });
	};

	handleCloseSnackbar = () => {
		this.setState({ ...this.state.snackbar, snackbar: { ...this.state.snackbar, open: false } });
	};

	switchMode = () => {
		this.setState({ ...this.state.snackbar, edited: false, editing: !this.state.editing });
	};

	updateGroupList = () => {
		this.setState({ ...this.state, updateGroups: !this.state.updateGroups });
	};

	updateUserList = () => {
		this.setState({ ...this.state, updateUsers: !this.state.updateUsers });
	};

	componentDidMount() {
		Api.get({ url: CamundaAdmin.get_all_groups() }).then((result) => {
			if (result.error) {
				console.log(result);
				this.showSnackbarMessage("error", result.error);
			}

			this.setState({ ...this.state, Groups: result, isLoadingGroups: false });
		});

		Api.get({ url: CamundaAdmin.get_all_users() }).then((result) => {
			if (result.error) {
				console.log(result);
				this.showSnackbarMessage("error", result.error);
			}

			this.setState({ ...this.state, Users: result, isLoadingUsers: false });
		});
	}

	componentDidUpdate(prevProps, prevState) {
		if (prevState.updateGroups !== this.state.updateGroups) {
			Api.get({ url: CamundaAdmin.get_all_groups() }).then((result) => {
				if (result.error) {
					console.log(result);
					this.showSnackbarMessage("error", result.error);
					return;
				}

				this.setState({ ...this.state, Groups: result, isLoadingGroups: false });
			});
		}

		if (prevState.updateUsers !== this.state.updateUsers) {
			Api.get({ url: CamundaAdmin.get_all_users() }).then((result) => {
				if (result.error) {
					console.log(result);
					this.showSnackbarMessage("error", result.error);
					return;
				}

				this.setState({ ...this.state, Users: result, isLoadingUsers: false });
			});
		}
	}

	render() {
		return (
			<>
				<Prompt when={this.state.edited} message={i18n.t("unsaved_changes")} />
				{this.state.edited && <Beforeunload onBeforeunload={(event) => event.preventDefault()} />}
				<SnackBar snackbar={this.state.snackbar} handleCloseSnackbar={this.handleCloseSnackbar} />
				<Helmet>
					<title>{i18n.t("camunda", { ns: "BAS_SYS" })}</title>
				</Helmet>
				<Paper>
					<Stack direction="row" justifyContent="space-between" sx={{ pt: 2, px: 2 }}>
						<Typography variant="h6">{i18n.t("camunda", { ns: "BAS_SYS" })}</Typography>
						<Stack direction="row" spacing={1}>
							{!this.state.editing && (
								<MuiButton tooltip={i18n.t("edit")} variant="contained" onClick={this.switchMode} content={<EditIcon />} />
							)}
							{this.state.editing && (
								<Stack direction="row" spacing={1}>
									<MuiButton
										tooltip={i18n.t("cancel")}
										variant="outlined"
										disabled={this.state.isSaving}
										onClick={this.handleCancel}
										content={<CancelIcon />}
									/>
									<MuiButton
										loading={this.state.isSaving}
										tooltip={this.state.isSaving ? i18n.t("saving") : i18n.t("save")}
										variant="contained"
										onClick={async () => {
											await this.handleValidate();
											this.saveAuthentication();
										}}
										content={<SaveIcon />}
									/>
								</Stack>
							)}
						</Stack>
					</Stack>
					<Box sx={{ p: 2 }}>
						<Stack direction="column" spacing={1}>
							<Groups state={this.state} getUsers={this.getUsers} updateGroupList={this.updateGroupList} />
							<Users
								state={this.state}
								getGroups={this.getGroups}
								updateUserList={this.updateUserList}
								showSnackbarMessage={this.showSnackbarMessage}
							/>
						</Stack>
					</Box>
				</Paper>
			</>
		);
	}
}

function Groups(props) {
	const [openAddDialog, setOpenAddDialog] = useState(false);
	const [openViewDialog, setOpenViewDialog] = useState(false);
	const [openDeleteDialog, setOpenDeleteDialog] = useState(false);
	const [group, setGroup] = useState({});

	const handleOpenAddDialog = () => {
		setOpenAddDialog(true);
	};
	const handleCloseAddDialog = () => {
		setOpenAddDialog(false);
	};

	const handleOpenViewDialog = (group) => {
		setGroup(group);
		setOpenViewDialog(true);
	};
	const handleCloseViewDialog = () => {
		setGroup({});
		setOpenViewDialog(false);
	};

	const handleOpenDeleteDialog = () => {
		setOpenDeleteDialog(true);
	};
	const handleCloseDeleteDialog = () => {
		setOpenDeleteDialog(false);
	};

	const [selectedGroups, setSelectedGroups] = useState([]);
	const onCheckGroup = () => {
		var groups = document.getElementsByName("CamundaGroup");
		let selected_groups = [];

		for (const group of groups) {
			if (group.checked) selected_groups.push(group.value);
		}

		setSelectedGroups(selected_groups);
	};

	const handleDeleteGroup = () => {
		for (const group of selectedGroups) {
			Api.delete({ url: CamundaAdmin.delete_group(group) }).then((result) => {
				if (!result.success) {
					console.log(result);
					return;
				}

				ActivityLogging("Delete Camunda Group " + group, "BAS_SYS");
			});
		}

		setSelectedGroups([]);
	};

	return (
		<>
			<AddGroupDialog openDialog={openAddDialog} handleCloseDialog={handleCloseAddDialog} updateGroupList={props.updateGroupList} />
			<ViewGroupDialog openDialog={openViewDialog} group={group} handleCloseDialog={handleCloseViewDialog} />
			<DeleteGroupDialog
				openDialog={openDeleteDialog}
				handleCloseDialog={handleCloseDeleteDialog}
				handleDeleteGroup={handleDeleteGroup}
				updateGroupList={props.updateGroupList}
			/>
			<Accordion disableGutters>
				<AccordionSummary expandIcon={<ExpandMoreIcon />}>
					<Typography>{i18n.t("groups", { ns: "BAS_SYS" })}</Typography>
				</AccordionSummary>
				<AccordionDetails>
					{props.state.isLoadingGroups && <LoadingSpinner className="text-center" />}
					{!props.state.isLoadingGroups && props.state.Groups.error && <div className="text-center">{i18n.t("contact_system_admin")}</div>}
					{!props.state.isLoadingGroups && !props.state.Groups.error && (
						<>
							<TableContainer>
								<Table stickyHeader size="small">
									<TableHead>
										<TableRow>
											<TableCell></TableCell>
											<TableCell>{i18n.t("id", { ns: "BAS_SYS" })}</TableCell>
											<TableCell>{i18n.t("name", { ns: "BAS_SYS" })}</TableCell>
											<TableCell>{i18n.t("type", { ns: "BAS_SYS" })}</TableCell>
										</TableRow>
									</TableHead>
									<TableBody>
										{props.state.Groups.map((group, index) => (
											<TableRow key={index}>
												<TableCell>
													{group.type !== "SYSTEM" && (
														<Checkbox
															name="CamundaGroup"
															value={group.id}
															checked={selectedGroups.find((value) => value === group.id) ? true : false}
															onChange={onCheckGroup}
														/>
													)}
												</TableCell>
												<TableCell>
													<Link component="button" onClick={() => handleOpenViewDialog(group)}>
														{group.id}
													</Link>
												</TableCell>
												<TableCell>{group.name}</TableCell>
												<TableCell>{group.type}</TableCell>
											</TableRow>
										))}
									</TableBody>
								</Table>
							</TableContainer>
							<Stack direction="row" spacing={1} sx={{ mt: 2 }}>
								<MuiButton tooltip={i18n.t("add")} variant="contained" content={<AddIcon />} onClick={handleOpenAddDialog} />
								<MuiButton
									tooltip={i18n.t("delete")}
									variant="contained"
									color="error"
									disabled={selectedGroups.length === 0}
									content={<DeleteIcon />}
									onClick={handleOpenDeleteDialog}
								/>
							</Stack>
						</>
					)}
				</AccordionDetails>
			</Accordion>
		</>
	);
}

function AddGroupDialog(props) {
	const [state, setState] = useState({ id: "", name: "", type: "WORKFLOW" });
	const [snackbar, setSnackbar] = useState({ open: false, type: "info", message: "" });

	const showSnackbarMessage = (type, message) => {
		setSnackbar({ ...snackbar, open: true, type, message });
	};

	const handleCloseSnackbar = () => {
		setSnackbar({ ...snackbar, open: false });
	};

	const onEditGroup = (e) => {
		setState((prevState) => ({ ...prevState, [e.target.name]: e.target.value }));
	};

	const handleAddGroup = () => {
		Api.post({
			url: CamundaAdmin.add_group(),
			body: state,
		}).then((result) => {
			if (!result.success) {
				console.log(result);
				showSnackbarMessage("warning", result.message ? result.message : i18n.t("contact_system_admin"));
				return;
			}

			ActivityLogging("Create Camunda Group " + state.name, "BAS_SYS");

			setState({ id: "", name: "", type: "WORKFLOW" });
			props.handleCloseDialog();
			props.updateGroupList();
		});
	};

	return (
		<Dialog open={props.openDialog} fullWidth={true} maxWidth="sm">
			<DialogTitle>{i18n.t("add_group", { ns: "BAS_SYS" })}</DialogTitle>
			<DialogContent>
				<SnackBar snackbar={snackbar} handleCloseSnackbar={handleCloseSnackbar} />
				<div className="row">
					<div className="col-3 col-form-label justify-content-end">{i18n.t("id", { ns: "BAS_SYS" })}</div>
					<div className="col-9 col-form-label">
						<MuiTextField name="id" value={state.id} onChange={onEditGroup} />
					</div>
				</div>
				<div className="row">
					<div className="col-3 col-form-label justify-content-end">{i18n.t("name", { ns: "BAS_SYS" })}</div>
					<div className="col-9 col-form-label">
						<MuiTextField name="name" value={state.name} onChange={onEditGroup} />
					</div>
				</div>
				<div className="row">
					<div className="col-3 col-form-label justify-content-end">{i18n.t("type", { ns: "BAS_SYS" })}</div>
					<div className="col-9 col-form-label">
						<MuiTextField name="type" inputProps={{ readOnly: true }} value={state.type} />
					</div>
				</div>
			</DialogContent>
			<DialogActions>
				<MuiButton tooltip={i18n.t("add_group", { ns: "BAS_SYS" })} variant="contained" content={<AddIcon />} onClick={handleAddGroup} />
				<MuiButton
					tooltip={i18n.t("close")}
					variant="outlined"
					content={<CloseIcon />}
					onClick={() => {
						setState({ id: "", name: "", type: "WORKFLOW" });
						props.handleCloseDialog();
					}}
				/>
			</DialogActions>
		</Dialog>
	);
}

function ViewGroupDialog(props) {
	const [users, setUsers] = useState([]);
	const [update, setUpdate] = useState(false);

	const [selectedUsers, setSelectedUsers] = useState([]);

	const onCheckUser = () => {
		var users = document.getElementsByName("CamundaUser");
		let selected_users = [];

		for (const user of users) {
			if (user.checked) selected_users.push(user.value);
		}

		setSelectedUsers(selected_users);
	};

	const [openDeleteDialog, setOpenDeleteDialog] = useState(false);
	const handleOpenDeleteDialog = () => {
		setOpenDeleteDialog(true);
	};
	const handleCloseDeleteDialog = () => {
		setOpenDeleteDialog(false);
	};

	const handleDeleteUser = () => {
		for (const user of selectedUsers) {
			Api.delete({ url: CamundaAdmin.delete_user_from_group(props.group.id, user) }).then((result) => {
				if (!result.success) {
					console.log(result);
					return;
				}

				ActivityLogging("Remove Camunda User " + user + " from Group " + props.group.id, "BAS_SYS");
			});
		}

		handleCloseDeleteDialog();
		setSelectedUsers([]);
	};

	const [openAddDialog, setOpenAddDialog] = useState(false);
	const handleOpenAddDialog = () => {
		setOpenAddDialog(true);
	};
	const handleCloseAddDialog = () => {
		setOpenAddDialog(false);
	};

	const updateUserList = () => {
		setUpdate((prevUpdate) => !prevUpdate);
	};

	useEffect(() => {
		Api.get({ url: CamundaAdmin.get_all_users_of_group(props.group.id) }).then((result) => {
			setUsers(result);
		});
	}, [props.group.id, update]);

	return (
		<>
			<AddUserDialog openDialog={openAddDialog} handleCloseDialog={handleCloseAddDialog} group={props.group} updateUserList={updateUserList} />
			<DeleteUserDialog
				openDialog={openDeleteDialog}
				handleCloseDialog={handleCloseDeleteDialog}
				handleDeleteUser={handleDeleteUser}
				updateUserList={updateUserList}
			/>
			<Dialog open={props.openDialog} fullWidth={true} maxWidth="lg">
				<DialogTitle>{props.group.name}</DialogTitle>
				<DialogContent>
					<TableContainer>
						<Table stickyHeader size="small">
							<TableHead>
								<TableRow>
									<TableCell></TableCell>
									<TableCell>{i18n.t("id", { ns: "BAS_SYS" })}</TableCell>
									<TableCell>{i18n.t("first_name", { ns: "BAS_SYS" })}</TableCell>
									<TableCell>{i18n.t("last_name", { ns: "BAS_SYS" })}</TableCell>
									<TableCell>{i18n.t("email", { ns: "BAS_SYS" })}</TableCell>
								</TableRow>
							</TableHead>
							<TableBody>
								{users.length === 0 && (
									<TableRow>
										<TableCell colSpan="5" align="center">
											No User
										</TableCell>
									</TableRow>
								)}
								{users.length > 0 &&
									users.map((user, index) => (
										<TableRow key={index}>
											<TableCell>
												<Checkbox
													name="CamundaUser"
													value={user.id}
													checked={selectedUsers.find((value) => value === user.id) ? true : false}
													onChange={onCheckUser}
												/>
											</TableCell>
											<TableCell>{user.id}</TableCell>
											<TableCell>{user.firstName}</TableCell>
											<TableCell>{user.lastName}</TableCell>
											<TableCell>{user.email}</TableCell>
										</TableRow>
									))}
							</TableBody>
						</Table>
					</TableContainer>
				</DialogContent>
				<DialogActions>
					<MuiButton
						tooltip={i18n.t("add_user", { ns: "BAS_SYS" })}
						variant="contained"
						content={<AddIcon />}
						onClick={handleOpenAddDialog}
					/>
					<MuiButton
						tooltip={i18n.t("delete")}
						variant="contained"
						color="error"
						content={<DeleteIcon />}
						onClick={handleOpenDeleteDialog}
					/>
					<MuiButton tooltip={i18n.t("close")} variant="outlined" content={<CloseIcon />} onClick={props.handleCloseDialog} />
				</DialogActions>
			</Dialog>
		</>
	);
}

function DeleteGroupDialog(props) {
	return (
		<Dialog open={props.openDialog}>
			<DialogTitle>{i18n.t("delete_group", { ns: "BAS_SYS" })}</DialogTitle>
			<DialogContent>{i18n.t("you_wont_be_able_to_revert_this")}</DialogContent>
			<DialogActions>
				<MuiButton
					tooltip={i18n.t("confirm")}
					variant="contained"
					color="error"
					content={<ConfirmIcon />}
					onClick={async () => {
						await props.handleDeleteGroup();
						props.handleCloseDialog();
						props.updateGroupList();
					}}
				/>
				<MuiButton tooltip={i18n.t("close")} variant="outlined" content={<CloseIcon />} onClick={props.handleCloseDialog} />
			</DialogActions>
		</Dialog>
	);
}

function AddUserDialog(props) {
	const [users, setUsers] = useState([]);

	const [selectedUsers, setSelectedUsers] = useState([]);
	const onCheckUser = () => {
		var users = document.getElementsByName("CamundaAllUser");
		let selected_users = [];

		for (const user of users) {
			if (user.checked) selected_users.push(user.value);
		}

		setSelectedUsers(selected_users);
	};

	const handleAddUserToGroup = () => {
		for (const user of selectedUsers) {
			Api.put({ url: CamundaAdmin.add_user_to_group(props.group.id, user) }).then((result) => {
				if (!result.success) {
					console.log(result);
					return;
				}

				ActivityLogging("Add Camunda User " + user + " to Group " + props.group.id, "BAS_SYS");
			});
		}

		props.updateUserList();
		props.handleCloseDialog();
	};

	useEffect(() => {
		Api.get({ url: CamundaAdmin.get_all_users() }).then((result) => {
			if (result.error) {
				console.log(result);
				return;
			}

			setUsers(result);
		});
	}, [props.openDialog]);

	return (
		<Dialog open={props.openDialog} fullWidth={true} maxWidth="md">
			<DialogTitle>{i18n.t("add_user", { ns: "BAS_SYS" })}</DialogTitle>
			<DialogContent>
				<TableContainer sx={{ maxHeight: "70vh" }}>
					<Table stickyHeader size="small">
						<TableHead>
							<TableRow>
								<TableCell></TableCell>
								<TableCell>{i18n.t("id", { ns: "BAS_SYS" })}</TableCell>
								<TableCell>{i18n.t("first_name", { ns: "BAS_SYS" })}</TableCell>
								<TableCell>{i18n.t("last_name", { ns: "BAS_SYS" })}</TableCell>
								<TableCell>{i18n.t("email", { ns: "BAS_SYS" })}</TableCell>
							</TableRow>
						</TableHead>
						<TableBody>
							{users.map((user, index) => (
								<TableRow key={index}>
									<TableCell>
										<Checkbox name="CamundaAllUser" value={user.id} onChange={onCheckUser} />
									</TableCell>
									<TableCell>{user.id}</TableCell>
									<TableCell>{user.firstName}</TableCell>
									<TableCell>{user.lastName}</TableCell>
									<TableCell>{user.email}</TableCell>
								</TableRow>
							))}
						</TableBody>
					</Table>
				</TableContainer>
			</DialogContent>
			<DialogActions>
				<MuiButton tooltip={i18n.t("add")} variant="contained" content={<AddIcon />} onClick={handleAddUserToGroup} />
				<MuiButton tooltip={i18n.t("close")} variant="outlined" content={<CloseIcon />} onClick={props.handleCloseDialog} />
			</DialogActions>
		</Dialog>
	);
}

function DeleteUserDialog(props) {
	return (
		<Dialog open={props.openDialog}>
			<DialogTitle>{i18n.t("remove_user", { ns: "BAS_SYS" })}</DialogTitle>
			<DialogContent>{i18n.t("you_wont_be_able_to_revert_this")}</DialogContent>
			<DialogActions>
				<MuiButton
					tooltip={i18n.t("confirm")}
					variant="contained"
					color="error"
					content={<ConfirmIcon />}
					onClick={async () => {
						await props.handleDeleteUser();
						props.updateUserList();
					}}
				/>
				<MuiButton tooltip={i18n.t("close")} variant="outlined" content={<CloseIcon />} onClick={props.handleCloseDialog} />
			</DialogActions>
		</Dialog>
	);
}

function Users(props) {
	const [openDialog, setOpenDialog] = useState(false);
	const [user, setUser] = useState({});

	const handleOpenDialog = (user) => {
		setUser(user);
		setOpenDialog(true);
	};

	const handleCloseDialog = () => {
		setUser({});
		setOpenDialog(false);
	};

	const [isSyncing, setIsSyncing] = useState(false);
	const syncCamundaUsers = () => {
		setIsSyncing(true);

		Api.put({ url: CamundaAdmin.sync_users() }).then((result) => {
			if (!result.success) {
				console.log(result);
				setIsSyncing(false);
				return;
			}

			ActivityLogging("Sync Camunda User", "BAS_SYS");

			props.showSnackbarMessage("success", i18n.t("sync_completed", { ns: "BAS_SYS" }));
			setTimeout(() => {
				props.updateUserList();
				setIsSyncing(false);
			}, 1000);
		});
	};

	return (
		<>
			<UserDialog openDialog={openDialog} user={user} handleCloseDialog={handleCloseDialog} />
			<Accordion disableGutters>
				<AccordionSummary expandIcon={<ExpandMoreIcon />}>
					<Typography>{i18n.t("users", { ns: "BAS_SYS" })}</Typography>
				</AccordionSummary>
				<AccordionDetails>
					{props.state.isLoadingUsers && <LoadingSpinner className="text-center" />}
					{!props.state.isLoadingUsers && props.state.Users.error && <div className="text-center">{i18n.t("contact_system_admin")}</div>}
					{!props.state.isLoadingUsers && !props.state.Users.error && (
						<>
							<TableContainer>
								<Table stickyHeader size="small">
									<TableHead>
										<TableRow>
											<TableCell>{i18n.t("id", { ns: "BAS_SYS" })}</TableCell>
											<TableCell>{i18n.t("first_name", { ns: "BAS_SYS" })}</TableCell>
											<TableCell>{i18n.t("last_name", { ns: "BAS_SYS" })}</TableCell>
											<TableCell>{i18n.t("email", { ns: "BAS_SYS" })}</TableCell>
										</TableRow>
									</TableHead>
									<TableBody>
										{props.state.Users.map((user, index) => (
											<TableRow key={index}>
												<TableCell>
													<Link component="button" onClick={() => handleOpenDialog(user)}>
														{user.id}
													</Link>
												</TableCell>
												<TableCell>{user.firstName}</TableCell>
												<TableCell>{user.lastName}</TableCell>
												<TableCell>{user.email}</TableCell>
											</TableRow>
										))}
									</TableBody>
								</Table>
							</TableContainer>
							<Stack direction="row" sx={{ mt: 2 }}>
								<MuiButton
									loading={isSyncing}
									tooltip={isSyncing ? `${i18n.t("syncing", { ns: "BAS_SYS" })}...` : i18n.t("sync_now", { ns: "BAS_SYS" })}
									variant="contained"
									content={<SyncIcon />}
									onClick={syncCamundaUsers}
								/>
							</Stack>
						</>
					)}
				</AccordionDetails>
			</Accordion>
		</>
	);
}

function UserDialog(props) {
	const [groups, setGroups] = useState([]);

	useEffect(() => {
		Api.get({ url: CamundaAdmin.get_groups_of_user(props.user.id) }).then((result) => {
			setGroups(result);
		});
	}, [props.user.id]);

	return (
		<Dialog open={props.openDialog} fullWidth={true} maxWidth="lg">
			<DialogTitle>{`${props.user.firstName} ${props.user.lastName}`}</DialogTitle>
			<DialogContent>
				<TableContainer>
					<Table stickyHeader size="small">
						<TableHead>
							<TableRow>
								<TableCell>{i18n.t("id", { ns: "BAS_SYS" })}</TableCell>
								<TableCell>Name</TableCell>
								<TableCell>Type</TableCell>
							</TableRow>
						</TableHead>
						<TableBody>
							{groups.length === 0 && (
								<TableRow>
									<TableCell colSpan="3" align="center">
										No Group
									</TableCell>
								</TableRow>
							)}
							{groups.length > 0 &&
								groups.map((group, index) => (
									<TableRow key={index}>
										<TableCell>{group.id}</TableCell>
										<TableCell>{group.name}</TableCell>
										<TableCell>{group.type}</TableCell>
									</TableRow>
								))}
						</TableBody>
					</Table>
				</TableContainer>
			</DialogContent>
			<DialogActions>
				<MuiButton tooltip={i18n.t("close")} variant="outlined" content={<CloseIcon />} onClick={props.handleCloseDialog} />
			</DialogActions>
		</Dialog>
	);
}

export default Camunda;
